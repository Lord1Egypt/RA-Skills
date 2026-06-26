from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def now_labels() -> tuple[str, str]:
    now = datetime.now()
    return now.strftime("%Y-%m-%d"), now.strftime("%m.%d")


def build_notes_markdown(topic_name: str, date_label: str, papers: list[dict[str, Any]]) -> str:
    lines = [f"# {topic_name} arXiv Notes - {date_label}", ""]
    if not papers:
        lines.append("今天没有抓到足够匹配的新论文。")
        return "\n".join(lines)
    for index, paper in enumerate(papers, start=1):
        lines.append(f"## {index}. {paper['title']}")
        lines.append(f"- authors: {', '.join(paper.get('authors', []))}")
        lines.append(f"- categories: {', '.join(paper.get('categories', []))}")
        lines.append(f"- problem: {paper['problem']}")
        lines.append(f"- method: {paper['method']}")
        lines.append(f"- result: {paper['result']}")
        lines.append(f"- my thought: {paper['my_thought']}")
        lines.append("")
    return "\n".join(lines)


def build_xhs_post(topic_name: str, topic_config: dict[str, Any], date_label: str, papers: list[dict[str, Any]]) -> dict[str, str]:
    hashtags = " ".join(f"#{tag}" for tag in topic_config.get("post_hashtags", []))
    compact_date = date_label.replace('.', '')
    title = f"扩散LLM日报{compact_date}"
    if not papers:
        content = (
            f"{topic_name} 今天没有刷到特别贴近的新 paper。\n\n"
            f"我先记一笔，后面继续看。\n\n"
            f"{hashtags}"
        )
        return {"title": title[:20], "content": content.strip()}

    lines = [
        "两篇：一篇讲 EoS token / hidden scratchpad；另一篇讲 diverse sampling / test-time search。",
    ]
    for index, paper in enumerate(papers[:3], start=1):
        lines.extend(
            [
                "",
                f"{index}️⃣ {paper['title']}",
                f"arXiv: {_arxiv_short_id(paper.get('id', ''))}",
                f"问题：{paper['problem']}",
                f"方法：{paper['method']}",
                f"效果：{paper['result']}",
                f"评价：{paper['my_thought']}",
            ]
        )
    lines.extend(
        [
            "",
            "#AI #DiffusionLLM #科研",
        ]
    )
    return {"title": title[:20], "content": "\n".join(lines).strip()}


def _build_hook(topic_name: str, papers: list[dict[str, Any]]) -> str:
    if not papers:
        return f"{topic_name} 今天没有特别值得记的更新。"
    first = papers[0]
    text = f"{first.get('title', '')} {first.get('summary', '')}".lower()
    if 'eos' in text or 'scratchpad' in text:
        return f"{topic_name} 这两天最有意思的一个问题，是 diffusion LLM 会不会把 EoS token 当成 hidden scratchpad。"
    if 'pass@$k' in text or 'sampling' in text:
        return f"{topic_name} 这两天一个明显趋势，是大家开始认真碰 test-time scaling 和 sampling diversity。"
    return f"{topic_name} 今天有几篇 paper 的问题意识还不错。"


def _arxiv_short_id(url: str) -> str:
    last = (url or '').rstrip('/').split('/')[-1]
    return last[:-2] if last.endswith('v1') or last.endswith('v2') or last.endswith('v3') else last


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
