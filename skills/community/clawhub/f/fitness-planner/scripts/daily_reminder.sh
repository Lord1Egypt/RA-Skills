#!/bin/bash
# 每日健身提醒 - 通过 OpenClaw 发送

SKILL_DIR="$HOME/.openclaw/workspace/skills/fitness-planner"
LOG_DIR="/var/log/fitness_reminder"
mkdir -p "$LOG_DIR"

DATE_STR=$(date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/${DATE_STR}.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ===== 开始生成健身提醒 =====" >> "$LOG_FILE"

cd "$SKILL_DIR"

# 确保已编译
if [ ! -d "dist" ]; then
  npm install --silent 2>/dev/null
  npm run build 2>/dev/null
fi

# 获取今日计划和异常检测
MESSAGE=$(node -e "
import('./dist/index.js').then(mod => {
  const result = mod.handleInput('今天');
  
  // 如果是休息日，发送简单的问候
  if (result.message.includes('休息日')) {
    console.log('🌅 早上好！今天是休息日，好好放松 💪\n\n明天有训练安排，今天可以适当活动一下。');
  } else {
    console.log('🏋️ ' + result.message);
  }
});
" 2>/dev/null)

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 今日计划: $MESSAGE" >> "$LOG_FILE"

# 检查是否需要主动询问（异常检测）
INQUIRY=$(node -e "
import('./dist/adjustment.js').then(mod => {
  const inquiry = mod.checkProactiveInquiry();
  if (inquiry) {
    console.log('\n\n📢 ' + inquiry);
  }
});
" 2>/dev/null)

MESSAGE="$MESSAGE$INQUIRY"

# 发送消息到企业微信
USER_ID="o9cq800M8K-wyrmql8S5MSqz9piM@im.wechat"

openclaw agent \
    --channel openclaw-weixin \
    --to "$USER_ID" \
    --message "$MESSAGE" \
    --deliver >> "$LOG_FILE" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ===== 健身提醒发送完成 =====" >> "$LOG_FILE"
