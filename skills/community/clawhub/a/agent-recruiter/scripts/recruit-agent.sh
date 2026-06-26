#!/bin/bash
# recruit-agent.sh - 招聘 Agent 自动化脚本
# 用法：./recruit-agent.sh <agent_id> <agent_name> <群聊 ID>

set -e

AGENT_ID="$1"
AGENT_NAME="$2"
GROUP_ID="$3"

if [[ -z "$AGENT_ID" || -z "$AGENT_NAME" ]]; then
    echo "用法：$0 <agent_id> <agent_name> [群聊 ID]"
    echo "例如：$0 tim 'Tim 维护专员' oc_a669e950b71b06b09a6e293ee6ec4683"
    exit 1
fi

OPENCLAW_DIR="$HOME/.openclaw"
AGENTS_DIR="$OPENCLAW_DIR/agents"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace-$AGENT_ID"
AGENT_DIR="$AGENTS_DIR/$AGENT_ID/agent"
CONFIG_FILE="$OPENCLAW_DIR/openclaw.json"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATES_DIR="$SKILL_DIR/templates"

echo "⚡ 正在招聘 Agent: $AGENT_ID ($AGENT_NAME)"

# 1. 创建目录结构
echo "📁 创建目录..."
mkdir -p "$AGENT_DIR"
mkdir -p "$WORKSPACE_DIR"

# 2. 创建 agent.json
echo "📝 创建 agent.json..."
cat > "$AGENT_DIR/agent.json" << EOF
{
  "id": "$AGENT_ID",
  "name": "$AGENT_NAME",
  "workspace": "$WORKSPACE_DIR",
  "agentDir": "$AGENT_DIR",
  "model": "modelstudio/qwen3.5-plus"
}
EOF

# 3. 复制模型和认证配置
echo "🔧 复制配置..."
if [[ -f "$AGENTS_DIR/mike/agent/models.json" ]]; then
    cp "$AGENTS_DIR/mike/agent/models.json" "$AGENT_DIR/"
    cp "$AGENTS_DIR/mike/agent/auth-profiles.json" "$AGENT_DIR/"
    echo "✅ 已复制 mike 的配置模板"
else
    echo "⚠️ 警告：找不到 mike 的配置模板，需要手动配置 models.json 和 auth-profiles.json"
fi

# 4. 生成核心文件（SOUL.md, AGENTS.md, IDENTITY.md）
echo "📄 生成核心文件..."
if [[ -d "$TEMPLATES_DIR" ]]; then
    # 复制模板
    [[ -f "$TEMPLATES_DIR/SOUL.md.template" ]] && cp "$TEMPLATES_DIR/SOUL.md.template" "$WORKSPACE_DIR/SOUL.md"
    [[ -f "$TEMPLATES_DIR/AGENTS.md.template" ]] && cp "$TEMPLATES_DIR/AGENTS.md.template" "$WORKSPACE_DIR/AGENTS.md"
    [[ -f "$TEMPLATES_DIR/IDENTITY.md.template" ]] && cp "$TEMPLATES_DIR/IDENTITY.md.template" "$WORKSPACE_DIR/IDENTITY.md"
    
    # 创建 memory 目录
    mkdir -p "$WORKSPACE_DIR/memory"
    
    # 生成简单的 USER.md
    cat > "$WORKSPACE_DIR/USER.md" << EOF
# USER.md - About Your Human

_Learn about the person you're helping. Update this as you go._

- **Name**: [待填写]
- **Timezone**: Asia/Shanghai
- **Notes**: [待填写]

---
The more you know, the better you can help.
EOF
    
    # 生成空的 HEARTBEAT.md
    cat > "$WORKSPACE_DIR/HEARTBEAT.md" << 'EOF'
# HEARTBEAT.md
# Add periodic tasks below (or leave empty to skip heartbeat API calls)
EOF

    # 如果有示例 SOUL.md（如 tim），优先使用
    if [[ -f "$TEMPLATES_DIR/examples/$AGENT_ID/SOUL.md" ]]; then
        cp "$TEMPLATES_DIR/examples/$AGENT_ID/SOUL.md" "$WORKSPACE_DIR/SOUL.md"
        echo "✅ 已使用 $AGENT_ID 专用 SOUL.md 模板"
    fi
    if [[ -f "$TEMPLATES_DIR/examples/$AGENT_ID/IDENTITY.md" ]]; then
        cp "$TEMPLATES_DIR/examples/$AGENT_ID/IDENTITY.md" "$WORKSPACE_DIR/IDENTITY.md"
        echo "✅ 已使用 $AGENT_ID 专用 IDENTITY.md 模板"
    fi
    
    echo "✅ 已生成 SOUL.md, AGENTS.md, IDENTITY.md"
else
    echo "⚠️ 警告：找不到模板目录，需要手动创建核心文件"
fi

# 5. 添加到 openclaw.json
echo "📋 更新 openclaw.json..."

# 检查 agent 是否已存在
if grep -q "\"id\": \"$AGENT_ID\"" "$CONFIG_FILE"; then
    echo "⚠️ 警告：Agent '$AGENT_ID' 已存在于配置中"
else
    # 添加 agent 到 agents.list
    # 找到 mike 的配置，在它后面添加新 agent
    if grep -q '"id": "mike"' "$CONFIG_FILE"; then
        # 使用 node 来安全地修改 JSON
        node -e "
const fs = require('fs');
const config = JSON.parse(fs.readFileSync('$CONFIG_FILE', 'utf8'));

// 添加 agent
config.agents.list.push({
  id: '$AGENT_ID',
  name: '$AGENT_NAME',
  workspace: '$WORKSPACE_DIR',
  agentDir: '$AGENT_DIR',
  model: 'modelstudio/qwen3.5-plus'
});

// 添加 binding（如果有群 ID）
if ('$GROUP_ID') {
  config.bindings.push({
    type: 'route',
    agentId: '$AGENT_ID',
    match: {
      channel: 'feishu',
      peer: {
        kind: 'group',
        id: '$GROUP_ID'
      }
    }
  });
}

fs.writeFileSync('$CONFIG_FILE', JSON.stringify(config, null, 2) + '\n');
console.log('✅ 已更新 openclaw.json');
"
    fi
fi

# 6. 重启 Gateway
echo "🔄 重启 Gateway..."
openclaw gateway restart

echo ""
echo "✅ Agent '$AGENT_ID' 招聘完成！"
echo ""
echo "📌 配置摘要:"
echo "   - Agent ID: $AGENT_ID"
echo "   - 名称：$AGENT_NAME"
echo "   - Workspace: $WORKSPACE_DIR"
echo "   - Agent 目录：$AGENT_DIR"
if [[ -n "$GROUP_ID" ]]; then
    echo "   - 绑定群聊：$GROUP_ID"
fi
echo ""
echo "📄 核心文件:"
echo "   - SOUL.md: $WORKSPACE_DIR/SOUL.md"
echo "   - IDENTITY.md: $WORKSPACE_DIR/IDENTITY.md"
echo "   - AGENTS.md: $WORKSPACE_DIR/AGENTS.md"
echo ""
echo "🔍 验证命令:"
echo "   openclaw gateway status"
echo "   cat $WORKSPACE_DIR/SOUL.md"
echo ""
echo "💡 下一步:"
echo "   1. 编辑 SOUL.md 定义 Agent 人格和职责"
echo "   2. 编辑 IDENTITY.md 设置名称和 Emoji"
echo "   3. 在群聊中测试 Agent 响应"
