#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

INPUT=""
OUTPUT=""
MODE="removelogo"
WORKDIR=""
KEEP_WORKDIR=0
EDITOR_CMD=""
PROMPT=""
MODEL=""
IMAGE_SIZE=""
CONCURRENCY=""
FPS=""
REGIONS=()
PRESETS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input) INPUT="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --mode) MODE="$2"; shift 2 ;;
    --workdir) WORKDIR="$2"; shift 2 ;;
    --keep-workdir) KEEP_WORKDIR=1; shift 1 ;;
    --editor-cmd) EDITOR_CMD="$2"; shift 2 ;;
    --prompt) PROMPT="$2"; shift 2 ;;
    --model) MODEL="$2"; shift 2 ;;
    --image-size) IMAGE_SIZE="$2"; shift 2 ;;
    --concurrency) CONCURRENCY="$2"; shift 2 ;;
    --fps) FPS="$2"; shift 2 ;;
    --region) REGIONS+=("$2"); shift 2 ;;
    --preset) PRESETS+=("$2"); shift 2 ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$INPUT" || -z "$OUTPUT" ]]; then
  echo "Usage: clean_video.sh --input in.mp4 --output out.mp4 [--mode removelogo|frame-edit|gemini-nano-banana] [--region x:y:w:h] [--preset name]" >&2
  exit 1
fi

