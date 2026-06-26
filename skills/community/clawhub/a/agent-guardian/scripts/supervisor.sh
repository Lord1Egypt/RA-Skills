#!/bin/bash
# ========================================
# 🐕 Agent Supervisor (看门狗)
# 检测任务卡住/死循环/错误累积/僵尸进程
# 由 openclaw cron 每3分钟调用
# ========================================

STATE_FILE="/tmp/agent-work-state.json"
LOG_FILE="/tmp/agent-supervisor.log"
LOCK_FILE="/tmp/agent-supervisor.lock"
STUCK_THRESHOLD=180  # 3分钟无更新视为卡住
LOOP_THRESHOLD=5     # 同一状态出现5次视为死循环

cleanup() { rm -f "$LOCK_FILE"; }
trap cleanup EXIT
if [ -f "$LOCK_FILE" ]; then
  old_pid=$(cat "$LOCK_FILE" 2>/dev/null)
  if kill -0 "$old_pid" 2>/dev/null; then
    exit 0
  fi
fi
echo $$ > "$LOCK_FILE"

log() {
  echo "[$(date '+%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
  tail -200 "$LOG_FILE" > "${LOG_FILE}.tmp" 2>/dev/null && mv "${LOG_FILE}.tmp" "$LOG_FILE"
}

init_state() {
  cat > "$STATE_FILE" << 'EOF'
{
  "current_task": null,
  "status": "idle",
  "started_at": 0,
  "last_update": 0,
  "update_count": 0,
  "last_status_values": [],
  "error_count": 0,
  "last_report_at": 0
}
EOF
}

[ ! -f "$STATE_FILE" ] && init_state

read_state() {
  if [ -f "$STATE_FILE" ]; then
    cat "$STATE_FILE"
  else
    init_state
    cat "$STATE_FILE"
  fi
}

NOW=$(date +%s)
STATE=$(read_state)

parse() {
  echo "$STATE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('$1', '$2'))" 2>/dev/null || echo "$2"
}

STATUS=$(parse "status" "idle")
LAST_UPDATE=$(parse "last_update" "0")
TASK=$(parse "current_task" "none")
ERROR_COUNT=$(parse "error_count" "0")
LAST_REPORT=$(parse "last_report_at" "0")

SINCE_UPDATE=$((NOW - LAST_UPDATE))
SINCE_REPORT=$((NOW - LAST_REPORT))

ALERT=""
ALERT_LEVEL="info"

# 1. 任务卡住检测
if [ "$STATUS" = "working" ] && [ "$SINCE_UPDATE" -gt "$STUCK_THRESHOLD" ]; then
  ALERT="⚠️ 任务可能卡住了（${SINCE_UPDATE}秒无更新）\n任务: $TASK\n状态: $STATUS"
  ALERT_LEVEL="warning"
  log "WARNING: Task stuck - ${SINCE_UPDATE}s since last update, task=$TASK"
fi

# 2. 错误累积检测
if [ "$ERROR_COUNT" -gt 3 ]; then
  ALERT="🚨 连续错误 ${ERROR_COUNT} 次！\n任务: $TASK\n可能陷入错误循环"
  ALERT_LEVEL="critical"
  log "CRITICAL: Error loop detected - ${ERROR_COUNT} errors, task=$TASK"
fi

# 3. 死循环检测
REPEAT_COUNT=$(echo "$STATE" | python3 -c "
import sys, json
d = json.load(sys.stdin)
vals = d.get('last_status_values', [])
if len(vals) >= 5 and len(set(vals[-5:])) == 1:
    print(5)
else:
    print(0)
" 2>/dev/null || echo "0")

if [ "$REPEAT_COUNT" -ge 5 ]; then
  ALERT="🔄 检测到死循环！同一状态重复 ${REPEAT_COUNT} 次\n任务: $TASK"
  ALERT_LEVEL="critical"
  log "CRITICAL: Loop detected - same status repeated ${REPEAT_COUNT} times"
fi

# 4. 僵尸进程检查
ZOMBIE_COUNT=$(ps aux 2>/dev/null | grep -c '[Z]')
if [ "$ZOMBIE_COUNT" -gt 3 ]; then
  ALERT="${ALERT}\n👻 发现 ${ZOMBIE_COUNT} 个僵尸进程"
  log "WARNING: ${ZOMBIE_COUNT} zombie processes found"
fi

# 输出报告
REPORT_FILE="/tmp/agent-supervisor-report.txt"

if [ -n "$ALERT" ]; then
  echo -e "$ALERT" > "$REPORT_FILE"
  echo "$ALERT_LEVEL" > "${REPORT_FILE}.level"
  log "Alert generated: level=$ALERT_LEVEL"
elif [ "$SINCE_REPORT" -gt 180 ]; then
  if [ "$STATUS" = "working" ]; then
    echo "🔧 任务进行中: $TASK (已运行 ${SINCE_UPDATE}s)" > "$REPORT_FILE"
  else
    echo "✅ 一切正常，待命中" > "$REPORT_FILE"
  fi
  echo "info" > "${REPORT_FILE}.level"
  log "Routine report: status=$STATUS"
else
  log "No report needed: since_report=${SINCE_REPORT}s"
  echo "" > "$REPORT_FILE"
fi

# 更新报告时间
python3 -c "
import json
with open('$STATE_FILE', 'r') as f:
    d = json.load(f)
d['last_report_at'] = $NOW
with open('$STATE_FILE', 'w') as f:
    json.dump(d, f, indent=2)
" 2>/dev/null

log "Check complete: status=$STATUS, since_update=${SINCE_UPDATE}s, errors=$ERROR_COUNT"
