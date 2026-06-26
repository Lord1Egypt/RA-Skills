#!/bin/bash

# Audio Transcription Script
# Transcribes audio files using available tools

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Arguments
AUDIO_FILE="${1:-}"
LANGUAGE="${2:-auto}"

if [[ -z "$AUDIO_FILE" ]]; then
    echo -e "${RED}Erro: Especifique o arquivo de áudio${NC}"
    echo "Uso: $0 <arquivo_audio> [idioma]"
    exit 1
fi

if [[ ! -f "$AUDIO_FILE" ]]; then
    echo -e "${RED}Erro: Arquivo não encontrado: $AUDIO_FILE${NC}"
    exit 1
fi

# Create temporary directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Function to find and convert audio if needed
prepare_audio() {
    local input="$1"
    local output="$TEMP_DIR/audio_conv.wav"
    
    # Get file extension
    local ext="${input##*.}"
    ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
    
    # If it's already a format whisper can handle, use it directly if possible
    # Otherwise convert to wav using ffmpeg
    if command -v ffmpeg &> /dev/null; then
        if [[ "$ext" == "ogg" ]] || [[ "$ext" == "opus" ]] || [[ "$ext" == "m4a" ]]; then
            echo -e "${YELLOW}Convertendo $ext -> wav...${NC}"
            ffmpeg -i "$input" -ar 16000 -ac 1 -c:a pcm_s16le "$output" -y -hide_banner -loglevel error
            echo "$output"
            return
        fi
    fi
    
    echo "$input"
}

AUDIO_CONV=$(prepare_audio "$AUDIO_FILE")

echo -e "${GREEN}=== Transcrição de Áudio ===${NC}"
echo "Arquivo: $AUDIO_FILE"
echo -e "${YELLOW}Transcrevendo, aguarde...${NC}"

# Try different transcription methods in order of preference

# 1. Try whisper (Python package)
if command -v whisper &> /dev/null; then
    echo "Usando: OpenAI Whisper (Python)"
    if [[ "$LANGUAGE" == "auto" ]]; then
        whisper "$AUDIO_CONV" --model small --output_dir "$TEMP_DIR" --output_format txt --fp16 False 2>/dev/null | head -1 > "$TEMP_DIR/output.txt"
    else
        whisper "$AUDIO_CONV" --model small --language "$LANGUAGE" --output_dir "$TEMP_DIR" --output_format txt --fp16 False 2>/dev/null | head -1 > "$TEMP_DIR/output.txt"
    fi
    cat "$TEMP_DIR"/*.txt 2>/dev/null | head -c 10000
    exit 0
fi

# 2. Try whisper.cpp if available
WHISPER_CPP="$HOME/whisper.cpp/main"
WHISPER_MODEL="$HOME/whisper.cpp/models/ggml-small.bin"

if [[ -f "$WHISPER_CPP" ]] && [[ -f "$WHISPER_MODEL" ]]; then
    echo "Usando: whisper.cpp (local)"
    "$WHISPER_CPP" -f "$AUDIO_CONV" -m "$WHISPER_MODEL" -otxt -of "$TEMP_DIR/output" --no-timestamps 2>/dev/null
    cat "$TEMP_DIR/output.txt" 2>/dev/null | head -c 10000
    exit 0
fi

# 3. Try using OpenAI API if key is set
if [[ -n "${OPENAI_API_KEY:-}" ]]; then
    echo "Usando: OpenAI API"
    
    # Convert to mp3 if needed
    if [[ "$AUDIO_CONV" != *.mp3 ]]; then
        ffmpeg -i "$AUDIO_CONV" "$TEMP_DIR/audio.mp3" -y -hide_banner -loglevel error
        AUDIO_CONV="$TEMP_DIR/audio.mp3"
    fi
    
    if [[ "$LANGUAGE" == "auto" ]]; then
        curl -s -X POST https://api.openai.com/v1/audio/transcriptions \
            -H "Authorization: Bearer $OPENAI_API_KEY" \
            -H "Content-Type: multipart/form-data" \
            -F file=@"$AUDIO_CONV" \
            -F "model=whisper-1" \
            -F "response_format=text"
    else
        curl -s -X POST https://api.openai.com/v1/audio/transcriptions \
            -H "Authorization: Bearer $OPENAI_API_KEY" \
            -H "Content-Type: multipart/form-data" \
            -F file=@"$AUDIO_CONV" \
            -F "model=whisper-1" \
            -F "response_format=text" \
            -F "language=$LANGUAGE"
    fi
    echo ""  # newline
    exit 0
fi

# No transcription tool available
echo -e "${RED}Erro: Nenhuma ferramenta de transcrição disponível.${NC}"
echo "Instale uma das opções:"
echo "  - pip install openai-whisper"
echo "  - Configurar OPENAI_API_KEY"
echo "  - Instalar whisper.cpp em ~/whisper.cpp"
exit 1
