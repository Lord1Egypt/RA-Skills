#!/bin/bash
# 获取指定风格的 DESIGN.md 路径

if [ -z "$1" ]; then
    echo "用法: $0 <风格名称>"
    echo "示例: $0 apple"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DESIGN_MD_DIR="$SCRIPT_DIR/../design-md"
style="$1"

design_file="$DESIGN_MD_DIR/$style/DESIGN.md"

if [ -f "$design_file" ]; then
    echo "$design_file"
else
    echo "错误：未找到风格 '$style'" >&2
    exit 1
fi
