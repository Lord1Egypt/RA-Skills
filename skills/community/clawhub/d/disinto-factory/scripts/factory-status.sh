#!/usr/bin/env bash
# factory-status.sh — Quick status check for a running disinto factory
set -euo pipefail

FACTORY_ROOT="${1:-$(cd "$(dirname "$0")/../.." && pwd)}"
source "${FACTORY_ROOT}/.env" 2>/dev/null || { echo "No .env found at ${FACTORY_ROOT}"; exit 1; }

FORGE_URL="${FORGE_URL:-http://localhost:3000}"
REPO=$(grep '^repo ' "${FACTORY_ROOT}/projects/"*.toml 2>/dev/null | head -1 | sed 's/.*= *"//;s/"//')
[ -z "$REPO" ] && { echo "No project TOML found"; exit 1; }

echo "=== Stack ==="
docker ps --format "table {{.Names}}\t{{.Status}}" 2>/dev/null | grep disinto

echo ""
echo "=== Open Issues ==="
curl -sf "${FORGE_URL}/api/v1/repos/${REPO}/issues?state=open&limit=20" \
  -H "Authorization: token ${FORGE_TOKEN}" \
  | jq -r '.[] | "#\(.number) [\(.labels | map(.name) | join(","))] \(.title)"' 2>/dev/null || echo "(API error)"

echo ""
echo "=== Open PRs ==="
curl -sf "${FORGE_URL}/api/v1/repos/${REPO}/pulls?state=open&limit=10" \
  -H "Authorization: token ${FORGE_TOKEN}" \
  | jq -r '.[] | "PR #\(.number) [\(.head.ref)] \(.title)"' 2>/dev/null || echo "none"

echo ""
echo "=== Agent Activity ==="
docker exec disinto-agents-1 bash -c "tail -5 /home/agent/data/logs/dev/dev-agent.log 2>/dev/null" || echo "(no logs)"

echo ""
echo "=== Claude Running? ==="
docker exec disinto-agents-1 bash -c "
  found=false
  for f in /proc/[0-9]*/cmdline; do
    cmd=\$(tr '\0' ' ' < \"\$f\" 2>/dev/null)
    if echo \"\$cmd\" | grep -q 'claude.*-p'; then found=true; echo 'Yes — Claude is actively working'; break; fi
  done
  \$found || echo 'No — idle'
" 2>/dev/null

echo ""
echo "=== Mirrors ==="
cd "${FACTORY_ROOT}" 2>/dev/null && git remote -v | grep -E 'github|codeberg' | grep push || echo "none configured"
