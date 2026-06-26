#!/bin/bash
# sync_skill.sh - 同步 SKILL.md 文件
# 用法: ./scripts/sync_skill.sh [direction]
# direction:
#   src2root (默认) - 从 src/skills/SKILL.md 同步到根目录
#   root2src - 从根目录同步到 src/skills/SKILL.md
#   diff - 显示两个文件的差异
#   check - 检查文件一致性

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 文件路径
SRC_SKILL="$PROJECT_ROOT/src/skills/SKILL.md"
ROOT_SKILL="$PROJECT_ROOT/SKILL.md"

# 检查文件是否存在
if [ ! -f "$SRC_SKILL" ]; then
    echo "❌ 错误: src/skills/SKILL.md 不存在"
    exit 1
fi

if [ ! -f "$ROOT_SKILL" ]; then
    echo "❌ 错误: 根目录 SKILL.md 不存在"
    exit 1
fi

# 获取方向参数
DIRECTION="${1:-src2root}"

case "$DIRECTION" in
    src2root)
        echo "📥 从 src/skills/SKILL.md 同步到根目录..."
        
        # 复制文件并调整路径
        # 将 references/ 替换为 src/skills/references/
        sed 's|references/|src/skills/references/|g' "$SRC_SKILL" > "$ROOT_SKILL"
        
        echo "✅ 同步完成 (路径已调整)"
        echo ""
        echo "文件大小对比:"
        echo "  src/skills/SKILL.md: $(wc -c < "$SRC_SKILL") bytes"
        echo "  SKILL.md: $(wc -c < "$ROOT_SKILL") bytes"
        echo ""
        echo "路径调整示例:"
        grep -n "src/skills/references/" "$ROOT_SKILL" | head -3
        ;;
    
    root2src)
        echo "📤 从根目录同步到 src/skills/SKILL.md..."
        
        # 复制文件并调整路径 (反向)
        # 将 src/skills/references/ 替换回 references/
        sed 's|src/skills/references/|references/|g' "$ROOT_SKILL" > "$SRC_SKILL"
        
        echo "✅ 同步完成 (路径已调整)"
        echo ""
        echo "文件大小对比:"
        echo "  src/skills/SKILL.md: $(wc -c < "$SRC_SKILL") bytes"
        echo "  SKILL.md: $(wc -c < "$ROOT_SKILL") bytes"
        ;;
    
    diff)
        echo "📊 显示两个文件的差异..."
        
        # 创建临时文件用于比较 (调整路径后)
        TEMP_ROOT=$(mktemp)
        sed 's|references/|src/skills/references/|g' "$SRC_SKILL" > "$TEMP_ROOT"
        
        if diff -q "$TEMP_ROOT" "$ROOT_SKILL" > /dev/null 2>&1; then
            echo "✅ 两个文件内容相同 (路径已调整)"
        else
            echo "⚠️ 两个文件有差异:"
            diff -u "$TEMP_ROOT" "$ROOT_SKILL" | head -50
            echo ""
            echo "差异行数: $(diff "$TEMP_ROOT" "$ROOT_SKILL" | grep -c "^[<>]")"
        fi
        
        rm -f "$TEMP_ROOT"
        ;;
    
    check)
        echo "🔍 检查文件一致性..."
        
        # 创建临时文件用于比较 (调整路径后)
        TEMP_ROOT=$(mktemp)
        sed 's|references/|src/skills/references/|g' "$SRC_SKILL" > "$TEMP_ROOT"
        
        if diff -q "$TEMP_ROOT" "$ROOT_SKILL" > /dev/null 2>&1; then
            echo "✅ 两个文件一致 (路径已调整)"
            rm -f "$TEMP_ROOT"
            exit 0
        else
            echo "❌ 两个文件不一致"
            echo ""
            echo "src/skills/SKILL.md 行数: $(wc -l < "$SRC_SKILL")"
            echo "根目录 SKILL.md 行数: $(wc -l < "$ROOT_SKILL")"
            rm -f "$TEMP_ROOT"
            exit 1
        fi
        ;;
    
    *)
        echo "❌ 未知方向: $DIRECTION"
        echo ""
        echo "用法: $0 [src2root|root2src|diff|check]"
        echo ""
        echo "参数说明:"
        echo "  src2root - 从 src/skills/SKILL.md 同步到根目录 (默认)"
        echo "  root2src - 从根目录同步到 src/skills/SKILL.md"
        echo "  diff     - 显示两个文件的差异"
        echo "  check    - 检查文件一致性 (用于 CI)"
        exit 1
        ;;
esac
