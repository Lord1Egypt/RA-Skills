#!/bin/bash
# Trim audio file

set -e

if [[ $# -lt 4 ]]; then
    echo "Usage: $0 <input> <output> <start> <end>"
    echo "Time format: seconds or HH:MM:SS"
    echo "Examples:"
    echo "  $0 podcast.mp3 clip.mp3 30 90       # From 30s to 90s"
    echo "  $0 interview.mp3 part.mp3 1:30 5:00 # From 1:30 to 5:00"
    echo "  $0 audio.mp3 start.mp3 0 60         # First 60 seconds"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"
START="$3"
END="$4"

if [[ ! -f "$INPUT" ]]; then
    echo "Error: Input file not found: $INPUT" >&2
    exit 1
fi

# Get duration for validation
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$INPUT")

echo "Input duration: ${DURATION}s"
echo "Trimming: $START to $END"

# Use -ss before -i for fast seeking, then encode for accuracy
ffmpeg -y -v warning -ss "$START" -i "$INPUT" -to "$END" -c:a copy "$OUTPUT" 2>/dev/null || {
    echo "Fast trim failed, re-encoding for accuracy..."
    ffmpeg -y -v warning -i "$INPUT" -ss "$START" -to "$END" "$OUTPUT"
}

echo "Done!"
ls -lh "$OUTPUT" | awk '{print "Output size:", $5}'