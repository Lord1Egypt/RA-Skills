#!/bin/bash

# ClawHub Skill 安装脚本 - 自动重试版本
# 用法: bash install_skill.sh <skill-name>

SKILL_NAME="$1"
MAX_WAIT_TIME=1800  # 30分钟
RETRY_INTERVAL=10   # 10秒重试间隔

if [ -z "$SKILL_NAME" ]; then
    echo "错误: 请提供 skill 名称"
    echo "用法: bash install_skill.sh <skill-name>"
    exit 1
fi

echo "开始安装 skill: $SKILL_NAME"
echo "最大等待时间: $((MAX_WAIT_TIME / 60)) 分钟"
echo "---"

START_TIME=$(date +%s)
ATTEMPT=0

while true; do
    ATTEMPT=$((ATTEMPT + 1))
    ELAPSED=$(($(date +%s) - START_TIME))
    
    echo "[尝试 $ATTEMPT] 正在安装 $SKILL_NAME... (已耗时 ${ELAPSED}秒)"
    
    # 执行安装命令
    OUTPUT=$(clawhub install "$SKILL_NAME" --force 2>&1)
    EXIT_CODE=$?
    
    # 检查结果
    if [ $EXIT_CODE -eq 0 ]; then
        echo "---"
        echo "✅ 安装成功！"
        echo "耗时: ${ELAPSED} 秒，共尝试 $ATTEMPT 次"
        exit 0
    fi
    
    # 检查是否包含速率限制
    if echo "$OUTPUT" | grep -qi "Rate limit"; then
        echo "⚠️  遇到速率限制，等待 ${RETRY_INTERVAL} 秒后重试..."
        sleep $RETRY_INTERVAL
    elif echo "$OUTPUT" | grep -qi "flagged as suspicious"; then
        # 已经使用了 --force，仍然失败
        echo "⚠️  安装被标记为可疑，继续重试..."
        sleep $RETRY_INTERVAL
    else
        # 其他错误，也重试
        echo "⚠️  安装失败: $OUTPUT"
        echo "等待 ${RETRY_INTERVAL} 秒后重试..."
        sleep $RETRY_INTERVAL
    fi
    
    # 检查是否超时
    if [ $ELAPSED -ge $MAX_WAIT_TIME ]; then
        echo "---"
        echo "❌ 安装失败: 已尝试 $ATTEMPT 次，耗时 $((ELAPSED / 60)) 分钟"
        echo "建议: 稍后再试，或检查 skill 名称是否正确"
        exit 1
    fi
done
