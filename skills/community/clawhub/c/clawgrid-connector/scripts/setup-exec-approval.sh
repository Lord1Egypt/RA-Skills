#!/usr/bin/env bash
# Configure OpenClaw exec approval for automated ClawGrid task execution.
# Sets autoAllowSkills=true + askFallback=allowlist so cron-triggered
# sessions can run skill scripts without manual approval.
#
# Usage:
#   bash setup-exec-approval.sh          # interactive with output
#   bash setup-exec-approval.sh --quiet  # silent, for install.sh / heartbeat.sh
set -euo pipefail

APPROVALS_FILE="$HOME/.openclaw/exec-approvals.json"
QUIET=false
[ "${1:-}" = "--quiet" ] && QUIET=true

_log() { $QUIET || echo "$@"; }
_log_err() { $QUIET || echo "$@" >&2; }

# --- Check current state ---
SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
CHECK_SCRIPT="$SKILL_DIR/scripts/check-exec-approval.sh"
if [ -x "$CHECK_SCRIPT" ]; then
  _current=$(bash "$CHECK_SCRIPT" 2>/dev/null | head -1 || echo "UNKNOWN")
  if [ "$_current" = "OK" ]; then
    _log "[exec-approval] Already configured. No changes needed."
    exit 0
  fi
fi

_log "[exec-approval] Configuring exec approval for automated task execution..."

# --- Try CLI first ---
_oc_bin=$(command -v openclaw 2>/dev/null || echo "")
if [ -z "$_oc_bin" ]; then
  for _p in /opt/homebrew/bin/openclaw /usr/local/bin/openclaw "$HOME/.local/bin/openclaw"; do
    [ -x "$_p" ] && _oc_bin="$_p" && break
  done
fi

_cli_ok=false
if [ -n "$_oc_bin" ]; then
  _log "[exec-approval] Using openclaw CLI..."
  if "$_oc_bin" approvals set defaults.autoAllowSkills true 2>/dev/null && \
     "$_oc_bin" approvals set defaults.askFallback allowlist 2>/dev/null && \
     "$_oc_bin" approvals set defaults.security allowlist 2>/dev/null && \
     "$_oc_bin" approvals set defaults.ask on-miss 2>/dev/null; then
    _cli_ok=true
    _log "[exec-approval] CLI configuration succeeded."
  else
    _log_err "[exec-approval] CLI failed, falling back to JSON file edit."
  fi
fi

# --- Fallback: direct JSON edit ---
if [ "$_cli_ok" = "false" ]; then
  _log "[exec-approval] Writing $APPROVALS_FILE..."
  mkdir -p "$(dirname "$APPROVALS_FILE")"

  python3 -c "
import json, os, sys

path = sys.argv[1]
data = {}
if os.path.exists(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception:
        data = {}

if 'version' not in data:
    data['version'] = 1

defaults = data.setdefault('defaults', {})
defaults['security'] = 'allowlist'
defaults['ask'] = 'on-miss'
defaults['askFallback'] = 'allowlist'
defaults['autoAllowSkills'] = True

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
" "$APPROVALS_FILE"

  _log "[exec-approval] JSON file updated."
fi

# --- Verify ---
if [ -x "$CHECK_SCRIPT" ]; then
  _verify=$(bash "$CHECK_SCRIPT" 2>/dev/null | head -1 || echo "UNKNOWN")
  if [ "$_verify" = "OK" ]; then
    _log "[exec-approval] Verified: exec approval is correctly configured."
  else
    _log_err "[exec-approval] WARNING: verification returned $_verify. Check manually:"
    _log_err "  cat $APPROVALS_FILE"
  fi
fi

# --- Hint about Option B ---
if ! $QUIET; then
  echo ""
  echo "=== Exec Approval Configured ==="
  echo ""
  echo "Policy: autoAllowSkills=true, askFallback=allowlist"
  echo "  - Skill scripts (poll.sh, submit.sh, etc.) run automatically in cron sessions"
  echo "  - Non-skill commands still require approval when a UI is available"
  echo ""
  echo "Alternative: For stricter control, you can forward approval prompts"
  echo "to Telegram and approve each command with /approve. Add to openclaw.json:"
  echo '  { "approvals": { "exec": { "enabled": true, "mode": "targets",'
  echo '    "targets": [{ "channel": "telegram", "to": "<your_telegram_id>" }] } } }'
  echo ""
  echo "Docs: https://docs.openclaw.ai/tools/exec-approvals"
fi
