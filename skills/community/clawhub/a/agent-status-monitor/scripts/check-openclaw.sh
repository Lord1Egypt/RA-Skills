#!/bin/bash
# check-openclaw.sh - 检查 OpenClaw 运行状态
# 用法：./check-openclaw.sh

set -e

COLOR_RESET="\033[0m"
COLOR_GREEN="\033[32m"
COLOR_YELLOW="\033[33m"
COLOR_BLUE="\033[34m"

SESSIONS_DIR="$HOME/.openclaw/agents"

echo -e "${COLOR_BLUE}--- OpenClaw 状态 ---${COLOR_RESET}"

# 检查进程
PROCESSES=$(ps aux | grep -i "openclaw" | grep -v grep | wc -l | tr -d ' ')

if [ "$PROCESSES" -gt 0 ]; then
    # 检查会话文件活动状态
    if [ -d "$SESSIONS_DIR" ]; then
        SESSION_COUNT=$(find "$SESSIONS_DIR" -name "*.json" -type f 2>/dev/null | wc -l | tr -d ' ')
        
        # 检查 2 分钟内是否有文件更新
        RECENT_FILES=$(find "$SESSIONS_DIR" -type f -name "*.json" -mmin -2 2>/dev/null | wc -l | tr -d ' ')
        if [ "$RECENT_FILES" -gt 0 ]; then
            echo -e "${COLOR_GREEN}● OpenClaw${COLOR_RESET}: 🔥 工作中 (2 分钟内有更新) · $SESSION_COUNT 个会话"
        else
            # 检查 10 分钟内是否有文件更新
            RECENT_FILES_10=$(find "$SESSIONS_DIR" -type f -name "*.json" -mmin -10 2>/dev/null | wc -l | tr -d ' ')
            if [ "$RECENT_FILES_10" -gt 0 ]; then
                echo -e "${COLOR_GREEN}● OpenClaw${COLOR_RESET}: ⏳ 等待中 (10 分钟内有更新) · $SESSION_COUNT 个会话"
            else
                echo -e "${COLOR_GREEN}● OpenClaw${COLOR_RESET}: 💤 闲置 (最近无更新) · $SESSION_COUNT 个会话"
            fi
        fi
    else
        echo -e "${COLOR_GREEN}● OpenClaw${COLOR_RESET}: 运行中 ($PROCESSES 个进程)"
    fi
    
    # 显示 OpenClaw status
    if command -v openclaw &> /dev/null; then
        echo ""
        openclaw status 2>/dev/null | head -15
    fi
else
    echo -e "${COLOR_YELLOW}○ OpenClaw${COLOR_RESET}: 未运行"
fi
