#!/bin/bash
# Design Daily Cron 包装脚本
# 每天北京时间 9:00 触发（UTC 1:00 执行）
# 使用方式：openclaw cron create --task "bash /path/to/design-daily-cron.sh" ...

OPENCLAW_BIN="${OPENCLAW_BIN:-openclaw}"

# 获取当前北京时间小时
# UTC+8，date -u 获取 UTC 时间
UTC_HOUR=$(date -u +%H)
BEIJING_HOUR=$(( (UTC_HOUR + 8) % 24 ))

# 只在 9 点北京时执行
if [ "$BEIJING_HOUR" -eq 9 ]; then
  $OPENCLAW_BIN run "今日设计资讯" --channel feishu
else
  echo "[Design Daily Cron] 当前北京时间 ${BEIJING_HOUR} 点，不是 9 点，跳过执行"
fi
