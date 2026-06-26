#!/usr/bin/env python3
"""Run Baidu research adaptively to reduce wasted API calls."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from baidu_web_search import RECENCY_VALUES, load_keys, search_baidu, split_csv  # noqa: E402
from build_research_pack import render_pack  # noqa: E402
from dedupe_results import canonicalize_url, dedupe, read_jsonl  # noqa: E402
from plan_queries import MODE_LIMITS, build_plan  # noqa: E402
from run_search_plan import extract_references  # noqa: E402


STOPWORDS = {
    "评测",
    "缺点",
    "优点",
    "价格",
    "产品",
    "怎么样",
    "论坛",
    "官方",
    "官网",
    "车主",
    "真实",
    "体验",
    "搜狐",
    "百度",
    "知乎",
    "贴吧",
    "小红书",
    "微博",
    "汽车",
    "之家",
    "国内",
    "系列",
    "车型",
    "发布",
    "新闻",
}


def append_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("a", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def slugify_topic(topic: str) -> str:
    slug = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", topic.strip(), flags=re.UNICODE)
    slug = re.sub(r"-+", "-", slug).strip("-_")
    return (slug or "baidu-api-search")[:48]


def default_out_dir(topic: str, mode: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    return SCRIPT_DIR.parent / "runs" / f"{stamp}-{os.getpid()}-{mode}-{slugify_topic(topic)}"


def default_cache_dir() -> Path:
    return SCRIPT_DIR.parent / "cache" / "web_search"


def source_records(plan: dict, query_item: dict, result: dict) -> list[dict]:
    records = []
    for rank, ref in enumerate(extract_references(result), start=1):
        record = dict(ref)
        record.update(
            {
                "topic": plan.get("topic"),
                "mode": plan.get("mode"),
                "query": query_item.get("query"),
                "query_intent": query_item.get("intent"),
                "query_stage": query_item.get("stage"),
                "query_source": query_item.get("source"),
                "rank": rank,
                "key_id": result.get("key_id"),
            }
        )
        records.append(record)
    return records


def records_unique_yield(records: list[dict], seen_urls: set[str]) -> tuple[int, float]:
    new_count = 0
    for record in records:
        canonical = canonicalize_url(str(record.get("url", "")))
        if canonical and canonical not in seen_urls:
            new_count += 1
    yield_ratio = new_count / max(len(records), 1)
    return new_count, yield_ratio


def update_seen(records: list[dict], seen_urls: set[str]) -> None:
    for record in records:
        canonical = canonicalize_url(str(record.get("url", "")))
        if canonical:
            seen_urls.add(canonical)


def extract_terms(records: list[dict], topic: str, max_terms: int) -> list[str]:
    if max_terms <= 0:
        return []
    text = "\n".join(
        " ".join(str(record.get(key, "")) for key in ("title", "snippet", "content", "website"))
        for record in records
    )
    text = text.replace(topic, " ")
    tokens = re.findall(r"[A-Za-z]+[A-Za-z0-9\-]{1,20}|[\u4e00-\u9fff]{2,8}|[A-Za-z]*\d+[A-Za-z0-9\-]*", text)
    counter = Counter()
    topic_lower = topic.lower()
    for token in tokens:
        token = token.strip(" -_，。！？、：:;；()（）[]【】")
        if not token or token.lower() in topic_lower:
            continue
        if token in STOPWORDS or len(token) < 2 or len(token) > 20:
            continue
        counter[token] += 1
    return [term for term, _count in counter.most_common(max_terms)]


def should_stop(
    queries_run: int,
    initial_queries: int,
    low_yield_streak: int,
    low_yield_patience: int,
    raw_count: int,
    max_raw_results: int,
    required_intents: set[str],
    attempted_intents: set[str],
) -> str | None:
    if queries_run < initial_queries:
        return None
    missing_required = required_intents - attempted_intents
    if missing_required:
        return None
    if raw_count >= max_raw_results:
        return "max_raw_results_reached"
    if low_yield_streak >= low_yield_patience:
        return "low_unique_yield"
    return None


def required_intents_for(mode: str, profile: str) -> set[str]:
    if mode == "fast":
        return {"overview"}
    required = {"overview", "official"}
    if profile == "product":
        required.update({"review", "complaint", "platform", "experience"})
    elif profile == "event":
        required.update({"freshness", "timeline", "platform"})
    elif profile == "project":
        required.update({"docs", "code"})
    else:
        required.update({"review", "platform"})
    return required


def default_max_raw_results(mode: str, top_k: int) -> int:
    defaults = {"fast": 30, "normal": 150, "deep": 600}
    minimum_query_counts = {"fast": 1, "normal": 6, "deep": 10}
    return max(defaults[mode], minimum_query_counts[mode] * top_k)


def run_adaptive(args: argparse.Namespace) -> dict[str, Any]:
    plan = build_plan(args.topic.strip(), args.mode, args.max_queries, [])
    out_dir = Path(args.out_dir) if args.out_dir else default_out_dir(plan["topic"], args.mode)
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "raw_results.jsonl"
    errors_path = out_dir / "errors.jsonl"
    plan_path = out_dir / "query_plan.json"
    dedupe_path = out_dir / "deduped_sources.json"
    trace_path = out_dir / "adaptive_trace.json"
    summary_path = out_dir / "run_summary.json"
    pack_path = out_dir / "research_pack.md"

    raw_path.write_text("", encoding="utf-8")
    errors_path.write_text("", encoding="utf-8")

    strategy = dict(plan.get("strategy", {}))
    initial_queries = args.initial_queries or strategy.get("initial_queries", 3)
    top_k = args.top_k or strategy.get("default_top_k", 20)
    min_unique_yield = args.min_unique_yield if args.min_unique_yield is not None else strategy.get("min_unique_yield", 0.25)
    low_yield_patience = args.low_yield_patience or strategy.get("low_yield_patience", 2)
    second_pass_terms = args.second_pass_terms if args.second_pass_terms is not None else strategy.get("second_pass_terms", 0)
    max_raw_results = args.max_raw_results or default_max_raw_results(args.mode, top_k)
    edition = args.edition or ("lite" if args.mode == "fast" else "standard")
    if args.fixed:
        initial_queries = len(plan["queries"])
        min_unique_yield = -1.0
        low_yield_patience = len(plan["queries"]) + 1
        if args.second_pass_terms is None:
            second_pass_terms = 0
        if args.max_raw_results is None:
            max_raw_results = max(len(plan["queries"]) * top_k, 1)
    required_intents = required_intents_for(args.mode, plan.get("profile", "general"))

    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.dry_run:
        return {
            "topic": plan["topic"],
            "mode": plan["mode"],
            "dry_run": True,
            "top_k": top_k,
            "initial_queries": initial_queries,
            "max_raw_results": max_raw_results,
            "required_intents": sorted(required_intents),
            "cache_enabled": not args.no_cache,
            "cache_dir": None if args.no_cache else args.cache_dir,
            "cache_ttl": args.cache_ttl,
            "edition": edition,
            "max_queries": len(plan["queries"]),
            "fixed": args.fixed,
            "queries": plan["queries"],
            "plan": str(plan_path),
            "out_dir": str(out_dir),
        }

    keys = load_keys(args.key_env)
    if not keys:
        raise RuntimeError(f"No API keys found. Set {args.key_env}.")

    seen_urls: set[str] = set()
    all_records: list[dict] = []
    trace: list[dict] = []
    queries = list(plan["queries"])
    queried = set()
    attempted_intents: set[str] = set()
    low_yield_streak = 0
    error_count = 0
    cache_hit_count = 0
    started = time.time()
    stop_reason = None
    stopped_early = False
    i = 0

    while i < len(queries):
        query_item = queries[i]
        i += 1
        query = query_item["query"]
        if query.casefold() in queried:
            continue
        queried.add(query.casefold())
        if query_item.get("intent"):
            attempted_intents.add(str(query_item.get("intent")))

        try:
            result = search_baidu(
                query=query,
                top_k=top_k,
                keys=keys,
                edition=edition,
                freshness=args.freshness,
                include_domains=split_csv(args.include_domains),
                block_domains=split_csv(args.block_domains),
                timeout=args.timeout,
                auth_header=args.auth_header,
                cache_dir=None if args.no_cache else args.cache_dir,
                cache_ttl_seconds=args.cache_ttl,
            )
            records = source_records(plan, query_item, result)
            if result.get("cache_hit"):
                cache_hit_count += 1
            new_unique, unique_yield = records_unique_yield(records, seen_urls)
            update_seen(records, seen_urls)
            append_jsonl(raw_path, records)
            all_records.extend(records)

            if len(queried) == initial_queries and second_pass_terms > 0:
                for offset, term in enumerate(extract_terms(all_records, plan["topic"], second_pass_terms), start=1):
                    expanded_query = f"{plan['topic']} {term}"
                    if expanded_query.casefold() not in queried:
                        queries.insert(
                            i + offset - 1,
                            {
                                "query": expanded_query,
                                "intent": "expanded",
                                "stage": "result_expansion",
                                "priority": 70 + offset,
                                "order": 10000 + offset,
                                "source": "result_terms",
                                "reason": f"term extracted from first-pass results: {term}",
                            },
                        )

            low_yield_streak = low_yield_streak + 1 if unique_yield < min_unique_yield else 0
            trace.append(
                {
                    "query": query,
                    "intent": query_item.get("intent"),
                    "stage": query_item.get("stage"),
                    "reference_count": len(records),
                    "new_unique_count": new_unique,
                    "unique_yield": round(unique_yield, 3),
                    "cache_hit": bool(result.get("cache_hit")),
                    "low_yield_streak": low_yield_streak,
                    "required_intents_missing": sorted(required_intents - attempted_intents),
                }
            )
            print(f"{query}: {len(records)} refs, {new_unique} new, yield={unique_yield:.2f}")
        except Exception as exc:
            error_count += 1
            append_jsonl(errors_path, [{"query": query, "error": str(exc)}])
            trace.append({"query": query, "error": str(exc)})
            print(f"{query}: ERROR {exc}", file=sys.stderr)

        stop_reason = should_stop(
            queries_run=len(queried),
            initial_queries=initial_queries,
            low_yield_streak=low_yield_streak,
            low_yield_patience=low_yield_patience,
            raw_count=len(all_records),
            max_raw_results=max_raw_results,
            required_intents=required_intents,
            attempted_intents=attempted_intents,
        )
        if stop_reason and i < len(queries):
            stopped_early = True
            break
        time.sleep(args.sleep)

    deduped = dedupe(
        records=read_jsonl(raw_path),
        title_threshold=args.title_threshold,
        summary_threshold=args.summary_threshold,
        domain_limit=args.domain_limit,
    )
    dedupe_path.write_text(json.dumps(deduped, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = {
        "topic": plan.get("topic"),
        "mode": plan.get("mode"),
        "query_count": len(queried),
        "planned_query_count": len(plan.get("queries", [])),
        "raw_result_count": len(all_records),
        "deduped_count": deduped.get("summary", {}).get("deduped_count", 0),
        "duplicate_count": deduped.get("summary", {}).get("duplicate_count", 0),
        "error_count": error_count,
        "cache_hit_count": cache_hit_count,
        "stop_reason": stop_reason if stopped_early else "plan_exhausted",
        "top_k": top_k,
        "edition": edition,
        "fixed": args.fixed,
        "cache_enabled": not args.no_cache,
        "cache_dir": None if args.no_cache else args.cache_dir,
        "cache_ttl": args.cache_ttl,
        "required_intents": sorted(required_intents),
        "attempted_intents": sorted(attempted_intents),
        "missing_required_intents": sorted(required_intents - attempted_intents),
        "elapsed_seconds": round(time.time() - started, 2),
        "out_dir": str(out_dir),
        "raw_results": str(raw_path),
        "deduped_sources": str(dedupe_path),
        "research_pack": str(pack_path),
        "errors": str(errors_path),
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    trace_path.write_text(json.dumps({"summary": summary, "trace": trace}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pack_path.write_text(render_pack(out_dir), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--mode", choices=sorted(MODE_LIMITS), default="normal")
    parser.add_argument("--out-dir", help="Output directory. Defaults to skill/runs/<timestamp>-<mode>-<topic>.")
    parser.add_argument("--max-queries", type=int)
    parser.add_argument("--initial-queries", type=int)
    parser.add_argument("--top-k", type=int)
    parser.add_argument("--edition", choices=["standard", "lite"], help="Baidu web_search edition. Defaults to lite for fast mode and standard otherwise.")
    parser.add_argument("--max-raw-results", type=int)
    parser.add_argument("--min-unique-yield", type=float)
    parser.add_argument("--low-yield-patience", type=int)
    parser.add_argument("--second-pass-terms", type=int)
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
    parser.add_argument("--title-threshold", type=float, default=0.92)
    parser.add_argument("--summary-threshold", type=float, default=0.94)
    parser.add_argument("--domain-limit", type=int, default=8)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--fixed", action="store_true", help="Run the full planned query set instead of stopping on low unique yield.")
    args = parser.parse_args()

    try:
        result = run_adaptive(args)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
