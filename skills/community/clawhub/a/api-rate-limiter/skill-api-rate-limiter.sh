#!/bin/bash
# skill-api-rate-limiter.sh - OpenClaw技能入口

# 检查参数
if [ $# -eq 0 ]; then
    echo "全局API请求频率限制器"
    echo "用法: $0 [apply-delay|check-status|show-config|update-config|reset-config]"
    exit 0
fi

# 调用主要脚本
exec /root/.openclaw/workspace/skills/api-rate-limiter/scripts/api-rate-limiter.sh "$@"