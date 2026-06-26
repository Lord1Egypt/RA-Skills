#!/bin/bash
# Enhanced Audio Processing - Production-grade voice workflow
# FIXED: Corrected SCRIPT_DIR syntax and script paths

set -o pipefail
IFS=$'\n\t'

# ============================================================================
# Configuration
# ============================================================================

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly WORKSPACE="${WORKSPACE:-${HOME}/.openclaw/workspace}"
readonly SKILL_DIR="${SKILL_DIR:-${WORKSPACE}/skills/audio-ptbr-autoreply}"
readonly LOG_LEVEL="${LOG_LEVEL:-WARNING}"
readonly RESPONSE_TIMEOUT="${RESPONSE_TIMEOUT:-30}"

# Find Python executable (portable across environments)
find_python() {
    if [[ -f "${WORKSPACE}/venv/bin/python" ]]; then
        echo "${WORKSPACE}/venv/bin/python"
    elif command -v python3 &>/dev/null; then
        echo "python3"
    elif command -v python &>/dev/null; then
        echo "python"
    else
        return 1
    fi
}

readonly PYTHON="$(find_python)" || {
    echo "ERROR: Python not found in PATH or virtualenv" >&2
    exit 127
}

# ============================================================================
# Logging & Error Handling
# ============================================================================

log() {
    local level="$1"
    shift
    local msg="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        DEBUG) [[ "$LOG_LEVEL" == "DEBUG" ]] && echo "[${timestamp}] DEBUG: ${msg}" >&2 ;;
        INFO)  [[ "$LOG_LEVEL" =~ ^(DEBUG|INFO)$ ]] && echo "[${timestamp}] INFO: ${msg}" >&2 ;;
        WARN)  [[ "$LOG_LEVEL" =~ ^(DEBUG|INFO|WARN)$ ]] && echo "[${timestamp}] WARN: ${msg}" >&2 ;;
        ERROR) echo "[${timestamp}] ERROR: ${msg}" >&2 ;;
    esac
}

error_exit() {
    local msg="$1"
    local code="${2:-1}"
    log ERROR "$msg"
    exit "$code"
}

validate_file() {
    local file="$1"
    local desc="${2:-File}"
    
    if [[ ! -f "$file" ]]; then
        error_exit "$desc not found: $file" 127
    fi
}

# ============================================================================
# Input Validation
# ============================================================================

validate_inputs() {
    local audio_in="$1"
    local target="${2:-}"
    local reply_to="${3:-}"
    
    if [[ -z "$audio_in" ]]; then
        error_exit "Usage: $0 <audio_file> [target] [reply_to]" 1
    fi
    
    if [[ ! -f "$audio_in" ]]; then
        error_exit "Audio file not found: $audio_in" 2
    fi
    
    # Check file size
    local size=$(stat -f%z "$audio_in" 2>/dev/null || stat -c%s "$audio_in" 2>/dev/null)
    if [[ $size -lt 1000 ]]; then
        log WARN "Audio file suspiciously small: ${size} bytes"
    fi
    if [[ $size -gt 157286400 ]]; then
        error_exit "Audio file too large: ${size} bytes" 2
    fi
}

# ============================================================================
# Stage 1: Transcription
# ============================================================================

transcribe_audio() {
    local audio_in="$1"
    
    log INFO "Stage 1: Transcribing audio..."
    
    # FIXED: Support both scripts/ subdirectory and top-level
    local transcribe_script
    if [[ -f "${SKILL_DIR}/scripts/transcribe_universal.py" ]]; then
        transcribe_script="${SKILL_DIR}/scripts/transcribe_universal.py"
    elif [[ -f "${SKILL_DIR}/transcribe_universal.py" ]]; then
        transcribe_script="${SKILL_DIR}/transcribe_universal.py"
    else
        error_exit "Transcribe script not found" 127
    fi
    
    validate_file "$transcribe_script" "Transcribe script"
    
    local transcript
    transcript=$(timeout "$RESPONSE_TIMEOUT" "$PYTHON" \
        "$transcribe_script" \
        "$audio_in" 2>/dev/null | jq -r '.text' 2>/dev/null) || {
        local code=$?
        if [[ $code -eq 124 ]]; then
            error_exit "Transcription timeout (>${RESPONSE_TIMEOUT}s)" 3
        else
            error_exit "Transcription failed (exit code: $code)" 3
        fi
    }
    
    if [[ -z "$transcript" ]]; then
        error_exit "Transcription returned empty text" 3
    fi
    
    log INFO "Transcribed: ${transcript:0:50}..."
    echo "$transcript"
}

# ============================================================================
# Stage 2: Response Generation
# ============================================================================

