#!/bin/bash
# AutoDream Core 安装脚本
# 用法：./install.sh [目标目录]

set -e

TARGET_DIR="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 AutoDream Core 安装程序"
echo "=========================="
echo ""

# 检查目标目录
if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ 目标目录不存在：$TARGET_DIR"
    exit 1
fi

echo "📦 目标目录：$TARGET_DIR"
echo ""

# 创建目录结构
echo "📁 创建目录结构..."
mkdir -p "$TARGET_DIR/autodream_core/core/stages"
mkdir -p "$TARGET_DIR/autodream_core/core/utils"
mkdir -p "$TARGET_DIR/autodream_core/adapters"
mkdir -p "$TARGET_DIR/autodream_core/config"
mkdir -p "$TARGET_DIR/autodream_core/tests"

# 复制核心文件
echo "📄 复制核心文件..."
cp "$SCRIPT_DIR/core/__init__.py" "$TARGET_DIR/autodream_core/core/__init__.py"
cp "$SCRIPT_DIR/core/engine.py" "$TARGET_DIR/autodream_core/core/engine.py"
cp "$SCRIPT_DIR/core/analytics.py" "$TARGET_DIR/autodream_core/core/analytics.py"

cp "$SCRIPT_DIR/core/stages/orientation.py" "$TARGET_DIR/autodream_core/core/stages/orientation.py"
cp "$SCRIPT_DIR/core/stages/gather.py" "$TARGET_DIR/autodream_core/core/stages/gather.py"
cp "$SCRIPT_DIR/core/stages/consolidate.py" "$TARGET_DIR/autodream_core/core/stages/consolidate.py"
cp "$SCRIPT_DIR/core/stages/prune.py" "$TARGET_DIR/autodream_core/core/stages/prune.py"

cp "$SCRIPT_DIR/core/utils/frontmatter.py" "$TARGET_DIR/autodream_core/core/utils/frontmatter.py"
cp "$SCRIPT_DIR/core/utils/text.py" "$TARGET_DIR/autodream_core/core/utils/text.py"
cp "$SCRIPT_DIR/core/utils/dates.py" "$TARGET_DIR/autodream_core/core/utils/dates.py"
cp "$SCRIPT_DIR/core/utils/state.py" "$TARGET_DIR/autodream_core/core/utils/state.py"

cp "$SCRIPT_DIR/adapters/__init__.py" "$TARGET_DIR/autodream_core/adapters/__init__.py"
cp "$SCRIPT_DIR/adapters/base.py" "$TARGET_DIR/autodream_core/adapters/base.py"
cp "$SCRIPT_DIR/adapters/openclaw.py" "$TARGET_DIR/autodream_core/adapters/openclaw.py"

cp "$SCRIPT_DIR/config/default.json" "$TARGET_DIR/autodream_core/config/default.json"
cp "$SCRIPT_DIR/tests/test_core.py" "$TARGET_DIR/autodream_core/tests/test_core.py"

# 创建 __init__.py（如果不存在）
touch "$TARGET_DIR/autodream_core/__init__.py"

echo ""
echo "✅ 安装完成！"
echo ""
echo "📚 使用方法:"
echo ""
echo "  from pathlib import Path"
echo "  from autodream_core import AutoDreamEngine, OpenClawAdapter"
echo ""
echo "  adapter = OpenClawAdapter(workspace=Path('/your/workspace'))"
echo "  engine = AutoDreamEngine(adapter)"
echo "  result = engine.run(force=True)"
echo ""
echo "🧪 运行测试:"
echo ""
echo "  cd $TARGET_DIR/autodream_core"
echo "  python3 tests/test_core.py"
echo ""
