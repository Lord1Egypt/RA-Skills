#!/usr/bin/env python3
"""
Markdown 转 PDF 工具
使用 Chrome headless 将 Markdown 渲染为带样式的 PDF。

用法：
  python3 md2pdf.py --input <file.md> [--output <file.pdf>]
"""

import argparse
import html as html_mod
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


CSS = """
<style>
body {
    font-family: 'Microsoft YaHei', 'PingFang SC', 'Helvetica Neue', sans-serif;
    background: white;
    padding: 40px 50px;
    color: #333;
    line-height: 1.7;
    max-width: 900px;
    margin: 0 auto;
    font-size: 14px;
}
h1 { color: #1a1a1a; border-bottom: 2px solid #333; padding-bottom: 10px; font-size: 22px; }
h2 { color: #2563eb; margin-top: 28px; font-size: 18px; }
h3 { color: #16a34a; font-size: 15px; }
h4 { color: #7c3aed; font-size: 14px; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 13px; }
th, td { border: 1px solid #ddd; padding: 6px 10px; text-align: left; }
th { background: #f5f5f5; font-weight: 600; }
tr:nth-child(even) { background: #fafafa; }
code { background: #f0f0f0; padding: 2px 5px; border-radius: 3px; font-size: 12px; }
pre { background: #f8f8f8; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 12px; line-height: 1.4; }
blockquote { color: #666; border-left: 3px solid #ccc; padding-left: 12px; margin-left: 0; }
hr { border: none; border-top: 1px solid #ddd; margin: 20px 0; }
ul, ol { padding-left: 24px; }
p { margin: 6px 0; }
strong { color: #111; }
</style>
"""


def inline_format(text):
    """行内 Markdown 格式化"""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def md_to_html(md_path):
    """Markdown → HTML"""
    with open(md_path, "r", encoding="utf-8") as f:
        md = f.read()

    parts = [
        "<!DOCTYPE html><html><head><meta charset=\"UTF-8\">",
        CSS,
        "</head><body>",
    ]

    lines = md.split("\n")
    in_code = False
    in_table = False

    def close_table():
        nonlocal in_table
        if in_table:
            parts.append("</table>")
            in_table = False

    for line in lines:
        if line.startswith("```"):
            if not in_code:
                close_table()
                parts.append("<pre>")
                in_code = True
            else:
                parts.append("</pre>")
                in_code = False
            continue

        if in_code:
            parts.append(html_mod.escape(line))
            continue

        if line.startswith("# "):
            close_table()
            parts.append(f"<h1>{inline_format(line[2:])}</h1>")
        elif line.startswith("## "):
            close_table()
            parts.append(f"<h2>{inline_format(line[3:])}</h2>")
        elif line.startswith("### "):
            close_table()
            parts.append(f"<h3>{inline_format(line[4:])}</h3>")
        elif line.startswith("#### "):
            close_table()
            parts.append(f"<h4>{inline_format(line[5:])}</h4>")
        elif line.startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            # 检测分隔行（如 |---|---|---|）
            if all(set(c) <= set("-: ") for c in cells):
                # 分隔行不关闭表格，只跳过
                if not in_table:
                    # 没有表头直接遇到分隔行，跳过
                    pass
                continue
            if not in_table:
                parts.append("<table>")
                parts.append("<tr>" + "".join(f"<th>{inline_format(c)}</th>" for c in cells) + "</tr>")
                in_table = True
            else:
                parts.append("<tr>" + "".join(f"<td>{inline_format(c)}</td>" for c in cells) + "</tr>")
        elif line.startswith("|-"):
            # 备用：以 |- 开头的分隔行
            if not in_table:
                pass
            continue
        elif line.strip() == "---":
            close_table()
            parts.append("<hr>")
        elif line.strip() == "":
            # 空行不关闭表格（表格内的空行在 Markdown 中不应断开表格）
            pass
        elif line.startswith("> "):
            parts.append(f"<blockquote>{inline_format(line[2:])}</blockquote>")
        else:
            close_table()
            parts.append(f"<p>{inline_format(line)}</p>")

    close_table()
    parts.append("</body></html>")
    return "\n".join(parts)


def html_to_pdf(html_path, pdf_path):
    """Chrome headless: HTML → PDF"""
    cmd = [
        "google-chrome", "--headless", "--disable-gpu",
        "--no-margins", "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        f"file://{html_path}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if not Path(pdf_path).exists():
        print(f"错误: PDF 生成失败", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    size_kb = Path(pdf_path).stat().st_size / 1024
    print(f"✅ PDF 已生成: {pdf_path} ({size_kb:.0f}KB)")


def main():
    parser = argparse.ArgumentParser(description="Markdown 转 PDF")
    parser.add_argument("--input", "-i", required=True, help="输入 Markdown 文件")
    parser.add_argument("--output", "-o", help="输出 PDF 路径（默认同目录 .pdf）")
    args = parser.parse_args()

    md_path = Path(args.input).resolve()
    if not md_path.exists():
        print(f"错误: 文件不存在 {md_path}", file=sys.stderr)
        sys.exit(1)

    pdf_path = Path(args.output).resolve() if args.output else md_path.with_suffix(".pdf")

    # MD → HTML → PDF
    html_content = md_to_html(str(md_path))

    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8",
                                     delete=False) as tmp:
        tmp.write(html_content)
        html_path = tmp.name

    try:
        html_to_pdf(html_path, str(pdf_path))
    finally:
        os.unlink(html_path)


if __name__ == "__main__":
    main()
