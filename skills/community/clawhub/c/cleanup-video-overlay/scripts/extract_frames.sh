#!/usr/bin/env bash
set -euo pipefail

INPUT=""
OUTDIR=""
FPS=""
PATTERN="frame_%06d.png"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input) INPUT="$2"; shift 2 ;;
    --outdir) OUTDIR="$2"; shift 2 ;;
    --fps) FPS="$2"; shift 2 ;;
    --pattern) PATTERN="$2"; shift 2 ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$INPUT" || -z "$OUTDIR" ]]; then
  echo "Usage: extract_frames.sh --input file --outdir dir [--fps value] [--pattern frame_%06d.png]" >&2
  exit 1
fi

mkdir -p "$OUTDIR"

if [[ -n "$FPS" ]]; then
  ffmpeg -y -i "$INPUT" -vf "fps=$FPS" "$OUTDIR/$PATTERN"
else
  ffmpeg -y -i "$INPUT" "$OUTDIR/$PATTERN"
fi
