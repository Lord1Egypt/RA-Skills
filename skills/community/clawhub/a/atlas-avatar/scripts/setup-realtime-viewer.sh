#!/usr/bin/env bash
# Clone or update the official atlas-realtime-example Next app and write .env.local
# from your shell env (so you can talk to the avatar in the browser after npm run dev).
#
# Requires: git, npm, curl. Uses ATLAS_API_KEY (required).
#
# Env:
#   ATLAS_API_KEY          (required)
#   ATLAS_API_BASE          Atlas host; default https://api.atlasv1.com (written as ATLAS_API_URL in .env.local)
#   ATLAS_REALTIME_VIEWER_DIR  Where to clone; default ~/atlas-realtime-example
#   ATLAS_REALTIME_EXAMPLE_GIT Clone URL; default NorthModelLabs/atlas-realtime-example
#
# Optional passthrough through to .env.local if already set in the shell:
#   LLM_API_KEY LLM_BASE_URL LLM_MODEL ELEVENLABS_API_KEY ELEVENLABS_VOICE_ID
#
set -euo pipefail

if [[ -z "${ATLAS_API_KEY:-}" ]]; then
  echo "ERROR: export ATLAS_API_KEY first (North Model Labs dashboard)." >&2
  exit 2
fi

BASE="${ATLAS_API_BASE:-https://api.atlasv1.com}"
BASE="${BASE%/}"
DEST="${ATLAS_REALTIME_VIEWER_DIR:-${HOME}/atlas-realtime-example}"
REPO="${ATLAS_REALTIME_EXAMPLE_GIT:-https://github.com/NorthModelLabs/atlas-realtime-example.git}"

echo "== Target directory: $DEST"
if [[ ! -d "$DEST" ]]; then
  git clone "$REPO" "$DEST"
elif [[ ! -f "$DEST/package.json" ]]; then
  echo "ERROR: $DEST exists but does not look like atlas-realtime-example (no package.json). Remove it or set ATLAS_REALTIME_VIEWER_DIR." >&2
  exit 2
else
  (cd "$DEST" && git pull --ff-only) || echo "(warn) git pull failed — continuing"
fi

cd "$DEST"

TMP_ENV="$(mktemp)"
trap 'rm -f "$TMP_ENV"' EXIT
{
  printf 'ATLAS_API_KEY=%s\n' "$ATLAS_API_KEY"
  printf 'ATLAS_API_URL=%s\n' "$BASE"
} >"$TMP_ENV"

for v in LLM_API_KEY LLM_BASE_URL LLM_MODEL ELEVENLABS_API_KEY ELEVENLABS_VOICE_ID; do
  eval "val=\${$v:-}"
  if [[ -n "${val}" ]]; then
    printf '%s=%s\n' "$v" "$val" >>"$TMP_ENV"
  fi
done

mv "$TMP_ENV" .env.local
trap - EXIT
chmod 600 .env.local || true

echo "== npm install (may take a minute)"
npm install

echo ""
echo "OK. Next steps:"
echo "  1)  cd \"$DEST\""
echo "  2)  npm run dev"
echo "  3)  Open http://localhost:3000 — Connect (default face loads from /public; or use face URL in the UI)."
echo "  4)  If an agent created a session elsewhere with the same API key, open:"
echo "        http://localhost:3000/watch/<session_id>"
echo ""
echo "This repo uses ATLAS_API_BASE in places; the example app expects ATLAS_API_URL."
echo "This script wrote ATLAS_API_URL=$BASE into .env.local."
