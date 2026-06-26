#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  exec_error_triage.sh <error_text_or_file>
  cat error.log | exec_error_triage.sh

Output:
  CATEGORY=<...>
  CONFIDENCE=<high|medium|low>
  WHY=<short reason>
  NEXT=<suggested action>
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

INPUT=""
if [[ $# -ge 1 ]]; then
  if [[ -f "$1" ]]; then
    INPUT="$(cat "$1")"
  else
    INPUT="$1"
  fi
else
  if [ -t 0 ]; then
    usage
    exit 2
  fi
  INPUT="$(cat)"
fi

LOWER="$(printf '%s' "$INPUT" | tr '[:upper:]' '[:lower:]')"

emit() {
  local cat="$1" conf="$2" why="$3" next="$4"
  printf 'CATEGORY=%s\nCONFIDENCE=%s\nWHY=%s\nNEXT=%s\n' "$cat" "$conf" "$why" "$next"
  exit 0
}

if grep -qiE 'unknown json field|unknown option|unknown argument' <<<"$LOWER"; then
  emit "schema-or-flag-mismatch" "high" "Command arguments/JSON fields not supported by this CLI version." "Check --help, replace unsupported fields (e.g. nameWithOwner -> fullName), or use gh_search_repos_safe.sh."
fi

if grep -qiE 'not logged in|unauthorized|forbidden|authentication|auth' <<<"$LOWER"; then
  emit "auth-missing-or-invalid" "high" "Missing/expired credentials." "Re-authenticate and verify identity (whoami/auth status), then retry."
fi

if grep -qiE 'command not found|enoent|spawn .* enoent' <<<"$LOWER"; then
  emit "missing-binary-or-launcher" "high" "Required binary/launcher is unavailable in this environment." "Install/check required binary with command -v; use token/headless flow when browser open fails."
fi

if grep -qiE 'permission denied|eacces|operation not permitted' <<<"$LOWER"; then
  emit "permission-error" "high" "Insufficient file/system permissions." "Fix ownership/permissions/executable bit for target files; avoid broad sudo unless required."
fi

if grep -qiE 'timed out|timeout|code 124|deadline exceeded' <<<"$LOWER"; then
  emit "timeout" "medium" "Operation exceeded time budget." "Increase timeout, split workload, or reduce scope before retrying."
fi

if grep -qiE 'sigkill|signal 9|killed' <<<"$LOWER"; then
  emit "killed-process" "medium" "Process was forcibly terminated (resource pressure/manual/system kill)." "Check memory/CPU pressure and external killers; rerun with lighter workload."
fi

if grep -qiE 'hidden while security scan is pending|skill not found' <<<"$LOWER"; then
  emit "transient-registry-visibility" "medium" "Likely post-publish indexing/moderation delay." "Use bounded retry/backoff and verify by direct /skills/<slug> URL."
fi

if grep -qiE 'econnreset|enotfound|temporary failure|network|connection reset|5[0-9]{2}' <<<"$LOWER"; then
  emit "network-or-transient-platform" "medium" "Likely temporary connectivity/platform issue." "Retry with backoff; verify DNS/connectivity and platform status."
fi

emit "unclassified" "low" "Pattern not matched in built-in taxonomy." "Capture full stderr/stdout and inspect with tool-specific help/docs."
