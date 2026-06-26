#!/usr/bin/env bash
# Main entry point: check env → auto-fix → install script → run
# Usage: run_tunnel.sh [start|stop|status] --port <PORT> [other args]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROJECT_DIR="$(pwd)"
TUNNEL_ARGS=("$@")

# ── Step 1: ensure project-tunnel.sh is in the project ──────────────────────
ASSET="${SKILL_ROOT}/assets/project-tunnel.sh"
TARGET="${PROJECT_DIR}/project-tunnel.sh"
if [[ ! -f "${TARGET}" ]] || ! diff -q "${ASSET}" "${TARGET}" >/dev/null 2>&1; then
  cp "${ASSET}" "${TARGET}"
  chmod +x "${TARGET}"
  echo "[tunnel] installed/updated project-tunnel.sh"
fi

# ── Step 2: check environment ────────────────────────────────────────────────
ENV_CHECK="$("${SCRIPT_DIR}/check_env.sh" 2>&1)" || true
if echo "${ENV_CHECK}" | grep -q "❌"; then
  MISSING_TOOLS="$(echo "${ENV_CHECK}" | sed 's/.*missing: //')"
  echo "[tunnel] missing tools: ${MISSING_TOOLS}"
  echo "[tunnel] attempting auto-fix..."
  # shellcheck disable=SC2086
  "${SCRIPT_DIR}/fix_env.sh" ${MISSING_TOOLS}
  # Re-check after fix
  if ! "${SCRIPT_DIR}/check_env.sh" >/dev/null 2>&1; then
    echo "❌ auto-fix failed. Please install the missing tools manually." >&2
    echo "   Run: ${SCRIPT_DIR}/check_env.sh  to see what's missing" >&2
    exit 1
  fi
  echo "[tunnel] ✅ environment ready after auto-fix"
else
  echo "[tunnel] ✅ environment OK"
fi

# ── Step 3: run ──────────────────────────────────────────────────────────────
exec sh "${TARGET}" "${TUNNEL_ARGS[@]}"
