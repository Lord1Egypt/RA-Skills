#!/usr/bin/env bash
# memory-orchestrator：任意 Agent 每轮结束时调用的实时统一闸门。
# 只读取指定 thread_id 的轮数和 token-usage 实测指标，不读取/记录无关会话正文；
# 纯本地，不上传网络。五项任一触发：轮数、累计 token、请求峰值、请求数、累计 input。
# 用法（在 Agent 规则中固化，每轮用户提问结束时执行一次）：
#   MEMORY_AGENT=claude bash <skill>/scripts/agent_hook.sh active_project=项目名 thread_id=对话框ID
#   bash <skill>/scripts/agent_hook.sh agent=claude active_project=项目名 thread_id=对话框ID
# 可用环境变量覆盖阈值：TURN_THRESHOLD / TURN_WARN_AT（默认 8 / 7）；
# TOKEN_THRESHOLD / TOKEN_WARN_AT（默认 150000 / 130000）；请求峰值/请求数/累计 input
# 默认 100000 / 120 / 8000000。可用 --dry-run 只判定不写 state。
set -u
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"
exec env \
  ${CODEX_MEMORY_STATE:+CODEX_MEMORY_STATE="$CODEX_MEMORY_STATE"} \
  ${MEMORY_AGENT:+MEMORY_AGENT="$MEMORY_AGENT"} \
  ${TURN_THRESHOLD:+TURN_THRESHOLD="$TURN_THRESHOLD"} \
  ${TURN_WARN_AT:+TURN_WARN_AT="$TURN_WARN_AT"} \
  ${TOKEN_THRESHOLD:+TOKEN_THRESHOLD="$TOKEN_THRESHOLD"} \
  ${TOKEN_WARN_AT:+TOKEN_WARN_AT="$TOKEN_WARN_AT"} \
  "$PYTHON" "$SKILL_DIR/scripts/memory_gate.py" "$@"
