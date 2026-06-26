#!/bin/bash
# Agent Deleter Script
# Usage: ./delete-agent.sh <agent-id>

set -e

AGENT_ID="$1"
CONFIG_FILE="/home/admin/.openclaw/openclaw.json"
AGENTS_DIR="/home/admin/.openclaw/agents"
WORKSPACE_BASE="/home/admin/.openclaw"

if [ -z "$AGENT_ID" ]; then
    echo "❌ 请提供 agent-id"
    echo "用法: $0 <agent-id>"
    exit 1
fi

if [ "$AGENT_ID" = "main" ]; then
    echo "❌ 不能删除 main agent"
    exit 1
fi

if [ ! -d "$AGENTS_DIR/$AGENT_ID" ]; then
    echo "❌ Agent '$AGENT_ID' 不存在"
    exit 1
fi

echo "⚠️  即将删除 Agent: $AGENT_ID"
read -p "确认删除？(y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "已取消"
    exit 0
fi

# Remove from config using node
node -e "
const fs = require('fs');
const configPath = '$CONFIG_FILE';
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const agentId = '$AGENT_ID';

// Remove from agents.list
config.agents.list = config.agents.list.filter(a => a.id !== agentId);

// Remove feishu account
delete config.channels.feishu.accounts[agentId];

// Remove binding
config.bindings = config.bindings.filter(b => b.agentId !== agentId);

// Remove from agentToAgent allow list
if (config.tools.agentToAgent && config.tools.agentToAgent.allow) {
    config.tools.agentToAgent.allow = config.tools.agentToAgent.allow.filter(id => id !== agentId);
}

fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
console.log('✅ 配置已更新');
"

# Remove directories
echo "🗑️  删除目录..."
rm -rf "$AGENTS_DIR/$AGENT_ID"
rm -rf "$WORKSPACE_BASE/workspace-$AGENT_ID"

echo "🎉 Agent '$AGENT_ID' 已删除"
echo "⚠️  请执行 openclaw gateway restart 使更改生效"