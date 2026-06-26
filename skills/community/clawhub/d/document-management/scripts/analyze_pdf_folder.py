import os
import sys
import json

def safe_import_pypdf():
    try:
        from pypdf import PdfReader
        return PdfReader
    except ImportError:
        print("❌ 缺少依赖：pypdf，请先安装：pip install pypdf")
        sys.exit(1)

def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\r", "\n")
    lines = [line.strip() for line in text.split("\n")]
    lines = [line for line in lines if line]
    return "\n".join(lines).strip()

def extract_pdf_text(pdf_path: str) -> str:
    PdfReader = safe_import_pypdf()
    try:
        reader = PdfReader(pdf_path)
        pages_text = []

        for page_index, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text() or ""
            except Exception as e:
                page_text = f"[第 {page_index} 页提取失败: {str(e)}]"

            page_text = normalize_text(page_text)
            if page_text:
                pages_text.append(page_text)

        return "\n\n".join(pages_text).strip()
    except Exception as e:
        return f"❌ PDF读取失败：{str(e)}"

def collect_pdf_files(folder_path: str):
    pdf_files = []
    for name in sorted(os.listdir(folder_path)):
        full_path = os.path.join(folder_path, name)
        if os.path.isfile(full_path) and name.lower().endswith(".pdf"):
            pdf_files.append(full_path)
    return pdf_files

def analyze_pdf_folder(folder_path: str) -> dict:
    if not os.path.exists(folder_path):
        return {
            "success": False,
            "error": f"❌ 路径不存在：{folder_path}"
        }

    if not os.path.isdir(folder_path):
        return {
            "success": False,
            "error": f"❌ 这不是目录：{folder_path}"
        }

    pdf_files = collect_pdf_files(folder_path)
    if not pdf_files:
        return {
            "success": False,
            "error": f"❌ 目录中没有 PDF 文件：{folder_path}"
        }

    documents = []
    errors = []

    for pdf_path in pdf_files:
        file_name = os.path.basename(pdf_path)
        text = extract_pdf_text(pdf_path)

        if text.startswith("❌"):
            errors.append({
                "file_name": file_name,
                "file_path": pdf_path,
                "error": text
            })
            continue

        if not text.strip():
            errors.append({
                "file_name": file_name,
                "file_path": pdf_path,
                "error": "❌ 未提取到文本，可能是扫描版 PDF 或文件内容为空"
            })
            continue

        documents.append({
            "file_name": file_name,
            "file_path": pdf_path,
            "text": text
        })

    return {
        "success": True,
        "folder_path": folder_path,
        "document_count": len(documents),
        "documents": documents,
        "errors": errors
    }

def main():
    if len(sys.argv) < 2:
        print("❌ 使用方法：python extract_pdf_folder.py <本地PDF目录路径>")
        sys.exit(1)

    folder_path = sys.argv[1]
    result = analyze_pdf_folder(folder_path)
    
    # Write to file instead of stdout to avoid encoding issues
    output_file = os.path.join(folder_path, "_extracted_texts.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Done. Output saved to: " + output_file)

if __name__ == "__main__":
    main()