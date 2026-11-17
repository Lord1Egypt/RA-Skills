#!/bin/bash
# Conclave pre-flight: Phase A updates all panelist CLIs (best-effort),
# Phase B ignition-pings each agent. Debate only when all pings pass.
# Usage: bash preflight.sh [<arena-path>] [--skip-update]
#   If no arena path is given, results are only printed, not written to disk.
#   If a path is given, results are written to 00_preflight/preflight.log.
#   --skip-update  Skip Phase A (use the currently installed versions).
set -u

# OS / shell detection (macOS, Linux, WSL, Windows Git Bash/MSYS)
case "$(uname -s 2>/dev/null)" in
  Darwin) OS=macos ;;
  Linux)  grep -qi microsoft /proc/version 2>/dev/null && OS=wsl || OS=linux ;;
  MINGW*|MSYS*|CYGWIN*) OS=windows ;;
  *) OS=unknown ;;
esac
# Interactive shell used for ignition pings that rely on rc-persisted env vars
# (zsh on macOS, bash elsewhere; both source their rc files with -i).
if command -v zsh >/dev/null 2>&1; then RC_SHELL=zsh; else RC_SHELL=bash; fi
echo "OS: $OS | rc shell: $RC_SHELL"

ARENA=""
SKIP_UPDATE=0
for arg in "$@"; do
  case "$arg" in
    --skip-update) SKIP_UPDATE=1 ;;
    *) [ -z "$ARENA" ] && ARENA="$arg" ;;
  esac
done

PASS=0; FAIL=0
ok()  { echo "  [OK] $1"; PASS=$((PASS+1)); }
bad() { echo "  [FAIL] $1 — $2"; FAIL=$((FAIL+1)); }

LOG=""
append_log() { LOG="${LOG}$1\n"; }

npm_managed() { # is this npm package installed globally?
  npm ls -g "$1" >/dev/null 2>&1
}

try_update() { # $1=name, $2...=update command (best-effort, never fatal)
  local name="$1"; shift
  printf '  [%s] update: ' "$name"
  local out
  if out=$(CONDA_NO_PLUGINS=true no_proxy='*' "$@" 2>&1 | tail -2); then
    echo "done"
    append_log "update_$name: ok"
  else
    echo "skipped/failed (non-fatal)"
    append_log "update_$name: failed ($(echo "$out" | head -1))"
  fi
}

echo "== Phase A: CLI updates (best-effort) =="
if [ "$SKIP_UPDATE" -eq 1 ]; then
  echo "  (skipped via --skip-update)"
  append_log "updates: skipped"
else
  try_update claude claude update
  if npm_managed "@openai/codex"; then
    try_update codex npm install -g @openai/codex@latest
  else
    try_update codex codex update
  fi
  try_update gemini npm install -g @google/gemini-cli@latest
  if npm_managed "@qwen-code/qwen-code"; then
    try_update qwen npm install -g @qwen-code/qwen-code@latest
  else
    try_update qwen qwen update
  fi
  echo "  Installed versions:"
  for c in claude codex gemini qwen; do
    command -v "$c" >/dev/null 2>&1 \
      && echo "    $c: $(CONDA_NO_PLUGINS=true no_proxy='*' "$c" --version 2>/dev/null | head -1)" \
      || echo "    $c: MISSING (run scripts/install.sh first)"
  done
fi

echo
echo "== Phase B: Ignition pings =="

echo "== 1/4 Claude =="
OUT=$(CONDA_NO_PLUGINS=true no_proxy='*' claude -p 'reply with one word: pong' --max-turns 1 2>&1 | tail -5)
echo "$OUT" | grep -qi pong && ok claude || bad claude "$(echo "$OUT" | head -2)"
append_log "claude: $(echo "$OUT" | grep -qi pong && echo pong || echo fail)"

echo "== 2/4 Codex =="
OUT=$(CONDA_NO_PLUGINS=true no_proxy='*' codex exec --skip-git-repo-check -c model_reasoning_effort="low" 'reply with one word: pong' 2>&1 | tail -5)
echo "$OUT" | grep -qi pong && ok codex || bad codex "$(echo "$OUT" | head -2)"
append_log "codex: $(echo "$OUT" | grep -qi pong && echo pong || echo fail)"

echo "== 3/4 Gemini =="
OUT=$(CONDA_NO_PLUGINS=true no_proxy='*' GEMINI_CLI_TRUST_WORKSPACE=true "$RC_SHELL" -i -c 'gemini -p "reply with one word: pong"' 2>&1 | tail -5)
echo "$OUT" | grep -qi pong && ok gemini || bad gemini "$(echo "$OUT" | head -2)"
append_log "gemini: $(echo "$OUT" | grep -qi pong && echo pong || echo fail)"

echo "== 4/4 Qwen =="
OUT=$(CONDA_NO_PLUGINS=true no_proxy='*' qwen -y -p 'reply with one word: pong' 2>&1 | tail -5)
echo "$OUT" | grep -qi pong && ok qwen || bad qwen "$(echo "$OUT" | head -2)"
append_log "qwen: $(echo "$OUT" | grep -qi pong && echo pong || echo fail)"

echo "== Manus External Advisor ==  (The chair must manually verify via mcp__manus_mcp__create_task; this script cannot cover it.)"
append_log "manus: manual"

echo
echo "Result: $PASS OK / $FAIL FAIL"
[ "$FAIL" -eq 0 ] && echo "Ready to debate" || echo "Fix disconnected agents before debating"

# If an arena path was provided, write the log to disk
if [ -n "$ARENA" ] && [ -d "$ARENA/00_preflight" ]; then
  NOW=$(date '+%Y-%m-%d %H:%M:%S')
  cat > "$ARENA/00_preflight/preflight.log" << EOF
# Preflight Log
- Time: $NOW
- Result: $PASS OK / $FAIL FAIL

$(echo -e "$LOG")

$( [ "$FAIL" -eq 0 ] && echo "Status: Ready to debate" || echo "Status: Fix disconnected agents before debating" )
EOF
  echo "Written to: $ARENA/00_preflight/preflight.log"
fi

# Non-zero exit when any ignition ping fails, so callers can branch on $?
[ "$FAIL" -eq 0 ]
