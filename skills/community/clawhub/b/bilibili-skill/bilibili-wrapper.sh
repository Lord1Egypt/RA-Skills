#!/bin/bash
# Bilibili CLI Wrapper for OpenClaw Skill
# 自动从配置文件读取 Cookies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BILIBILI_CLI="/root/.openclaw/workspace/external/bilibili-api/bilibili-cli.py"
COOKIES_FILE="/root/.openclaw/workspace/bilibili-cookies.md"

# 从环境变量或配置文件读取 Cookies
if [ -n "$BILIBILI_SESSDATA" ]; then
    SESSDATA="$BILIBILI_SESSDATA"
    BILI_JCT="$BILIBILI_BILI_JCT"
    BUVID3="$BILIBILI_BUVID3"
else
    # 从配置文件解析（简单提取）
    if [ -f "$COOKIES_FILE" ]; then
        SESSDATA=$(grep "SESSDATA=" "$COOKIES_FILE" | cut -d'=' -f2 | cut -d';' -f1 | tr -d ' ')
        BILI_JCT=$(grep "bili_jct=" "$COOKIES_FILE" | cut -d'=' -f2 | cut -d';' -f1 | tr -d ' ')
        BUVID3=$(grep "buvid3=" "$COOKIES_FILE" | cut -d'=' -f2 | cut -d';' -f1 | tr -d ' ')
    fi
fi

if [ -z "$SESSDATA" ] || [ -z "$BILI_JCT" ]; then
    echo "❌ 错误：未找到 B 站认证信息"
    echo "请设置环境变量或在 $COOKIES_FILE 中配置 Cookies"
    echo ""
    echo "使用方法:"
    echo "  export BILIBILI_SESSDATA='your_sessdata'"
    echo "  export BILIBILI_BILI_JCT='your_bili_jct'"
    echo "  export BILIBILI_BUVID3='your_buvid3'"
    exit 1
fi

# 执行 CLI 命令
python3 "$BILIBILI_CLI" \
    --sessdata "$SESSDATA" \
    --bili_jct "$BILI_JCT" \
    --buvid3 "$BUVID3" \
    "$@"
