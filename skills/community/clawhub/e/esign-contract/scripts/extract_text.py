"""从 PDF/Word 文件中提取文本和布局信息。

用法:
    python3 extract_text.py text <file_path>      提取纯文本
    python3 extract_text.py layout <file_path>     提取最后一页布局（含坐标）
"""

import json
import sys
from pathlib import Path


def extract_text(file_path: str) -> str:
    """从 PDF 或 Word 文件提取纯文本。"""
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    suffix = p.suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf_text(file_path)
    elif suffix == ".docx":
        return _extract_docx_text(file_path)
    elif suffix == ".doc":
        return _extract_doc_text(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {suffix}（仅支持 .pdf、.docx 和 .doc）")


def _extract_pdf_text(file_path: str) -> str:
    """用 pdfplumber 提取 PDF 全文。"""
    import pdfplumber

    texts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                texts.append(text)
    return "\n\n".join(texts)


def _extract_docx_text(file_path: str) -> str:
    """用 python-docx 提取 Word 文档全文。"""
    from docx import Document

    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def _extract_doc_text(file_path: str) -> str:
    """提取 .doc 文件全文，按优先级尝试多种工具以支持跨平台。"""
    import shutil
    import subprocess

    # 优先级 1: macOS textutil（内置，速度快）
    if shutil.which("textutil"):
        result = subprocess.run(
            ["textutil", "-convert", "txt", "-stdout", file_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return result.stdout.strip()

    # 优先级 2: antiword（轻量级，Linux 常见）
    if shutil.which("antiword"):
        result = subprocess.run(
            ["antiword", file_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return result.stdout.strip()

    # 优先级 3: LibreOffice（重量级但跨平台；Windows 可执行文件名为 soffice）
    lo_bin = shutil.which("libreoffice") or shutil.which("soffice")
    if lo_bin:
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [
                    lo_bin,
                    "--headless",
                    "--convert-to",
                    "txt:Text",
                    "--outdir",
                    tmpdir,
                    file_path,
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                txt_name = Path(file_path).stem + ".txt"
                txt_path = Path(tmpdir) / txt_name
                if txt_path.exists():
                    return txt_path.read_text(encoding="utf-8").strip()

    raise RuntimeError(
        "无法提取 .doc 文件：未找到可用工具。请安装以下任一工具：\n"
        "  - macOS: textutil（系统内置）\n"
        "  - Linux: sudo apt install antiword  或  sudo apt install libreoffice\n"
        "  - Windows: 安装 LibreOffice 并添加到 PATH"
    )


def extract_layout(file_path: str) -> list:
    """提取 PDF 最后一页的文本及坐标信息。

    Returns: list of {"text": str, "x0": float, "y0": float,
                       "x1": float, "y1": float, "page": int}
    用于 Agent 分析签章区域位置。
    """
    import pdfplumber

    with pdfplumber.open(file_path) as pdf:
        if not pdf.pages:
            return []
        last_page = pdf.pages[-1]
        words = last_page.extract_words()
        return [
            {
                "text": w["text"],
                "x0": round(w["x0"], 1),
                "y0": round(w["top"], 1),
                "x1": round(w["x1"], 1),
                "y1": round(w["bottom"], 1),
                "page": len(pdf.pages),
            }
            for w in words
        ]


def _cli():
    if len(sys.argv) < 3:
        print(
            json.dumps(
                {"error": "用法: python3 extract_text.py <text|layout> <file_path>"}
            )
        )
        sys.exit(1)

    cmd, file_path = sys.argv[1], sys.argv[2]
    try:
        if cmd == "text":
            result = extract_text(file_path)
            print(json.dumps({"text": result}, ensure_ascii=False))
        elif cmd == "layout":
            result = extract_layout(file_path)
            print(json.dumps({"layout": result}, ensure_ascii=False))
        else:
            print(json.dumps({"error": f"未知命令: {cmd}"}))
            sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    _cli()
