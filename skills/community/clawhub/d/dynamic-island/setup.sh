#!/bin/bash
# OpenClaw Dynamic Island — one-click setup
# Usage: bash setup.sh

set -e
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🏝️  OpenClaw Dynamic Island Setup"
echo "=================================="
echo ""

# 1. Check macOS
if [[ "$(uname)" != "Darwin" ]]; then
  echo "❌ 仅支持 macOS"
  exit 1
fi
echo "✅ macOS $(sw_vers -productVersion)"

# 2. Check Swift compiler
if ! command -v swiftc &>/dev/null; then
  echo "❌ 未找到 Swift 编译器，请先安装 Xcode Command Line Tools:"
  echo "   xcode-select --install"
  exit 1
fi
echo "✅ Swift $(swiftc --version 2>&1 | head -1 | grep -oE '[0-9]+\.[0-9]+')"

# 3. Check Python3
if ! command -v python3 &>/dev/null; then
  echo "❌ 未找到 Python3，请先安装:"
  echo "   brew install python3"
  exit 1
fi
echo "✅ Python $(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"

# 4. Install websockets
if ! python3 -c "import websockets" 2>/dev/null; then
  echo "📦 安装 websockets..."
  pip3 install websockets
fi
echo "✅ websockets 已安装"

# 5. Check OpenClaw agents directory
AGENTS_DIR="$HOME/.openclaw/agents"
if [ ! -d "$AGENTS_DIR" ]; then
  echo "⚠️  未找到 $AGENTS_DIR"
  echo "   请先启动 OpenClaw，然后再运行灵动岛"
  echo ""
fi

# 6. Compile Swift widget
echo ""
echo "🔨 编译 widget..."
swiftc "$DIR/widget.swift" -o "$DIR/widget" -framework Cocoa -framework WebKit 2>&1
if [ $? -eq 0 ]; then
  echo "✅ widget 编译成功"
else
  echo "❌ widget 编译失败"
  exit 1
fi

# 7. Copy config if not exists
if [ ! -f "$DIR/config.json" ]; then
  cp "$DIR/config.example.json" "$DIR/config.json"
  echo "✅ 已创建 config.json（从 config.example.json 复制）"
else
  echo "✅ config.json 已存在"
fi

# 8. Make scripts executable
chmod +x "$DIR/start.sh"
chmod +x "$DIR/widget"

echo ""
echo "=================================="
echo "🎉 安装完成！"
echo ""
echo "启动灵动岛：  ./start.sh"
echo "停止灵动岛：  ./start.sh stop"
echo "重启灵动岛：  ./start.sh restart"
echo ""
echo "配置文件：    config.json"
echo "  - agent_names: 设置 Agent 显示名"
echo "  - agent_links: 设置飞书聊天链接（可选）"
echo ""
