#!/bin/bash
# 基金每日汇报 - 运行监控并更新飞书文档

cd ~/.openclaw/workspace/skills/fund-monitor

# 运行基金监控获取数据
DATA=$(python3 fund_monitor_v2.py 2>/dev/null)

# 调用Node.js脚本更新飞书
node ~/.openclaw/workspace/skills/fund-monitor/update-feishu.js "$DATA"
