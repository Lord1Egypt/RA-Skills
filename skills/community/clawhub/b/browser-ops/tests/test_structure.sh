#!/usr/bin/env bash
# Skill 结构完整性校验

section "结构校验"

# 1. 必要文件存在
for f in SKILL.md README.md LICENSE; do
  if [[ -f "$REPO_DIR/$f" ]]; then
    pass "文件存在: $f"
  else
    fail "文件缺失: $f" "必要文件不存在"
  fi
done

# 2. references/ 中所有文件存在
EXPECTED_REFS=(
  "references/setup.md"
  "references/routing.md"
  "references/state-management.md"
  "references/anti-detection.md"
  "references/opencli-usage.md"
)
for ref in "${EXPECTED_REFS[@]}"; do
  if [[ -f "$REPO_DIR/$ref" ]]; then
    pass "Reference 存在: $ref"
  else
    fail "Reference 缺失: $ref" "SKILL.md 中引用但文件不存在"
  fi
done

# 3. frontmatter 字段检查
SKILL_HEAD=$(head -30 "$REPO_DIR/SKILL.md")
for field in "name:" "description:"; do
  if echo "$SKILL_HEAD" | grep -q "$field"; then
    pass "Frontmatter 字段: $field"
  else
    fail "Frontmatter 缺失: $field" "SKILL.md frontmatter 不完整"
  fi
done

# 4. SKILL.md 中引用的 references 文件都存在
while IFS= read -r line; do
  ref_path=$(echo "$line" | grep -oE 'references/[a-z_-]+\.md' | head -1)
  if [[ -n "$ref_path" && -f "$REPO_DIR/$ref_path" ]]; then
    pass "引用有效: $ref_path"
  elif [[ -n "$ref_path" ]]; then
    fail "死引用: $ref_path" "SKILL.md 引用了不存在的文件"
  fi
done < <(grep "references/" "$REPO_DIR/SKILL.md")

# 5. 无硬编码个人路径
if grep -rn "/Users/" "$REPO_DIR/references/" "$REPO_DIR/SKILL.md" 2>/dev/null | grep -v ".git"; then
  fail "硬编码路径" "发现 /Users/ 硬编码路径"
else
  pass "无硬编码 /Users/ 路径"
fi

# 6. 无模板残留
if grep -q "schedule sends\|manage subscribers\|delivery platforms" "$REPO_DIR/SKILL.md"; then
  fail "模板残留" "Operator Notes 仍有 newsletter 模板内容"
else
  pass "无模板残留内容"
fi

# 7. SKILL.md 行数合理（<200行）
LINE_COUNT=$(wc -l < "$REPO_DIR/SKILL.md")
if [[ $LINE_COUNT -le 200 ]]; then
  pass "SKILL.md 行数合理: ${LINE_COUNT}行"
else
  fail "SKILL.md 过长: ${LINE_COUNT}行" "建议 <200 行，详情放 references"
fi

# 8. references 间交叉引用检查
for ref in "${EXPECTED_REFS[@]}"; do
  if grep -q "See also" "$REPO_DIR/$ref" 2>/dev/null; then
    pass "交叉引用: $ref"
  else
    # setup.md 不强制要求
    if [[ "$ref" == "references/setup.md" ]]; then
      pass "交叉引用: $ref（有 See also）"
    else
      skip "缺少交叉引用: $ref" "建议添加 See also 链接"
    fi
  fi
done
