#!/usr/bin/env python3
"""Translate arXiv metadata to Chinese and render a Markdown table."""

import json
import subprocess
import os
import sys


def extract_json_array(text):
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no JSON array found")
    return json.loads(text[start:end + 1])

def call_claude_translate(text, target_lang="Chinese"):
    """
    Call Claude API to translate text.
    Falls back to returning original text if API is not available.
    """
    prompt = f"""Translate the following academic paper title/abstract to {target_lang}.
Keep the translation accurate and professional. Keep technical terms in English when no good translation exists.

Text:
{text}

Respond ONLY with the translation, nothing else."""

    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--tools", ""],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass

    # Fallback: return original with a marker
    return f"[需要翻译] {text}"


def translate_papers(papers):
    payload = [
        {
            "index": index,
            "title": paper.get("title", ""),
            "abstract": paper.get("abstract", ""),
        }
        for index, paper in enumerate(papers)
    ]

    prompt = f"""你负责把 arXiv 论文元数据翻译成简体中文。
请翻译每篇论文的 title 和 abstract，保持准确、完整、专业，不要截断摘要。
技术术语在中文不自然时可以保留英文。
只返回 JSON 数组，不要输出 markdown 代码块，不要输出解释。

输入 JSON：
{json.dumps(payload, ensure_ascii=False)}

输出 JSON 格式：
[
  {{
    "index": 0,
    "title_zh": "中文标题",
    "abstract_zh": "中文摘要"
  }}
]"""

    result = subprocess.run(
        ["claude", "-p", prompt, "--tools", ""],
        capture_output=True,
        text=True,
        timeout=180
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "claude translate failed")

    translated_items = extract_json_array(result.stdout.strip())
    translated_map = {item["index"]: item for item in translated_items}

    translated_papers = []
    for index, paper in enumerate(papers):
        translated = translated_map.get(index)
        if not translated:
            raise RuntimeError(f"missing translation for paper index {index}")
        translated_papers.append(
            {
                **paper,
                "title_zh": translated["title_zh"],
                "abstract_zh": translated["abstract_zh"],
            }
        )
    return translated_papers


def format_markdown_table(papers):
    """Generate Markdown table from papers list"""

    # Table header
    header = """| 标题（中文） | 摘要（中文） | 原文链接 | 发布日期 |
| ------ | ------ | ---- | ---- |"""

    rows = []
    for paper in papers:
        title = paper.get('title_zh', paper.get('title', ''))
        abstract = paper.get('abstract_zh', paper.get('abstract', ''))
        link = paper.get('link', '')
        published = paper.get('published_sort', '')

        # Escape pipe characters in content
        title = title.replace('|', '\|')
        abstract = abstract.replace('|', '\|')
        title = title.replace('\n', '<br>')
        abstract = abstract.replace('\n', '<br>')

        row = f"| {title} | {abstract} | {link} | {published} |"
        rows.append(row)

    return header + "\n" + "\n".join(rows)


def main():
    # Read JSON from stdin
    input_data = sys.stdin.read()
    papers = json.loads(input_data)

    papers = translate_papers(papers)

    # Output Markdown table
    markdown = format_markdown_table(papers)
    print(markdown)


if __name__ == '__main__':
    main()
