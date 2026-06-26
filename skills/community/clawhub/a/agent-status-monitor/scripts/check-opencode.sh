#!/bin/bash
# check-opencode.sh - 检查 OpenCode 运行状态
# 用法：./check-opencode.sh

set -e

COLOR_RESET="\033[0m"
COLOR_GREEN="\033[32m"
COLOR_YELLOW="\033[33m"
COLOR_BLUE="\033[34m"

SESSIONS_DIR="$HOME/.local/state/opencode"
CONFIG_FILE="$HOME/.config/opencode/opencode.json"
EXECUTABLE="$HOME/.opencode/bin/opencode"

echo -e "${COLOR_BLUE}--- OpenCode 状态 ---${COLOR_RESET}"

# 检查进程
PROCESSES=$(ps aux | grep -i "opencode" | grep -v grep | wc -l | tr -d ' ')

if [ "$PROCESSES" -gt 0 ]; then
    # 检查会话文件活动状态
    if [ -d "$SESSIONS_DIR" ]; then
        SESSION_COUNT=$(ls -1 "$SESSIONS_DIR" 2>/dev/null | wc -l | tr -d ' ')
        
        # 检查 2 分钟内是否有文件更新
        RECENT_FILES=$(find "$SESSIONS_DIR" -type f -mmin -2 2>/dev/null | wc -l | tr -d ' ')
        if [ "$RECENT_FILES" -gt 0 ]; then
            echo -e "${COLOR_GREEN}● OpenCode${COLOR_RESET}: 🔥 工作中 (2 分钟内有更新) · $SESSION_COUNT 个会话"
        else
            # 检查 10 分钟内是否有文件更新
            RECENT_FILES_10=$(find "$SESSIONS_DIR" -type f -mmin -10 2>/dev/null | wc -l | tr -d ' ')
            if [ "$RECENT_FILES_10" -gt 0 ]; then
                # 如果只有 1 个文件且超过 5 分钟，可能是初始配置
                if [ "$SESSION_COUNT" -le 1 ]; then
                    LATEST_FILE=$(find "$SESSIONS_DIR" -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
                    if [ -n "$LATEST_FILE" ]; then
                        LATEST_MTIME=$(stat -f "%m" "$LATEST_FILE" 2>/dev/null || stat -c "%Y" "$LATEST_FILE" 2>/dev/null)
                        NOW=$(date +%s)
                        DIFF_MINS=$(( (NOW - LATEST_MTIME) / 60 ))
                        if [ "$DIFF_MINS" -gt 5 ]; then
                            echo -e "${COLOR_GREEN}● OpenCode${COLOR_RESET}: 💤 闲置 (未使用) · $SESSION_COUNT 个会话"
                        else
                            echo -e "${COLOR_GREEN}● OpenCode${COLOR_RESET}: ⏳ 等待中 (10 分钟内有更新) · $SESSION_COUNT 个会话"
                        fi
                    else
                        echo -e "${COLOR_GREEN}● OpenCode${COLOR_RESET}: 💤 闲置 (未使用) · $SESSION_COUNT 个会话"
                    fi
                else
                    echo -e "${COLOR_GREEN}● OpenCode${COLOR_RESET}: ⏳ 等待中 (10 分钟内有更新) · $SESSION_COUNT 个会话"
                fi
            else
                echo -e "${COLOR_GREEN}● OpenCode${COLOR_RESET}: 💤 闲置 (最近无更新) · $SESSION_COUNT 个会话"
            fi
        fi
    else
        echo -e "${COLOR_GREEN}● OpenCode${COLOR_RESET}: 运行中 ($PROCESSES 个进程)"
    fi
    
    # 显示详细信息
    if [ -f "$EXECUTABLE" ]; then
        VERSION=$("$EXECUTABLE" --version 2>/dev/null)
        echo ""
        echo -e "${COLOR_BLUE}详情:${COLOR_RESET}"
        echo "  版本：$VERSION"
        if [ -f "$CONFIG_FILE" ]; then
            echo "  配置：$CONFIG_FILE"
        fi
    fi
else
    echo -e "${COLOR_YELLOW}○ OpenCode${COLOR_RESET}: 未运行"
fi
