#!/usr/bin/env python3
"""Search the bundled Datawhale source-link catalog without network access."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def tokens(query: str) -> list[str]:
    normalized = query.strip().lower()
    values = [normalized]
    values += re.findall(r"[a-z][a-z0-9_.+-]*|[\u4e00-\u9fff]{2,}", normalized)
    domain_terms = (
        "低代码", "知识库", "大语言模型", "智能体基础", "发展史", "持续评测",
        "审批", "部署", "事故", "回流", "越权", "回滚", "治理", "pr",
        "intent.md", "spec.md", "plan.md", "dify", "rag", "sdlc", "hook",
    )
    values += [term for term in domain_terms if term in normalized]
    return list(dict.fromkeys(value for value in values if value))


def score_line(line: str, needles: list[str]) -> float:
    lower = line.lower()
    generic = {"ai", "agent", "智能体", "开发", "应用", "学习", "问题"}
    score = 12.0 if needles[0] in lower else 0.0
    for needle in needles[1:]:
        weight = 0.25 if needle in generic else 3.0
        if re.fullmatch(r"[a-z][a-z0-9_.+-]*", needle):
            count = len(re.findall(rf"(?<![a-z0-9]){re.escape(needle)}(?![a-z0-9])", lower))
        else:
            count = lower.count(needle)
        score += count * weight
    return score


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: search_sources.py "<question or keywords>"', file=sys.stderr)
        return 2

    catalog = Path(__file__).resolve().parents[1] / "references" / "source-catalog.md"
    needles = tokens(" ".join(sys.argv[1:]))
    results: list[tuple[int, str]] = []

    try:
        catalog_text = catalog.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Cannot read source catalog: {exc}", file=sys.stderr)
        return 1

    for line in catalog_text.splitlines():
        if not line.startswith("- ["):
            continue
        if "](#" in line:
            continue
        score = score_line(line, needles)
        if score:
            results.append((score, line[2:]))

    for _, line in sorted(results, reverse=True)[:12]:
        print(line)
    if not results:
        print("No exact catalog match. Try a broader Chinese or English concept name.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
