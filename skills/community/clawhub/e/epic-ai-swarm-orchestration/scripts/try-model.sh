#!/usr/bin/env bash
# try-model.sh — Test a model, return 0 if it works, 1 if it fails.
# Usage: try-model.sh <agent> <model>
#   agent: deepseek | gemini | codex
#   model: model name (e.g. gemini-2.5-pro, deepseek-v4-pro)

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
[ -f "$SWARM_DIR/swarm.conf" ] && source "$SWARM_DIR/swarm.conf" 2>/dev/null || true
[[ -n "${DEEPSEEK_API_KEY:-}" ]] && export DEEPSEEK_API_KEY

# macOS compatibility: use gtimeout if timeout not available
if ! command -v timeout &>/dev/null && command -v gtimeout &>/dev/null; then
  timeout() { gtimeout "$@"; }
fi

AGENT="${1:?Usage: try-model.sh <agent> <model>}"
MODEL="${2:?Missing model}"

TIMEOUT=45

case "$AGENT" in
  gemini)
    timeout "$TIMEOUT" bash -c "gemini -m $MODEL -y -p 'Reply with just OK'" >/dev/null 2>&1
    ;;
  deepseek)
    timeout "$TIMEOUT" bash -c "deepseek -m $MODEL -y -p 'Reply with just OK'" >/dev/null 2>&1
    ;;
  codex)
    # codex requires a git repo as CWD; create a throwaway one.
    _TMP=$(mktemp -d) && (cd "$_TMP" && git init -q) && \
      timeout "$TIMEOUT" bash -c "cd $_TMP && codex exec --model $MODEL 'Reply with just OK'" >/dev/null 2>&1
    _RC=$?
    rm -rf "$_TMP" 2>/dev/null
    exit $_RC
    ;;
  *)
    echo "[try-model] Unknown agent: $AGENT" >&2
    exit 1
    ;;
esac
