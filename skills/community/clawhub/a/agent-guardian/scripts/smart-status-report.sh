#!/bin/bash
# ========================================
# 📊 智能状态汇报
# 系统 crontab 每5分钟调用
# 对话时推送状态，不说话10分钟自动静默
# ========================================
# 配置项（安装时由 install.sh 替换）
# GUARDIAN_CHANNEL: 渠道名 (qqbot/telegram/wechat/feishu等)
# GUARDIAN_TARGET: 用户ID

export PATH="/root/.nvm/versions/node/v22.22.0/bin:/root/.local/share/pnpm:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
export HOME="/root"

ACTIVE_FILE="/tmp/user-last-active.txt"
SILENCE_THRESHOLD=600  # 10分钟
CONFIG_FILE="/tmp/agent-guardian-config.json"

# 读取配置
if [ -f "$CONFIG_FILE" ]; then
  CHANNEL=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('channel',''))" 2>/dev/null)
  TARGET=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('target',''))" 2>/dev/null)
else
  echo "ERROR: Config file not found: $CONFIG_FILE"
  exit 1
fi

[ -z "$CHANNEL" ] || [ -z "$TARGET" ] && { echo "ERROR: channel or target not configured"; exit 1; }

NOW=$(date +%s)

# 检查活跃
[ ! -f "$ACTIVE_FILE" ] && exit 0
LAST_ACTIVE=$(cat "$ACTIVE_FILE" 2>/dev/null | tr -d '[:space:]')
[ -z "$LAST_ACTIVE" ] || [ "$LAST_ACTIVE" = "0" ] && exit 0
[ $((NOW - LAST_ACTIVE)) -gt $SILENCE_THRESHOLD ] && exit 0

# 生成报告
TIME_STR=$(date '+%H:%M')
QUEUE_REPORT=""
QUEUE_SCRIPT="$(dirname "$0")/msg-queue.py"
[ -f "$QUEUE_SCRIPT" ] && QUEUE_REPORT=$(python3 "$QUEUE_SCRIPT" report 2>/dev/null)

MEM=$(free -h 2>/dev/null | awk '/Mem:/{print $3"/"$2}')
LOAD=$(uptime 2>/dev/null | awk -F'load average:' '{print $2}' | cut -d',' -f1 | xargs)

MSG="📊 状态汇报 $TIME_STR
${QUEUE_REPORT}
🔧 内存 $MEM | 负载 $LOAD"

# 发送
RESULT=$(openclaw message send --channel "$CHANNEL" --target "$TARGET" --message "$MSG" 2>&1)
if echo "$RESULT" | grep -q "Sent via"; then
    echo "Report sent at $TIME_STR (OK)"
else
    echo "Report FAILED at $TIME_STR: $RESULT"
fi
