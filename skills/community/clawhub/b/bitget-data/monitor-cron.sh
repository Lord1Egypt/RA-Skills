#!/bin/bash
# Bitget 高频网格监控 - Cron 包装脚本
# 用于定时执行监控任务

cd /Users/zongzi/.openclaw/workspace/bitget_data

# 记录执行时间
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 执行高频网格监控..." >> cron_monitor.log

# 运行监控脚本
node auto-monitor.js >> cron_monitor.log 2>&1

# 记录完成状态
if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 监控完成" >> cron_monitor.log
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ 监控失败" >> cron_monitor.log
fi
