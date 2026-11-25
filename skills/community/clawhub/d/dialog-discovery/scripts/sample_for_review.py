#!/usr/bin/env python3
"""
人工校准抽样脚本

用途：
- 从 weak supervision / seed 分桶结果中抽样
- 生成供人工 review 的 JSON / Markdown
- 快速校准 good_seed / bad_seed / gray_* 的准确性
"""
import argparse
import json
import random
from datetime import datetime
from typing import Any, Dict, List


DEFAULT_BUCKETS = [
    "good_seed",
    "bad_seed",
    "gray_high_risk",
    "gray_potential_good",
]


def load_results(input_path: str) -> List[Dict[str, Any]]:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("results", [])


def group_by_bucket(results: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for item in results:
        bucket = item.get("seed_label", "gray")
        grouped.setdefault(bucket, []).append(item)
    return grouped


def sample_bucket(items: List[Dict[str, Any]], sample_size: int, seed: int) -> List[Dict[str, Any]]:
    if len(items) <= sample_size:
        return items
    rng = random.Random(seed)
    return rng.sample(items, sample_size)


def simplify_item(item: Dict[str, Any]) -> Dict[str, Any]:
    dialog = item.get("dialog", {})
    return {
        "dialog_id": item.get("dialog_id"),
        "seed_label": item.get("seed_label"),
        "reason_summary": item.get("reason_summary"),
        "scores": item.get("scores", {}),
        "signals": item.get("signals", {}),
        "features": item.get("features", {}),
        "meta": dialog.get("meta", {}),
        "raw_text": dialog.get("raw_text", "")[:2000],
        "agent_text": dialog.get("agent_text", "")[:1000],
        "user_text": dialog.get("user_text", "")[:1000],
    }


def generate_markdown(samples: Dict[str, List[Dict[str, Any]]]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = f"# 人工校准抽样包\n\n> 生成时间：{now}\n\n"
    for bucket, items in samples.items():
        md += f"---\n\n## {bucket}（{len(items)} 条）\n\n"
        for i, item in enumerate(items, 1):
            md += f"### {i}. dialog_id={item['dialog_id']}\n\n"
            md += f"- seed_label: {item['seed_label']}\n"
            md += f"- reason_summary: {item['reason_summary']}\n"
            md += f"- scores: {json.dumps(item['scores'], ensure_ascii=False)}\n"
            md += f"- signals: {json.dumps(item['signals'], ensure_ascii=False)}\n"
            md += f"- meta: {json.dumps(item['meta'], ensure_ascii=False)}\n"
            md += f"- user_text: {item['user_text']}\n"
            md += f"- agent_text: {item['agent_text']}\n"
            md += f"- raw_text: {item['raw_text']}\n\n"
    return md


def main():
    parser = argparse.ArgumentParser(description="从 seed 结果中抽样生成人工 review 包")
    parser.add_argument("--input", required=True, help="weak supervision 结果 json")
    parser.add_argument("--output-json", required=True, help="输出 review json")
    parser.add_argument("--output-md", required=True, help="输出 review markdown")
    parser.add_argument("--sample-size", type=int, default=30, help="每个桶抽样数量")
    parser.add_argument("--seed", type=int, default=42, help="随机种子")
    args = parser.parse_args()

    results = load_results(args.input)
    grouped = group_by_bucket(results)

    sampled: Dict[str, List[Dict[str, Any]]] = {}
    for bucket in DEFAULT_BUCKETS:
        items = grouped.get(bucket, [])
        sampled[bucket] = [simplify_item(i) for i in sample_bucket(items, args.sample_size, args.seed)]

    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump(
            {
                "created_at": datetime.now().isoformat(),
                "sample_size": args.sample_size,
                "buckets": sampled,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    md = generate_markdown(sampled)
    with open(args.output_md, "w", encoding="utf-8") as f:
        f.write(md)

    print("✅ review 抽样包已生成")
    for bucket, items in sampled.items():
        print(f"  - {bucket}: {len(items)} 条")
    print(f"  - json: {args.output_json}")
    print(f"  - md: {args.output_md}")


if __name__ == "__main__":
    main()
