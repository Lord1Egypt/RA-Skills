#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
BASE_URL="${EFM_BASE_URL:-$($SCRIPT_DIR/_resolve_base_url.py)}"

python3 - "$BASE_URL" "$@" <<'PY'
import argparse
import json
import sys
import urllib.request

base_url = sys.argv[1]
argv = sys.argv[2:]

parser = argparse.ArgumentParser(
    prog="store.sh",
    description="Store a memory or image through the unified tool contract. Prefer minimal inputs: memory uses content+summary+type, image uses file_path/url plus optional caption/tags/ocr_text.",
)
parser.add_argument("payload", nargs="?")
parser.add_argument("--object-type", choices=["memory", "image"], default="memory")
parser.add_argument("--type", dest="memory_type", default="project")
parser.add_argument("--summary", default="")
parser.add_argument("--importance", type=float, default=0.8)
parser.add_argument("--ref", default="session:manual")
parser.add_argument("--kind", default="chat")
parser.add_argument("--conflict-group", default="")
parser.add_argument("--session", default="")
parser.add_argument("--actor", default="")
parser.add_argument("--url", default="")
parser.add_argument("--caption", default="")
parser.add_argument("--tag", action="append", dest="tags", default=[])
parser.add_argument("--ocr-text", default="")
parser.add_argument("--memory-id", action="append", dest="memory_ids", default=[])
args = parser.parse_args(argv)

payload = {"object_type": args.object_type}
if args.object_type == "memory":
    if not args.payload:
        raise SystemExit("usage: store.sh <content> [--summary TEXT] [--type TYPE]")
    payload.update(
        {
            "content": args.payload,
            "memory_type": args.memory_type,
            "summary": args.summary,
            "importance": float(args.importance),
            "source_kind": args.kind,
            "source_ref": args.ref,
        }
    )
    if args.conflict_group:
        payload["conflict_group"] = args.conflict_group
else:
    if not args.payload and not args.url:
        raise SystemExit("usage: store.sh <file-path> --object-type image [--caption TEXT] [--tag TAG] [--ocr-text TEXT] or store.sh --object-type image --url URL")
    payload.update(
        {
            "file_path": args.payload or "",
            "url": args.url,
            "source_session": args.session,
            "source_kind": args.kind,
            "source_actor": args.actor,
            "caption": args.caption,
            "tags": args.tags,
            "ocr_text": args.ocr_text,
            "linked_memory_ids": args.memory_ids,
        }
    )

req = urllib.request.Request(
    f"{base_url.rstrip('/')}/v1/tools/store",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode("utf-8"))
print(json.dumps(data, indent=2, ensure_ascii=False))
PY
