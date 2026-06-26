#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

VALID_TYPES = {"mistake", "correction", "discovery", "decision", "regression"}


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:48]
    return slug or "learning"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True, help="Path to JSONL learning store")
    ap.add_argument("--type", default="discovery", choices=sorted(VALID_TYPES))
    ap.add_argument("--summary", required=True)
    ap.add_argument("--details", default="")
    ap.add_argument("--evidence", default="")
    ap.add_argument("--source", default="manual")
    ap.add_argument("--confidence", choices=["low", "medium", "high"], default=None)
    ap.add_argument("--reuse-value", choices=["low", "medium", "high"], default=None)
    ap.add_argument("--impact-scope", choices=["single-task", "project", "workspace", "cross-session"], default=None)
    args = ap.parse_args()

    now = datetime.now(timezone.utc).isoformat()
    record = {
        "id": f"{slugify(args.summary)}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "timestamp": now,
        "source": args.source,
        "type": args.type,
        "summary": args.summary,
        "details": args.details,
        "evidence": args.evidence,
        "confidence": args.confidence,
        "reuse_value": args.reuse_value,
        "impact_scope": args.impact_scope,
        "promotion_target_candidates": [],
        "status": "captured",
        "related_ids": [],
    }

    store = Path(args.store)
    store.parent.mkdir(parents=True, exist_ok=True)
    with store.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
