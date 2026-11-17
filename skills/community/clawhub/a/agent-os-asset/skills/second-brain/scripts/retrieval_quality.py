#!/usr/bin/env python3
"""Evaluate strict Top-1 retrieval. English is normative; ZH-CN is paired. / 评估严格 Top-1 检索；英文为规范文本，简体中文为配对译文。"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import query_index


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_benchmark(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("queries"), list):
        raise ValueError("benchmark must be an object with a queries array / benchmark 必须是包含 queries array 的 object")
    return payload


def matches_expected(result: dict[str, Any], case: dict[str, Any]) -> bool:
    expected_id = str(case.get("expected_record_id", ""))
    expected_title = str(case.get("expected_title", ""))
    expected_path = str(case.get("expected_path", ""))
    return bool(
        (expected_id and result.get("record_id") == expected_id)
        or (expected_title and result.get("title") == expected_title)
        or (expected_path and result.get("path") == expected_path)
    )


def evaluate(
    index_path: Path,
    benchmark: dict[str, Any],
    top_k: int = 5,
    semantic_rerank: str = "never",
) -> dict[str, Any]:
    cases = [item for item in benchmark.get("queries", []) if isinstance(item, dict) and str(item.get("query", "")).strip()]
    results: list[dict[str, Any]] = []
    strict_total = 0
    strict_top1 = 0
    semantic_statuses: list[str] = []
    for case in cases:
        query = str(case["query"])
        if semantic_rerank == "never":
            ranked = query_index.search(index_path, query, top_k=top_k)
            semantic_status = {"status": "disabled"}
        else:
            ranked, semantic_status = query_index.search_with_semantic_rerank(
                index_path,
                query,
                top_k=top_k,
                semantic_rerank=semantic_rerank,
            )
        semantic_statuses.append(str(semantic_status.get("status", "unknown")))
        rank = next((index + 1 for index, item in enumerate(ranked) if matches_expected(item, case)), None)
        strict = bool(case.get("strict", True))
        top1 = rank == 1
        if strict:
            strict_total += 1
            strict_top1 += int(top1)
        results.append(
            {
                "id": str(case.get("id", query)),
                "query": query,
                "strict": strict,
                "expected_title": str(case.get("expected_title", "")),
                "expected_record_id": str(case.get("expected_record_id", "")),
                "expected_path": str(case.get("expected_path", "")),
                "rank": rank,
                "top1": top1,
                "top_results": [
                    {"title": item.get("title", ""), "path": item.get("path", ""), "score": item.get("score", 0)}
                    for item in ranked
                ],
                "semantic_rerank": semantic_status,
            }
        )
    strict_passed = strict_total > 0 and strict_top1 == strict_total
    return {
        "generated_at": utc_now(),
        "index_path": str(index_path),
        "benchmark_name": str(benchmark.get("name", "")),
        "summary": {
            "cases": len(cases),
            "strict_total": strict_total,
            "strict_top1": strict_top1,
            "strict_top1_rate": round(strict_top1 / strict_total, 4) if strict_total else 0.0,
            "strict_top1_passed": strict_passed,
            "embedding_recommended": not strict_passed,
            "semantic_rerank": semantic_rerank,
            "semantic_rerank_statuses": sorted(set(semantic_statuses)),
        },
        "results": results,
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# SecondBrain Retrieval Quality Report / 第二大脑检索质量报告",
        "",
        "## Summary / 摘要",
        "",
        f"- Strict Top-1 / 严格 Top-1: `{summary['strict_top1']}/{summary['strict_total']}` (`{summary['strict_top1_rate']:.0%}`)",
        f"- Strict gate passed / 严格质量门通过: `{summary['strict_top1_passed']}`",
        f"- Embedding rerank recommended / 建议 embedding rerank: `{summary['embedding_recommended']}`",
        f"- Semantic rerank statuses / Semantic rerank 状态: `{', '.join(summary['semantic_rerank_statuses']) or 'none'}`",
        "",
        "## Cases / 用例",
        "",
        "| id | query / 查询 | expected / 预期 | rank / 排名 | top result / 首位结果 |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for item in report["results"]:
        top = item["top_results"][0]["title"] if item["top_results"] else "—"
        expected = item["expected_title"] or item["expected_record_id"] or item["expected_path"]
        lines.append(
            "| " + " | ".join(
                [
                    str(item["id"]).replace("|", "\\|"),
                    str(item["query"]).replace("|", "\\|"),
                    expected.replace("|", "\\|"),
                    str(item["rank"] or "—"),
                    top.replace("|", "\\|"),
                ]
            ) + " |"
        )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True, help="Index path. / 索引路径。")
    parser.add_argument("--benchmark", type=Path, required=True, help="Benchmark JSON path. / Benchmark JSON 路径。")
    parser.add_argument("--out", type=Path, required=True, help="JSON report output path; Markdown is written beside it. / JSON 报告输出路径；旁边会写入 Markdown。")
    parser.add_argument("--top-k", type=int, default=5, help="Number of candidates per query. / 每个查询的候选数量。")
    parser.add_argument("--semantic-rerank", choices=["auto", "always", "never"], default="never", help="Semantic rerank policy. / Semantic rerank 策略。")
    parser.add_argument("--json", action="store_true", help="Print the full JSON report. / 打印完整 JSON 报告。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = evaluate(
            args.index,
            load_benchmark(args.benchmark),
            top_k=args.top_k,
            semantic_rerank=args.semantic_rerank,
        )
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.out.with_suffix(".md").write_text(render_markdown(report), encoding="utf-8")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(report["summary"], ensure_ascii=False))
    return 0 if report["summary"]["strict_top1_passed"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
