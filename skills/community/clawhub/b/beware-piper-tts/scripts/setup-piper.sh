#!/usr/bin/env bash
set -euo pipefail

# Piper TTS Setup — installs piper-tts and downloads voices
# Usage: setup-piper.sh [--voice <voice-name>] [--voices-dir <path>]

VOICES_DIR="${PIPER_VOICES_DIR:-$HOME/.local/share/piper-voices}"
VOICE=""
HF_BASE="https://huggingface.co/rhasspy/piper-voices/resolve/main/en"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --voice) VOICE="$2"; shift 2 ;;
    --voices-dir) VOICES_DIR="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

mkdir -p "$VOICES_DIR"

# Install piper-tts if not present
if ! python3 -m piper --help &>/dev/null; then
  echo "📦 Installing piper-tts..."
  pip3 install piper-tts
  echo "✅ piper-tts installed"
else
  echo "✅ piper-tts already installed"
fi

# Install ffmpeg if not present (needed for MP3 conversion)
if ! command -v ffmpeg &>/dev/null; then
  echo "📦 Installing ffmpeg..."
  if command -v brew &>/dev/null; then
    brew install ffmpeg
  elif command -v apt-get &>/dev/null; then
    sudo apt-get install -y ffmpeg
  else
    echo "⚠️  Please install ffmpeg manually"
    exit 1
  fi
  echo "✅ ffmpeg installed"
else
  echo "✅ ffmpeg already installed"
fi

# Download voice
download_voice() {
  local voice_name="$1"
  local onnx_file="$VOICES_DIR/${voice_name}.onnx"
  
  if [[ -f "$onnx_file" ]]; then
    echo "✅ Voice already downloaded: $voice_name"
    return 0
  fi

  # Parse voice name: en_US-kusal-medium → en/en_US/kusal/medium
  local lang_region="${voice_name%%-*}"          # en_US
  local rest="${voice_name#*-}"                   # kusal-medium
  local speaker="${rest%-*}"                      # kusal
  local quality="${rest##*-}"                     # medium
  local lang="${lang_region%%_*}"                 # en

  local base_url="${HF_BASE}/${lang_region}/${speaker}/${quality}"
  
  echo "📥 Downloading voice: $voice_name..."
  curl -L -o "$onnx_file" "${base_url}/${voice_name}.onnx"
  curl -L -o "${onnx_file}.json" "${base_url}/${voice_name}.onnx.json"
  echo "✅ Voice downloaded: $voice_name ($(du -h "$onnx_file" | cut -f1))"
}

if [[ -n "$VOICE" ]]; then
  download_voice "$VOICE"
else
  # Default voice
  download_voice "en_US-kusal-medium"
fi

echo ""
echo "🎤 Piper TTS ready!"
echo "   Voices dir: $VOICES_DIR"
echo "   Generate speech: piper-speak.sh \"Hello world!\""
