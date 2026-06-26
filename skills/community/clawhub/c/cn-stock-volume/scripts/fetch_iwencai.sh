#!/bin/bash
#
# fetch_iwencai.sh - 从同花顺问财获取数据
#
# 用法:
#   ./fetch_iwencai.sh index 上证指数
#   ./fetch_iwencai.sh index 深证成指
#   ./fetch_iwencai.sh index 创业板指
#   ./fetch_iwencai.sh sentiment A 股上涨数量
#   ./fetch_iwencai.sh sentiment A 股下跌数量
#
# 输出: 页面 snapshot 文本（stdout）
#

set -e

TYPE="$1"
QUERY="$2"

if [ -z "$TYPE" ] || [ -z "$QUERY" ]; then
    echo "用法：$0 <index|sentiment> <查询语句>" >&2
    echo "示例：$0 index 上证指数" >&2
    exit 1
fi

# 构建 URL
BASE_URL="https://www.iwencai.com/unifiedwap/result"
URL="${BASE_URL}?w=${QUERY}&querytype=zhishu"

echo "[INFO] 访问：${URL}" >&2

# 使用 OpenClaw browser 工具
# 注意：这里需要通过 OpenClaw 的 browser 工具调用
# 由于这是在 OpenClaw 环境内，我们使用特殊的方式调用

# 方法：输出 URL 和查询类型，由 Python 脚本解析并调用 browser 工具
echo "URL:${URL}"
echo "TYPE:${TYPE}"
echo "QUERY:${QUERY}"
