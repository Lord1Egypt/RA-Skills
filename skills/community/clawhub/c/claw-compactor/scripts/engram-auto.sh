#!/bin/bash
# engram-auto.sh — Engram Auto-Runner for OpenClaw
#
# Scans OpenClaw session logs, detects channels, converts format,
# and feeds messages to Engram Observer/Reflector concurrently.
#
# Usage:
#   ./scripts/engram-auto.sh              # run once
#   ./scripts/engram-auto.sh --daemon     # continuous mode (every 15 min)
#   ./scripts/engram-auto.sh --config /path/to/engram.yaml
#   ./scripts/engram-auto.sh --dry-run    # detect only, no LLM calls
#
# Environment variables (all overridable; prefer engram.yaml for config):
#   OPENAI_API_KEY       — LLM API key (OpenAI-compatible)
#   ANTHROPIC_API_KEY    — Anthropic API key (alternative)
#   ENGRAM_THRESHOLD     — Observer threshold tokens (legacy; prefer engram.yaml)
#   OPENCLAW_WORKSPACE   — OpenClaw workspace root path
#   ENGRAM_CONFIG        — Path to engram.yaml / engram.json config file

set -euo pipefail

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAW_COMPACTOR="$(dirname "$SCRIPT_DIR")"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
ENGRAM_WORKSPACE="$WORKSPACE"

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
DAEMON_MODE=false
DRY_RUN=false
CONFIG_ARG=""
INTERVAL=900

while [[ $# -gt 0 ]]; do
    case "$1" in
        --daemon)   DAEMON_MODE=true ;;
        --dry-run)  DRY_RUN=true ;;
        --config)   CONFIG_ARG="$2"; shift ;;
        --interval) INTERVAL="$2"; shift ;;
        *) echo "Unknown argument: $1" >&2; exit 1 ;;
    esac
    shift
done

# ---------------------------------------------------------------------------
# Load .env (lowest priority)
# ---------------------------------------------------------------------------
if [ -f "$CLAW_COMPACTOR/.env" ]; then
    set -a
    # shellcheck disable=SC1090
    source "$CLAW_COMPACTOR/.env"
    set +a
fi

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
ENGRAM_STORE="${WORKSPACE}/memory/engram"
mkdir -p "$ENGRAM_STORE"
LOG_FILE="${ENGRAM_STORE}/auto-runner.log"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "$msg"
    echo "$msg" >> "$LOG_FILE"
}

# ---------------------------------------------------------------------------
# API key check
# ---------------------------------------------------------------------------
check_api_key() {
    if [ -z "${ANTHROPIC_API_KEY:-}" ] && [ -z "${OPENAI_API_KEY:-}" ]; then
        log "WARNING: Neither ANTHROPIC_API_KEY nor OPENAI_API_KEY is set."
        log "  Set one in environment, .env file, or engram.yaml (api_key_env)."
    elif [ -n "${OPENAI_API_KEY:-}" ]; then
        log "INFO: Using OpenAI-compatible provider (base_url=${OPENAI_BASE_URL:-auto}, model=${ENGRAM_MODEL:-from config})"
    else
        log "INFO: Using Anthropic API"
    fi
}

# ---------------------------------------------------------------------------
# Build Python command args
# ---------------------------------------------------------------------------
build_python_args() {
    local args=()

    if [ -n "$CONFIG_ARG" ]; then
        args+=("--config" "$CONFIG_ARG")
    elif [ -n "${ENGRAM_CONFIG:-}" ]; then
        args+=("--config" "$ENGRAM_CONFIG")
    elif [ -f "$CLAW_COMPACTOR/engram.yaml" ]; then
        args+=("--config" "$CLAW_COMPACTOR/engram.yaml")
    fi

    args+=("--workspace" "$ENGRAM_WORKSPACE")

    if [ "$DRY_RUN" = true ]; then
        args+=("--dry-run")
    fi

    echo "${args[@]}"
}

# ---------------------------------------------------------------------------
# Run once via Python (engram_auto.py)
# ---------------------------------------------------------------------------
run_once() {
    log "Engram auto-run starting..."
    check_api_key

    cd "$CLAW_COMPACTOR"

    local py_args
    py_args=$(build_python_args)

    local out
    # shellcheck disable=SC2086
    if out=$(python3 scripts/engram_auto.py $py_args 2>&1); then
        while IFS= read -r line; do log "  $line"; done <<< "$out"
    else
        local rc=$?
        while IFS= read -r line; do log "  ERROR: $line"; done <<< "$out"
        log "engram_auto.py exited with code $rc"
        return $rc
    fi

    # Print status
    log "--- Engram Status ---"
    python3 scripts/engram_auto.py $py_args --status 2>&1 | while IFS= read -r line; do
        log "  $line"
    done || true

    log "Engram auto-run complete."
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if [ "$DAEMON_MODE" = true ]; then
    log "Engram daemon mode: checking every ${INTERVAL}s..."
    while true; do
        run_once || true
        sleep "$INTERVAL"
    done
else
    run_once
fi
