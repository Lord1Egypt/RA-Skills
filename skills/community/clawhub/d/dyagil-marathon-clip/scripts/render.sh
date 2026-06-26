#!/usr/bin/env bash
# marathon-clip — Render a weekly running recap video.
#
# Usage:
#   marathon-clip [--days N] [--out PATH] [--no-music] [--music FILE] [--send-telegram]
set -euo pipefail

DAYS=7
OUT=""
NO_MUSIC=0
MUSIC=""
SEND_TG=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --days) DAYS="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    --no-music) NO_MUSIC=1; shift;;
    --music) MUSIC="$2"; shift 2;;
    --send-telegram) SEND_TG=1; shift;;
    -h|--help)
      sed -n '2,12p' "$0"; exit 0;;
    *) echo "marathon-clip: unknown arg $1" >&2; exit 2;;
  esac
done

PROJ="$HOME/.openclaw/workspace/projects/sahi-video"
SKILL_DIR="$HOME/.openclaw/workspace/skills/marathon-clip"
[[ -z "$OUT" ]] && OUT="$PROJ/out/marathon-week.mp4"

if [[ ! -d "$PROJ" ]]; then
  echo "marathon-clip: project not found at $PROJ" >&2
  echo "  See SKILL.md → first-time setup." >&2
  exit 1
fi

echo "[1/4] Building stats data from sahi-diet (last ${DAYS} days)…"
node "$SKILL_DIR/scripts/build-data.cjs" --days "$DAYS" --out "$PROJ/data.json"

echo "[2/4] Fetching GPX tracks from Garmin…"
if ! node "$SKILL_DIR/scripts/build-tracks.cjs" --days "$DAYS" --out "$PROJ/tracks.json"; then
  echo "  (failed; falling back to existing tracks.json if any)" >&2
  [[ -f "$PROJ/tracks.json" ]] || echo "[]" > "$PROJ/tracks.json"
fi

# Handle music
if [[ $NO_MUSIC -eq 1 ]]; then
  # Temporarily move music out of public/ so Remotion can't find it
  if [[ -f "$PROJ/public/music.mp3" ]]; then
    mv "$PROJ/public/music.mp3" "$PROJ/public/.music.mp3.bak"
  fi
  trap 'if [[ -f "$PROJ/public/.music.mp3.bak" ]]; then mv "$PROJ/public/.music.mp3.bak" "$PROJ/public/music.mp3"; fi' EXIT
elif [[ -n "$MUSIC" ]]; then
  if [[ ! -f "$MUSIC" ]]; then echo "marathon-clip: music file not found: $MUSIC" >&2; exit 1; fi
  cp "$MUSIC" "$PROJ/public/music.mp3"
fi

echo "[3/4] Rendering with Remotion…"
mkdir -p "$(dirname "$OUT")"
cd "$PROJ"
npx remotion render src/index.ts MarathonClip "$OUT" --log=info

echo "[4/4] Done. → $OUT"
ls -la "$OUT"

if [[ $SEND_TG -eq 1 ]]; then
  echo "[4/4] Sending to Telegram…"
  if command -v openclaw >/dev/null 2>&1; then
    openclaw message send --channel telegram --to 6034574482 --media "$OUT" --text "🏃‍♂️ Marathon recap — last $DAYS days" || true
  else
    echo "marathon-clip: openclaw CLI not in PATH; skipped telegram send" >&2
  fi
fi
