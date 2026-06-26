#!/bin/bash
# 溯源检查脚本：验证报告中的数据是否能在对应卡片中找到

REPORT=${1:-"reports/final-report.md"}
SOURCES_DIR=${2:-"sources"}

echo "=== 溯源检查 ==="
echo "报告: $REPORT"
echo "来源目录: $SOURCES_DIR"
echo ""

ERRORS=0

# 获取所有引用的卡片ID
CARD_IDS=$(grep -oP '\[\[card-[0-9]+\]\]' "$REPORT" | sed 's/\[\[//;s/\]\]//' | sort -u)

echo "发现引用的卡片: $CARD_IDS"
echo ""

for CARD in $CARD_IDS; do
    CARD_FILE="$SOURCES_DIR/$CARD.md"
    
    if [ ! -f "$CARD_FILE" ]; then
        echo "❌ 错误: 引用了 $CARD 但文件不存在"
        ERRORS=$((ERRORS + 1))
        continue
    fi
    
    # 提取报告中引用该卡片的数据点（数值）
    DATA_POINTS=$(grep "$CARD" "$REPORT" | grep -oE '[0-9]+(\.[0-9]+)?%?|[$][0-9,]+' | sort -u)
    
    if [ -z "$DATA_POINTS" ]; then
        echo "⚪ $CARD: 无具体数据引用"
        continue
    fi
    
    # 检查每个数据点是否在卡片中
    FOUND=0
    for DP in $DATA_POINTS; do
        if grep -q "$DP" "$CARD_FILE"; then
            FOUND=$((FOUND + 1))
        fi
    done
    
    TOTAL=$(echo "$DATA_POINTS" | wc -w)
    if [ $FOUND -eq $TOTAL ]; then
        echo "✅ $CARD: $FOUND/$TOTAL 数据点可溯源"
    else
        echo "❌ $CARD: 只有 $FOUND/$TOTAL 数据点可溯源"
        echo "   缺失数据点:"
        for DP in $DATA_POINTS; do
            if ! grep -q "$DP" "$CARD_FILE"; then
                echo "   - $DP"
            fi
        done
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✅ 所有引用数据均可溯源"
    exit 0
else
    echo "❌ 发现 $ERRORS 个溯源问题"
    exit 1
fi
