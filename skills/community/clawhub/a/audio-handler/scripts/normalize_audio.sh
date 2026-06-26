#!/bin/bash
# Normalize audio volume

set -e

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <input> <output> [target_loudness=-16]"
    echo "Target loudness is in LUFS (default -16, standard for podcasts)"
    echo "Examples:"
    echo "  $0 quiet.mp3 normalized.mp3"
    echo "  $0 podcast.mp3 loud.mp3 -14"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"
TARGET="${3:--16}"

if [[ ! -f "$INPUT" ]]; then
    echo "Error: Input file not found: $INPUT" >&2
    exit 1
fi

echo "Normalizing audio to ${TARGET} LUFS..."

ffmpeg -y -v warning -i "$INPUT" -af "loudnorm=I=${TARGET}:TP=-1.5:LRA=11" "$OUTPUT"

echo "Done!"
ls -lh "$OUTPUT" | awk '{print "Output size:", $5}'