#!/usr/bin/env bash
# weekly.sh — Render and deliver the weekly marathon clip.
#
# Always renders the previous Mon→Sun week (week that just ended yesterday
# if today is Monday in Asia/Jerusalem). Falls back to last-7-days if the
# computation produces an empty range.
set -euo pipefail

SKILL_DIR="$HOME/.openclaw/workspace/skills/marathon-clip"
PROJ="$HOME/.openclaw/workspace/projects/sahi-video"

# Compute "last Monday → last Sunday" in Asia/Jerusalem.
# date supports %u (1=Mon..7=Sun) so we offset from today.
TZ="Asia/Jerusalem"
export TZ

TODAY=$(date +%Y-%m-%d)
DOW=$(date +%u)                # 1..7

# If today is Monday (1), the just-ended week is yesterday-6 .. yesterday.
# Otherwise compute the most recent Sunday and step back 6 days to that Monday.
if [[ "$DOW" == "1" ]]; then
  END=$(date -d "$TODAY -1 day" +%Y-%m-%d)
else
  END=$(date -d "$TODAY -$DOW day +1 day" +%Y-%m-%d 2>/dev/null)
  # fallback simple computation: days_back = DOW
  END=$(date -d "$TODAY -$DOW day" +%Y-%m-%d)
fi
START=$(date -d "$END -6 day" +%Y-%m-%d)
echo "[weekly] window: $START → $END (today=$TODAY, dow=$DOW)"

OUT_DIR="$PROJ/out"
OUT="$OUT_DIR/weekly-$END.mp4"
mkdir -p "$OUT_DIR"

echo "[weekly] [1/3] Building data…"
node "$SKILL_DIR/scripts/build-data.cjs" --from "$START" --to "$END" --out "$PROJ/data.json"

echo "[weekly] [2/3] Fetching GPX tracks…"
if ! node "$SKILL_DIR/scripts/build-tracks.cjs" --days 7 --out "$PROJ/tracks.json"; then
  echo "[weekly]   (tracks fetch failed; using empty)" >&2
  echo "[]" > "$PROJ/tracks.json"
fi

# Re-trim music to a longer duration matching the expected video length.
# total = 4 + 9 + N*4 + 8 + 8 + 5; bound to [40, 70].
N_TRACKS=$(node -e "console.log(JSON.parse(require('fs').readFileSync(process.argv[1])).length)" "$PROJ/tracks.json")
DURATION=$((4 + 9 + N_TRACKS * 4 + 8 + 8 + 5))
MUSIC_LEN=$((DURATION + 5))
if [[ -f "$PROJ/public/music-full.mp3" ]]; then
  ffmpeg -y -loglevel error -i "$PROJ/public/music-full.mp3" -ss 0 -t "$MUSIC_LEN" \
    -af "afade=t=in:st=0:d=0.5,afade=t=out:st=$((MUSIC_LEN - 2)):d=2" \
    -ac 2 -ar 44100 -b:a 192k "$PROJ/public/music.mp3"
fi

echo "[weekly] [3/3] Rendering ($DURATION s)…"
cd "$PROJ"
npx remotion render src/index.ts MarathonClip "$OUT" --log=info

echo "[weekly] Output: $OUT"
ls -la "$OUT"

# Copy to OpenClaw managed outbound directory so MEDIA: delivery works.
OUTBOUND_DIR="$HOME/.openclaw/media/outbound"
mkdir -p "$OUTBOUND_DIR"
UUID=$(python3 -c "import uuid; print(uuid.uuid4())" 2>/dev/null || cat /proc/sys/kernel/random/uuid)
DELIVER="$OUTBOUND_DIR/weekly-${END}---${UUID}.mp4"
cp "$OUT" "$DELIVER"
echo "[weekly] Delivery copy: $DELIVER"

# Emit BOTH the source path (for debugging) and the delivery path (the one to ship).
# Downstream agents should prefer MARATHON_CLIP_DELIVER for MEDIA: lines.
echo "MARATHON_CLIP_OUT=$OUT"
echo "MARATHON_CLIP_DELIVER=$DELIVER"
