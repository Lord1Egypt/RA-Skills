#!/usr/bin/env bash
# Validate an Epic AI Swarm Orchestration install.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${SWARM_TARGET_DIR:-$HOME/workspace/swarm}"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-}"
PROBE_MODELS=0
STRICT=0

usage() {
  cat <<'EOF'
Usage: bash doctor.sh [options]

Options:
  --target <dir>       Runtime install directory (default: ~/workspace/swarm)
  --workspace <dir>    OpenClaw workspace (default: infer, then ~/.openclaw/workspace)
  --probe-models       Run assess-models.sh --dry-run (uses provider CLIs/API quota)
  --strict             Treat warnings as failure
  -h, --help           Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET_DIR="${2:?--target requires a directory}"; shift 2 ;;
    --workspace) WORKSPACE_DIR="${2:?--workspace requires a directory}"; shift 2 ;;
    --probe-models) PROBE_MODELS=1; shift ;;
    --strict) STRICT=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

abs_path() {
  python3 - "$1" <<'PY'
import os, sys
print(os.path.abspath(os.path.expanduser(sys.argv[1])))
PY
}

infer_workspace() {
  if [[ -n "$WORKSPACE_DIR" ]]; then
    abs_path "$WORKSPACE_DIR"
    return
  fi
  local d="$SCRIPT_DIR"
  while [[ "$d" != "/" ]]; do
    if [[ -f "$d/AGENTS.md" || -f "$d/roles/active.json" ]]; then
      printf '%s\n' "$d"
      return
    fi
    d="$(dirname "$d")"
  done
  if [[ -d "$HOME/.openclaw/workspace" ]]; then
    printf '%s\n' "$HOME/.openclaw/workspace"
  else
    printf '%s\n' "$HOME/.openclaw/workspace"
  fi
}

TARGET_DIR="$(abs_path "$TARGET_DIR")"
WORKSPACE_DIR="$(infer_workspace)"
FAILS=0
WARNS=0

ok() { printf '✅ %s\n' "$*"; }
warn() { printf '⚠️  %s\n' "$*"; WARNS=$((WARNS+1)); }
fail() { printf '❌ %s\n' "$*"; FAILS=$((FAILS+1)); }
info() { printf '• %s\n' "$*"; }

have() { command -v "$1" >/dev/null 2>&1; }

printf '🐝 Epic AI Swarm Doctor\n'
printf '  Runtime:   %s\n' "$TARGET_DIR"
printf '  Workspace: %s\n\n' "$WORKSPACE_DIR"

if [[ -d "$TARGET_DIR" ]]; then ok "Runtime directory exists"; else fail "Runtime directory missing: $TARGET_DIR (run install.sh)"; fi

for cmd in bash git python3 tmux; do
  if have "$cmd"; then ok "Required command available: $cmd"; else fail "Missing required command: $cmd"; fi
done
for cmd in gh openclaw; do
  if have "$cmd"; then ok "Optional integration command available: $cmd"; else warn "Optional command missing: $cmd (GitHub/notifications may be limited)"; fi
done

MODEL_CLIS=()
for cmd in codex gemini deepseek claude; do
  if have "$cmd"; then MODEL_CLIS+=("$cmd"); ok "Model CLI available: $cmd"; else warn "Model CLI not found: $cmd"; fi
