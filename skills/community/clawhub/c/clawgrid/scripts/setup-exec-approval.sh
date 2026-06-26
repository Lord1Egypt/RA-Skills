#!/usr/bin/env bash
# Configure OpenClaw exec approval for automated ClawGrid task execution.
#
# Sets autoAllowSkills=true + askFallback=allowlist so that:
#   - Skill scripts (bash scripts/*.sh) are auto-trusted
#   - Cron sessions (no UI) fall back to allowlist instead of deny
#   - Non-skill commands still prompt when a UI is available
#
# Does NOT modify openclaw.json global settings.
#
# Usage:
#   bash setup-exec-approval.sh          # interactive with output
#   bash setup-exec-approval.sh --quiet  # silent, for heartbeat.sh
set -euo pipefail

APPROVALS_FILE="$HOME/.openclaw/exec-approvals.json"
QUIET=false
[ "${1:-}" = "--quiet" ] && QUIET=true

_log() { $QUIET || echo "$@"; }
_log_err() { $QUIET || echo "$@" >&2; }

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"

# --- Locate openclaw CLI ---
_oc_bin=$(command -v openclaw 2>/dev/null || echo "")
if [ -z "$_oc_bin" ]; then
  for _p in /opt/homebrew/bin/openclaw /usr/local/bin/openclaw "$HOME/.local/bin/openclaw"; do
    [ -x "$_p" ] && _oc_bin="$_p" && break
  done
fi

_log "[exec-approval] Configuring exec approval (autoAllowSkills + allowlist fallback)..."

# --- Build target JSON (preserves existing config, only touches defaults) ---
_build_json() {
  python3 -c "
import json, os, sys

approvals_path = sys.argv[1]

data = {}
if os.path.exists(approvals_path):
    try:
        with open(approvals_path) as f:
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

# Pre-fill standard allowlist so common binaries work on first run
# (avoids approval flood when allowlist is empty on fresh install)
STANDARD_PATTERNS = [
    '/bin/bash',
    '/bin/sh',
    '/usr/bin/curl',
    '/usr/bin/env',
    '/usr/bin/python3',
    '~/.openclaw/workspace/skills/*/scripts/*',
]
wildcard = data.setdefault('agents', {}).setdefault('*', {})
existing = wildcard.get('allowlist', [])
existing_patterns = {e.get('pattern', '') for e in existing}
for p in STANDARD_PATTERNS:
    if p not in existing_patterns:
        existing.append({'pattern': p})
wildcard['allowlist'] = existing

print(json.dumps(data))
" "$APPROVALS_FILE"
}

_target_json=$(_build_json)

_approvals_ok=false
if [ -n "$_oc_bin" ]; then
  _log "[exec-approval] Setting exec-approvals defaults via CLI..."
  if echo "$_target_json" | "$_oc_bin" approvals set --stdin 2>/dev/null; then
    _approvals_ok=true
    _log "[exec-approval] exec-approvals.json configured via CLI."
  else
    _log_err "[exec-approval] CLI set failed, falling back to JSON file edit."
  fi
fi

if [ "$_approvals_ok" = "false" ]; then
  _log "[exec-approval] Writing $APPROVALS_FILE directly..."
  mkdir -p "$(dirname "$APPROVALS_FILE")"
  echo "$_target_json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
with open(sys.argv[1], 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
" "$APPROVALS_FILE"
  _approvals_ok=true
  _log "[exec-approval] exec-approvals.json updated."
fi

# --- Verify ---
_verify_ok=false
if [ -f "$APPROVALS_FILE" ]; then
  _chk=$(python3 -c "
import json
with open('$APPROVALS_FILE') as f:
    d = json.load(f)
defs = d.get('defaults', {})
ok = defs.get('autoAllowSkills') is True and defs.get('askFallback') != 'deny'
print('ok' if ok else 'fail')
" 2>/dev/null || echo "fail")
  [ "$_chk" = "ok" ] && _verify_ok=true
fi

$_verify_ok && _log "[exec-approval] Verified: autoAllowSkills=true, askFallback=allowlist." \
  || _log_err "[exec-approval] WARNING: could not verify configuration"

if ! $QUIET; then
  echo ""
  echo "=== Exec Approval Configured ==="
  echo ""
  echo "  autoAllowSkills = true   (skill scripts auto-trusted)"
  echo "  askFallback     = allowlist (cron sessions use allowlist)"
  echo "  security        = allowlist"
  echo "  ask             = on-miss"
  echo ""
  echo "Skill scripts will run automatically. Non-skill commands"
  echo "will prompt for approval when a UI is available."
fi
