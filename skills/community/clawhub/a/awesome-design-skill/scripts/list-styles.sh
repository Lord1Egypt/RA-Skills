#!/bin/bash
# 列出所有可用的设计风格

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DESIGN_MD_DIR="$SCRIPT_DIR/../design-md"

echo "可用的设计风格："
echo "================"
echo ""

ls -1 "$DESIGN_MD_DIR" 2>/dev/null | while read style; do
    design_file="$DESIGN_MD_DIR/$style/DESIGN.md"
    if [ -f "$design_file" ]; then
        # 尝试从 README 或 DESIGN.md 获取描述
        readme_file="$DESIGN_MD_DIR/$style/README.md"
        if [ -f "$readme_file" ]; then
            desc=$(grep -m1 "# " "$readme_file" | sed 's/^# //' | head -c 50)
            echo "  - $style: $desc"
        else
            echo "  - $style"
        fi
    fi
done

echo ""
echo "总计: $(ls -1 "$DESIGN_MD_DIR" 2>/dev/null | wc -l | tr -d ' ') 种风格"
