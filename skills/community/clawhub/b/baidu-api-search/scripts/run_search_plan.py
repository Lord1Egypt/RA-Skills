#!/usr/bin/env python3
"""Run a query plan and write Baidu raw results as JSONL."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from baidu_web_search import RECENCY_VALUES, load_keys, search_baidu, split_csv  # noqa: E402


def default_cache_dir() -> Path:
    return SCRIPT_DIR.parent / "cache" / "web_search"


def extract_references(api_result: dict) -> list[dict]:
    response = api_result.get("response", {})
    if isinstance(response, dict):
        refs = response.get("references")
        if isinstance(refs, list):
            return refs
        data = response.get("data")
        if isinstance(data, dict) and isinstance(data.get("references"), list):
            return data["references"]
    return []


def write_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("a", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--freshness", choices=RECENCY_VALUES)
    parser.add_argument("--include-domains")
    parser.add_argument("--block-domains")
    parser.add_argument("--key-env", default="BAIDU_AI_SEARCH_API_KEYS")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--auth-header", choices=["authorization", "x-appbuilder", "both"], default="both")
    parser.add_argument("--cache-dir", default=str(default_cache_dir()), help="Query-level cache directory. API keys are never written.")
    parser.add_argument("--cache-ttl", type=int, default=86400, help="Cache TTL in seconds.")
    parser.add_argument("--no-cache", action="store_true", help="Disable query-level cache and force live API calls.")
    parser.add_argument("--sleep", type=float, default=0.5)
    args = parser.parse_args()

    plan_path = Path(args.plan)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "raw_results.jsonl"
    errors_path = out_dir / "errors.jsonl"
    summary_path = out_dir / "run_summary.json"
    raw_path.write_text("", encoding="utf-8")
    errors_path.write_text("", encoding="utf-8")

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    keys = load_keys(args.key_env)
    if not keys:
        raise SystemExit(f"No API keys found. Set {args.key_env}.")

    total_refs = 0
    error_count = 0
    cache_hit_count = 0
    started = time.time()
    for query_item in plan.get("queries", []):
        query = query_item["query"]
        try:
            result = search_baidu(
                query=query,
                top_k=args.top_k,
                keys=keys,
                freshness=args.freshness,
                include_domains=split_csv(args.include_domains),
                block_domains=split_csv(args.block_domains),
                timeout=args.timeout,
                auth_header=args.auth_header,
                cache_dir=None if args.no_cache else args.cache_dir,
                cache_ttl_seconds=args.cache_ttl,
            )
            if result.get("cache_hit"):
                cache_hit_count += 1
            refs = extract_references(result)
            records = []
            for rank, ref in enumerate(refs, start=1):
                record = dict(ref)
                record.update(
                    {
                        "topic": plan.get("topic"),
                        "mode": plan.get("mode"),
                        "query": query,
                        "query_intent": query_item.get("intent"),
                        "query_stage": query_item.get("stage"),
                        "query_source": query_item.get("source"),
                        "rank": rank,
                        "key_id": result.get("key_id"),
                    }
                )
                records.append(record)
            write_jsonl(raw_path, records)
            total_refs += len(records)
            print(f"{query}: {len(records)} references")
        except Exception as exc:
            error_count += 1
            write_jsonl(errors_path, [{"query": query, "error": str(exc)}])
            print(f"{query}: ERROR {exc}", file=sys.stderr)
        time.sleep(args.sleep)

    summary = {
        "topic": plan.get("topic"),
        "mode": plan.get("mode"),
        "query_count": len(plan.get("queries", [])),
        "raw_result_count": total_refs,
        "error_count": error_count,
        "cache_hit_count": cache_hit_count,
        "cache_enabled": not args.no_cache,
        "cache_dir": None if args.no_cache else args.cache_dir,
        "cache_ttl": args.cache_ttl,
        "elapsed_seconds": round(time.time() - started, 2),
        "raw_results": str(raw_path),
        "errors": str(errors_path),
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
