#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

SYSTEM_PROMPT = "Answer as a neutral technical assistant. Keep the answer concise but complete."


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_links(text):
    return re.findall(r"https?://\S+", text or "")


def get_client():
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise SystemExit("openai package is required. Install with: pip install -r requirements.txt") from exc
    return OpenAI()


def call_model(client, model_cfg, query):
    resp = client.responses.create(
        model=model_cfg["api_model"],
        temperature=model_cfg.get("temperature", 0.1),
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )
    text = getattr(resp, "output_text", "") or ""
    return {"response_text": text, "response_id": getattr(resp, "id", None)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query-pool", required=True)
    ap.add_argument("--model-config", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--manual-responses", help="Optional JSON object keyed by model_id::query_id")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    query_pool = load_json(args.query_pool)
    model_config = load_json(args.model_config)
    manual = load_json(args.manual_responses) if args.manual_responses else {}

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_id = out_dir.name
    created_at = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    client = None
    enabled_models = [m for m in model_config.get("models", []) if m.get("enabled", True)]
    queries = query_pool["segments"][: args.limit] if args.limit else query_pool["segments"]

    raw_path = out_dir / "raw_responses.jsonl"
    draft_path = out_dir / "score_draft.jsonl"
    manifest_path = out_dir / "run_manifest.json"

    with raw_path.open("w", encoding="utf-8") as raw_f, draft_path.open("w", encoding="utf-8") as draft_f:
        for model in enabled_models:
            for query in queries:
                key = f"{model['id']}::{query['id']}"
                if key in manual:
                    result = {"response_text": manual[key], "response_id": None, "mode": "manual"}
                else:
                    if model.get("provider") != "openai_compatible":
                        result = {"response_text": "", "response_id": None, "mode": "unsupported", "error": "unsupported provider"}
                    else:
                        client = client or get_client()
                        try:
                            call = call_model(client, model, query["query"])
                            result = {**call, "mode": "api"}
                        except Exception as exc:
                            result = {"response_text": "", "response_id": None, "mode": "api", "error": str(exc)}

                raw_record = {
                    "run_id": run_id,
                    "project": query_pool["project"],
                    "query_id": query["id"],
                    "query_type": query["type"],
                    "language": query["language"],
                    "funnel_stage": query.get("funnel_stage"),
                    "target_surface": query.get("target_surface"),
                    "desired_action": query.get("desired_action"),
                    "model_id": model["id"],
                    "query_text": query["query"],
                    "response_text": result.get("response_text", ""),
                    "response_id": result.get("response_id"),
                    "mode": result.get("mode"),
                    "error": result.get("error"),
                    "source_links": extract_links(result.get("response_text", "")),
                    "captured_at": created_at,
                }
                draft_record = {
                    **raw_record,
                    "mention_score": None,
                    "sentiment_score": None,
                    "capability_score": None,
                    "ecosystem_score": None,
                    "needs_repair": None,
                    "repair_type": "none",
                    "annotator": None,
                    "review_status": "draft",
                }
                raw_f.write(json.dumps(raw_record, ensure_ascii=False) + "\n")
                draft_f.write(json.dumps(draft_record, ensure_ascii=False) + "\n")

    manifest = {
        "run_id": run_id,
        "project": query_pool["project"],
        "created_at": created_at,
        "query_pool": str(args.query_pool),
        "model_config": str(args.model_config),
        "record_count": len(enabled_models) * len(queries),
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.exit(main())