generate_response() {
    local transcript="$1"
    
    log INFO "Stage 2: Generating response..."
    
    # FIXED: Support both scripts/ subdirectory and top-level
    local adapter_script
    if [[ -f "${SKILL_DIR}/scripts/claude_adapter.py" ]]; then
        adapter_script="${SKILL_DIR}/scripts/claude_adapter.py"
    elif [[ -f "${SKILL_DIR}/claude_adapter.py" ]]; then
        adapter_script="${SKILL_DIR}/claude_adapter.py"
    else
        error_exit "Claude adapter script not found" 127
    fi
    
    validate_file "$adapter_script" "Response generator"
    
    local response
    response=$(timeout "$RESPONSE_TIMEOUT" "$PYTHON" \
        "$adapter_script" \
        "$transcript" \
        --json 2>/dev/null | jq -r '.response' 2>/dev/null) || {
        local code=$?
        if [[ $code -eq 124 ]]; then
            log WARN "Response generation timeout, using fallback"
            response="Entendi: ${transcript:0:30}... Como posso ajudar?"
        else
            log WARN "Response generation failed (exit code: $code), using fallback"
            response="Entendi: ${transcript:0:30}... Como posso ajudar?"
        fi
    }
    
    if [[ -z "$response" ]]; then
        log WARN "Response empty, using fallback"
        response="Entendi: ${transcript:0:30}... Como posso ajudar?"
    fi
    
    log INFO "Response: ${response:0:50}..."
    echo "$response"
}

# ============================================================================
# Stage 3: Synthesis
# ============================================================================

synthesize_audio() {
    local response="$1"
    
    log INFO "Stage 3: Synthesizing audio..."
    
    # FIXED: Support both scripts/ subdirectory and top-level
    local synthesize_script
    if [[ -f "${SKILL_DIR}/scripts/synthesize_universal.py" ]]; then
        synthesize_script="${SKILL_DIR}/scripts/synthesize_universal.py"
    elif [[ -f "${SKILL_DIR}/synthesize_universal.py" ]]; then
        synthesize_script="${SKILL_DIR}/synthesize_universal.py"
    else
        error_exit "Synthesis script not found" 127
    fi
    
    validate_file "$synthesize_script" "Synthesis script"
    
    local voice="${AUDIO_VOICE:-jeff}"
    
    local output_path
    output_path=$(timeout "$RESPONSE_TIMEOUT" "$PYTHON" \
        "$synthesize_script" \
        "$response" "$voice" 2>/dev/null) || {
        local code=$?
        error_exit "Synthesis failed (exit code: $code)" 4
    }
    
    if [[ -z "$output_path" ]] || [[ ! -f "$output_path" ]]; then
        error_exit "Synthesis produced no output file" 4
    fi
    
    log INFO "Audio synthesized: $output_path"
    echo "$output_path"
}

# ============================================================================
# Stage 4: Sending (OpenClaw only)
# ============================================================================

send_audio_reply() {
    local audio_out="$1"
    local target="${2:-}"
    local reply_to="${3:-}"
    
    # REQUIRED: Output the media directive for OpenClaw to handle the response
    # For Telegram, [[audio_as_voice]] ensures it renders as a voice bubble
    echo "MEDIA:${audio_out} [[audio_as_voice]]"
    
    if [[ -z "$target" ]]; then
        log INFO "No target specified, skipping direct send via CLI"
        return 0
    fi
    
    if ! command -v openclaw &>/dev/null; then
        log WARN "openclaw command not found, skipping direct send via CLI"
        return 0
    fi
    
    log INFO "Stage 4: Sending reply via OpenClaw sessions..."
    
    # FIXED: Use openclaw sessions send with MEDIA: payload
    if timeout "$RESPONSE_TIMEOUT" openclaw sessions send \
        --target "$target" \
        --message "MEDIA:${audio_out} [[audio_as_voice]]" \
        --reply-to "$reply_to" 2>/dev/null; then
        log INFO "Message sent successfully"
    else
        local code=$?
        if [[ $code -eq 124 ]]; then
            error_exit "Send timeout" 5
        else
            error_exit "Send failed (exit code: $code)" 5
        fi
    fi
}

# ============================================================================
# Main Workflow
# ============================================================================

main() {
    local audio_in="$1"
    local target="${2:-}"
    local reply_to="${3:-}"
    
    log DEBUG "Script started with args: audio_in=$audio_in target=$target reply_to=$reply_to"
    log DEBUG "Python: $PYTHON"
    log DEBUG "Skill dir: $SKILL_DIR"
    
    validate_inputs "$audio_in" "$target" "$reply_to"
    
    local transcript
    transcript=$(transcribe_audio "$audio_in") || exit $?
    
    local response
    response=$(generate_response "$transcript") || exit $?
    
    local audio_out
    audio_out=$(synthesize_audio "$response") || exit $?
    
    send_audio_reply "$audio_out" "$target" "$reply_to" || exit $?
    
    log INFO "Pipeline complete"
    echo "$audio_out"
    return 0
}

main "$@"
