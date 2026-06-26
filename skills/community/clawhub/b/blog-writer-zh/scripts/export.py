#!/usr/bin/env python3
"""
blog-writer-zh 导出脚本

生成平台兼容的 Markdown 文件, DOCX 通过 pandoc 转换 (可选).

用法: python3 export.py <文章路径> [-o <输出目录>]

依赖:
  - 必须: 无 (纯标准库)
  - 可选: pandoc (用于生成 docx, https://pandoc.org/)
"""

import re
import shutil
import argparse
import subprocess
from pathlib import Path


# ---------------------------------------------------------------------------
# MD 转换
# ---------------------------------------------------------------------------

def transform_headings(text: str) -> str:
    """将 H2->H1, H3->H2, H4+->加粗段落."""
    lines = text.split("\n")
    result = []
    for line in lines:
        heading_match = re.match(r"^(#{2,})\s+(.+)", line)
        if not heading_match:
            result.append(line)
            continue
        hashes = heading_match.group(1)
        content = heading_match.group(2)
        if len(hashes) == 2:
            result.append(f"# {content}")
        elif len(hashes) == 3:
            result.append(f"## {content}")
        else:
            result.append(f"**{content}**")
    return "\n".join(result)


def convert_footnotes(text: str) -> str:
    """将文末脚注 [^n]: ... 转为有序列表, 并移除正文中的 [^n] 标记."""
    lines = text.split("\n")
    body_lines = []
    footnote_defs = []
    in_footnotes = False
    for line in lines:
        fn_match = re.match(r"^\[\^(\d+)\]:\s*(.+)", line)
        if fn_match:
            in_footnotes = True
            footnote_defs.append((int(fn_match.group(1)), fn_match.group(2).strip()))
            continue
        if in_footnotes:
            if line.strip() == "":
                continue
            if footnote_defs and line.strip():
                num, text_val = footnote_defs[-1]
                footnote_defs[-1] = (num, f"{text_val} {line.strip()}")
            continue
        body_lines.append(line)
    body = "\n".join(body_lines)
    body = re.sub(r"\[\^\d+\]", "", body)
    if footnote_defs:
        body += "\n\n参考来源\n\n"
        footnote_defs.sort(key=lambda x: x[0])
        for i, (_, text_val) in enumerate(footnote_defs, 1):
            body += f"{i}. {text_val}\n"
    return body


def convert_md(text: str) -> str:
    """对文章的正文内容 (不含 frontmatter) 做标题和脚注转换."""
    fm_match = re.match(r"^(---\n.*?\n---)\n*", text, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        body = text[fm_match.end():]
        return fm + "\n\n" + convert_footnotes(transform_headings(body))
    else:
        return convert_footnotes(transform_headings(text))


# ---------------------------------------------------------------------------
# DOCX 转换 (pandoc)
# ---------------------------------------------------------------------------

def has_pandoc() -> bool:
    return shutil.which("pandoc") is not None


def convert_to_docx(md_path: Path, docx_path: Path) -> bool:
    """用 pandoc 将 md 转为 docx. 成功返回 True."""
    if not has_pandoc():
        print("[!] pandoc 未安装, 跳过 docx 生成")
        print("    安装方式: brew install pandoc  (macOS)")
        print("             apt-get install pandoc  (Linux)")
        print("             https://pandoc.org/installing.html  (其他)")
        return False
    try:
        subprocess.run(
            ["pandoc", str(md_path), "-o", str(docx_path), "--from", "markdown", "--to", "docx"],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"[x] pandoc 转换失败: {e.stderr}")
        return False


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="blog-writer-zh 导出: 生成平台兼容 .md, 可选通过 pandoc 生成 .docx"
    )
    parser.add_argument("input", type=Path, help="原始文章 .md 文件路径")
    parser.add_argument("-o", "--output-dir", type=Path, default=None,
                        help="输出目录 (默认原文同级)")
    parser.add_argument("--skip-docx", action="store_true",
                        help="跳过 docx 生成")
    args = parser.parse_args()

    source_path: Path = args.input
    if not source_path.exists():
        print(f"[x] 文件不存在: {source_path}")
        return 1

    out_dir = args.output_dir or source_path.parent
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    stem = source_path.stem

    # 1. 转换 MD
    original = source_path.read_text(encoding="utf-8")
    md_content = convert_md(original)
    md_path = out_dir / f"{stem}-export.md"
    md_path.write_text(md_content, encoding="utf-8")
    print(f"[ok] {md_path}  (小红书)")

    # 2. 生成 DOCX (可选)
    if not args.skip_docx:
        docx_path = out_dir / f"{stem}-export.docx"
        if convert_to_docx(md_path, docx_path):
            print(f"[ok] {docx_path}  (公众号/知乎)")
    else:
        print("[skip] docx 生成已跳过 (--skip-docx)")

    return 0


if __name__ == "__main__":
    exit(main())
