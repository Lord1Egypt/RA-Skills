#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_pdf_content.py
======================
批量从 C++ 教材 PDF 文件中提取文本内容，输出为标准 JSON 格式，
供 PPT/Word/HTML 生成脚本使用。

用法：
    python extract_pdf_content.py --input_dir "E:/课程/信奥初级教程/" --output "course_content.json"
    python extract_pdf_content.py --input_dir "E:/课程/" --output "course_content.json" --prefix "第"

依赖：
    pip install pdfplumber

输出 JSON 格式见 references/course_schema.md
"""

import argparse
import json
import os
import re
import sys

try:
    import pdfplumber
except ImportError:
    print("请先安装 pdfplumber：pip install pdfplumber")
    sys.exit(1)


# ── 课程文件名到元数据的映射辅助 ──────────────────────────────────
def parse_course_title(filename: str) -> dict:
    """
    从文件名提取课程编号和标题。
    示例：
        "第 0 课.信息学竞赛介绍.pdf" → {"num": 0, "title": "信息学竞赛介绍"}
        "第 13 课.for 语句.pdf"      → {"num": 13, "title": "for 语句"}
    """
    base = os.path.splitext(filename)[0]
    # 匹配 "第 N 课.标题" 或 "第N课.标题" 等格式
    m = re.match(r"第\s*(\d+)\s*课[.．。](.+)", base)
    if m:
        return {"num": int(m.group(1)), "title": m.group(2).strip()}
    # 兜底：直接用文件名
    return {"num": -1, "title": base}


# ── 文本清洗 ──────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    """去除多余空行和页眉页脚噪声"""
    if not text:
        return ""
    # 删除页码行（纯数字行）
    lines = [l for l in text.splitlines() if not re.fullmatch(r"\s*\d+\s*", l)]
    # 合并连续空行
    result = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
    return result.strip()


# ── 段落拆分：尝试识别知识点小节 ─────────────────────────────────
def split_sections(text: str) -> list:
    """
    尝试将全文按标题行切割成若干知识点小节。
    返回 [{"heading": str, "body": str}, ...]
    若无法识别，整篇作为一节返回。
    """
    # 常见标题模式：数字+. 或 一/二/三/四 或 【...】
    section_re = re.compile(
        r"^(?:\d+[.、．]|[一二三四五六七八九十]+[、.．]|【.+?】|#+\s)",
        re.MULTILINE
    )
    positions = [m.start() for m in section_re.finditer(text)]
    if not positions:
        return [{"heading": "", "body": text}]

    sections = []
    for i, pos in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(text)
        chunk = text[pos:end].strip()
        lines = chunk.splitlines()
        heading = lines[0].strip() if lines else ""
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
        sections.append({"heading": heading, "body": body})
    return sections


# ── 主提取函数 ────────────────────────────────────────────────────
def extract_course(pdf_path: str) -> dict:
    """提取单个 PDF 课程的内容，返回结构化字典"""
    filename = os.path.basename(pdf_path)
    meta = parse_course_title(filename)

    full_text = ""
    page_count = 0
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    full_text += t + "\n"
    except Exception as e:
        return {
            "course_num": meta["num"],
            "title": meta["title"],
            "filename": filename,
            "page_count": 0,
            "full_text": "",
            "sections": [],
            "error": str(e)
        }

    cleaned = clean_text(full_text)
    sections = split_sections(cleaned)

    # 尝试提取代码片段（含 #include 或 int main 等特征）
    code_blocks = re.findall(
        r"(#include[^\n]*(?:\n.+){2,30})",
        cleaned
    )

    return {
        "course_num": meta["num"],
        "title": meta["title"],
        "filename": filename,
        "page_count": page_count,
        "full_text": cleaned,
        "sections": sections,
        "code_blocks": code_blocks,
        "error": None
    }


# ── 批量处理 ──────────────────────────────────────────────────────
def batch_extract(input_dir: str, output_path: str, prefix: str = "第"):
    """
    批量提取指定目录下所有以 prefix 开头的 PDF 文件。
    结果保存为 JSON。
    """
    pdf_files = sorted([
        f for f in os.listdir(input_dir)
        if f.endswith(".pdf") and f.startswith(prefix)
    ])

    if not pdf_files:
        print(f"在 {input_dir} 中未找到以 '{prefix}' 开头的 PDF 文件")
        sys.exit(1)

    print(f"找到 {len(pdf_files)} 个课程 PDF，开始提取...")

    courses = []
    for i, fname in enumerate(pdf_files):
        fpath = os.path.join(input_dir, fname)
        print(f"  [{i+1:2d}/{len(pdf_files)}] 处理: {fname}")
        data = extract_course(fpath)
        if data.get("error"):
            print(f"    ⚠️ 警告: {data['error']}")
        else:
            print(f"    ✅ 提取完成，{data['page_count']} 页，{len(data['sections'])} 节，{len(data.get('code_blocks', []))} 段代码")
        courses.append(data)

    result = {
        "total": len(courses),
        "source_dir": input_dir,
        "courses": courses
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 提取完成！共 {len(courses)} 课，结果已保存至: {output_path}")
    print(f"   可使用此 JSON 文件驱动 PPT/Word/HTML 批量生成脚本。")


# ── CLI 入口 ──────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量从 C++ 教材 PDF 提取课程内容")
    parser.add_argument("--input_dir", required=True, help="包含 PDF 文件的目录")
    parser.add_argument("--output", required=True, help="输出 JSON 文件路径")
    parser.add_argument("--prefix", default="第", help="只处理文件名以此前缀开头的 PDF（默认：第）")
    args = parser.parse_args()

    batch_extract(args.input_dir, args.output, args.prefix)
