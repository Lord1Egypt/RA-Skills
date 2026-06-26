#!/bin/bash
# A股交易时段自动推送脚本
# 添加到 crontab: crontab -e

SKILL_DIR="/root/.openclaw/workspace/skills/a-stock-reporter"
VENV="/root/.openclaw/workspace/venv/bin/activate"

# 加载虚拟环境
source "$VENV"

# 获取当前时间
TIME=$(date +%H%M)

# 运行对应时段的更新
cd "$SKILL_DIR/scripts"
python3 trading_update.py --time "$TIME"
