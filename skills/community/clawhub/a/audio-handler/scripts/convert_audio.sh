#!/bin/bash
# Convert audio between formats

set -e

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <input> <output> [quality]"
    echo "Examples:"
    echo "  $0 recording.wav output.mp3"
    echo "  $0 input.flac output.mp3 192"
    echo "  $0 voice.mp3 podcast.opus"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"
QUALITY="${3:-}"

if [[ ! -f "$INPUT" ]]; then
    echo "Error: Input file not found: $INPUT" >&2
    exit 1
fi

OUT_EXT="${OUTPUT##*.}"
OUT_EXT="${OUT_EXT,,}"

# Determine codec and quality settings
case "$OUT_EXT" in
    mp3)
        CODEC="libmp3lame"
        if [[ -n "$QUALITY" ]]; then
            QUAL_OPTS="-b:a ${QUALITY}k"
        else
            QUAL_OPTS="-qscale:a 2"  # VBR ~190kbps, good quality
        fi
        ;;
    wav)
        CODEC="pcm_s16le"
        QUAL_OPTS=""
        ;;
    flac)
        CODEC="flac"
        QUAL_OPTS=""
        ;;
    m4a|aac)
        CODEC="aac"
        if [[ -n "$QUALITY" ]]; then
            QUAL_OPTS="-b:a ${QUALITY}k"
        else
            QUAL_OPTS="-b:a 256k"
        fi
        ;;
    ogg)
        CODEC="libvorbis"
        if [[ -n "$QUALITY" ]]; then
            QUAL_OPTS="-qscale:a $((QUALITY / 40))"  # Approximate mapping
        else
            QUAL_OPTS="-qscale:a 5"
        fi
        ;;
    opus)
        CODEC="libopus"
        if [[ -n "$QUALITY" ]]; then
            QUAL_OPTS="-b:a ${QUALITY}k"
        else
            QUAL_OPTS="-b:a 64k"  # Good for speech
        fi
        ;;
    *)
        echo "Error: Unsupported output format: $OUT_EXT" >&2
        exit 1
        ;;
esac

echo "Converting: $INPUT -> $OUTPUT"
ffmpeg -y -v warning -i "$INPUT" -codec:a $CODEC $QUAL_OPTS "$OUTPUT"

echo "Done!"
ls -lh "$OUTPUT" | awk '{print "Output size:", $5}'