#!/bin/bash
# validate-handoff.sh — 交接文档格式校验
# 用法：./validate-handoff.sh <handoff_file.md>
# 返回码：0=通过, 1=格式错误, 2=语义错误

set -e

FILE="${1:-}"

if [[ -z "$FILE" ]]; then
  echo "用法: $0 <handoff_file.md>"
  exit 2
fi

if [[ ! -f "$FILE" ]]; then
  echo "错误: 文件不存在: $FILE"
  exit 2
fi

ERRORS=()
WARNINGS=()

# 1. 检查 YAML frontmatter 是否存在
if ! grep -q "^---" "$FILE"; then
  ERRORS+=("缺少 YAML frontmatter（文件必须以 --- 开头）")
fi

# 2. 提取 frontmatter 区块
FRONTMATTER=$(sed -n '/^---$/,/^---$/p' "$FILE" | sed '1d;$d')
if [[ -z "$FRONTMATTER" ]]; then
  ERRORS+=("YAML frontmatter 为空或格式错误")
else
  # 3. 检查必要字段
  for field in schema_version document_type task_id created sender receiver status; do
    if ! echo "$FRONTMATTER" | grep -qE "^${field}:"; then
      ERRORS+=("缺少必填字段: $field")
    fi
  done

  # 4. 检查 status 值
  STATUS=$(echo "$FRONTMATTER" | grep "^status:" | sed 's/status: *//' | tr -d ' ')
  VALID_STATUSES="submitted|working|input-required|completed|failed|canceled"
  if [[ ! "$STATUS" =~ ^($VALID_STATUSES)$ ]]; then
    ERRORS+=("status 值无效: '$STATUS'（必须是: $VALID_STATUSES）")
  fi

  # 5. 检查 priority 值
  PRIORITY=$(echo "$FRONTMATTER" | grep "^priority:" | sed 's/priority: *//' | tr -d ' ')
  if [[ ! "$PRIORITY" =~ ^(P0|P1|P2)$ ]]; then
    ERRORS+=("priority 值无效: '$PRIORITY'（必须是 P0|P1|P2）")
  fi

  # 6. 检查 sender/receiver 结构
  if ! echo "$FRONTMATTER" | grep -q "^sender:"; then
    ERRORS+=("sender 字段缺失或格式错误")
  fi
  if ! echo "$FRONTMATTER" | grep -q "^receiver:"; then
    ERRORS+=("receiver 字段缺失或格式错误")
  fi
fi

# 7. 检查正文八节
REQUIRED_SECTIONS=("目标" "当前状态" "来源依据" "上游依赖" "下游产物" "接手建议" "约束与禁区" "验证标准")
for section in "${REQUIRED_SECTIONS[@]}"; do
  if ! grep -q "^## ${section}" "$FILE"; then
    ERRORS+=("缺少必要章节: ## ${section}")
  fi
done

# 8. 检查 forbidden_terms_checked 字段
if ! echo "$FRONTMATTER" | grep -q "forbidden_terms_checked:"; then
  WARNINGS+=("缺少 forbidden_terms_checked 字段（强烈推荐添加）")
fi

# 输出结果
echo "=== 交接文档校验: $FILE ==="
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
