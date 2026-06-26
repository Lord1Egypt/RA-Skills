#!/usr/bin/env python3
"""Analyze a topic's breadth and depth gaps for deepen/superlearn."""

from __future__ import annotations

import argparse
import json
import pathlib

from clawexpert_common import (
    extract_checklist_items,
    extract_section,
    first_sentence,
    knowledge_dir,
    list_all_knowledge_nodes,
    parse_frontmatter_and_body,
    read_text,
    topic_dir,
    write_text,
)


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        key = " ".join(item.split()).strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(item.strip())
    return output


def topic_breadth_tasks(topic_root: pathlib.Path) -> list[dict]:
    tasks: list[dict] = []

    topic_index = topic_root / "index.md"
    if topic_index.exists():
        text = read_text(topic_index)
        for question in extract_checklist_items(extract_section(text, "Further Directions"), checked=False):
            tasks.append(
                {
                    "scope": "topic",
                    "source": "topic-index",
                    "prompt": question,
                    "goal": f"Create or extend knowledge coverage for: {question}",
                }
            )

    for node_path in list_all_knowledge_nodes(topic_root):
        frontmatter, body = parse_frontmatter_and_body(read_text(node_path))
        label = frontmatter.get("label") or node_path.stem
        questions = extract_checklist_items(extract_section(body, "Further Directions"), checked=False)
        for question in questions:
            tasks.append(
                {
                    "scope": "node",
                    "source": str(node_path),
                    "label": label,
                    "prompt": question,
                    "goal": f"Extend the topic beyond current coverage of {label}: {question}",
                }
            )

    return dedupe_keep_order_json(tasks)


def dedupe_keep_order_json(items: list[dict]) -> list[dict]:
    seen: set[str] = set()
    output: list[dict] = []
    for item in items:
        key = json.dumps(item, ensure_ascii=False, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        output.append(item)
    return output


def infer_depth_questions(label: str, summary: str, source_count: int, explicit: list[str]) -> list[str]:
    questions = list(explicit)
    if source_count < 3:
        questions.append(f"{label} 目前缺少哪些 primary sources、官方文档或原始论文来支撑核心结论？")
    questions.append(f"{label} 的关键机制、实验细节、时间线或代表性方法，还有哪些重要空缺？")
    questions.append(f"{label} 目前有哪些争议点、局限性、失败案例或反方证据尚未补充？")
    if summary:
        questions.append(f"基于当前总结“{first_sentence(summary)}”，哪些关键论断还需要进一步核验或量化？")
    return dedupe_keep_order(questions)


def node_depth_task(node_path: pathlib.Path) -> dict:
    frontmatter, body = parse_frontmatter_and_body(read_text(node_path))
    label = frontmatter.get("label") or node_path.stem
    source_count = int(frontmatter.get("source_count") or 0)
    confidence = frontmatter.get("confidence") or "unknown"
    summary = extract_section(body, "Summary")
    explicit_questions = extract_checklist_items(extract_section(body, "Further Directions"), checked=False)
    open_questions = infer_depth_questions(label, summary, source_count, explicit_questions)

    priority = "medium"
    if source_count < 3 or confidence == "low":
        priority = "high"
    elif explicit_questions:
        priority = "high"

    missing_primary = source_count < 3
    return {
        "node_path": str(node_path),
        "node_id": frontmatter.get("id") or node_path.stem,
        "label": label,
        "type": frontmatter.get("type") or "topic",
        "confidence": confidence,
        "source_count": source_count,
        "priority": priority,
        "summary": first_sentence(summary),
        "open_questions": open_questions[:5],
        "must_verify_claims": [
            f"Verify the strongest conclusion currently stated in {label} with higher-tier evidence.",
            f"Look for counterexamples, limitations, or disputed findings for {label}.",
        ],
        "priority_source_types": [
            "primary source / official documentation",
            "peer-reviewed paper or original benchmark report",
            "high-quality survey only when primary sources are insufficient",
        ],
        "needs_primary_sources": missing_primary,
    }


def depth_tasks(topic_root: pathlib.Path) -> list[dict]:
    return [node_depth_task(node_path) for node_path in list_all_knowledge_nodes(topic_root)]


def compute_summary(breadth: list[dict], depth: list[dict]) -> dict:
    high_priority_depth = sum(1 for item in depth if item.get("priority") == "high")
    weak_nodes = sum(1 for item in depth if int(item.get("source_count", 0)) < 3)
    return {
        "breadth_task_count": len(breadth),
        "depth_task_count": len(depth),
        "high_priority_depth_count": high_priority_depth,
        "weak_node_count": weak_nodes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    root = topic_dir(kb, args.slug)
    payload = {
        "slug": args.slug,
        "breadth_tasks": topic_breadth_tasks(root),
        "depth_tasks": depth_tasks(root),
    }
    payload["summary"] = compute_summary(payload["breadth_tasks"], payload["depth_tasks"])

    if args.output:
        output = pathlib.Path(args.output).expanduser().resolve()
        write_text(output, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
