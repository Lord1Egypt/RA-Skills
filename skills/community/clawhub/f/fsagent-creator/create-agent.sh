#!/bin/bash
# Agent Creator Script
# Usage: ./create-agent.sh <agent-id> <agent-name> <app-id> <app-secret> [model] [description]

set -e

AGENT_ID="$1"
AGENT_NAME="$2"
APP_ID="$3"
APP_SECRET="$4"
MODEL="${5:-glm-5}"
DESCRIPTION="$6"

CONFIG_FILE="/home/admin/.openclaw/openclaw.json"
AGENTS_DIR="/home/admin/.openclaw/agents"
WORKSPACE_BASE="/home/admin/.openclaw"

# Validate parameters
if [ -z "$AGENT_ID" ] || [ -z "$AGENT_NAME" ] || [ -z "$APP_ID" ] || [ -z "$APP_SECRET" ]; then
    echo "❌ 参数不完整"
    echo "用法: $0 <agent-id> <agent-name> <app-id> <app-secret> [model] [description]"
    exit 1
fi

# Check if agent already exists
if [ -d "$AGENTS_DIR/$AGENT_ID" ]; then
    echo "❌ Agent '$AGENT_ID' 已存在"
    exit 1
fi

echo "🚀 创建 Agent: $AGENT_NAME ($AGENT_ID)"
echo "   模型: $MODEL"
echo "   飞书 App ID: $APP_ID"

# Create agent directory structure
mkdir -p "$AGENTS_DIR/$AGENT_ID/agent"
mkdir -p "$AGENTS_DIR/$AGENT_ID/sessions"

# Create workspace
WORKSPACE_DIR="$WORKSPACE_BASE/workspace-$AGENT_ID"
mkdir -p "$WORKSPACE_DIR"
mkdir -p "$WORKSPACE_DIR/memory"

# Create default workspace files
cat > "$WORKSPACE_DIR/AGENTS.md" << 'AGENTEOF'
# AGENTS.md - Your Workspace

This folder is home. Treat it that way.

## Session Startup

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` — raw logs of what happened
- **Long-term:** `MEMORY.md` — your curated memories

## Red Lines

- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
AGENTEOF

cat > "$WORKSPACE_DIR/SOUL.md" << SOULEOF
# SOUL.md - Who You Are

## Identity

**Name:** $AGENT_NAME
**Role:** $DESCRIPTION

## Core Truths

**Be genuinely helpful, not performatively helpful.** Skip the "Great question!" and "I'd be happy to help!" — just help.

**Have opinions.** You're allowed to disagree, prefer things, find stuff amusing or boring.

**Be resourceful before asking.** Try to figure it out. Read the file. Check the context. Search for it.

## Boundaries

- Private things stay private. Period.
- When in doubt, ask before acting externally.
SOULEOF

cat > "$WORKSPACE_DIR/USER.md" << 'USEREOF'
# USER.md - About Your Human

_Learn about the person you're helping. Update this as you go._

- **Name:**
- **What to call them:**
- **Notes:**
USEREOF

cat > "$WORKSPACE_DIR/HEARTBEAT.md" << 'HEARTBEATEOF'
# HEARTBEAT.md

# Keep this file empty to skip heartbeat API calls.
HEARTBEATEOF

# Create MEMORY.md
touch "$WORKSPACE_DIR/MEMORY.md"
touch "$WORKSPACE_DIR/TOOLS.md"
touch "$WORKSPACE_DIR/IDENTITY.md"

# Create models.json for the agent (copy from main)
if [ -f "$AGENTS_DIR/main/agent/models.json" ]; then
    cp "$AGENTS_DIR/main/agent/models.json" "$AGENTS_DIR/$AGENT_ID/agent/"
fi

echo "✅ 目录结构已创建"

# Now we need to update openclaw.json
# Using node for JSON manipulation
node -e "
const fs = require('fs');
const configPath = '$CONFIG_FILE';
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

const agentId = '$AGENT_ID';
const agentName = '$AGENT_NAME';
const appId = '$APP_ID';
const appSecret = '$APP_SECRET';
const model = '$MODEL';

// Add to agents.list
config.agents.list.push({
    id: agentId,
    name: agentName,
    workspace: '/home/admin/.openclaw/workspace-' + agentId,
    model: 'dashscope-coding/' + model
});

// Add feishu account
config.channels.feishu.accounts[agentId] = {
    appId: appId,
    appSecret: appSecret,
    domain: 'feishu',
    enabled: true
};

// Add binding
config.bindings.push({
    agentId: agentId,
    match: {
        channel: 'feishu',
        accountId: agentId,
        peer: {
            kind: 'group',
            id: 'oc_b34e7d612305f015d0a9a061fef1dec3'
        }
    }
});

// Add to agentToAgent allow list
if (config.tools.agentToAgent && config.tools.agentToAgent.allow) {
    config.tools.agentToAgent.allow.push(agentId);
}

// Write back
fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
console.log('✅ 配置已更新');
"

echo ""
echo "🎉 Agent 创建完成！"
echo ""
echo "📋 后续步骤："
echo "   1. 重启 OpenClaw: openclaw gateway restart"
echo "   2. 在飞书开放平台配置事件订阅地址"
echo "   3. 在群里 @ $AGENT_NAME 测试"