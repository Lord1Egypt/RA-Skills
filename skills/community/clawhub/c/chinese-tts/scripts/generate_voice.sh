#!/bin/bash
# Chinese TTS: text → opus voice file ready for Feishu
# Usage: generate_voice.sh "你好世界" /path/to/output.opus [voice]
# Voice default: zh-CN-YunxiNeural

set -euo pipefail
export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

TEXT="${1:?Usage: generate_voice.sh TEXT OUTPUT_OPUS [VOICE]}"
OUTPUT="${2:?Usage: generate_voice.sh TEXT OUTPUT_OPUS [VOICE]}"
VOICE="${3:-zh-CN-YunxiNeural}"
TMP_MP3=$(mktemp /tmp/tts_XXXXXX.mp3)

trap "rm -f $TMP_MP3" EXIT

/home/clawpi/.local/bin/edge-tts --voice "$VOICE" --text "$TEXT" --write-media "$TMP_MP3"
ffmpeg -i "$TMP_MP3" -c:a libopus -b:a 64k -ar 48000 "$OUTPUT" -y -loglevel error

echo "Generated: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))"
