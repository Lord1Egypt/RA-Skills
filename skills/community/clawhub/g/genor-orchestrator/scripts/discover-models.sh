#!/usr/bin/env bash
# scripts/discover-models.sh
# Discover available models from all configured providers.
# Usage: bash scripts/discover-models.sh [--json] [--providers openrouter,lmstudio]
#
# Probes each provider for available models and prints results.
# Does NOT write to models.json — that's done interactively during onboarding.
# Data stored in $ORCHESTRATOR_DATA_DIR (default: ../../orchestrator-data/ from skill root)

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="${ORCHESTRATOR_DATA_DIR:-$(dirname "$(dirname "$SKILL_DIR")")/orchestrator-data}"
OUTPUT_JSON=false
PROVIDER_FILTER=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) OUTPUT_JSON=true; shift ;;
    --providers) PROVIDER_FILTER="$2"; shift 2 ;;
    *) echo "Usage: $0 [--json] [--providers openrouter,lmstudio]"; exit 1 ;;
  esac
done

echo "🔍 Discovering models from all providers..."
echo ""

# Function to check LM Studio
check_lmstudio() {
  local name="$1"
  local url="$2"
  echo "  Checking $name at $url..."
  local result
  result=$(curl -s --max-time 5 "$url/v1/models" 2>/dev/null || echo '{"error":"unreachable"}')
  if echo "$result" | grep -q '"data"'; then
    echo "    ✅ $name is online"
    echo "$result" | grep -o '"id"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/"id"://;s/"//g;s/ //g' | while IFS= read -r model; do
      echo "    - $model"
    done
    return 0
  else
    echo "    ❌ $name is unreachable"
    return 1
  fi
}

# Check OpenRouter
echo "  Checking OpenRouter..."
OR_RESULT=$(curl -s --max-time 10 "https://openrouter.ai/api/v1/models" 2>/dev/null || echo '{"error":"unreachable"}')
if echo "$OR_RESULT" | grep -q '"data"'; then
  echo "    ✅ OpenRouter is online"
  OR_COUNT=$(echo "$OR_RESULT" | grep -o '"id"' | wc -l)
  echo "    ($OR_COUNT models available)"
else
  echo "    ⚠️  OpenRouter check failed (may be rate limited)"
  OR_COUNT=0
fi

# Check LM Studio
echo ""
echo "  Checking LM Studio..."
check_lmstudio "local" "http://127.0.0.1:1234" || true

# Check OpenCode
echo ""
echo "  Checking OpenCode..."
if command -v opencode &>/dev/null; then
  echo "    ✅ opencode CLI found"
else
  echo "    ⚠️  opencode CLI not found locally"
fi

echo ""
echo "✅ Discovery complete."
echo ""
echo "Models found: OpenRouter ($OR_COUNT available), LM Studio (local)"
echo ""
echo "To auto-populate the orchestrator catalog from OpenClaw config:"
echo "  python3 scripts/auto-populate-models.py"
echo ""
echo "This reads configured model entries from openclaw.json and merges"
echo "them into orchestrator-data/models.json (preserving manual ratings)."
echo "Runs automatically nightly at 03:00 via cron."