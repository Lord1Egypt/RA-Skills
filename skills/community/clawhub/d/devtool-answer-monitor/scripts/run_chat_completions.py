#!/usr/bin/env python3
"""
run_chat_completions.py — Multi-model answer monitor runner using Chat Completions API.

Supports any OpenAI-compatible provider (OpenAI, Anthropic via proxy,
Google Gemini, DeepSeek, Qwen, MiniMax, GLM, etc.).

Unlike run_monitor.py which uses the Responses API (OpenAI-only),
this runner uses the universal Chat Completions endpoint so every
model behind an OpenAI-compatible gateway works out of the box.

Usage:
    export OPENAI_API_KEY=<your-key>
    export OPENAI_BASE_URL=<your-base-url>   # optional, defaults to OpenAI
    python scripts/run_chat_completions.py \\
        --query-pool  data/query-pools/mineru-example.json \\
        --model-config data/models.sample.json \\
        --out-dir data/runs/my-run

Output:
    <out-dir>/raw_responses.jsonl   — raw answers per model/query
    <out-dir>/run_manifest.json     — run metadata

After this step, annotate scores and run:
    python -m devtool_answer_monitor report --input <out-dir>/raw_responses.jsonl --output-dir <out-dir>
"""
import argparse
import concurrent.futures
import datetime as dt
import json
import os
import sys
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    raise SystemExit("openai package required. Run: pip install -r requirements.txt")

SYSTEM_PROMPT = (
    "Answer as a neutral technical assistant. Keep the answer concise but complete."
)

DEFAULT_TIMEOUT = 25  # seconds per request
DEFAULT_WORKERS = 16  # concurrent threads


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def call_model(client: "OpenAI", model_cfg: dict, query_text: str, timeout: int) -> dict:
    """Call one model via Chat Completions. Returns dict with response_text, response_id, error."""
    try:
        resp = client.chat.completions.create(
            model=model_cfg["api_model"],
            temperature=model_cfg.get("temperature", 0.1),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query_text},
            ],
            timeout=timeout,
        )
        text = resp.choices[0].message.content or ""
        return {"response_text": text, "response_id": resp.id, "error": None}
    except Exception as exc:
        return {"response_text": "", "response_id": None, "error": str(exc)[:200]}


def build_row(run_id: str, project: str, model_cfg: dict, query: dict,
              result: dict, created_at: str) -> dict:
    return {
        "run_id": run_id,
        "project": project,
        "query_id": query["id"],
        "query_type": query["type"],
        "language": query.get("language", ""),
        "funnel_stage": query.get("funnel_stage"),
        "target_surface": query.get("target_surface"),
        "desired_action": query.get("desired_action"),
        "model_id": model_cfg["id"],
        "query_text": query["query"],
        "response_text": result["response_text"],
        "response_id": result["response_id"],
        "mode": "api",
        "error": result["error"],
        "source_links": [],
        "captured_at": created_at,
        # Scores left null — fill via annotation or auto-score step
        "mention_score": None,
        "sentiment_score": None,
        "capability_score": None,
        "ecosystem_score": None,
        "needs_repair": None,
        "repair_type": None,
        "annotator": None,
        "review_status": "pending",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Developer-tool answer monitor runner (Chat Completions)")
    ap.add_argument("--query-pool", required=True, help="Path to query pool JSON")
    ap.add_argument("--model-config", required=True, help="Path to model config JSON")
    ap.add_argument("--out-dir", required=True, help="Output directory")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                    help=f"Per-request timeout in seconds (default: {DEFAULT_TIMEOUT})")
    ap.add_argument("--workers", type=int, default=DEFAULT_WORKERS,
                    help=f"Concurrent threads (default: {DEFAULT_WORKERS})")
    ap.add_argument("--limit", type=int, help="Limit number of queries per model (for testing)")
    args = ap.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")  # None = use OpenAI default

    if not api_key:
        raise SystemExit("Set OPENAI_API_KEY environment variable first.")

    query_pool = load_json(args.query_pool)
    model_config = load_json(args.model_config)

    project = query_pool.get("project", "unknown")
    queries = query_pool["segments"]
    if args.limit:
        queries = queries[: args.limit]

    enabled_models = [m for m in model_config.get("models", []) if m.get("enabled", True)]
    if not enabled_models:
        raise SystemExit("No enabled models found in model config.")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_id = out_dir.name
    created_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

    total = len(enabled_models) * len(queries)
    print(f"[devtool-answer-monitor] project={project} models={len(enabled_models)} "
          f"queries={len(queries)} total={total} workers={args.workers}")

    # Build task list
    tasks = [(m, q) for m in enabled_models for q in queries]

    def run_task(task):
        model_cfg, query = task
        # Each thread gets its own client instance (thread-safe)
        client = OpenAI(api_key=api_key, base_url=base_url)
        result = call_model(client, model_cfg, query["query"], args.timeout)
        row = build_row(run_id, project, model_cfg, query, result, created_at)
        return row

    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futs = {executor.submit(run_task, t): t for t in tasks}
        for fut in concurrent.futures.as_completed(futs, timeout=args.timeout * len(tasks) + 30):
            row = fut.result()
            rows.append(row)
            status = "✓" if not row["error"] else "✗"
            err_snippet = f" | err: {row['error'][:60]}" if row["error"] else ""
            print(f"  {status} {row['model_id']:35s} {row['query_id']}{err_snippet}")

    # Sort for deterministic output
    rows.sort(key=lambda r: (r["model_id"], r["query_id"]))

    # Write raw_responses.jsonl
    raw_path = out_dir / "raw_responses.jsonl"
    with raw_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # Write run manifest
    manifest = {
        "run_id": run_id,
        "project": project,
        "created_at": created_at,
        "runner": "chat_completions",
        "query_pool": str(args.query_pool),
        "model_config": str(args.model_config),
        "model_count": len(enabled_models),
        "query_count": len(queries),
        "record_count": len(rows),
        "timeout_per_request": args.timeout,
        "workers": args.workers,
    }
    manifest_path = out_dir / "run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n[devtool-answer-monitor] Done. {len(rows)} records written to {raw_path}")
    print(f"[devtool-answer-monitor] Manifest: {manifest_path}")
    print(f"\nNext step — annotate scores, then generate report:")
    print(f"  python -m devtool_answer_monitor report --input {raw_path} --output-dir {out_dir}")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
