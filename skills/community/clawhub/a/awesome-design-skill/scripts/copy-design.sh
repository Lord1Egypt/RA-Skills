#!/bin/bash
# 复制指定风格的 DESIGN.md 到当前工作目录
# 用法: copy-design.sh <风格名称> [目标目录]

if [ -z "$1" ]; then
    echo "用法: $0 <风格名称> [目标目录]"
    echo "示例: $0 linear.app"
    echo "示例: $0 apple ./my-project"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DESIGN_MD_DIR="$SCRIPT_DIR/../design-md"
STYLE="$1"
TARGET_DIR="${2:-.}"

# 获取 DESIGN.md 路径
DESIGN_FILE="$DESIGN_MD_DIR/$STYLE/DESIGN.md"

if [ ! -f "$DESIGN_FILE" ]; then
    echo "错误：未找到风格 '$STYLE'" >&2
    echo "可用风格请运行: scripts/list-styles.sh" >&2
    exit 1
fi

# 确保目标目录存在
mkdir -p "$TARGET_DIR"

# 复制文件
TARGET_FILE="$TARGET_DIR/DESIGN.md"
cp "$DESIGN_FILE" "$TARGET_FILE"

if [ $? -eq 0 ]; then
    echo "已复制 $STYLE 的 DESIGN.md 到: $TARGET_FILE"
    echo "风格描述: $(grep -m1 "^# " "$DESIGN_FILE" | sed 's/^# //')"
else
    echo "错误：复制失败" >&2
    exit 1
fi
