#!/bin/bash
# Config-Sentinel — safer config snapshots, validation, rollback, and health checks
#
# Usage:
#   scripts/sentinel.sh pre-change
#   scripts/sentinel.sh validate
#   scripts/sentinel.sh rollback
#   scripts/sentinel.sh health
#
# Environment overrides:
#   CONFIG_SENTINEL_CONFIG_FILE
#   CONFIG_SENTINEL_DIR
#   CONFIG_SENTINEL_MIN_AGENTS
#   CONFIG_SENTINEL_REQUIRED_FILES   (comma-separated, e.g. SOUL.md,IDENTITY.md)
#   CONFIG_SENTINEL_VALIDATE_BINDINGS (1 default, 0 disable)
#   CONFIG_SENTINEL_VALIDATE_TELEGRAM_TOKENS (0 default, 1 enable)

set -u

CONFIG_FILE="${CONFIG_SENTINEL_CONFIG_FILE:-$HOME/.openclaw/openclaw.json}"
SENTINEL_DIR="${CONFIG_SENTINEL_DIR:-$HOME/.openclaw/.sentinel}"
BACKUP_DIR="$SENTINEL_DIR/backup"
LOG_FILE="$SENTINEL_DIR/log"
LAST_GOOD_FILE="$SENTINEL_DIR/last-good"
MIN_AGENTS="${CONFIG_SENTINEL_MIN_AGENTS:-3}"
REQUIRED_FILES_RAW="${CONFIG_SENTINEL_REQUIRED_FILES:-}"
VALIDATE_BINDINGS="${CONFIG_SENTINEL_VALIDATE_BINDINGS:-1}"
VALIDATE_TELEGRAM_TOKENS="${CONFIG_SENTINEL_VALIDATE_TELEGRAM_TOKENS:-0}"

log() {
  local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
  echo "$msg" | tee -a "$LOG_FILE"
}

init() {
  mkdir -p "$BACKUP_DIR"
  chmod 700 "$SENTINEL_DIR" "$BACKUP_DIR" 2>/dev/null || true
  touch "$LOG_FILE"
  chmod 600 "$LOG_FILE" 2>/dev/null || true
}

fail() {
  log "FAIL: $1"
  echo "FAIL: $1"
  exit 1
}

require_config() {
  if [ ! -f "$CONFIG_FILE" ]; then
    fail "Config file not found: $CONFIG_FILE"
  fi
}

json_ok() {
  python3 - "$CONFIG_FILE" <<'PY' 2>/dev/null
import json, sys
with open(sys.argv[1]) as f:
    json.load(f)
print("ok")
PY
}

pre_change() {
  init
  require_config

  local ts
  ts=$(date '+%Y-%m-%d_%H-%M-%S')

  cp "$CONFIG_FILE" "$BACKUP_DIR/${ts}.json"
  chmod 600 "$BACKUP_DIR/${ts}.json" 2>/dev/null || true
  log "Backup created: $BACKUP_DIR/${ts}.json"

  local config_dir
  config_dir=$(dirname "$CONFIG_FILE")
  if [ -d "$config_dir/.git" ]; then
    cd "$config_dir" || fail "Could not enter $config_dir"
    git add "$(basename "$CONFIG_FILE")" 2>/dev/null || true
    if git diff --cached --quiet; then
      log "No git snapshot created (no staged changes)"
    else
      git commit -m "config-sentinel: pre-change snapshot $ts" >/dev/null 2>&1 || true
      if git rev-parse HEAD >/dev/null 2>&1; then
        git rev-parse HEAD > "$LAST_GOOD_FILE"
        log "Git snapshot committed: $(cat "$LAST_GOOD_FILE")"
      fi
    fi
  else
    log "No git repo at $config_dir — backup only"
  fi

  echo "OK: pre-change snapshot complete"
}

