#!/usr/bin/env bash
# ============================================================
# {{AGENT_DISPLAY_NAME}} — OpenClaw Deployment Script
# ============================================================
# Deploys the {{PLUGIN_NAME}} Claude plugin as an OpenClaw agent workspace.
#
# Usage:
#   bash openclaw-install.sh
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_HOME="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
WORKSPACE="$OPENCLAW_HOME/agents/{{PLUGIN_NAME}}"
PLUGIN_DIR="$SCRIPT_DIR/{{PLUGIN_NAME}}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log()  { echo -e "${GREEN}✅ $1${NC}"; }
info() { echo -e "${BLUE}📋 $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
err()  { echo -e "${RED}❌ $1${NC}"; }

echo ""
echo "============================================================"
echo "{{AGENT_EMOJI}} {{AGENT_DISPLAY_NAME}} — OpenClaw Deployment"
echo "============================================================"
echo ""

# --- Prereq checks ------------------------------------------
info "Checking prerequisites..."

if ! command -v openclaw &> /dev/null; then
    err "OpenClaw not found. Install: curl -fsSL https://openclaw.ai/install.sh | bash"
    exit 1
fi
log "OpenClaw: $(openclaw --version 2>/dev/null || echo 'installed')"

if [ ! -d "$PLUGIN_DIR" ]; then
    err "Plugin directory not found at $PLUGIN_DIR"
    err "Run this script from the repo root."
    exit 1
fi
log "Plugin source: $PLUGIN_DIR"

# --- Create workspace ---------------------------------------
info "Setting up workspace at $WORKSPACE..."

mkdir -p "$WORKSPACE/memory"
mkdir -p "$WORKSPACE/skills/{{SKILL_DOMAIN}}/agents"
mkdir -p "$WORKSPACE/data"

# --- Create SOUL.md ------------------------------------------
cat > "$WORKSPACE/SOUL.md" << 'SOUL_EOF'
{{SOUL_MD_CONTENT}}
SOUL_EOF

# --- Create AGENTS.md ----------------------------------------
cat > "$WORKSPACE/AGENTS.md" << 'AGENTS_EOF'
{{AGENTS_MD_CONTENT}}
AGENTS_EOF

# --- Create MEMORY.md ----------------------------------------
cat > "$WORKSPACE/MEMORY.md" << 'MEMORY_EOF'
{{MEMORY_MD_CONTENT}}
MEMORY_EOF

# --- Copy skills and agents ----------------------------------
info "Copying skills and agent prompts..."

{{COPY_COMMANDS}}

# --- Initial memory seed -------------------------------------
TODAY=$(date +%Y-%m-%d)
cat > "$WORKSPACE/memory/$TODAY.md" << EOF
# Memory — $TODAY

## Agent Initialized
- {{AGENT_DISPLAY_NAME}} deployed to OpenClaw
- Workspace: $WORKSPACE
- Ready for use

## Notes
- Claude plugin format adapted for OpenClaw single-context execution
- All agent perspectives run sequentially with mental isolation discipline
EOF

# --- Verify --------------------------------------------------
info "Verifying workspace..."

EXPECTED=(
    "SOUL.md"
    "AGENTS.md"
    "MEMORY.md"
{{EXPECTED_FILES}}
)

MISSING=0
for f in "${EXPECTED[@]}"; do
    if [ ! -f "$WORKSPACE/$f" ]; then
        err "Missing: $f"
        MISSING=$((MISSING + 1))
    fi
done

if [ "$MISSING" -eq 0 ]; then
    log "All ${#EXPECTED[@]} workspace files verified"
else
    err "$MISSING files missing!"
    exit 1
fi

# --- Done ----------------------------------------------------
echo ""
echo "============================================================"
echo "{{AGENT_EMOJI}} {{AGENT_DISPLAY_NAME}} — Installed to OpenClaw"
echo "============================================================"
echo ""
echo "Next steps:"
echo ""
echo "  1. Add the agent to your openclaw.json config:"
echo ""
echo '      {'
echo "        \"id\": \"{{PLUGIN_NAME}}\","
echo "        \"workspace\": \"$WORKSPACE\","
echo '        "model": {'
echo '          "primary": "anthropic/claude-opus-4-6",'
echo '          "fallbacks": ["anthropic/claude-sonnet-4-6"]'
echo '        }'
echo '      }'
echo ""
echo "  2. Test:"
echo "      openclaw agent --agent {{PLUGIN_NAME}} \\"
echo "        --message '{{TEST_MESSAGE}}'"
echo ""
echo "  3. Monitor logs:"
echo "      openclaw logs --agent {{PLUGIN_NAME}} --follow"
echo ""
echo "============================================================"