done
if [[ ${#MODEL_CLIS[@]} -eq 0 ]]; then
  fail "No model CLI found. Authenticate/install at least one of: codex, gemini, deepseek, claude."
fi

if [[ -d "$TARGET_DIR" ]]; then
  mapfile -t scripts < <(find "$TARGET_DIR" -maxdepth 1 -type f -name '*.sh' -printf '%f\n' | sort)
  if [[ ${#scripts[@]} -ge 10 ]]; then ok "Runtime scripts present (${#scripts[@]})"; else fail "Too few runtime scripts found (${#scripts[@]}); install may be incomplete"; fi

  bad_exec=0
  for s in "$TARGET_DIR"/*.sh; do
    [[ -e "$s" ]] || continue
    [[ -x "$s" ]] || { warn "Script is not executable: $(basename "$s")"; bad_exec=1; }
  done
  [[ "$bad_exec" == "0" ]] && ok "Runtime scripts are executable"

  if bash -n "$TARGET_DIR"/*.sh >/tmp/swarm-doctor-bashn.log 2>&1; then
    ok "All runtime scripts pass bash -n"
  else
    fail "bash syntax check failed; see /tmp/swarm-doctor-bashn.log"
  fi

  for d in logs endorsements; do
    [[ -d "$TARGET_DIR/$d" ]] && ok "State directory exists: $d" || fail "Missing state directory: $d"
  done
  for f in swarm.conf duty-table.json active-tasks.json pending-notifications.txt usage-log.json; do
    [[ -e "$TARGET_DIR/$f" ]] && ok "State/config file exists: $f" || fail "Missing state/config file: $f"
  done

  if [[ -f "$TARGET_DIR/duty-table.json" ]]; then
    if python3 -m json.tool "$TARGET_DIR/duty-table.json" >/tmp/swarm-doctor-duty.json 2>/tmp/swarm-doctor-duty.err; then
      ok "duty-table.json is valid JSON"
      python3 - "$TARGET_DIR/duty-table.json" <<'PY' >/tmp/swarm-doctor-duty-report.txt 2>/dev/null
import json, shutil, sys
with open(sys.argv[1]) as f: data=json.load(f)
for role, entry in data.get('dutyTable', {}).items():
    primary = entry.get('agent','')
    fallback = (entry.get('fallback') or {}).get('agent','')
    primary_ok = bool(primary and shutil.which(primary))
    fallback_ok = bool(fallback and shutil.which(fallback))
    status = 'ok' if primary_ok else ('fallback-ok' if fallback_ok else 'missing-cli')
    print(f'{role}\t{entry.get("agent","")}\t{entry.get("model","")}\t{fallback}\t{status}')
PY
      while IFS=$'\t' read -r role agent model fallback status; do
        [[ -n "$role" ]] || continue
        case "$status" in
          ok) ok "Duty role $role -> $agent/$model CLI available" ;;
          fallback-ok) warn "Duty role $role primary CLI '$agent' missing, but fallback '$fallback' exists" ;;
          *) fail "Duty role $role has no available primary/fallback CLI ($agent, fallback=$fallback)" ;;
        esac
      done < /tmp/swarm-doctor-duty-report.txt
    else
      fail "duty-table.json is invalid JSON"
    fi
  fi

  if grep -RInE '(/home/dz|/mnt/d|postgresql://|npg_[A-Za-z0-9]|sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|BOT_TOKEN="[^"]+"|API_KEY="[^"]+")' "$TARGET_DIR"/*.sh "$TARGET_DIR"/*.json "$TARGET_DIR"/*.conf >/tmp/swarm-doctor-leakscan.txt 2>/dev/null; then
    warn "Potential local path/secret patterns found; inspect /tmp/swarm-doctor-leakscan.txt"
  else
    ok "No obvious local path/secret patterns in runtime files"
  fi
fi

if have tmux; then
  sess="swarm-doctor-$$"
  if tmux new-session -d -s "$sess" 'sleep 10' >/dev/null 2>&1; then
    tmux kill-session -t "$sess" >/dev/null 2>&1 || true
    ok "tmux can create/kill sessions"
  else
    fail "tmux could not create a test session"
  fi
fi

if have git; then
  tmp="$(mktemp -d 2>/dev/null || mktemp -d -t swarm-doctor)"
  wt="$tmp-wt"
  if (
    cd "$tmp" && git init -q && echo ok > README.md && git add README.md && \
    git -c user.name='Swarm Doctor' -c user.email='doctor@example.invalid' commit -q -m init && \
    git worktree add -q -b doctor-test "$wt"
  ) >/tmp/swarm-doctor-git.log 2>&1; then
    ok "git worktree smoke test passed"
  else
    fail "git worktree smoke test failed; see /tmp/swarm-doctor-git.log"
  fi
  rm -rf "$tmp" "$wt" >/dev/null 2>&1 || true
fi

if [[ -d "$WORKSPACE_DIR/roles/swarm-lead" ]]; then
  ok "swarm-lead role files installed"
else
  warn "swarm-lead role not found in workspace roles"
fi
if [[ -f "$WORKSPACE_DIR/roles/active.json" ]]; then
  if python3 - "$WORKSPACE_DIR/roles/active.json" <<'PY' >/dev/null 2>&1
import json, sys
with open(sys.argv[1]) as f: data=json.load(f)
raise SystemExit(0 if 'swarm-lead' in data.get('activeRoles', []) else 1)
PY
  then ok "swarm-lead is active in roles/active.json"; else warn "swarm-lead is installed but not active"; fi
else
  warn "roles/active.json not found"
fi

if [[ "$PROBE_MODELS" == "1" ]]; then
  if [[ -x "$TARGET_DIR/assess-models.sh" ]]; then
    info "Running provider model probes: assess-models.sh --dry-run"
    if "$TARGET_DIR/assess-models.sh" --dry-run; then ok "Model probe completed"; else fail "Model probe failed"; fi
  else
    fail "Cannot probe models: assess-models.sh missing/not executable"
  fi
else
  info "Skipping live model probes. Use --probe-models when ready; it may consume provider quota."
fi

printf '\nDoctor summary: %s failure(s), %s warning(s)\n' "$FAILS" "$WARNS"
if [[ "$STRICT" == "1" && "$WARNS" -gt 0 ]]; then
  exit 1
fi
[[ "$FAILS" -eq 0 ]] || exit 1
exit 0
