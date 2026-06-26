import sys
import os
import subprocess

def run_skill(pdf_path):
    # Determine the directory of the PDF file
    pdf_dir = os.path.dirname(pdf_path)
    # Create a temporary text file in the same directory as the PDF
    txt_path = os.path.join(pdf_dir, "temp_paper_for_translation.txt")

    try:
        # Check if pdftotext is installed
        subprocess.run(["which", "pdftotext"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Error: pdftotext command not found. Please install poppler-utils (e.g., sudo apt-get install -y poppler-utils).")
        sys.exit(1)

    try:
        subprocess.run(["pdftotext", pdf_path, txt_path], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting PDF to text: {e.stderr.decode()}")
        sys.exit(1)

    with open(txt_path, "r", encoding="utf-8") as f:
        paper_content = f.read()
    
    # Print the extracted content and a prompt for the agent to continue
    print(f"---BEGIN_PAPER_TEXT---\n{paper_content}\n---END_PAPER_TEXT---")
    print(f"Agent, please translate and summarize the above text into a markdown file, following the specified format and highlighting bioinformatics details. The original PDF was located at: {pdf_path}. Please save the resulting markdown file in the same directory.")
    
    # Clean up temporary file
    os.remove(txt_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python SKILL.py <pdf_path>")
        sys.exit(1)
    
    pdf_file_path = sys.argv[1]
    run_skill(pdf_file_path)
