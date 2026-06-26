#!/bin/bash
# validate-deliverable.sh — 产物结构自动化校验
# 用法：./validate-deliverable.sh <交付物目录> <交付物类型>
# 示例：./validate-deliverable.sh "03_PPT框架协作包/08_v4审核收口版" "pptx"
# 交付物类型：pptx | docx | pdf | html

set -e

DELIVERY_DIR="${1:-}"
DELIVERY_TYPE="${2:-}"

if [[ -z "$DELIVERY_DIR" || -z "$DELIVERY_TYPE" ]]; then
  echo "用法: $0 <交付物目录> <交付物类型>"
  echo "交付物类型: pptx | docx | pdf | html"
  exit 2
fi

if [[ ! -d "$DELIVERY_DIR" ]]; then
  echo "错误: 目录不存在: $DELIVERY_DIR"
  exit 2
fi

ERRORS=()
WARNINGS=()

echo "=== 交付物校验: $DELIVERY_DIR ==="
echo "交付物类型: $DELIVERY_TYPE"
echo ""

case "$DELIVERY_TYPE" in
  pptx)
    # 1. 检查主文件是否存在
    MAIN_FILE=$(ls "$DELIVERY_DIR"/*.pptx 2>/dev/null | head -1 || true)
    if [[ -z "$MAIN_FILE" ]]; then
      ERRORS+=("主 PPTX 文件不存在")
    else
      echo "主文件: $(basename "$MAIN_FILE")"

      # 2. 解包检查页数
      if command -v unzip &>/dev/null; then
        SLIDE_COUNT=$(unzip -l "$MAIN_FILE" 2>/dev/null | grep -c "ppt/slides/slide[0-9]" || echo "0")
        echo "检测页数: $SLIDE_COUNT"
        if [[ "$SLIDE_COUNT" -eq 0 ]]; then
          ERRORS+=("未检测到幻灯片文件")
        fi
      fi

      # 3. 检查图表文件引用（如果图表目录存在）
      CHARTS_DIR="$DELIVERY_DIR/charts"
      if [[ -d "$CHARTS_DIR" ]]; then
        CHART_COUNT=$(ls "$CHARTS_DIR"/*.png "$CHARTS_DIR"/*.jpg 2>/dev/null | wc -l)
        echo "图表文件数: $CHART_COUNT"
      fi
    fi

    # 4. 检查修订日志
    if ls "$DELIVERY_DIR"/*修订日志* "$DELIVERY_DIR"/*revision* "$DELIVERY_DIR"/*CHANGELOG* 2>/dev/null | grep -q .; then
      echo "修订日志: ✅ 存在"
    else
      WARNINGS+=("未找到修订日志（强烈推荐）")
    fi

    # 5. 检查验证记录
    if ls "$DELIVERY_DIR"/*验证* "$DELIVERY_DIR"/*validation* 2>/dev/null | grep -q .; then
      echo "验证记录: ✅ 存在"
    else
      WARNINGS+=("未找到验证记录（推荐）")
    fi
    ;;

  html)
    if ls "$DELIVERY_DIR"/*.html 2>/dev/null | grep -q .; then
      echo "HTML 文件: ✅ 存在"
    else
      ERRORS+=("未找到 HTML 文件")
    fi
    ;;

  docx)
    if ls "$DELIVERY_DIR"/*.docx 2>/dev/null | grep -q .; then
      echo "DOCX 文件: ✅ 存在"
    else
      ERRORS+=("未找到 DOCX 文件")
    fi
    ;;
esac

# 通用检查：交接文档
HANDOVER_DOC=$(ls "$DELIVERY_DIR"/*handoff* "$DELIVERY_DIR"/*交接* 2>/dev/null | head -1 || true)
if [[ -n "$HANDOVER_DOC" && -f "$HANDOVER_DOC" ]]; then
  echo "交接文档: ✅ $(basename "$HANDOVER_DOC")"
else
  WARNINGS+=("未找到交接文档（影响下游 Agent 接手）")
fi

# 输出结果
echo ""
if [[ ${#ERRORS[@]} -eq 0 && ${#WARNINGS[@]} -eq 0 ]]; then
  echo "✅ 校验通过"
  exit 0
fi

for e in "${ERRORS[@]}"; do
  echo "🔴 错误: $e"
done

for w in "${WARNINGS[@]}"; do
  echo "🟡 警告: $w"
done

echo ""
if [[ ${#ERRORS[@]} -gt 0 ]]; then
  echo "校验失败：${#ERRORS[@]} 个错误"
  exit 1
else
  echo "校验通过（${#WARNINGS[@]} 个警告）"
  exit 0
fi
