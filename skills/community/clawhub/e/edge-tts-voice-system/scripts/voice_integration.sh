#!/bin/bash
# Voice Integration Script for OpenClaw
# Handles voice messages and responses

set -e

# Configuration
VENV_PYTHON="/tmp/venv/bin/python"
TTS_WRAPPER="/root/.openclaw/tts/tts_edge_wrapper.py"
VOICE_HANDLER_SCRIPT="/root/.openclaw/tts/voice_handler.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to transcribe audio
transcribe_audio() {
    local audio_file="$1"
    
    if [ ! -f "$audio_file" ]; then
        log_error "Audio file not found: $audio_file"
        return 1
    fi
    
    log_info "Transcribing audio: $audio_file"
    
    # Use faster-whisper via Python
    "$VENV_PYTHON" -c "
from faster_whisper import WhisperModel
import sys
import json

model = WhisperModel('base', device='cpu', compute_type='int8')
segments, info = model.transcribe('$audio_file', beam_size=5)
text = ' '.join(segment.text for segment in segments)
print(json.dumps({
    'text': text.strip(),
    'language': info.language,
    'probability': info.language_probability
}))
" 2>/dev/null
}

# Function to generate TTS audio
generate_tts() {
    local text="$1"
    local output_file="${2:-/tmp/tts_output.wav}"
    
    log_info "Generating TTS for text: ${text:0:50}..."
    
    "$VENV_PYTHON" "$PIPER_TTS_SCRIPT" "$text" "$output_file"
    
    if [ -f "$output_file" ]; then
        echo "$output_file"
    else
        log_error "Failed to generate TTS audio"
        return 1
    fi
}

# Function to process a voice message
process_voice_message() {
    local audio_file="$1"
    
    log_info "Processing voice message: $audio_file"
    
    # Step 1: Transcribe
    transcription_json=$(transcribe_audio "$audio_file")
    if [ $? -ne 0 ]; then
        log_error "Transcription failed"
        return 1
    fi
    
    # Parse JSON output
    transcription=$(echo "$transcription_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data['text'])")
    language=$(echo "$transcription_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data['language'])")
    probability=$(echo "$transcription_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data['probability'])")
    
    log_info "Transcription: $transcription"
    log_info "Language: $language (probability: $probability)"
    
    # Step 2: Generate response (this would normally come from AI)
    response_text="I heard you say: $transcription. This is a response from the voice system."
    
    # Step 3: Generate TTS response
    response_audio=$(generate_tts "$response_text")
    
    if [ $? -eq 0 ]; then
        log_info "Response audio generated: $response_audio"
        echo "$transcription|$response_audio"
    else
        log_error "Failed to generate response audio"
        return 1
    fi
}

# Main execution
case "${1:-}" in
    "transcribe")
        if [ -z "$2" ]; then
            log_error "Usage: $0 transcribe <audio_file>"
            exit 1
        fi
        transcribe_audio "$2"
        ;;
    "tts")
        if [ -z "$2" ]; then
            log_error "Usage: $0 tts <text> [output_file]"
            exit 1
        fi
        generate_tts "$2" "${3:-}"
        ;;
    "process")
        if [ -z "$2" ]; then
            log_error "Usage: $0 process <audio_file>"
            exit 1
        fi
        process_voice_message "$2"
        ;;
    "test")
        log_info "Testing voice system..."
        test_file="/tmp/test_voice_$(date +%s).wav"
        generate_tts "This is a test of the Edge TTS voice system." "$test_file"
        if [ -f "$test_file" ]; then
            log_info "Test successful: $test_file"
            echo "$test_file"
        else
            log_error "Test failed"
        fi
        ;;
    *)
        echo "Voice System for OpenClaw"
        echo "========================="
        echo "Commands:"
        echo "  transcribe <audio_file>  - Transcribe audio to text"
        echo "  tts <text> [output]      - Convert text to speech"
        echo "  process <audio_file>     - Full voice message processing"
        echo "  test                     - Test the voice system"
        echo ""
        echo "Current configuration:"
        echo "  TTS Voice: ${OPENCLAW_EDGE_TTS_VOICE:-en-IE-ConnorNeural}"
        echo "  STT Model: faster-whisper base"
        echo "  Python: $VENV_PYTHON"
        ;;
esac