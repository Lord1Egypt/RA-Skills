#!/bin/bash
# Obsidian 快速同步脚本

VAULT_PATH="${OBSIDIAN_VAULT:-/home/sandbox/.openclaw/workspace/repo/obsidian-vault}"

cd "$VAULT_PATH" || exit 1

echo "📥 拉取最新..."
git pull origin main

echo "📦 提交变更..."
git add .
git commit -m "sync: $(date '+%Y-%m-%d %H:%M') 自动同步"

echo "📤 推送到远程..."
git push origin main

echo "✅ 同步完成！"
