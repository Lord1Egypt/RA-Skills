#!/usr/bin/env bash
set -euo pipefail

HOME_DIR="${HOME}"
SKILL_DIR="${HOME_DIR}/.openclaw/skills/douyin-upload-mcp-skill"
XIAOICE_DIR="${HOME_DIR}/自动营销/xiaoice-video-tool"
STATE_DIR="${DOUYIN_MONITOR_STATE_DIR:-${HOME_DIR}/.openclaw/workspace/douyin-ops}"
BROWSER_DIR="${BROWSER_USER_DATA_DIR:-${HOME_DIR}/.wjz_browser_data}"

if [ ! -f "${SKILL_DIR}/SKILL.md" ]; then
  echo "missing skill: ${SKILL_DIR}" >&2
  exit 1
fi

mkdir -p "${STATE_DIR}/logs" "${STATE_DIR}/output" "${BROWSER_DIR}" "${HOME_DIR}/.openclaw"

export DOUYIN_MONITOR_STATE_DIR="${STATE_DIR}"
export BROWSER_USER_DATA_DIR="${BROWSER_DIR}"
export BROWSER_DEBUG_PORT="${BROWSER_DEBUG_PORT:-19800}"
export BROWSER_PROTOCOL_TIMEOUT="${BROWSER_PROTOCOL_TIMEOUT:-1200000}"
export DAEMON_PORT="${DAEMON_PORT:-41225}"
export DOUYIN_USE_XVFB="${DOUYIN_USE_XVFB:-true}"
export XIAOICE_VIDEO_TOOL_DIR="${XIAOICE_VIDEO_TOOL_DIR:-${XIAOICE_DIR}}"
export XIAOICE_VIDEO_ENV_PATH="${XIAOICE_VIDEO_ENV_PATH:-${XIAOICE_DIR}/.env}"

cd "${SKILL_DIR}"

node scripts/bootstrap-openclaw.js --apply --no-restart-openclaw-gateway || true
node scripts/start-lab-daemon.js || true
node scripts/openclaw-douyin-health.js --fix --restart-gateway || true
node scripts/preflight.js --online || true
node scripts/agent-ready.js || true
node scripts/douyin-schedule-manager.js status || true

cat <<'MSG'
OpenClaw Douyin template first run finished.
Next steps in Feishu:
1. 绑定当前会话
2. 发布抖音
MSG
