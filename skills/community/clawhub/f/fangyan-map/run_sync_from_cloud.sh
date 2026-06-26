#!/bin/bash
# 切换 Node.js 环境
source ~/.nvm/nvm.sh > /dev/null 2>&1
node_version=$(node --version 2>/dev/null || echo "v22.22.0")
cd /root/.openclaw/workspace-zhiduoxia/skills/fangyan-map
python3 sync_from_cloud.py >> logs/sync_from_cloud.log 2>&1
