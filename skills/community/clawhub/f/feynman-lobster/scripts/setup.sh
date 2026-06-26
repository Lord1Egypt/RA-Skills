#!/bin/bash
# 费曼虾 — Workspace 初始化脚本
# 安装 skill 后自动执行，或手动运行：
# bash ~/.openclaw/skills/feynman-lobster/scripts/setup.sh

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw}"
CONTRACTS_FILE="$WORKSPACE/contracts.json"

echo "🦞 费曼虾初始化中..."

# 确保 workspace 目录存在
mkdir -p "$WORKSPACE"

# 初始化 contracts.json（如果不存在）
if [ ! -f "$CONTRACTS_FILE" ]; then
  echo "[]" > "$CONTRACTS_FILE"
  echo "  ✓ 创建 contracts.json"
else
  echo "  ✓ contracts.json 已存在，跳过"
fi

# 提示心跳配置
echo ""
echo "  建议配置心跳间隔（费曼追问频率）："
echo "  openclaw config set agents.defaults.heartbeat.every \"4h\""
echo ""
echo "🦞 初始化完成！"
echo "  在 IM 里跟龙虾说「我想学 XXX」开始签约。"
echo ""

START_SCRIPT="$WORKSPACE/skills/feynman-lobster/scripts/start-panel.sh"
if [ -f "$START_SCRIPT" ]; then
  echo "  正在自动启动面板并尝试打开浏览器..."
  bash "$START_SCRIPT" --detached --open >/tmp/feynman-panel-boot.log 2>&1 || true
  echo "  面板地址：http://localhost:19380"
  echo "  启动日志：/tmp/feynman-panel-boot.log"
else
  echo "  启动面板：bash $WORKSPACE/skills/feynman-lobster/scripts/start-panel.sh"
  echo "  面板地址：http://localhost:19380"
fi
