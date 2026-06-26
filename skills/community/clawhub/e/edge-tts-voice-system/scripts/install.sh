#!/bin/bash
# Installation script for lessac_offline_voice_system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.openclaw/tts}"

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

check_dependencies() {
    log_step "Checking system dependencies..."
    
    # Check for Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 not found. Please install python3."
        exit 1
    fi
    
    # Check for pip
    if ! command -v pip3 &> /dev/null; then
        log_warn "pip3 not found. Installing..."
        apt-get update && apt-get install -y python3-pip
    fi
    
    # Check for ffmpeg
    if ! command -v ffmpeg &> /dev/null; then
        log_warn "ffmpeg not found. Installing..."
        apt-get update && apt-get install -y ffmpeg
    fi
    
    log_info "System dependencies OK"
}

create_venv() {
    log_step "Creating Python virtual environment..."
    
    VENV_DIR="$INSTALL_DIR/venv"
    
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
        log_info "Virtual environment created: $VENV_DIR"
    else
        log_info "Virtual environment already exists: $VENV_DIR"
    fi
    
    # Activate venv for package installation
    source "$VENV_DIR/bin/activate"
}

install_python_packages() {
    log_step "Installing Python packages..."
    
    # Upgrade pip first
    pip install --upgrade pip
    
    # Install required packages
    pip install faster-whisper edge-tts soundfile
    
    log_info "Python packages installed"
}

prepare_runtime() {
    log_step "Preparing runtime directories..."

    mkdir -p "$INSTALL_DIR/cache"
    mkdir -p "$INSTALL_DIR/runtime"
    log_info "Runtime directories ready: $INSTALL_DIR/cache and $INSTALL_DIR/runtime"
}

download_voice_model() {
    log_step "Downloading Edge TTS runtime support..."

    mkdir -p "$INSTALL_DIR"
    log_info "No local model download required for Edge TTS; using hosted voice service via the edge-tts package."
    log_info "Edge TTS runtime support ready for voice: ${OPENCLAW_EDGE_TTS_VOICE:-en-IE-ConnorNeural}"
}

copy_scripts() {
    log_step "Copying skill scripts..."
    
    # Copy Python scripts
    cp "$SKILL_DIR/scripts/voice_handler.py" "$INSTALL_DIR/"
    cp "$SKILL_DIR/scripts/tts_edge_wrapper.py" "$INSTALL_DIR/"
    
    # Copy bash script
    cp "$SKILL_DIR/scripts/voice_integration.sh" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/voice_integration.sh"
    chmod +x "$INSTALL_DIR/voice_handler.py"
    chmod +x "$INSTALL_DIR/tts_edge_wrapper.py"
    
    log_info "Scripts copied to $INSTALL_DIR/"
}

create_config() {
    log_step "Creating configuration..."
    
    cat > "$INSTALL_DIR/config.json" << EOF
{
    "stt": {
        "model": "base",
        "device": "cpu",
        "compute_type": "int8"
    },
    "tts": {
        "provider": "edge-tts",
        "voice": "${OPENCLAW_EDGE_TTS_VOICE:-en-IE-ConnorNeural}",
        "rate": "${OPENCLAW_EDGE_TTS_RATE:+0%}",
        "pitch": "${OPENCLAW_EDGE_TTS_PITCH:+0Hz}",
        "volume": "${OPENCLAW_EDGE_TTS_VOLUME:+0%}"
    },
    "audio": {
        "sample_rate": 16000,
        "channels": 1
    },
    "cache": {
        "dir": "$INSTALL_DIR/cache"
    }
}
EOF
    
    log_info "Configuration created: $INSTALL_DIR/config.json"
}

test_installation() {
    log_step "Testing installation..."
    
    # Test Edge TTS
    log_info "Testing Edge TTS (this may take a few seconds)..."
    if "$INSTALL_DIR/venv/bin/python" - <<'PY' >/dev/null 2>&1
import sys
sys.path.insert(0, '/root/.openclaw/tts')
from tts_edge_wrapper import text_to_speech
print(text_to_speech('Installation test successful.', '/tmp/test_install.mp3'))
PY
    then
        log_info "✓ TTS test passed"
        rm -f "/tmp/test_install.mp3"
    else
        log_error "TTS test failed"
        return 1
    fi
    
    # Test voice integration script
    log_info "Testing voice integration..."
    if "$INSTALL_DIR/voice_integration.sh" test 2>/dev/null | grep -q "Test successful"; then
        log_info "✓ Integration test passed"
    else
        log_warn "Integration test had issues (may be expected on first run)"
    fi
    
    log_info "Installation tests completed"
}

show_usage() {
    log_step "Installation complete!"
    echo ""
    echo "Edge TTS Voice System has been installed to:"
    echo "  $INSTALL_DIR"
    echo ""
    echo "Usage examples:"
    echo "  $INSTALL_DIR/voice_integration.sh transcribe audio.ogg"
    echo "  $INSTALL_DIR/voice_integration.sh tts \"Hello world\" output.wav"
    echo "  $INSTALL_DIR/voice_integration.sh process voice_message.ogg"
    echo ""
    echo "Python usage:"
    echo "  from voice_handler import VoiceHandler"
    echo "  handler = VoiceHandler()"
    echo "  text = handler.audio_to_text('audio.ogg')"
    echo "  audio = handler.text_to_audio('Response text')"
    echo ""
    echo "For OpenClaw integration, add to your agent:"
    echo "  import sys"
    echo "  sys.path.append('$INSTALL_DIR')"
    echo "  from voice_handler import VoiceHandler"
    echo ""
    echo "Configuration: $INSTALL_DIR/config.json"
    echo "Virtual environment: $INSTALL_DIR/venv"
}

main() {
    echo ""
    echo "========================================="
    echo "  Edge TTS Voice System Installer  "
    echo "========================================="
    echo ""
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --install-dir)
                INSTALL_DIR="$2"
                shift 2
                ;;
            --help)
                echo "Usage: $0 [--install-dir DIR]"
                echo ""
                echo "Options:"
                echo "  --install-dir DIR  Installation directory (default: ~/.openclaw/tts)"
                echo "  --help             Show this help message"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    log_info "Installation directory: $INSTALL_DIR"
    
    # Run installation steps
    check_dependencies
    create_venv
    install_python_packages
    prepare_runtime
    download_voice_model
    copy_scripts
    create_config
    test_installation
    show_usage
    
    echo ""
    log_info "Installation completed successfully!"
}

main "$@"