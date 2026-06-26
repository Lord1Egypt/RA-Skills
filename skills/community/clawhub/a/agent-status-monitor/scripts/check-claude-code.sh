#!/bin/bash
# check-claude-code.sh - 检查 Claude Code 运行状态
# 用法：./check-claude-code.sh

set -e

COLOR_RESET="\033[0m"
COLOR_GREEN="\033[32m"
COLOR_YELLOW="\033[33m"
COLOR_BLUE="\033[34m"

SESSIONS_DIR="$HOME/.claude/projects"

echo -e "${COLOR_BLUE}--- Claude Code 状态 ---${COLOR_RESET}"

# 检查进程
PROCESSES=$(ps aux | grep -i "claude" | grep -v grep | wc -l | tr -d ' ')

if [ "$PROCESSES" -gt 0 ]; then
    # 检查会话文件活动状态
    if [ -d "$SESSIONS_DIR" ]; then
        SESSION_COUNT=$(ls -1 "$SESSIONS_DIR" 2>/dev/null | wc -l | tr -d ' ')
        
        # 检查 2 分钟内是否有文件更新
        RECENT_FILES=$(find "$SESSIONS_DIR" -type f -mmin -2 2>/dev/null | wc -l | tr -d ' ')
        if [ "$RECENT_FILES" -gt 0 ]; then
            echo -e "${COLOR_GREEN}● Claude Code${COLOR_RESET}: 🔥 工作中 (2 分钟内有更新) · $SESSION_COUNT 个会话"
        else
            # 检查 10 分钟内是否有文件更新
            RECENT_FILES_10=$(find "$SESSIONS_DIR" -type f -mmin -10 2>/dev/null | wc -l | tr -d ' ')
            if [ "$RECENT_FILES_10" -gt 0 ]; then
                echo -e "${COLOR_GREEN}● Claude Code${COLOR_RESET}: ⏳ 等待中 (10 分钟内有更新) · $SESSION_COUNT 个会话"
            else
                echo -e "${COLOR_GREEN}● Claude Code${COLOR_RESET}: 💤 闲置 (最近无更新) · $SESSION_COUNT 个会话"
            fi
        fi
    else
        echo -e "${COLOR_GREEN}● Claude Code${COLOR_RESET}: 运行中 ($PROCESSES 个进程)"
    fi
else
    echo -e "${COLOR_YELLOW}○ Claude Code${COLOR_RESET}: 未运行"
fi
