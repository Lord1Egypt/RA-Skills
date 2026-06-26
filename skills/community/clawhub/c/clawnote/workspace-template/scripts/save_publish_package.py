#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime
from pathlib import Path


OUTPUT_DIR = Path(".openclaw/pending-xhs")


def slugify(text):
    text = re.sub(r"\s+", "-", text.strip().lower())
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff_-]", "", text)
    return text[:48] or "draft"


def load_payload(path_arg):
    if path_arg:
        return json.loads(Path(path_arg).read_text(encoding="utf-8"))
    import sys
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise SystemExit("Provide --input <json-file> or pipe JSON via stdin.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--kind", default="general")
    args = parser.parse_args()

    payload = load_payload(args.input)
    title = str(payload.get("title", "")).strip()
    if not title:
        raise SystemExit("Payload must include a non-empty title.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = OUTPUT_DIR / f"{stamp}-{args.kind}-{slugify(title)}.json"

    enriched = dict(payload)
    enriched.setdefault("status", "pending_review")
    enriched.setdefault("created_at", datetime.now().isoformat(timespec="seconds"))
    enriched.setdefault("kind", args.kind)

    path.write_text(json.dumps(enriched, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
