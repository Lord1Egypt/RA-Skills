#!/bin/bash
set -e
echo "🧬 Eternal Memory v3.4.1 安装中..."
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_TOOLS="${HOME}/.openclaw/workspace-v4-pro/tools"
mkdir -p "$TARGET_TOOLS"
cp -v "$SKILL_DIR/tools/"*.py "$TARGET_TOOLS/" 2>/dev/null || true
echo "✅ Eternal Memory 安装完成!"
echo "  测试: SKIP_ONNX=1 python3 tools/local_embedder.py"
echo "  初始化: python3 tools/memory_system.py --archive"
echo "  基准: python3 tools/memory_topology.py --benchmark 50"