validate() {
  init
  require_config

  local issues=""

  if ! json_ok >/dev/null; then
    issues="$issues\n  ❌ Invalid JSON"
  else
    log "OK: Valid JSON"
  fi

  local top_level
  top_level=$(python3 - "$CONFIG_FILE" <<'PY' 2>/dev/null
import json, sys
with open(sys.argv[1]) as f:
    cfg = json.load(f)
missing = []
for key in ["agents"]:
    if key not in cfg:
        missing.append(key)
print(", ".join(missing))
PY
)
  if [ -n "$top_level" ]; then
    issues="$issues\n  ⚠️  Missing expected top-level keys: $top_level"
  else
    log "OK: expected top-level keys present"
  fi

  local agent_count
  agent_count=$(python3 - "$CONFIG_FILE" <<'PY' 2>/dev/null
import json, sys
with open(sys.argv[1]) as f:
    cfg = json.load(f)
print(len(cfg.get("agents", {}).get("list", [])))
PY
)
  if [ -z "$agent_count" ]; then
    issues="$issues\n  ❌ Could not determine agent count"
  elif [ "$agent_count" -lt "$MIN_AGENTS" ]; then
    issues="$issues\n  ⚠️  agents.count=$agent_count (below minimum $MIN_AGENTS)"
  else
    log "OK: agents.count=$agent_count"
  fi

  if [ "$VALIDATE_BINDINGS" = "1" ]; then
    local bad_bindings
    bad_bindings=$(python3 - "$CONFIG_FILE" <<'PY' 2>/dev/null
import json, sys
with open(sys.argv[1]) as f:
    cfg = json.load(f)
agent_ids = {a.get("id") for a in cfg.get("agents", {}).get("list", []) if a.get("id")}
issues = []
for b in cfg.get("bindings", []):
    aid = b.get("agentId")
    if aid and aid not in agent_ids:
        issues.append(aid)
print(", ".join(issues))
PY
)
    if [ -n "$bad_bindings" ]; then
      issues="$issues\n  ⚠️  Bindings reference unknown agents: $bad_bindings"
    else
      log "OK: bindings reference known agents"
    fi
  fi

  if [ -n "$REQUIRED_FILES_RAW" ]; then
    local missing_files
    missing_files=$(python3 - "$CONFIG_FILE" "$REQUIRED_FILES_RAW" <<'PY' 2>/dev/null
import json, os, sys
with open(sys.argv[1]) as f:
    cfg = json.load(f)
required = [x.strip() for x in sys.argv[2].split(",") if x.strip()]
issues = []
for agent in cfg.get("agents", {}).get("list", []):
    ws = agent.get("workspace")
    aid = agent.get("id", "<unknown>")
    if ws:
        for fname in required:
            if not os.path.isfile(os.path.join(ws, fname)):
                issues.append(f"{aid}/{fname}")
print(", ".join(issues[:20]))
PY
)
    if [ -n "$missing_files" ]; then
      issues="$issues\n  ⚠️  Missing required workspace files: $missing_files"
    else
      log "OK: required workspace files present"
    fi
  fi

  if [ "$VALIDATE_TELEGRAM_TOKENS" = "1" ]; then
    local dup_tokens
    dup_tokens=$(python3 - "$CONFIG_FILE" <<'PY' 2>/dev/null
import json, sys
from collections import Counter
with open(sys.argv[1]) as f:
    cfg = json.load(f)
accounts = cfg.get("channels", {}).get("telegram", {}).get("accounts", {})
tokens = [acc.get("botToken", "") for acc in accounts.values() if acc.get("botToken")]
dups = [tok for tok, count in Counter(tokens).items() if count > 1]
print(", ".join(dups[:5]))
PY
)
    if [ -n "$dup_tokens" ]; then
      issues="$issues\n  ⚠️  Duplicate Telegram tokens detected"
    else
      log "OK: Telegram tokens unique"
    fi
  fi

  local file_size
  file_size=$(wc -c < "$CONFIG_FILE" 2>/dev/null || echo 0)
  if [ "$file_size" -le 2 ]; then
    issues="$issues\n  ❌ Config file appears empty or truncated"
  else
    log "OK: config file is non-empty"
  fi

  if [ -z "$issues" ]; then
    log "VALIDATE: PASS — no issues"
    echo "✅ VALIDATE: PASS"
    return 0
  else
    log "VALIDATE: ISSUES found:$issues"
    echo "⚠️ VALIDATE: ISSUES$issues"
    return 2
  fi
}

rollback() {
  init
  require_config

  if [ -f "$LAST_GOOD_FILE" ]; then
    local commit
    commit=$(cat "$LAST_GOOD_FILE")
    local config_dir
    config_dir=$(dirname "$CONFIG_FILE")
    if [ -d "$config_dir/.git" ] && git -C "$config_dir" rev-parse "$commit" >/dev/null 2>&1; then
      git -C "$config_dir" show "$commit:$(basename "$CONFIG_FILE")" > "$CONFIG_FILE" || fail "Rollback from git failed"
      log "ROLLBACK: Restored from git commit $commit"
      echo "✅ ROLLED BACK to $commit"
      validate
      return
    fi
  fi

  local latest_backup
  latest_backup=$(ls -1t "$BACKUP_DIR"/*.json 2>/dev/null | head -n 1 || true)
  if [ -n "$latest_backup" ]; then
    cp "$latest_backup" "$CONFIG_FILE" || fail "Rollback from backup failed"
    log "ROLLBACK: Restored from backup $latest_backup"
    echo "✅ ROLLED BACK from backup"
    validate
    return
  fi

  fail "No rollback source found"
}

health() {
  validate
}

ACTION="${1:-health}"
case "$ACTION" in
  pre-change) pre_change ;;
  validate) validate ;;
  rollback) rollback ;;
  health) health ;;
  *)
    echo "Usage: scripts/sentinel.sh {pre-change|validate|rollback|health}"
    exit 1
    ;;
esac
