#!/bin/zsh
set -euo pipefail

export PATH="/opt/homebrew/bin:/opt/homebrew/opt/node/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

SKILL_DIR="${HOME}/.openclaw/workspace/skills/claw-ecosystem-monitor"
LOG_DIR="${HOME}/.openclaw/logs"

mkdir -p "${LOG_DIR}"
cd "${SKILL_DIR}"

{
  echo "== $(date -u '+%Y-%m-%dT%H:%M:%SZ') openclaw ecosystem monitor =="
  node scripts/collect-openclaw-ecosystem.mjs
  node scripts/render-demo-report.mjs
  echo "== complete =="
} >> "${LOG_DIR}/earn-money-openclaw-monitor.log" 2>&1
