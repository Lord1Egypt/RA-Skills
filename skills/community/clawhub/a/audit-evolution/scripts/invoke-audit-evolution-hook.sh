#!/usr/bin/env bash
set -euo pipefail

EVENT_TYPE="manual"
WORKSPACE_PATH="$(pwd)"
SUMMARY=""
FILES_READ="0"
CONTEXT_PERCENT="0"
EVIDENCE_PATH=""
USER_FEEDBACK=""
NO_WRITE="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --event|--event-type)
      EVENT_TYPE="${2:-manual}"
      shift 2
      ;;
    --workspace)
      WORKSPACE_PATH="${2:-$(pwd)}"
      shift 2
      ;;
    --summary)
      SUMMARY="${2:-}"
      shift 2
      ;;
    --files-read)
      FILES_READ="${2:-0}"
      shift 2
      ;;
    --context-percent)
      CONTEXT_PERCENT="${2:-0}"
      shift 2
      ;;
    --evidence)
      EVIDENCE_PATH="${2:-}"
      shift 2
      ;;
    --user-feedback)
      USER_FEEDBACK="${2:-}"
      shift 2
      ;;
    --no-write)
      NO_WRITE="true"
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

case "$EVENT_TYPE" in
  manual|benchmark_completed|user_corrected_agent|task_failed_or_timeout_or_retry|context_over_60_percent|more_than_5_files_read|uncertainty_language_detected|skill_config_or_gear_changed)
    ;;
  *)
    echo "Unsupported event type: $EVENT_TYPE" >&2
    exit 2
    ;;
esac

WORKSPACE_PATH="$(cd "$WORKSPACE_PATH" && pwd)"
HOOK_ROOT="$WORKSPACE_PATH/.audit-evolution"
RUN_DIR="$HOOK_ROOT/run-records"
STAMP="$(date +"%Y%m%d_%H%M%S")"
RECORD_PATH="$RUN_DIR/run_${STAMP}_${EVENT_TYPE}.md"
LATEST_PATH="$RUN_DIR/latest.md"
CREATED_AT="$(date +"%Y-%m-%dT%H:%M:%S")"

if [[ -z "$SUMMARY" ]]; then
  SUMMARY="No summary provided. Agent should inspect current context and allowed files."
fi

if [[ -z "$EVIDENCE_PATH" ]]; then
  EVIDENCE_PATH="unknown"
fi

if [[ -z "$USER_FEEDBACK" ]]; then
  USER_FEEDBACK="none"
fi

read -r -d '' RECORD <<EOF || true
---
type: audit_evolution_run_record
protocol: SACP/0.1
event_type: $EVENT_TYPE
created_at: $CREATED_AT
workspace: "$WORKSPACE_PATH"
files_read: $FILES_READ
context_percent: $CONTEXT_PERCENT
evidence_path: "$EVIDENCE_PATH"
status: audit_needed
---

# Audit Evolution Run Record

## Event

$EVENT_TYPE

## What Happened

$SUMMARY

## Evidence Candidate

$EVIDENCE_PATH

## User Feedback

$USER_FEEDBACK

## Required Agent Action

\`\`\`text
开始调用 Audit Evolution。

请优先读取这个 run record，并在当前上下文和允许访问的文件里寻找最近任务记录、用户反馈、失败/超时/重试记录、benchmark 或评测结果、worklog、handoff、receipt、最近修改过的 skill/config/gear。

必须输出：
1. Evidence Pack
2. Snapshot
3. Evolution Card
4. Memory Ledger Entry
5. Minimal Skill Patch Proposal
6. Field Note
7. Next-Run Bootstrap
8. Short Command Menu

边界：
- 最多读取 5 个最相关文件。
- 没有 evidence 不许声明 completed。
- 未经批准不得 publish/upload/install/vote/comment/message/spend/official benchmark。
- 如果不知道 Memory Ledger 写到哪里，write_target 使用 proposed_only。
\`\`\`

## Short Command Menu

\`\`\`text
你可以直接回复：
进化 / 保存 / 暂停 / 跑分 / 继续 / 详情
\`\`\`
EOF

if [[ "$NO_WRITE" != "true" ]]; then
  mkdir -p "$RUN_DIR"
  printf "%s\n" "$RECORD" > "$RECORD_PATH"
  printf "%s\n" "$RECORD" > "$LATEST_PATH"
fi

cat <<JSON
{
  "event_type": "$EVENT_TYPE",
  "workspace": "$WORKSPACE_PATH",
  "record_path": "$([[ "$NO_WRITE" == "true" ]] && echo "not_written" || echo "$RECORD_PATH")",
  "latest_path": "$([[ "$NO_WRITE" == "true" ]] && echo "not_written" || echo "$LATEST_PATH")",
  "next_prompt": "开始调用 Audit Evolution。请优先读取 .audit-evolution/run-records/latest.md。"
}
JSON
