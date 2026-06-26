#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

echo "🗑️  卸载 content-repurposer..."

read -p "是否删除配置文件和输出？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f "$BASE_DIR/.env"
    rm -rf "$BASE_DIR/output"
    echo "✅ 已删除配置和输出"
fi

echo "✅ 卸载完成！"