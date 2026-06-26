#!/usr/bin/env python3
import sys, os, argparse

def extract_pdf(path):
    import pdfplumber
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)

def extract_docx(path):
    from docx import Document
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_excel(path):
    import pandas as pd
    try:
        xl = pd.ExcelFile(path)
        sheets = []
        for sheet_name in xl.sheet_names:
            df = xl.parse(sheet_name, header=None, dtype=str)
            # replace NaN with empty string and join cells
            df = df.fillna("")
            sheets.append(df.to_string(index=False, header=False))
        return "\n".join(sheets)
    except Exception as e:
        return f"[Error reading Excel: {e}]"

def main():
    parser = argparse.ArgumentParser(description='Extract text from PDF, DOCX, or Excel files')
    parser.add_argument('file', help='Path to the document')
    args = parser.parse_args()
    path = args.file
    if not os.path.isfile(path):
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        out = extract_pdf(path)
    elif ext in ('.docx', '.doc'):
        out = extract_docx(path)
    elif ext in ('.xlsx', '.xls'):
        out = extract_excel(path)
    else:
        print(f"Unsupported file type: {ext}", file=sys.stderr)
        sys.exit(1)
    print(out)

if __name__ == '__main__':
    main()
