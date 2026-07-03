#!/data/data/com.termux/files/usr/bin/env bash
# Code Audit Pro — 安装依赖
set -e

echo "🔍 Code Audit Pro — 安装依赖"
echo "═══════════════════════════════"

# Python 工具
echo ""
echo "📦 Python 工具..."
pip install flake8 bandit 2>/dev/null && echo "  ✅ flake8 + bandit 已安装" || echo "  ⚠️ 部分安装失败，可手动: pip install flake8 bandit"

# Node 工具
echo ""
echo "📦 Node 工具..."
if command -v npx &>/dev/null; then
  echo "  ✅ npx 可用 (prettier/eslint 按需自动下载)"
else
  echo "  ⚠️ npx 不可用，安装 Node.js 后可获得 prettier/eslint"
fi

echo ""
echo "✅ 安装完成"
echo ""
echo "使用:"
echo "  python3 scripts/audit.py app.py"
echo "  python3 scripts/audit.py src/"
echo "  python3 scripts/audit.py --check \"<code>\""