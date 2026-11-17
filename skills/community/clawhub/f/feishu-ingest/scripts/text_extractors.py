import csv
import io
import json
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


TEXT_SUFFIXES = {
    ".txt", ".md", ".markdown", ".csv", ".tsv", ".json", ".jsonl", ".yaml", ".yml",
    ".py", ".java", ".js", ".jsx", ".ts", ".tsx", ".vue", ".html", ".css", ".scss",
    ".sql", ".r", ".sh", ".bash", ".ps1", ".xml", ".toml", ".ini", ".cfg", ".conf",
    ".log", ".rst", ".tex", ".go", ".rs", ".kt", ".swift", ".c", ".h", ".cpp", ".hpp",
}
ARCHIVE_SUFFIXES = {".zip", ".tar", ".gz", ".7z", ".rar"}
MAX_PREVIEW_FILE_SIZE = 50 * 1024 * 1024


def read_text_preview(path, max_chars=6000):
    if not path:
        return ""
    file_path = Path(path)
    if not file_path.exists() or not file_path.is_file():
        return ""
    if file_path.stat().st_size > MAX_PREVIEW_FILE_SIZE:
        return ""
    suffix = file_path.suffix.lower()
    try:
        if suffix == ".docx":
            return read_docx_text(file_path, max_chars)
        if suffix == ".pptx":
            return read_pptx_text(file_path, max_chars)
        if suffix == ".xlsx":
            return read_xlsx_text(file_path, max_chars)
        if suffix == ".pdf":
            return read_pdf_text(file_path, max_chars)
        if suffix in TEXT_SUFFIXES:
            return read_text_file(file_path, max_chars)
        if suffix in ARCHIVE_SUFFIXES:
            return read_archive_listing(file_path, max_chars)
        return ""
    except Exception:
        return ""


def read_text_file(file_path, max_chars):
    raw = file_path.read_bytes()
    if b"\x00" in raw[:4096]:
        return ""
    return raw.decode("utf-8-sig", errors="replace")[:max_chars]


def read_docx_text(file_path, max_chars):
    with zipfile.ZipFile(file_path) as archive:
        parts = ["word/document.xml"]
        parts.extend(sorted(name for name in archive.namelist() if name.startswith("word/header") or name.startswith("word/footer")))
        texts = []
        for name in parts:
            if name not in archive.namelist():
                continue
            root = ET.fromstring(archive.read(name))
            for node in root.iter():
                if node.tag.endswith("}t") and node.text:
                    texts.append(node.text)
            if sum(len(item) for item in texts) >= max_chars:
                break
    return "\n".join(texts)[:max_chars]


def read_pptx_text(file_path, max_chars):
    texts = []
    with zipfile.ZipFile(file_path) as archive:
        slide_names = sorted(name for name in archive.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml"))
        for name in slide_names:
            root = ET.fromstring(archive.read(name))
            slide_text = []
            for node in root.iter():
                if node.tag.endswith("}t") and node.text:
                    slide_text.append(node.text)
            if slide_text:
                texts.append(" ".join(slide_text))
            if sum(len(item) for item in texts) >= max_chars:
                break
    return "\n\n".join(texts)[:max_chars]


def read_xlsx_text(file_path, max_chars):
    with zipfile.ZipFile(file_path) as archive:
        names = set(archive.namelist())
        shared = read_xlsx_shared_strings(archive) if "xl/sharedStrings.xml" in names else []
        sheet_names = sorted(name for name in names if name.startswith("xl/worksheets/sheet") and name.endswith(".xml"))
        sections = []
        for sheet_index, name in enumerate(sheet_names[:6], start=1):
            rows = []
            root = ET.fromstring(archive.read(name))
            for row in root.iter():
                if not row.tag.endswith("}row"):
                    continue
                cells = []
                for cell in row:
                    if not cell.tag.endswith("}c"):
                        continue
                    cells.append(read_xlsx_cell(cell, shared))
                if any(str(cell).strip() for cell in cells):
                    rows.append(cells)
                if len(rows) >= 60:
                    break
            if rows:
                sections.append(f"## Sheet {sheet_index}\n\n" + markdown_table(rows))
            if sum(len(section) for section in sections) >= max_chars:
                break
    return "\n\n".join(sections)[:max_chars]


def read_xlsx_shared_strings(archive):
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    strings = []
    for item in root.iter():
        if item.tag.endswith("}si"):
            parts = [node.text for node in item.iter() if node.tag.endswith("}t") and node.text]
            strings.append("".join(parts))
    return strings


def read_xlsx_cell(cell, shared):
    cell_type = cell.attrib.get("t")
    value = ""
    for child in cell:
        if child.tag.endswith("}v") and child.text is not None:
            value = child.text
            break
        if child.tag.endswith("}is"):
            parts = [node.text for node in child.iter() if node.tag.endswith("}t") and node.text]
            value = "".join(parts)
            break
    if cell_type == "s":
        try:
            index = int(value)
            return shared[index] if 0 <= index < len(shared) else value
        except Exception:
            return value
    return value


def read_pdf_text(file_path, max_chars):
    try:
        from pypdf import PdfReader
    except Exception:
        try:
            from PyPDF2 import PdfReader
        except Exception:
            return ""
    reader = PdfReader(str(file_path))
    texts = []
    for page in reader.pages[:20]:
        texts.append(page.extract_text() or "")
        if sum(len(item) for item in texts) >= max_chars:
            break
    return "\n\n".join(texts)[:max_chars]


def read_archive_listing(file_path, max_chars):
    if file_path.suffix.lower() != ".zip":
        return ""
    with zipfile.ZipFile(file_path) as archive:
        rows = [["path", "size", "modified"]]
        for info in archive.infolist()[:200]:
            rows.append([info.filename, str(info.file_size), "-".join(str(part) for part in info.date_time[:3])])
    return ("压缩包文件清单：\n\n" + markdown_table(rows))[:max_chars]


def markdown_table(rows):
    if not rows:
        return ""
    output = io.StringIO()
    writer = csv.writer(output, delimiter="|", lineterminator="\n")
    clean_rows = []
    width = max(len(row) for row in rows)
    for row in rows:
        clean_rows.append([str(row[index] if index < len(row) else "").replace("\n", " ") for index in range(width)])
    output.write("| " + " | ".join(clean_rows[0]) + " |\n")
    output.write("| " + " | ".join(["---"] * width) + " |\n")
    for row in clean_rows[1:]:
        output.write("| " + " | ".join(row) + " |\n")
    return output.getvalue()