#!/bin/bash
# Focus Audio Player - Optimized version for fast start/stop

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SAMPLES_DIR="$SCRIPT_DIR/../samples"
PID_FILE="/tmp/focus-audio.pid"

# Stop command
if [[ "$1" == "--stop" || "$1" == "stop" ]]; then
    if [[ -f "$PID_FILE" ]]; then
        kill -9 $(cat "$PID_FILE") 2>/dev/null
        rm -f "$PID_FILE"
    fi
    pkill -9 -f "ffplay.*focus-audio" 2>/dev/null
    echo "⏹ Stopped"
    exit 0
fi

# List command
if [[ "$1" == "--list" ]]; then
    echo "Available modes:"
    ls -1 "$SAMPLES_DIR" 2>/dev/null | sed 's/_10s.mp3//' | sed 's/^/  /'
    exit 0
fi

# Parse arguments
MODE="white"
DURATION=10
VOLUME="1.0"

while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--duration)
            DURATION="$2"
            shift 2
            ;;
        -v|--volume)
            VOLUME="$2"
            shift 2
            ;;
        *)
            MODE="$1"
            shift
            ;;
    esac
done

# Map mode to file
case "$MODE" in
    focus|work)       FILE="white_10s.mp3" ;;
    pink|relax)       FILE="pink_10s.mp3" ;;
    sleep|brown)      FILE="brown_10s.mp3" ;;
    rain)              FILE="rain_10s.mp3" ;;
    alpha)            FILE="alpha_10s.mp3" ;;
    beta)             FILE="beta_10s.mp3" ;;
    gamma)            FILE="gamma_10s.mp3" ;;
    meditation|theta) FILE="theta_10s.mp3" ;;
    binaural)         FILE="binaural_10s.mp3" ;;
    bowl|chant|sing)  FILE="bowl_10s.mp3" ;;
    *)                FILE="white_10s.mp3" ;;
esac

AUDIO_FILE="$SAMPLES_DIR/$FILE"

# Check if file exists
if [[ ! -f "$AUDIO_FILE" ]]; then
    echo "Error: Audio file not found: $AUDIO_FILE"
    exit 1
fi

# Kill any existing instance first (fast stop)
pkill -9 -f "ffplay.*focus-audio" 2>/dev/null
rm -f "$PID_FILE"

# Calculate loop count
LOOP_COUNT=$(( (DURATION + 9) / 10 ))

# Start immediately in background
ffplay -nodisp -loop 0 -af "volume=$VOLUME" -loglevel quiet "$AUDIO_FILE" -nostats &
PID=$!
echo $PID > "$PID_FILE"

echo "▶ Playing: $MODE | Duration: ${DURATION}s | Volume: $VOLUME"

# Background the wait so this script returns immediately
if [[ $DURATION -gt 0 ]]; then
    (
        sleep "$DURATION"
        pkill -9 -f "ffplay.*focus-audio" 2>/dev/null
        rm -f "$PID_FILE"
        echo "⏹ Finished"
    ) &
fi