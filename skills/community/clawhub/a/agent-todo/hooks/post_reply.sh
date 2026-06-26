#!/usr/bin/env bash
# post_reply.sh - Hook: convert reply commitments into executable tasks

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

REPLY_CONTENT="${REPLY_CONTENT:-${1:-}}"
FORUM_TOPIC_ID="${FORUM_TOPIC_ID:-}"
REPLY_ID="${REPLY_ID:-}"
REPLY_AUTHOR="${REPLY_AUTHOR:-unknown}"
REPLY_AUTHOR_AGENT_ID="${REPLY_AUTHOR_AGENT_ID:-}"

if [[ -z "$REPLY_CONTENT" ]]; then
  echo "post_reply hook: no content provided, skipping"
  exit 0
fi

TODO_PATTERNS=(
  "我会"
  "我来"
  "负责"
  "后续我来"
  "稍后我来"
  "我去处理"
  "我去做"
  "今天我来"
  "明天我来"
  "TODO"
  "\[TODO\]"
)

matched_pattern=""
for pattern in "${TODO_PATTERNS[@]}"; do
  if echo "$REPLY_CONTENT" | grep -iqE "$pattern"; then
    matched_pattern="$pattern"
    break
  fi
done

if [[ -z "$matched_pattern" ]]; then
  echo "post_reply hook: no executable commitment detected, skipping"
  exit 0
fi

infer_task_type() {
  local text="$1"
  if echo "$text" | grep -qiE '代码|修复|实现|开发|重构|脚本|bug|接口|deploy|发布'; then
    echo "coding"
  elif echo "$text" | grep -qiE '文档|README|说明|整理|总结|方案|spec|设计'; then
    echo "doc"
  elif echo "$text" | grep -qiE '查|调研|搜索|research|分析|排查'; then
    echo "research"
  elif echo "$text" | grep -qiE '回复|回帖|同步|汇报|通知'; then
    echo "reply"
  elif echo "$text" | grep -qiE 'review|审查|review comment|检查'; then
    echo "review"
  elif echo "$text" | grep -qiE '发布|发版|push|tag|clawhub|github'; then
    echo "publish"
  else
    echo "general"
  fi
}

infer_deadline() {
  local text="$1"
  if echo "$text" | grep -q '今天\|今晚'; then
    echo '今天 23:59'
  elif echo "$text" | grep -q '明天\|明早'; then
    echo '明天 18:00'
  elif echo "$text" | grep -q '这周\|本周\|周末'; then
    echo '本周日 23:59'
  else
    echo ''
  fi
}

extract_title() {
  local text="$1"
  echo "$text" | sed '/^[[:space:]]*$/d' | head -1 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | sed 's/^【[^】]*】//' | cut -c1-100
}

build_next_action() {
  local title="$1"
  local topic_id="$2"
  printf 'Complete the promised follow-up: %s. When finished, reply back to forum topic #%s.' "$title" "${topic_id:-0}"
}

build_success_criteria() {
  local title="$1"
  local topic_id="$2"
  printf 'The promised work "%s" is completed and a result update is posted back to forum topic #%s.' "$title" "${topic_id:-0}"
}

title=$(extract_title "$REPLY_CONTENT")
title="${title//|/∙}"
title="${title//$'\n'/ }"
task_type=$(infer_task_type "$REPLY_CONTENT")
deadline=$(infer_deadline "$REPLY_CONTENT")
next_action=$(build_next_action "$title" "$FORUM_TOPIC_ID")
success_criteria=$(build_success_criteria "$title" "$FORUM_TOPIC_ID")
source="forum:#${FORUM_TOPIC_ID:-0}/reply:${REPLY_ID:-0}"

tasks_file="${AGENT_TODO_WORKSPACE:-${SKILL_DIR}/../..}/.agent-todo/tasks.json"
if [[ -f "$tasks_file" ]] && grep -Fq "$source" "$tasks_file"; then
  echo "post_reply hook: dedup skip - source already queued"
  exit 0
fi

echo "post_reply hook: executable commitment detected"
echo "  pattern: $matched_pattern"
echo "  topic: #${FORUM_TOPIC_ID:-0}"
echo "  author: ${REPLY_AUTHOR}"
echo "  type: ${task_type}"
echo "  title: ${title}"

add_args=(
  --task-type "$task_type"
  --source "$source"
  --next-action "$next_action"
  --success-criteria "$success_criteria"
)

if [[ -n "$deadline" ]]; then
  add_args+=(--deadline "$deadline")
fi

if [[ -n "$REPLY_AUTHOR_AGENT_ID" ]]; then
  cmd=(dispatch "$title" --to-agent "$REPLY_AUTHOR_AGENT_ID" "${add_args[@]}")
else
  cmd=(add "$title" "${add_args[@]}")
fi

if result=$("${SKILL_DIR}/script.sh" "${cmd[@]}" 2>&1); then
  echo "post_reply hook: task queued successfully"
  echo "$result"
else
  echo "post_reply hook: task queue failed" >&2
  echo "$result" >&2
  exit 1
fi
