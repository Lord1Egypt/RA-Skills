#!/usr/bin/env bash
# gen_images.sh — self-contained storyboard image generator.
#
# Reads <job>/input.json, generates one PNG per image_prompts[] entry with
# Google's Gemini image model, and writes them into <job>/images/ using the
# filenames the timeline references. Up to IMAGE_GEN_PARALLEL images at a time.
#
# Env:
#   JOB                 job folder (required)
#   GEMINI_API_KEY      Google Generative Language API key (required)
#   IMAGE_GEN_PARALLEL  max concurrent generations (default 4)
#
# Exit non-zero if any image failed (after attempting the rest).
set -uo pipefail

JOB="${JOB:-${1:-}}"
[ -z "$JOB" ] && { echo "FAILED: set JOB=<job-folder>" >&2; exit 1; }
[ -z "${GEMINI_API_KEY:-}" ] && { echo "FAILED: GEMINI_API_KEY is not set" >&2; exit 1; }

INPUT="$JOB/input.json"
PARALLEL="${IMAGE_GEN_PARALLEL:-4}"
MODEL="gemini-3.1-flash-image-preview"
ENDPOINT="https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent"

mkdir -p "$JOB/images"

# Derive aspect ratio from resolution (WxH).
RES=$(jq -r '.resolution // "1080x1920"' "$INPUT")
case "$RES" in
  1080x1920) AR="9:16" ;;
  1920x1080) AR="16:9" ;;
  1080x1080) AR="1:1" ;;
  *) W=${RES%x*}; H=${RES#*x}; if [ "${W:-0}" -gt "${H:-0}" ]; then AR="16:9"; elif [ "${W:-0}" -lt "${H:-0}" ]; then AR="9:16"; else AR="1:1"; fi ;;
esac

STYLE_ANCHOR=$(jq -r '.image_style.consistency_anchor // ""' "$INPUT")
COLOR_GRADE=$(jq -r '.image_style.color_grade // ""' "$INPUT")

# Generate one image. Args: id  prompt  dest
gen_one() {
  local ID="$1" PROMPT="$2" DEST="$3"
  [ -s "$DEST" ] && { echo "SKIP $DEST (exists)"; return 0; }

  local FULL="$PROMPT"
  [ -n "$STYLE_ANCHOR" ] && FULL="$FULL. $STYLE_ANCHOR"
  [ -n "$COLOR_GRADE" ]  && FULL="$FULL Color grade: $COLOR_GRADE."

  local REQ RESP CODE
  REQ=$(mktemp); RESP=$(mktemp)
  jq -n --arg p "$FULL" --arg ar "$AR" '{
    contents: [{parts: [{text: $p}]}],
    generationConfig: {responseModalities: ["IMAGE"], imageConfig: {aspectRatio: $ar}}
  }' > "$REQ"

  local attempt
  for attempt in 1 2; do
    CODE=$(curl -sS -X POST "$ENDPOINT" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H "Content-Type: application/json" \
      -d @"$REQ" -w "%{http_code}" -o "$RESP")
    if [ "$CODE" = "200" ] && ! jq -e '.error' "$RESP" >/dev/null 2>&1; then
      jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' "$RESP" | base64 -d > "$DEST"
      local SZ
      SZ=$(stat -c%s "$DEST" 2>/dev/null || stat -f%z "$DEST" 2>/dev/null || echo 0)
      if [ "${SZ:-0}" -ge 10000 ]; then
        echo "OK $DEST"; rm -f "$REQ" "$RESP"; return 0
      fi
    fi
    [ "$attempt" = 1 ] && sleep 2
  done

  local ERR
  ERR=$(jq -r '.error.message // "HTTP '"$CODE"'"' "$RESP" 2>/dev/null || echo "HTTP $CODE")
  echo "FAILED $DEST (id=$ID): $ERR" >&2
  rm -f "$REQ" "$RESP"
  return 1
}

# Build the work list: (id \t prompt \t dest) per image_prompts entry,
# destination filename taken from the matching timeline entry's .image.
RC=0
RUNNING=0
while IFS=$'\t' read -r ID PROMPT FILE; do
  [ -z "$ID" ] && continue
  DEST="$JOB/images/$(basename "$FILE")"
  gen_one "$ID" "$PROMPT" "$DEST" &
  RUNNING=$((RUNNING+1))
  if [ "$RUNNING" -ge "$PARALLEL" ]; then wait -n 2>/dev/null || wait; RUNNING=$((RUNNING-1)); fi
done < <(jq -r '
  # Map each image_prompts[] entry to a destination filename. Prefer a timeline
  # entry whose .id matches the prompt id; otherwise positional; otherwise <id>.png.
  (.timeline // []) as $tl
  | [ $tl[] | select(.image) | {key: (.id // .image), image: .image} ] as $byid
  | .image_prompts as $ip
  | range(0; ($ip | length)) as $i
  | $ip[$i] as $p
  | ( ($byid[] | select(.key == $p.id) | .image)
      // $tl[$i].image
      // ($p.id + ".png") ) as $dest
  | [ $p.id, $p.prompt, $dest ] | @tsv
' "$INPUT")
wait

# Recompute result: every prompt id must have produced a file.
TOTAL=$(jq '.image_prompts | length' "$INPUT")
HAVE=$(ls -1 "$JOB/images/"*.png 2>/dev/null | wc -l | tr -d ' ')
echo "Generated $HAVE/$TOTAL images."
[ "${HAVE:-0}" -lt "${TOTAL:-0}" ] && RC=1
exit $RC
