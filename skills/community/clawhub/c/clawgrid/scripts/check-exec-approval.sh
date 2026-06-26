#!/usr/bin/env bash
# Check OpenClaw exec approval configuration for automated task execution.
# Outputs one of: OK, PARTIAL, NEEDS_CONFIG
# Exit code: 0 = OK, 1 = needs configuration
set -euo pipefail

APPROVALS_FILE="$HOME/.openclaw/exec-approvals.json"
OC_CONFIG="$HOME/.openclaw/openclaw.json"

_status="OK"
_issues=()

# --- Try CLI first (gives effective policy) ---
_oc_bin=$(command -v openclaw 2>/dev/null || echo "")
if [ -z "$_oc_bin" ]; then
  for _p in /opt/homebrew/bin/openclaw /usr/local/bin/openclaw "$HOME/.local/bin/openclaw"; do
    [ -x "$_p" ] && _oc_bin="$_p" && break
  done
fi

_auto_allow=""
_ask_fallback=""
_security=""

if [ -n "$_oc_bin" ]; then
  _cli_out=$("$_oc_bin" approvals get 2>/dev/null || echo "")
  if [ -n "$_cli_out" ]; then
    _auto_allow=$(echo "$_cli_out" | python3 -c "
import sys, re
for line in sys.stdin:
    m = re.search(r'autoAllowSkills[=:\s]+(true|false|on|off)', line, re.IGNORECASE)
    if m:
        v = m.group(1).lower()
        print('true' if v in ('true', 'on') else 'false')
        break
" 2>/dev/null || echo "")
    _ask_fallback=$(echo "$_cli_out" | python3 -c "
import sys, re
for line in sys.stdin:
    m = re.search(r'askFallback[:\s]+(\w+)', line, re.IGNORECASE)
    if m: print(m.group(1).lower()); break
" 2>/dev/null || echo "")
    _security=$(echo "$_cli_out" | python3 -c "
import sys, re
for line in sys.stdin:
    m = re.search(r'security[:\s]+(\w+)', line, re.IGNORECASE)
    if m: print(m.group(1).lower()); break
" 2>/dev/null || echo "")
  fi
fi

# --- Fallback: parse JSON files directly ---
if [ -z "$_auto_allow" ] || [ -z "$_ask_fallback" ]; then
  if [ -f "$APPROVALS_FILE" ]; then
    _json_result=$(python3 -c "
import json, sys
try:
    with open('$APPROVALS_FILE') as f:
        data = json.load(f)
    d = data.get('defaults', {})
    print(json.dumps({
        'autoAllowSkills': d.get('autoAllowSkills', False),
        'askFallback': d.get('askFallback', 'deny'),
        'security': d.get('security', ''),
    }))
except Exception:
    print('{}')
" 2>/dev/null || echo "{}")

    [ -z "$_auto_allow" ] && _auto_allow=$(echo "$_json_result" | python3 -c "import json,sys; print(str(json.load(sys.stdin).get('autoAllowSkills', False)).lower())" 2>/dev/null || echo "false")
    [ -z "$_ask_fallback" ] && _ask_fallback=$(echo "$_json_result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('askFallback', 'deny'))" 2>/dev/null || echo "deny")
    [ -z "$_security" ] && _security=$(echo "$_json_result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('security', ''))" 2>/dev/null || echo "")
  else
    _auto_allow="false"
    _ask_fallback="deny"
    _issues+=("exec-approvals.json not found")
  fi
fi

# --- Check openclaw.json for tools.exec.security override ---
if [ -f "$OC_CONFIG" ]; then
  _oc_security=$(python3 -c "
import json
try:
    with open('$OC_CONFIG') as f:
        data = json.load(f)
    print(data.get('tools', {}).get('exec', {}).get('security', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")
  if [ "$_oc_security" = "deny" ]; then
    _issues+=("openclaw.json has tools.exec.security=deny (overrides approvals)")
    _status="NEEDS_CONFIG"
  fi
fi

# --- Evaluate ---
if [ "$_auto_allow" != "true" ]; then
  _issues+=("autoAllowSkills is not enabled")
  _status="NEEDS_CONFIG"
fi

if [ "$_ask_fallback" = "deny" ]; then
  _issues+=("askFallback is deny (blocks cron sessions)")
  if [ "$_status" = "OK" ]; then
    _status="PARTIAL"
  fi
fi

if [ "$_security" = "deny" ]; then
  _issues+=("security is deny (blocks all host exec)")
  _status="NEEDS_CONFIG"
fi

# --- Output ---
if [ "$_status" = "OK" ]; then
  echo "OK"
  exit 0
fi

echo "$_status"
for _i in "${_issues[@]}"; do
  echo "  - $_i" >&2
done

if [ "$_status" = "NEEDS_CONFIG" ] || [ "$_status" = "PARTIAL" ]; then
  echo "" >&2
  echo "Fix: bash $(dirname "$0")/setup-exec-approval.sh" >&2
  echo "Docs: https://docs.openclaw.ai/tools/exec-approvals" >&2
fi
exit 1
