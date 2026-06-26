#!/usr/bin/env bash
# run-del.sh — agent-del 唯一入口（Agent 只需 find 本文件并 bash 执行）
# 用法: run-del.sh <agentId1> [agentId2] ...
# 内部转调 agent-del.sh，无需 Agent 再拼 SKILL_DIR

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec bash "$SCRIPT_DIR/agent-del.sh" "$@"
