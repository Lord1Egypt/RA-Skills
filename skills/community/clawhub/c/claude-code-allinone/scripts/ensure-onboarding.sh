#!/usr/bin/env bash
# ensure-onboarding.sh — 确保 ~/.claude.json 标记 onboarding 已完成
#
# Claude Code CLI 在非交互模式 (-p) 下,如果 ~/.claude.json 中
# hasCompletedOnboarding 不为 true,会直接报错退出:
#   "Onboarding has not been completed"
#
# 本脚本幂等地把这个字段设成 true,不动任何其他字段。

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/helpers.sh"

cc_ensure_onboarding_completed
cc_log "✅ ~/.claude.json: hasCompletedOnboarding=true"
