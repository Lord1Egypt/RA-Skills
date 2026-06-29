"""
lib/pdf_extract.py - 从 PDF 抽 4 个"能稳抽"的字段

为什么只 4 个：
- 9 字段里有 5 个（获奖/版本/作者其他作品/主题/书名/作者）几乎不在书里出现
- 强行 LLM 抽 = 违背用户"不展示不确定"原则
- 4 个能稳抽的：情节梗概 / 人物 / 金句 / 创作背景（前言/后记）

输入：PDF 路径
输出：结构化 dict（直接被 render.py 接管）
"""

import sys
import re
from pathlib import Path
from typing import Optional


def extract_text(pdf_path: str, max_pages: int = 200) -> dict:
    """
    用 PyMuPDF 抽 PDF 全文 + 章节标题
    max_pages 限制避免超大 PDF OOM
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return {"ok": False, "error": "PyMuPDF 没装：pip3 install pymupdf"}

    if not Path(pdf_path).exists():
        return {"ok": False, "error": f"文件不存在：{pdf_path}"}

    doc = fitz.open(pdf_path)
    page_count = doc.page_count

    if page_count > max_pages:
        return {
            "ok": False,
            "error": f"PDF 太长（{page_count} 页 > {max_pages} 页上限）。先用更短版本，或修改 max_pages 参数。",
        }

    pages: list = []
    for i in range(page_count):
        page = doc[i]
        text: str = page.get_text("text")
        if text.strip():
            pages.append({
                "page_num": i + 1,
                "text": text,
            })

    full_text = "\n".join(p["text"] for p in pages)

    # 提取可能的章节标题（粗体或字号大的行）
    chapter_titles = []
    for p in pages[:50]:  # 只看前 50 页找目录
        text_str: str = p["text"]
        for line in text_str.split("\n"):
            line = line.strip()
            # 启发式：第 X 章 / Chapter X / 序言 / 前言 / 后记 / 跋
            if re.match(r"^(第[一二三四五六七八九十百千0-9]+章|Chapter\s*\d+|序\s*言|前\s*言|后\s*记|跋|引\s*子|楔\s*子)", line, re.IGNORECASE):
                if 3 < len(line) < 30:
                    chapter_titles.append(line)

    doc.close()

    return {
        "ok": True,
        "page_count": page_count,
        "full_text": full_text,
        "char_count": len(full_text),
        "chapter_titles": chapter_titles[:30],
        "source_path": str(pdf_path),
    }


def split_for_llm(full_text: str, max_chars: int = 80000) -> list:
    """
    把全文切成 LLM 能处理的块
    默认 80K 字符（约 5-8 万字），适合大多数 LLM 上下文
    """
    if len(full_text) <= max_chars:
        return [full_text]
    # 按段落切
    paragraphs = re.split(r"\n\s*\n", full_text)
    chunks = []
    current = []
    current_len = 0
    for p in paragraphs:
        if current_len + len(p) > max_chars and current:
            chunks.append("\n\n".join(current))
            current = [p]
            current_len = len(p)
        else:
            current.append(p)
            current_len += len(p)
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def main():
    """CLI 测试入口"""
    if len(sys.argv) < 2:
        print("用法: python3 lib/pdf_extract.py <pdf_path>", file=sys.stderr)
        sys.exit(1)

    result = extract_text(sys.argv[1])
    if not result["ok"]:
        print(f"[FAIL] {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ 抽到 {result['page_count']} 页 / {result['char_count']} 字符")
    print(f"✓ 找到 {len(result['chapter_titles'])} 个章节标题")
    if result["chapter_titles"]:
        print("\n章节样例（前 10 个）：")
        for t in result["chapter_titles"][:10]:
            print(f"  - {t}")
    print(f"\n正文前 500 字符：")
    print(result["full_text"][:500])


if __name__ == "__main__":
    main()
