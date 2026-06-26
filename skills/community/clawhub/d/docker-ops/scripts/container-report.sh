#!/bin/bash
# Quick container report script
# Usage: ./container-report.sh <container_name> [since_period]
# Example: ./container-report.sh techbot_uuidgen 1h
#
# Requires: SYSCTL_WHITELIST_PATH env var pointing to the whitelist YAML file

set -euo pipefail

NAME="${1:?Usage: $0 <container_name> [since_period]}"
SINCE="${2:-1h}"

# --- Validate SYSCTL_WHITELIST_PATH ---
if [ -z "${SYSCTL_WHITELIST_PATH:-}" ]; then
    echo "ERROR: SYSCTL_WHITELIST_PATH is not set. Cannot proceed without whitelist." >&2
    exit 1
fi

if [ ! -f "${SYSCTL_WHITELIST_PATH}" ]; then
    echo "ERROR: Whitelist file not found: ${SYSCTL_WHITELIST_PATH}" >&2
    exit 1
fi

# --- Validate container name against whitelist ---
# Extract container names from YAML (lines matching "- name: <value>")
ALLOWED=$(grep -oP '^\s*-\s*name:\s*\K\S+' "${SYSCTL_WHITELIST_PATH}" || true)

FOUND=0
for ALLOWED_NAME in ${ALLOWED}; do
    if [ "${ALLOWED_NAME}" = "${NAME}" ]; then
        FOUND=1
        break
    fi
done

if [ "${FOUND}" -ne 1 ]; then
    echo "ERROR: Container '${NAME}' is not in the whitelist. Allowed: ${ALLOWED//$'\n'/, }" >&2
    exit 1
fi

# --- Validate SINCE format (digits + time suffix) ---
if ! [[ "${SINCE}" =~ ^[0-9]+(s|m|h)$ ]]; then
    echo "ERROR: Invalid time period '${SINCE}'. Expected format: <number>(s|m|h), e.g. 1h, 30m, 60s" >&2
    exit 1
fi

# --- Cap period at 168h (7 days) ---
SINCE_VALUE="${SINCE%[smh]}"
SINCE_UNIT="${SINCE: -1}"
case "${SINCE_UNIT}" in
    s) SINCE_SECONDS="${SINCE_VALUE}" ;;
    m) SINCE_SECONDS=$((SINCE_VALUE * 60)) ;;
    h) SINCE_SECONDS=$((SINCE_VALUE * 3600)) ;;
esac
MAX_SECONDS=$((168 * 3600))  # 7 days
if [ "${SINCE_SECONDS}" -gt "${MAX_SECONDS}" ]; then
    echo "WARNING: Period ${SINCE} exceeds 7-day limit. Capping to 168h." >&2
    SINCE="168h"
fi

echo "=== Container: ${NAME} ==="
echo ""

# Status
echo "--- STATUS ---"
timeout 30 docker inspect "${NAME}" 2>/dev/null | jq -r '.[0] | "Status: \(.State.Status)\nStartedAt: \(.State.StartedAt)\nRestartCount: \(.RestartCount)\nOOMKilled: \(.State.OOMKilled)\nExitCode: \(.State.ExitCode)\nHealth: \(.State.Health.Status // "n/a")"' || echo "ERROR: Container not found or docker-socket-proxy timeout"

echo ""

# Resources
echo "--- RESOURCES ---"
timeout 30 docker stats --no-stream --format 'CPU: {{.CPUPerc}} | RAM: {{.MemUsage}} ({{.MemPerc}}) | NET: {{.NetIO}} | BLOCK: {{.BlockIO}} | PIDs: {{.PIDs}}' "${NAME}" 2>/dev/null || echo "ERROR: Cannot get stats (container may be stopped or proxy timeout)"

echo ""

# Log stats — single fetch with --tail limit, then count locally
echo "--- LOG ANALYSIS (since ${SINCE}) ---"
LOG_CACHE=$(timeout 30 docker logs --since "${SINCE}" --tail 5000 "${NAME}" 2>&1 || true)
ERRORS=$(echo "${LOG_CACHE}" | grep -ci 'error\|exception\|fatal\|traceback' || true)
WARNINGS=$(echo "${LOG_CACHE}" | grep -ci 'warn' || true)
echo "Errors: ${ERRORS}"
echo "Warnings: ${WARNINGS}"

if [ "${ERRORS}" -gt 0 ]; then
    echo ""
    echo "--- LAST ERRORS ---"
    echo "${LOG_CACHE}" | grep -i 'error\|exception\|fatal\|traceback' | sort -u | tail -10
fi
