#!/usr/bin/env bash
# Mirror this authoritative geo-viz package into cursor-service HyperFrames skills.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SRC/../../../.." && pwd)" # design/public/aigc-web-push/geo-viz → project root
DST="$ROOT/cursor-service/cursor-config/skills/geo-viz"
if [[ ! -d "$ROOT/cursor-service/cursor-config/skills" ]]; then
  echo "cursor-service skills dir not found: $ROOT/cursor-service/cursor-config/skills" >&2
  exit 1
fi
mkdir -p "$DST"
rsync -a --delete \
  --exclude 'sync-to-hyperframes.sh' \
  "$SRC/" "$DST/"
echo "Synced geo-viz → $DST"
