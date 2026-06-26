#!/bin/bash
# 飞书日志记录工具 - Shell 包装脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE_SCRIPT="${SCRIPT_DIR}/feishu-log.js"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 需要安装 Node.js"
    exit 1
fi

# 检查环境变量（不再提供默认值，必须从.env 文件加载）
[ -z "$FEISHU_APP_ID" ] && echo "⚠️  未设置 FEISHU_APP_ID，请检查 .env 文件"
[ -z "$FEISHU_APP_SECRET" ] && echo "⚠️  未设置 FEISHU_APP_SECRET，请检查 .env 文件"
[ -z "$LOG_FOLDER_NAME" ] && export LOG_FOLDER_NAME="工作日志"
[ -z "$DEFAULT_OWNER_ID" ] && echo "⚠️  未设置 DEFAULT_OWNER_ID，请检查 .env 文件"

echo "📝 飞书日志记录工具"
echo "================================"
echo "👤 所有者 ID: $DEFAULT_OWNER_ID"
echo ""

# 执行
node "$NODE_SCRIPT" "$@"
