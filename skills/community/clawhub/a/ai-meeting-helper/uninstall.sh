#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

echo "🗑️  卸载 ai-meeting-helper..."

# 询问是否删除配置和备份
read -p "是否删除配置文件和备份数据？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f "$BASE_DIR/.env"
    rm -rf "$BASE_DIR/.ai_meeting_backup"
    rm -rf "$BASE_DIR/.ai_meeting_logs"
    echo "✅ 已删除配置和备份"
fi

echo "✅ 卸载完成！"