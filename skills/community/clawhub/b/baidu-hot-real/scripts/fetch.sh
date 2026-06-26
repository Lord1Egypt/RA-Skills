#!/bin/bash
# 百度热搜榜获取脚本
# 使用 OpenClaw web_fetch 工具
#
# 安全说明：
# - 只访问百度官方公开热榜页面
# - 临时文件存储在 /tmp，使用随机文件名
# - 执行后自动清理临时文件
# - 不访问任何敏感文件或目录

set -e  # 遇到错误立即退出

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 使用 mktemp 创建安全的临时文件（防止竞态条件）
TEMP_FILE=$(mktemp /tmp/baidu_hot.XXXXXX.html)

# 确保退出时清理临时文件
trap "rm -f '$TEMP_FILE'" EXIT

echo "正在获取百度热搜榜..."

# 安全限制：只允许访问百度热榜 URL
TARGET_URL="https://top.baidu.com/board"

# 使用 openclaw web_fetch 获取数据
# --maxChars 限制最大字符数，防止过大响应
if ! openclaw web_fetch "$TARGET_URL" --maxChars 50000 > "$TEMP_FILE" 2>&1; then
    echo "❌ web_fetch 执行失败"
    exit 1
fi

# 检查是否获取成功
if [ ! -s "$TEMP_FILE" ]; then
    echo "❌ 获取失败：返回内容为空"
    exit 1
fi

# 验证临时文件权限（应该是 600）
PERM=$(stat -c %a "$TEMP_FILE" 2>/dev/null || stat -f %Lp "$TEMP_FILE" 2>/dev/null)
if [ "$PERM" != "600" ] && [ "$PERM" != "644" ]; then
    chmod 600 "$TEMP_FILE"
fi

# 处理数据
# 参数验证：只接受数字或 "all"
TOP_N="${1:-10}"
if ! [[ "$TOP_N" =~ ^[0-9]+$ ]] && [ "$TOP_N" != "all" ]; then
    echo "❌ 参数错误：请使用数字或 'all'"
    echo "用法：$0 [10|20|50|all]"
    exit 1
fi

python3 "$SCRIPT_DIR/baidu_fetch.py" "$TOP_N" < "$TEMP_FILE"

# 临时文件由 trap 自动清理
