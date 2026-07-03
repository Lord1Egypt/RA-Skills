#!/data/data/com.termux/files/usr/bin/env bash
# Dev Toolkit Pro — 安装依赖
set -e

echo "🔧 Dev Toolkit Pro — 安装依赖"
echo "═══════════════════════════════"

# Node 运行时
echo ""
echo "📦 Node 工具..."
if command -v node &>/dev/null; then
  echo "  ✅ Node.js $(node -v)"
  npm install -g prettier 2>/dev/null && echo "  ✅ prettier 已安装" || echo "  ⚠️ prettier 安装失败"
else
  echo "  ⚠️ 需要 Node.js: https://nodejs.org"
fi

# Python 工具
echo ""
echo "📦 Python 工具..."
if command -v python3 &>/dev/null; then
  pip install flake8 black 2>/dev/null && echo "  ✅ flake8 + black 已安装" || echo "  ⚠️ Python 工具安装失败"
fi

echo ""
echo "✅ 安装完成"
echo ""
echo "使用:"
echo "  node scripts/dev-tk.js review"
echo "  node scripts/dev-tk.js dep"
echo "  node scripts/dev-tk.js scaffold my-app node"
echo "  # 或用入口: bin/dev-tk review"