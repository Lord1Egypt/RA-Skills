#!/bin/bash
# sync_daemon.sh — 轻量级增量同步守护进程
# 用法: sync_daemon.sh [--interval <秒>] [--state-file <路径>]
#
# 定期调用 GET /memory/changes 获取自上次同步以来的变更，输出到 stdout。
# 将 last_sync_time 持久化到 --state-file（默认：~/.agentmm_sync_state）。
#
# SECURITY MANIFEST:
#   Environment variables accessed: AGENTMM_API_KEY, AGENTMM_API_BASE (only)
#   External endpoints called: https://api.agentmm.site/memory/changes (GET, only)
#   Local files read: ~/.agentmm_sync_state (timestamp only)
#   Local files written: ~/.agentmm_sync_state (timestamp only)
set -euo pipefail

API_BASE="${AGENTMM_API_BASE:-https://api.agentmm.site}"
API_KEY="${AGENTMM_API_KEY:?Error: AGENTMM_API_KEY environment variable is not set. Format: amm_sk_xxx}"

INTERVAL=60
STATE_FILE="${HOME}/.agentmm_sync_state"

while [[ $# -gt 0 ]]; do
  case $1 in
    --interval)   INTERVAL="$2";   shift 2 ;;
    --state-file) STATE_FILE="$2"; shift 2 ;;
    *) echo "Error: Unknown parameter: $1" >&2; exit 1 ;;
  esac
done

log() { echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] $*"; }

# 读取上次同步时间
load_state() {
  if [[ -f "$STATE_FILE" ]]; then
    cat "$STATE_FILE"
  else
    echo "0"
  fi
}

# 保存同步时间
save_state() { echo "$1" > "$STATE_FILE"; }

# 单轮增量拉取
pull_changes() {
  local since="$1"
  local offset=0
  local total=0

  while true; do
    RESP=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
      "$API_BASE/memory/changes?since=${since}&limit=200&offset=${offset}" \
      -H "Authorization: Bearer $API_KEY")

    HTTP_STATUS=$(echo "$RESP" | tail -n1 | sed 's/^HTTP_STATUS://')
    BODY=$(echo "$RESP" | sed '$d')

    if [[ ! "$HTTP_STATUS" =~ ^2[0-9][0-9]$ ]]; then
      log "ERROR: /memory/changes returned HTTP $HTTP_STATUS"
      return 1
    fi

    COUNT=$(echo "$BODY" | jq '.changes | length')
    SERVER_TIME=$(echo "$BODY" | jq '.server_time')
    HAS_MORE=$(echo "$BODY" | jq -r '.has_more')
    total=$((total + COUNT))

    # 输出变更条目（调用方可根据需要处理）
    echo "$BODY" | jq -c '.changes[]' 2>/dev/null || true

    if [[ "$HAS_MORE" != "true" ]]; then
      echo "$SERVER_TIME"  # 最后一行输出新的 server_time
      break
    fi
    offset=$((offset + 200))
  done

  log "Pulled $total change(s) since $since"
}

log "sync_daemon started. interval=${INTERVAL}s, state_file=${STATE_FILE}"

while true; do
  LAST_SYNC=$(load_state)
  log "Pulling changes since ${LAST_SYNC}..."

  # 收集所有行输出，最后一行为新的 server_time
  OUTPUT=$(pull_changes "$LAST_SYNC" 2>&1) || { log "Pull failed, will retry."; sleep "$INTERVAL"; continue; }
  NEW_TIME=$(echo "$OUTPUT" | tail -n1)

  if [[ "$NEW_TIME" =~ ^[0-9]+$ && "$NEW_TIME" -gt 0 ]]; then
    save_state "$NEW_TIME"
    log "State updated to $NEW_TIME"
  fi

  sleep "$INTERVAL"
done