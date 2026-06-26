#!/bin/bash
# Agent Extract 验证脚本
# 用于验证 agent 剥离过程是否符合约束

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

AGENT_ID="${1:-}"
OPENCLAW_DIR="$HOME/.openclaw"

if [ -z "$AGENT_ID" ]; then
    echo "用法: $0 <agent-id>"
    echo "示例: $0 aiway"
    exit 1
fi

WORKSPACE_DIR="$OPENCLAW_DIR/workspace-$AGENT_ID"
MAIN_WORKSPACE="$OPENCLAW_DIR/workspace"

echo "=========================================="
echo "Agent Extract 验证报告"
echo "目标 Agent: $AGENT_ID"
echo "=========================================="
echo ""

# 检查 1: 新 Agent 配置
echo -e "${YELLOW}[检查 1] 新 Agent 配置${NC}"
AGENT_CONFIG=$(cat "$OPENCLAW_DIR/openclaw.json" | jq -r --arg id "$AGENT_ID" '.agents.list[] | select(.id == $id)')
if [ -n "$AGENT_CONFIG" ]; then
    echo -e "${GREEN}✓${NC} Agent '$AGENT_ID' 已在配置中"
    echo "  名称: $(echo "$AGENT_CONFIG" | jq -r '.name')"
    echo "  Workspace: $(echo "$AGENT_CONFIG" | jq -r '.workspace')"
else
    echo -e "${RED}✗${NC} Agent '$AGENT_ID' 未在配置中找到"
fi
echo ""

# 检查 2: Workspace 目录
echo -e "${YELLOW}[检查 2] 新 Workspace 目录${NC}"
if [ -d "$WORKSPACE_DIR" ]; then
    echo -e "${GREEN}✓${NC} Workspace 目录存在: $WORKSPACE_DIR"
    
    # 检查必要文件
    for file in SOUL.md IDENTITY.md AGENTS.md HEARTBEAT.md; do
        if [ -f "$WORKSPACE_DIR/$file" ]; then
            echo -e "  ${GREEN}✓${NC} $file 存在"
        else
            echo -e "  ${RED}✗${NC} $file 缺失"
        fi
    done
else
    echo -e "${RED}✗${NC} Workspace 目录不存在: $WORKSPACE_DIR"
fi
echo ""

# 检查 3: Main Session 未受影响
echo -e "${YELLOW}[检查 3] Main Session 完整性${NC}"
MAIN_SESSIONS=$(cat "$OPENCLAW_DIR/agents/main/sessions/sessions.json" 2>/dev/null | jq 'keys | length' 2>/dev/null || echo "0")
if [ "$MAIN_SESSIONS" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} Main session 数量: $MAIN_SESSIONS"
else
    echo -e "${YELLOW}!${NC} 无法获取 main session 数量"
fi
echo ""

# 检查 4: Channel 配置未受影响
echo -e "${YELLOW}[检查 4] Channel 配置完整性${NC}"
CHANNEL_COUNT=$(cat "$OPENCLAW_DIR/openclaw.json" | jq '.channels | keys | length')
if [ "$CHANNEL_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} Channel 配置数量: $CHANNEL_COUNT"
    cat "$OPENCLAW_DIR/openclaw.json" | jq -r '.channels | keys[]' | while read channel; do
        echo "  - $channel"
    done
else
    echo -e "${YELLOW}!${NC} 无 channel 配置"
fi
echo ""

# 检查 5: Cron Job
echo -e "${YELLOW}[检查 5] Cron Job 配置${NC}"
CRON_JOBS=$(openclaw cron list --json 2>/dev/null || echo '{"jobs": []}')
TARGET_CRON=$(echo "$CRON_JOBS" | jq -r --arg id "$AGENT_ID" '.jobs[] | select(.agentId == $id)')
if [ -n "$TARGET_CRON" ]; then
    echo -e "${GREEN}✓${NC} 找到 $AGENT_ID 的 cron job"
    echo "$TARGET_CRON" | jq -r '"  名称: \(.name)\n  Agent: \(.agentId)\n  Schedule: every \(.schedule.everyMs / 60000) minutes"'
else
    echo -e "${YELLOW}!${NC} 未找到 $AGENT_ID 的 cron job"
fi
echo ""

# 检查 6: 技能文件
echo -e "${YELLOW}[检查 6] 技能文件${NC}"
SKILL_DIR="$WORKSPACE_DIR/skills"
if [ -d "$SKILL_DIR" ]; then
    SKILL_COUNT=$(find "$SKILL_DIR" -name "SKILL.md" | wc -l | tr -d ' ')
    echo -e "${GREEN}✓${NC} 技能数量: $SKILL_COUNT"
    find "$SKILL_DIR" -name "SKILL.md" | while read skill; do
        SKILL_NAME=$(basename $(dirname "$skill"))
        echo "  - $SKILL_NAME"
    done
else
    echo -e "${YELLOW}!${NC} 无技能目录"
fi
echo ""

# 检查 7: 记忆文件
echo -e "${YELLOW}[检查 7] 记忆文件${NC}"
MEMORY_DIR="$WORKSPACE_DIR/memory"
if [ -d "$MEMORY_DIR" ]; then
    MEMORY_COUNT=$(find "$MEMORY_DIR" -name "*.md" | wc -l | tr -d ' ')
    echo -e "${GREEN}✓${NC} 记忆文件数量: $MEMORY_COUNT"
else
    echo -e "${YELLOW}!${NC} 无记忆目录"
fi
echo ""

# 检查 8: Main 原文件完整性
echo -e "${YELLOW}[检查 8] Main 原文件完整性${NC}"
if [ -f "$MAIN_WORKSPACE/SOUL.md" ]; then
    echo -e "${GREEN}✓${NC} Main SOUL.md 存在"
else
    echo -e "${RED}✗${NC} Main SOUL.md 缺失"
fi
if [ -f "$MAIN_WORKSPACE/IDENTITY.md" ]; then
    echo -e "${GREEN}✓${NC} Main IDENTITY.md 存在"
else
    echo -e "${RED}✗${NC} Main IDENTITY.md 缺失"
fi
echo ""

echo "=========================================="
echo "验证完成"
echo "=========================================="