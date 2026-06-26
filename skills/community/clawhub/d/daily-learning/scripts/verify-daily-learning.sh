#!/usr/bin/env bash
# verify-daily-learning.sh
# 检查 daily-learning 的三个产出是否都完成
# 1. 本地笔记: <workspace>/learning/notes/YYYY-MM-DD.md
# 2. Wiki 双写: <wiki-inbox>/YYYY-MM-DD_*_<agent-id>.md
# 3. 进度更新: <workspace>/learning/LEARNING.md 中对应主题标记为已学
#
# 用法: verify-daily-learning.sh <date> <agent-id> <workspace> <wiki-inbox-path>
# 例:   verify-daily-learning.sh 2026-05-13 learning-expert <your-workspace-path> <your-wiki-inbox-path>

set -euo pipefail

DATE="${1:?Usage: verify-daily-learning.sh <YYYY-MM-DD> <agent-id> <workspace> <wiki-inbox-path>}"
AGENT_ID="${2:?Missing agent-id}"
WORKSPACE="${3:?Missing workspace path}"
WIKI_INBOX="${4:?Missing wiki-inbox-path}"

PASS=0
FAIL=0

# ──────────────────────────────────────────────
# Check 1: 本地笔记
# ──────────────────────────────────────────────
NOTE_FILE="${WORKSPACE}/learning/notes/${DATE}.md"
if [ -f "$NOTE_FILE" ]; then
  SIZE=$(stat -f%z "$NOTE_FILE" 2>/dev/null || stat -c%s "$NOTE_FILE" 2>/dev/null || echo "?")
  if [ "$SIZE" -gt 50 ] 2>/dev/null; then
    echo "✅ [1/3] 本地笔记: ${NOTE_FILE} (${SIZE} bytes)"
    PASS=$((PASS + 1))
  else
    echo "❌ [1/3] 本地笔记: 文件存在但内容太少 (${SIZE} bytes)，疑似空壳: ${NOTE_FILE}"
    FAIL=$((FAIL + 1))
  fi
else
  echo "❌ [1/3] 本地笔记: 文件不存在: ${NOTE_FILE}"
  echo "   ACTION: 写笔记到 learning/notes/${DATE}.md"
  FAIL=$((FAIL + 1))
fi

# ──────────────────────────────────────────────
# Check 2: Wiki 双写
# ──────────────────────────────────────────────
if [ ! -d "$WIKI_INBOX" ]; then
  echo "❌ [2/3] Wiki 双写: inbox 目录不存在: $WIKI_INBOX"
  FAIL=$((FAIL + 1))
else
  PATTERN="${DATE}_*_${AGENT_ID}.md"
  MATCHES=$(find "$WIKI_INBOX" -name "$PATTERN" -type f 2>/dev/null || true)
  if [ -z "$MATCHES" ]; then
    echo "❌ [2/3] Wiki 双写: 未找到 ${DATE} 的 wiki 文件 (agent: ${AGENT_ID})"
    echo "   Expected: ${WIKI_INBOX}/${DATE}_<topic>_${AGENT_ID}.md"
    echo "   ACTION: 必须写 wiki 文件到 raw/inbox/"
    FAIL=$((FAIL + 1))
  else
    COUNT=$(echo "$MATCHES" | wc -l | tr -d ' ')
    echo "✅ [2/3] Wiki 双写: 找到 ${COUNT} 个文件"
    echo "$MATCHES" | while read -r f; do
      SIZE=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f" 2>/dev/null || echo "?")
      echo "   → $(basename "$f") (${SIZE} bytes)"
    done
    PASS=$((PASS + 1))
  fi
fi

# ──────────────────────────────────────────────
# Check 3: 进度更新 (LEARNING.md)
# ──────────────────────────────────────────────
LEARNING_MD="${WORKSPACE}/learning/LEARNING.md"
if [ ! -f "$LEARNING_MD" ]; then
  echo "❌ [3/3] 进度更新: LEARNING.md 不存在: ${LEARNING_MD}"
  echo "   ACTION: 用 references/learning-template.md 初始化"
  FAIL=$((FAIL + 1))
else
  # 检查 LEARNING.md 中是否有当天日期的标记（✅ 或已完成标记）
  if grep -q "${DATE}" "$LEARNING_MD" 2>/dev/null; then
    echo "✅ [3/3] 进度更新: LEARNING.md 中包含 ${DATE}"
    PASS=$((PASS + 1))
  else
    echo "❌ [3/3] 进度更新: LEARNING.md 中未找到 ${DATE} 的记录"
    echo "   ACTION: 更新 LEARNING.md，将今日主题标记为已学，记录日期"
    FAIL=$((FAIL + 1))
  fi
fi

# ──────────────────────────────────────────────
# Check 4: 四层结构质量检测
# ──────────────────────────────────────────────
echo ""
echo "── 四层结构质量检测 ──"

LAYER_PASS=0
LAYER_FAIL=0

# 检查本地笔记是否存在（前面已验证）
if [ -f "$NOTE_FILE" ]; then
  # 依据层：检查是否有具体数据/实验细节（数字 + 实验相关词）
  if grep -qiE '(\d{2,}|实验|研究|被试|参与者|样本|效应量|p[< =]|percentile|participants|sample|effect size)' "$NOTE_FILE"; then
    echo "✅ [依据层] 包含具体数据或实验描述"
    LAYER_PASS=$((LAYER_PASS + 1))
  else
    echo "❌ [依据层] 缺少具体数据或实验细节——只有结论没有证据"
    echo "   ACTION: 补充实验设计、样本量、关键数据或对比结果"
    LAYER_FAIL=$((LAYER_FAIL + 1))
  fi

  # 例子/案例层：检查是否有具体场景
  if grep -qiE '(例如|比如|举例|案例|场景|实例|e\.g\.|for example|such as|scenario|instance)' "$NOTE_FILE"; then
    echo "✅ [例子层] 包含具体案例或场景"
    LAYER_PASS=$((LAYER_PASS + 1))
  else
    echo "❌ [例子层] 缺少具体案例或场景——纯抽象描述"
    echo "   ACTION: 为核心概念补充真实场景、对话示例或行为对照"
    LAYER_FAIL=$((LAYER_FAIL + 1))
  fi

  # 边界层：检查是否有限制条件描述
  if grep -qiE '(不适用|前提|限制|条件|边界|例外|but|however|limitation|caveat|前提是|注意|风险|不.*适用)' "$NOTE_FILE"; then
    echo "✅ [边界层] 包含适用限制或边界条件"
    LAYER_PASS=$((LAYER_PASS + 1))
  else
    echo "⚠️  [边界层] 未检测到边界条件描述——建议补充适用限制"
    echo "   ACTION: 补充'什么情况下不适用'或'使用前提'"
    # 边界层为警告而非硬失败
  fi
fi

# ──────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results: ✅ ${PASS}/3 结构检查, 四层质量: ✅ ${LAYER_PASS} / ❌ ${LAYER_FAIL}"

if [ "$FAIL" -gt 0 ]; then
  echo "⛔ 未通过所有结构检查，必须补全缺失项后重新验证。"
  exit 1
elif [ "$LAYER_FAIL" -ge 2 ]; then
  echo "⚠️  结构完整但内容深度不足（依据层和例子层缺失），请补充后重新验证。"
  exit 1
else
  echo "🎉 全部通过，今日学习流程完整。"
  exit 0
fi
