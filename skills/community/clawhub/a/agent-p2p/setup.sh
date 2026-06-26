#!/bin/bash
# Agent P2P Skill 安装脚本
# 用法: ./setup.sh <agent-token>

set -e

AGENT_TOKEN="${1:-}"

if [ -z "$AGENT_TOKEN" ]; then
    echo "❌ 请提供 Agent Token"
    echo ""
    echo "用法: $0 <agent-token>"
    echo ""
    echo "获取 Token:"
    echo "1. 访问 https://your-domain.com/static/admin.html"
    echo "2. 登录管理后台"
    echo "3. 创建或获取 Agent Token"
    echo ""
    exit 1
fi

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
GATEWAY_ENV="$HOME/.openclaw/gateway.env"

echo "=== Agent P2P Skill 安装 ==="
echo ""

# 1. 配置 Token
echo "📝 步骤 1/4: 配置 Token..."
mkdir -p "$(dirname "$GATEWAY_ENV")"

if [ -f "$GATEWAY_ENV" ]; then
    if grep -q "AGENTP2P_TOKEN=" "$GATEWAY_ENV"; then
        sed -i "s/AGENTP2P_TOKEN=.*/AGENTP2P_TOKEN=$AGENT_TOKEN/" "$GATEWAY_ENV"
    else
        echo "AGENTP2P_TOKEN=$AGENT_TOKEN" >> "$GATEWAY_ENV"
    fi
else
    cat > "$GATEWAY_ENV" << EOF
AGENTP2P_TOKEN=$AGENT_TOKEN
AGENTP2P_HUB_URL=https://your-domain.com
EOF
fi

echo "   ✅ Token 已配置"

# 2. 生成 Hooks Token
echo ""
echo "🔑 步骤 2/4: 准备 Hooks 凭证..."

if [ -f "$OPENCLAW_CONFIG" ] && jq -e '.hooks.token' "$OPENCLAW_CONFIG" > /dev/null 2>&1; then
    HOOKS_TOKEN=$(jq -r '.hooks.token' "$OPENCLAW_CONFIG")
    echo "   ✅ 复用已有 Hooks Token"
else
    HOOKS_TOKEN=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    echo "   ✅ 生成新 Hooks Token"
fi

if grep -q "OPENCLAW_HOOKS_TOKEN=" "$GATEWAY_ENV" 2>/dev/null; then
    sed -i "s/OPENCLAW_HOOKS_TOKEN=.*/OPENCLAW_HOOKS_TOKEN=$HOOKS_TOKEN/" "$GATEWAY_ENV"
else
    cat >> "$GATEWAY_ENV" << EOF
OPENCLAW_HOOKS_TOKEN=$HOOKS_TOKEN
OPENCLAW_GATEWAY_URL=http://127.0.0.1:18789
EOF
fi

export OPENCLAW_HOOKS_TOKEN="$HOOKS_TOKEN"
export OPENCLAW_GATEWAY_URL="http://127.0.0.1:18789"

# 3. 安装依赖
echo ""
echo "📦 步骤 3/4: 安装依赖..."
cd "$SKILL_DIR"

if [ ! -d venv ]; then
    python3 -m venv venv
    echo "   ✅ 创建虚拟环境"
fi

if venv/bin/pip install -q websocket-client requests 2>/dev/null; then
    echo "   ✅ 依赖安装成功"
else
    echo "   ⚠️ 使用国内镜像重试..."
    venv/bin/pip install -q websocket-client requests -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
    echo "   ✅ 依赖安装成功"
fi

# 4. 启动客户端
echo ""
echo "🚀 步骤 4/4: 启动客户端..."

if [ -f client.pid ]; then
    OLD_PID=$(cat client.pid)
    kill $OLD_PID 2>/dev/null || true
    sleep 1
fi

nohup venv/bin/python3 client.py > client.log 2>&1 &
sleep 3

if [ -f client.pid ]; then
    PID=$(cat client.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "   ✅ 客户端已启动 (PID: $PID)"
    else
        echo "   ❌ 启动失败，检查 client.log"
        tail -20 client.log
        exit 1
    fi
else
    echo "   ⚠️ PID 文件未创建，检查 client.log"
    tail -20 client.log
    exit 1
fi

# 5. 配置 Gateway
echo ""
echo "🔧 配置 OpenClaw Gateway..."

NEEDS_RESTART="yes"
if [ -f "$OPENCLAW_CONFIG" ]; then
    HOOKS_OK=$(jq -e '.hooks.enabled == true and .hooks.token != null' "$OPENCLAW_CONFIG" 2>/dev/null && echo "yes" || echo "no")
    if [ "$HOOKS_OK" = "yes" ]; then
        NEEDS_RESTART="no"
    fi
fi

if [ "$NEEDS_RESTART" = "no" ]; then
    echo "   ✅ Gateway 已配置"
else
    echo "   📝 更新 Gateway 配置..."
    
    python3 << PYEOF
import json
from pathlib import Path

config_path = Path("$OPENCLAW_CONFIG")
config_path.parent.mkdir(parents=True, exist_ok=True)

if config_path.exists():
    config = json.loads(config_path.read_text())
else:
    config = {}

config["hooks"] = {
    "enabled": True,
    "path": "/hooks",
    "token": "$HOOKS_TOKEN"
}

config_path.write_text(json.dumps(config, indent=2))
print("   ✅ 配置已写入")
PYEOF

    (
        sleep 5
        for i in $(seq 1 30); do
            sleep 2
            if curl -s http://127.0.0.1:18789/health > /dev/null 2>&1; then
                break
            fi
        done
        sleep 2
        
        curl -s -X POST "http://127.0.0.1:18789/hooks/wake" \
            -H "Authorization: Bearer $HOOKS_TOKEN" \
            -H "Content-Type: application/json" \
            -d '{"text": "[系统] Agent P2P Skill 安装完成！客户端已连接。"}' > /dev/null 2>&1 || true
    ) &

    echo ""
    echo "   🔄 正在重启 OpenClaw Gateway..."
    openclaw restart 2>/dev/null || echo "   ⚠️ 请手动运行: openclaw restart"
fi

echo ""
echo "=== 安装完成 ==="
echo ""

if [ -f client.pid ]; then
    PID=$(cat client.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "   ✅ 客户端: 运行中 (PID: $PID)"
    else
        echo "   ❌ 客户端: 未运行"
    fi
else
    echo "   ❌ 客户端: 未启动"
fi

if [ -f client.log ]; then
    echo ""
    echo "📋 最近日志:"
    tail -5 client.log | sed 's/^/   /'
fi

echo ""
echo "🎉 Agent P2P Skill 安装完成！"
echo ""
echo "下一步:"
echo "1. 访问 https://your-domain.com 查看 Portal"
echo "2. 使用 ./send.py 发送消息测试"
echo "3. 查看完整文档: cat SKILL.md"
echo ""
