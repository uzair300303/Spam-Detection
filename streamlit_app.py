import streamlit as st
import os
from predict_pdf_module import predict_pdf  # your custom function

# Streamlit page config
st.set_page_config(page_title="PDF Spam Detector", layout="centered")
st.title("📄 PDF Spam Detector")
st.write("Upload a PDF file to predict if it is SPAM or HAM.")

uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

if uploaded_file is not None:
    # Save temporarily
    temp_path = "temp.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Processing PDF...")

    try:
        result = predict_pdf(temp_path)

        if "error" in result:
            st.error(result["error"])
        else:
            label = result["label"].upper()

            # Color + Emoji output
            if label == "SPAM":
                st.markdown(
                    f"<h3 style='color:red;'>🚫 Prediction: {label}</h3>",
                    unsafe_allow_html=True,
                )
            elif label == "HAM":
                st.markdown(
                    f"<h3 style='color:green;'>✅ Prediction: {label}</h3>",
                    unsafe_allow_html=True,
                )
            else:
                st.warning(f"Prediction: {label}")

            st.write(f"Text length: {result['text_length']}")
            st.write(f"Preview of extracted text: {result['preview']}")

    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)