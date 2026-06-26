#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from market_data import fetch_index_snapshot, fetch_sector_movers, fetch_tencent_quotes
from mx_api import data_query, get_mx_api_key, news_search, stock_screen
from news_iterator import DEFAULT_CONFIG, load_config, parse_feed
from runtime_config import get_output_dir, require_em_api_key


def timed_call(label: str, category: str, func) -> dict:
    start = time.perf_counter()
    try:
        payload = func()
        elapsed = round(time.perf_counter() - start, 3)
        details = summarize_payload(payload)
        return {
            "label": label,
            "category": category,
            "status": "ok",
            "latency_s": elapsed,
            "details": details,
        }
    except Exception as exc:
        elapsed = round(time.perf_counter() - start, 3)
        return {
            "label": label,
            "category": category,
            "status": "error",
            "latency_s": elapsed,
            "details": str(exc),
        }


def summarize_payload(payload) -> str:
    if isinstance(payload, list):
        return f"items={len(payload)}"
    if isinstance(payload, dict):
        if "items" in payload:
            return f"items={len(payload.get('items') or [])}"
        if "rows" in payload:
            return f"rows={len(payload.get('rows') or [])}, total={payload.get('total')}"
        if "tables" in payload:
            return f"tables={len(payload.get('tables') or [])}, entities={len(payload.get('entities') or [])}"
        return f"keys={len(payload)}"
    return type(payload).__name__


def render_markdown(rows: list[dict]) -> str:
    lines = ["# Source Benchmark", "", "| Category | Source | Status | Latency(s) | Details |", "| --- | --- | --- | ---: | --- |"]
    for row in rows:
        lines.append(
            f"| {row['category']} | {row['label']} | {row['status']} | {row['latency_s']:.3f} | {row['details']} |"
        )
    return "\n".join(lines) + "\n"


def save_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    markdown = render_markdown(rows)
    (output_dir / "benchmark.md").write_text(markdown, encoding="utf-8")
    (output_dir / "benchmark.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Benchmark public and MX-enhanced data sources used by the skill.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output-dir", help="Optional directory to save benchmark markdown and JSON.")
    parser.add_argument("--skip-mx", action="store_true", help="Skip MX API calls even if EM_API_KEY is configured.")
    return parser


def main() -> int:
    require_em_api_key(script_hint="python3 skill/uwillberich/scripts/runtime_config.py set-em-key --stdin")
    parser = build_parser()
    args = parser.parse_args()

    rows = [
        timed_call("Eastmoney indices", "public", fetch_index_snapshot),
        timed_call("Eastmoney sectors", "public", lambda: fetch_sector_movers(limit=5, rising=True)),
        timed_call("Tencent quotes", "public", lambda: fetch_tencent_quotes(["sz300502", "sh688981", "sh600938"])),
    ]

    feed_config = load_config(str(DEFAULT_CONFIG))
    first_feed = feed_config.get("feeds", [])[0]
    if first_feed:
        rows.append(timed_call(first_feed["label"], "public", lambda: parse_feed(first_feed)))

    mx_ready = False
    if not args.skip_mx:
        try:
            mx_ready = bool(get_mx_api_key())
        except Exception:
            mx_ready = False

    if mx_ready:
        rows.extend(
            [
                timed_call("MX news-search", "mx", lambda: news_search("立讯精密 最新资讯", size=6)),
                timed_call("MX stock-screen", "mx", lambda: stock_screen("A股 光模块概念股", page_size=8)),
                timed_call("MX data-query", "mx", lambda: data_query("浪潮信息 最新价 总市值 收盘价")),
            ]
        )
    else:
        rows.extend(
            [
                {"label": "MX news-search", "category": "mx", "status": "skipped", "latency_s": 0.0, "details": "EM_API_KEY not configured or skip requested"},
                {"label": "MX stock-screen", "category": "mx", "status": "skipped", "latency_s": 0.0, "details": "EM_API_KEY not configured or skip requested"},
                {"label": "MX data-query", "category": "mx", "status": "skipped", "latency_s": 0.0, "details": "EM_API_KEY not configured or skip requested"},
            ]
        )

    output_dir = Path(args.output_dir).expanduser() if args.output_dir else get_output_dir("benchmarks")
    save_outputs(rows, output_dir)

    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(rows))
        print(f"Saved: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
