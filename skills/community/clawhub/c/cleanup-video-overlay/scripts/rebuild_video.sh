#!/usr/bin/env bash
set -euo pipefail

FRAMES_DIR=""
SOURCE_VIDEO=""
OUTPUT=""
FPS=""
PATTERN="frame_%06d.png"
PIX_FMT="yuv420p"
CODEC="libx264"
CRF="18"
PRESET="medium"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --frames-dir) FRAMES_DIR="$2"; shift 2 ;;
    --source-video) SOURCE_VIDEO="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --fps) FPS="$2"; shift 2 ;;
    --pattern) PATTERN="$2"; shift 2 ;;
    --pix-fmt) PIX_FMT="$2"; shift 2 ;;
    --codec) CODEC="$2"; shift 2 ;;
    --crf) CRF="$2"; shift 2 ;;
    --preset) PRESET="$2"; shift 2 ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$FRAMES_DIR" || -z "$SOURCE_VIDEO" || -z "$OUTPUT" || -z "$FPS" ]]; then
  echo "Usage: rebuild_video.sh --frames-dir dir --source-video input --output out.mp4 --fps fps" >&2
  exit 1
fi

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT
SILENT_VIDEO="$TMPDIR/rebuilt_silent.mp4"

ffmpeg -y \
  -framerate "$FPS" \
  -i "$FRAMES_DIR/$PATTERN" \
  -c:v "$CODEC" \
  -preset "$PRESET" \
  -crf "$CRF" \
  -pix_fmt "$PIX_FMT" \
  "$SILENT_VIDEO"

if ffprobe -v error -select_streams a:0 -show_entries stream=codec_type -of csv=p=0 "$SOURCE_VIDEO" >/dev/null 2>&1; then
  ffmpeg -y -i "$SILENT_VIDEO" -i "$SOURCE_VIDEO" -map 0:v:0 -map 1:a? -c:v copy -c:a copy -shortest "$OUTPUT"
else
  cp "$SILENT_VIDEO" "$OUTPUT"
fi