if [[ ${#REGIONS[@]} -eq 0 && ${#PRESETS[@]} -eq 0 ]]; then
  echo "Provide at least one --region or --preset" >&2
  exit 1
fi

if [[ -z "$WORKDIR" ]]; then
  BASENAME="$(basename "$INPUT")"
  STEM="${BASENAME%.*}"
  WORKDIR="$(dirname "$OUTPUT")/${STEM}_overlay_cleanup_work"
fi

mkdir -p "$WORKDIR" "$WORKDIR/logs" "$WORKDIR/temp"
MANIFEST="$WORKDIR/manifest.json"
MASK="$WORKDIR/mask.pgm"
FRAME_DIR="$WORKDIR/frames"
EDITED_DIR="$WORKDIR/edited"
USAGE_DIR="$WORKDIR/usage"
PERSISTENT_LEARNINGS="$SKILL_DIR/persistent_learnings.json"
RUN_ADVICE_ENV="$WORKDIR/run_advice.env"

WIDTH="$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=nw=1:nk=1 "$INPUT")"
HEIGHT="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=nw=1:nk=1 "$INPUT")"
if [[ -z "$FPS" ]]; then
  FPS="$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=nw=1:nk=1 "$INPUT" | awk -F/ '{ if ($2 == "" || $2 == 0) print $1; else printf "%.6f", $1/$2 }')"
fi

MASK_ARGS=(--width "$WIDTH" --height "$HEIGHT" --output "$MASK" --manifest-output "$MANIFEST")
if (( ${#REGIONS[@]} > 0 )); then
  for region in "${REGIONS[@]}"; do
    MASK_ARGS+=(--region "$region")
  done
fi
if (( ${#PRESETS[@]} > 0 )); then
  for preset in "${PRESETS[@]}"; do
    MASK_ARGS+=(--preset "$preset")
  done
fi
python3 "$SCRIPT_DIR/make_mask.py" "${MASK_ARGS[@]}" >/dev/null

if [[ -f "$PERSISTENT_LEARNINGS" ]]; then
  python3 "$SCRIPT_DIR/prepare_run_advice.py" \
    --workdir "$WORKDIR" \
    --mode "$MODE" \
    --fps "$FPS" \
    --concurrency "${CONCURRENCY:-2}" \
    --model "${MODEL:-${GEMINI_MODEL:-}}" \
    --image-size "${IMAGE_SIZE:-${GEMINI_IMAGE_SIZE:-}}" \
    --persistent-learnings "$PERSISTENT_LEARNINGS" >/dev/null
  if [[ -f "$RUN_ADVICE_ENV" ]]; then
    # shellcheck disable=SC1090
    source "$RUN_ADVICE_ENV"
  fi
fi

cleanup() {
  if [[ "$KEEP_WORKDIR" -eq 0 ]]; then
    rm -rf "$WORKDIR"
  fi
}
trap cleanup EXIT

case "$MODE" in
  removelogo)
    ffmpeg -y -i "$INPUT" -vf "removelogo=f=$MASK" -map 0:v:0 -map 0:a? -c:v libx264 -crf 18 -preset medium -c:a copy "$OUTPUT"
    ;;
  frame-edit)
    if [[ -z "$EDITOR_CMD" ]]; then
      echo "--editor-cmd is required for --mode frame-edit" >&2
      exit 1
    fi
    bash "$SCRIPT_DIR/extract_frames.sh" --input "$INPUT" --outdir "$FRAME_DIR" --fps "$FPS"
    python3 "$SCRIPT_DIR/restore_frames.py" \
      --frames-dir "$FRAME_DIR" \
      --output-dir "$EDITED_DIR" \
      --editor-cmd "$EDITOR_CMD" \
      --mask "$MASK" \
      --progress-mode generic \
      --manifest-output "$WORKDIR/frame_jobs.json" >/dev/null
    bash "$SCRIPT_DIR/rebuild_video.sh" \
      --frames-dir "$EDITED_DIR" \
      --source-video "$INPUT" \
      --output "$OUTPUT" \
      --fps "$FPS"
    python3 "$SCRIPT_DIR/summarize_run.py" \
      --workdir "$WORKDIR" \
      --input-video "$INPUT" \
      --output-video "$OUTPUT" \
      --mode "$MODE" \
      --fps "$FPS" \
      --persistent-learnings "$PERSISTENT_LEARNINGS" >/dev/null
    ;;
  gemini-nano-banana)
    if [[ -z "${GEMINI_API_KEY:-}" ]]; then
      echo "Missing API key. Set GEMINI_API_KEY before using --mode gemini-nano-banana." >&2
      exit 1
    fi
    EDITOR_CMD="python3 $SCRIPT_DIR/gemini_nano_banana_edit.py --input {input} --mask {mask} --output {output} --usage-output {usage_output}"
    if [[ -n "$MODEL" ]]; then
      printf -v ESCAPED_MODEL '%q' "$MODEL"
      EDITOR_CMD="$EDITOR_CMD --model $ESCAPED_MODEL"
    fi
    if [[ -n "$IMAGE_SIZE" ]]; then
      printf -v ESCAPED_IMAGE_SIZE '%q' "$IMAGE_SIZE"
      EDITOR_CMD="$EDITOR_CMD --image-size $ESCAPED_IMAGE_SIZE"
    fi
    if [[ -n "$PROMPT" ]]; then
      printf -v ESCAPED_PROMPT '%q' "$PROMPT"
      EDITOR_CMD="$EDITOR_CMD --prompt $ESCAPED_PROMPT"
    fi
    if [[ -z "$CONCURRENCY" ]]; then
      CONCURRENCY=2
    fi
    if [[ -n "${LEARNED_CONCURRENCY:-}" ]]; then
      CONCURRENCY="$LEARNED_CONCURRENCY"
    fi
    bash "$SCRIPT_DIR/extract_frames.sh" --input "$INPUT" --outdir "$FRAME_DIR" --fps "$FPS"
    EDITOR_CMD="$EDITOR_CMD --request-retries ${LEARNED_REQUEST_RETRIES:-3}"
    if [[ -n "${LEARNED_PROMPT_ADDENDUM:-}" ]]; then
      printf -v ESCAPED_PROMPT_ADDENDUM '%q' "$LEARNED_PROMPT_ADDENDUM"
      EDITOR_CMD="$EDITOR_CMD --prompt-addendum $ESCAPED_PROMPT_ADDENDUM"
    fi
    python3 "$SCRIPT_DIR/restore_frames.py" \
      --frames-dir "$FRAME_DIR" \
      --output-dir "$EDITED_DIR" \
      --editor-cmd "$EDITOR_CMD" \
      --mask "$MASK" \
      --progress-mode gemini-nano-banana-2 \
      --image-size "${IMAGE_SIZE:-1K}" \
      --usage-dir "$USAGE_DIR" \
      --concurrency "$CONCURRENCY" \
      --manifest-output "$WORKDIR/frame_jobs.json" >/dev/null
    bash "$SCRIPT_DIR/rebuild_video.sh" \
      --frames-dir "$EDITED_DIR" \
      --source-video "$INPUT" \
      --output "$OUTPUT" \
      --fps "$FPS"
    python3 "$SCRIPT_DIR/summarize_run.py" \
      --workdir "$WORKDIR" \
      --input-video "$INPUT" \
      --output-video "$OUTPUT" \
      --mode "$MODE" \
      --fps "$FPS" \
      --model "${MODEL:-${GEMINI_MODEL:-gemini-3.1-flash-image-preview}}" \
      --image-size "${IMAGE_SIZE:-1K}" \
      --persistent-learnings "$PERSISTENT_LEARNINGS" >/dev/null
    ;;
  *)
    echo "Unknown mode: $MODE" >&2
    exit 1
    ;;
esac

if [[ "$KEEP_WORKDIR" -eq 1 ]]; then
  echo "Kept workdir: $WORKDIR"
fi

echo "Wrote: $OUTPUT"
