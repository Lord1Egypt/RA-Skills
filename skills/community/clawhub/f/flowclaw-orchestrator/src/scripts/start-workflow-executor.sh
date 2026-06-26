#!/bin/bash
# ============================================================
# FlowClaw Workflow Executor — Startup Script
# Launches via Gunicorn for concurrent request handling.
#
# Platform Support: macOS ✅  Linux ✅  Windows ❌
#   This script requires bash and Gunicorn, which are not
#   available on Windows. See README.md § Platform Support.
#
# Usage:
#   ./start-workflow-executor.sh
#
# Environment:
#   Set FLOWCLAW_ENV_FILE to override default .env path.
#   Default: <repo-root>/.env (two levels up from this script).
#
# Security:
#   - Never use shell=True or interpolate untrusted input here.
#   - gunicorn binds to 127.0.0.1 only (no external exposure).
#   - .env is loaded from disk — never hardcode credentials here.
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/.."
REPO_DIR="$SRC_DIR/.."
LOGS_DIR="$REPO_DIR/logs"
PID_FILE="$LOGS_DIR/workflow-executor.pid"

# ── Load .env file ──────────────────────────────────────────
# Priority: FLOWCLAW_ENV_FILE env var > <repo>/.env > <src>/.env
ENV_FILE="${FLOWCLAW_ENV_FILE:-}"
if [ -z "$ENV_FILE" ]; then
    if [ -f "$REPO_DIR/.env" ]; then
        ENV_FILE="$REPO_DIR/.env"
    elif [ -f "$SRC_DIR/.env" ]; then
        ENV_FILE="$SRC_DIR/.env"
    fi
fi

if [ -n "$ENV_FILE" ] && [ -f "$ENV_FILE" ]; then
    echo "Loading environment from: $ENV_FILE" >&2
    # Safe .env loader: skip comments and blank lines, no eval
    while IFS='=' read -r key value; do
        # Skip comments and blank lines
        [[ "$key" =~ ^[[:space:]]*# ]] && continue
        [[ -z "${key// /}" ]] && continue
        # Only export valid variable names (alphanumeric + underscore)
        if [[ "$key" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
            # Only set if not already in environment
            if [ -z "${!key+x}" ]; then
                export "$key=$value"
            fi
        fi
    done < "$ENV_FILE"
else
    echo "WARNING: No .env file found. Using system environment only." >&2
    echo "Copy config/example.env to .env and configure your credentials." >&2
fi

# ── Find Gunicorn ────────────────────────────────────────────
GUNICORN=""
# Check venv first (common install location)
for candidate in \
    "$SRC_DIR/../.venv/bin/gunicorn" \
    "$HOME/Library/Python/3.9/bin/gunicorn" \
    "$HOME/Library/Python/3.10/bin/gunicorn" \
    "$HOME/Library/Python/3.11/bin/gunicorn" \
    "$HOME/Library/Python/3.12/bin/gunicorn" \
    "$HOME/.local/bin/gunicorn"; do
    if [ -x "$candidate" ]; then
        GUNICORN="$candidate"
        break
    fi
done

# Fallback: search PATH
if [ -z "$GUNICORN" ]; then
    GUNICORN=$(command -v gunicorn 2>/dev/null || true)
fi

if [ -z "$GUNICORN" ] || [ ! -x "$GUNICORN" ]; then
    echo "ERROR: gunicorn not found." >&2
    echo "Install with: pip3 install gunicorn" >&2
    exit 1
fi

# ── Validate required credentials ───────────────────────────
if [ -z "${WORKFLOW_EXECUTOR_API_KEY:-}" ]; then
    echo "ERROR: WORKFLOW_EXECUTOR_API_KEY is not set." >&2
    echo "Generate one with: openssl rand -hex 32" >&2
    exit 1
fi

# ── Read server config ───────────────────────────────────────
PORT="${PORT:-8765}"
HOST="${HOST:-127.0.0.1}"
MAX_WORKERS="${MAX_WORKERS:-4}"

# ── Validate server config ───────────────────────────────────
# Validate PORT: must be an integer in [1, 65535]
if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
    echo "ERROR: PORT must be a number between 1 and 65535 (got: '$PORT')." >&2
    exit 1
fi

# Validate HOST: alphanumeric, dots, hyphens, colons only (IP or hostname, no shell metacharacters)
if ! [[ "$HOST" =~ ^[A-Za-z0-9._:-]+$ ]]; then
    echo "ERROR: HOST contains invalid characters (got: '$HOST')." >&2
    echo "Use an IP address (e.g. 127.0.0.1) or a plain hostname." >&2
    exit 1
fi

# Validate MAX_WORKERS: must be an integer in [1, 64]
if ! [[ "$MAX_WORKERS" =~ ^[0-9]+$ ]] || [ "$MAX_WORKERS" -lt 1 ] || [ "$MAX_WORKERS" -gt 64 ]; then
    echo "ERROR: MAX_WORKERS must be a number between 1 and 64 (got: '$MAX_WORKERS')." >&2
    exit 1
fi

# Ensure logs directory exists
mkdir -p "$LOGS_DIR"

cd "$SRC_DIR"

echo "Starting FlowClaw Workflow Executor..." >&2
echo "  Bind:    $HOST:$PORT" >&2
echo "  Workers: $MAX_WORKERS" >&2
echo "  Logs:    $LOGS_DIR/workflow-executor.log" >&2

exec "$GUNICORN" \
    --workers "$MAX_WORKERS" \
    --bind "$HOST:$PORT" \
    --timeout 600 \
    --graceful-timeout 30 \
    --keep-alive 5 \
    --worker-class sync \
    --log-level info \
    --access-logfile "$LOGS_DIR/workflow-executor.log" \
    --error-logfile "$LOGS_DIR/workflow-executor-error.log" \
    --pid "$PID_FILE" \
    --capture-output \
    workflow-executor:app
