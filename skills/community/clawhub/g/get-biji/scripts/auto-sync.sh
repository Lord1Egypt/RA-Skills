#!/bin/bash
set -e
cd "$(dirname "$0")/.."
echo "=== Get笔记自动同步 ==="
echo "时间: $(date)"
echo ""
echo "Step 1: 检查/刷新 Token..."
node scripts/refresh-token.js
echo ""
echo "Step 2: 开始同步..."
OUTPUT_DIR="/Users/sky/Documents/小龙虾知识库/00-Inbox/Get笔记" node scripts/sync.js
echo ""
echo "同步完成！"
