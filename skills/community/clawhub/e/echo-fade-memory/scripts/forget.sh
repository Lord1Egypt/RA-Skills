#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
BASE_URL="${EFM_BASE_URL:-$($SCRIPT_DIR/_resolve_base_url.py)}"
TARGET="${1:-}"
OBJECT_TYPE="${2:-auto}"

if [ -z "$TARGET" ]; then
  echo "usage: $(basename "$0") <query-or-id> [memory|image|auto]" >&2
  exit 1
fi

python3 - "$BASE_URL" "$TARGET" "$OBJECT_TYPE" <<'PY'
import json
import sys
import urllib.request

base_url, target, object_type = sys.argv[1], sys.argv[2], sys.argv[3]
payload = {"query": target, "k": 5}
if object_type and object_type != "auto":
    payload["object_type"] = object_type
req = urllib.request.Request(
    f"{base_url.rstrip('/')}/v1/tools/forget",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode("utf-8"))
print(json.dumps(data, indent=2, ensure_ascii=False))
PY
