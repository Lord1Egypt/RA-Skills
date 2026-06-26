#!/bin/bash
# auto-setup.sh — Full automated environment setup for OpenClaw Memory Hub
#
# This script configures OpenClaw's three-tier memory architecture:
# - L0: memory-core plugin with Ollama bge-m3 embedding + SQLite-vec
# - L1: working memory (daily markdown logs)
# - L2: long-term memory (MEMORY.md)
# - Dreaming pipeline for automatic insight promotion
#
# It only modifies files under ~/.openclaw/ — no system-level changes
# except Ollama installation (standard installer from ollama.com).
#
# Usage: bash auto-setup.sh
# Options:
#   --skip-ollama    Skip Ollama installation (use if already installed)
#   --skip-memos     Skip MemOS Cloud plugin setup
#   --dry-run        Print actions without executing
#   --help           Show this help

set -euo pipefail

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log()   { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; }
info()  { echo -e "${BLUE}[i]${NC} $1"; }

# --- Args ---
SKIP_OLLAMA=false
SKIP_MEMOS=false
DRY_RUN=false

for arg in "$@"; do
    case "$arg" in
        --skip-ollama) SKIP_OLLAMA=true ;;
        --skip-memos)  SKIP_MEMOS=true ;;
        --dry-run)     DRY_RUN=true ;;
        --help)        echo "Usage: bash auto-setup.sh [--skip-ollama] [--skip-memos] [--dry-run]"; exit 0 ;;
    esac
done

run() {
    if [ "$DRY_RUN" = true ]; then
        echo "  (dry-run) $*"
    else
        "$@"
    fi
}

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
OPENCLAW_JSON="$HOME/.openclaw/openclaw.json"
MEMORY_DIR="$WORKSPACE/memory"

echo "============================================"
echo "  OpenClaw Memory Hub — Auto Setup"
echo "============================================"
echo ""

# ===== Step 1: Install Ollama =====
echo "━━━ Step 1/8: Ollama ━━━"
if [ "$SKIP_OLLAMA" = true ]; then
    info "Skipping (--skip-ollama)"
elif command -v ollama &>/dev/null && curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    log "Ollama already running at http://127.0.0.1:11434"
else
    warn "Ollama not detected."
    echo "  Choose installation method:"
    echo "    1) Standard (ollama.com) — recommended for most users"
    echo "    2) Intel edition (OpenVINO backend) — for Intel CPU/GPU"
    echo "    s) Skip"

    if [ "$DRY_RUN" = false ]; then
        read -r -p "  Choose [1/2/s]: " choice
    else
        choice="1"
    fi

    case "$choice" in
        1)
            info "Installing standard Ollama..."
            run sh -c 'curl -fsSL https://ollama.com/install.sh -o /tmp/ollama-install.sh && sh /tmp/ollama-install.sh && rm -f /tmp/ollama-install.sh'
            run sudo systemctl start ollama 2>/dev/null || { warn "Could not start via systemctl (need sudo?). Trying ollama serve..."; run ollama serve & }
            log "Ollama installed"
            ;;
        2)
            info "Installing Intel Ollama..."
            INTEL_DIR="/opt/ollama-intel"
            warn "This requires sudo access to write to /opt and /usr/local/bin."
            run sudo mkdir -p "$INTEL_DIR"
            info "Downloading Intel Ollama from GitHub releases..."
            run sudo curl -L -o "$INTEL_DIR/ollama" "https://github.com/intel/ollama/releases/latest/download/ollama-linux-amd64"
            run sudo chmod +x "$INTEL_DIR/ollama"
            run sudo ln -sf "$INTEL_DIR/ollama" /usr/local/bin/ollama
            warn "Intel Ollama installed. Run: ollama serve"
            ;;
        s|S)
            warn "Skipping Ollama installation. Memory Hub requires Ollama to function."
            ;;
    esac
    sleep 2
fi
echo ""

# ===== Step 2: Pull bge-m3 model =====
echo "━━━ Step 2/8: Embedding Model (bge-m3) ━━━"
if command -v ollama &>/dev/null; then
    if ollama list 2>/dev/null | grep -q bge-m3; then
        log "bge-m3 model already downloaded"
    else
        info "Downloading bge-m3 model (~1.3GB, may take a few minutes)..."
        run ollama pull bge-m3
        log "bge-m3 model ready"
    fi
else
    error "Ollama not found. Install Ollama first."
fi
echo ""

# ===== Step 3: Check plugin conflicts =====
echo "━━━ Step 3/8: Plugin Conflict Check ━━━"
if [ -f "$OPENCLAW_JSON" ]; then
    # JSON-aware conflict check: look for active entry in plugins.entries
    if python3 -c "
import json, sys
with open('$OPENCLAW_JSON') as f:
    cfg = json.load(f)
entries = cfg.get('plugins', {}).get('entries', {})
if 'subconscious-personality-guardian' in entries:
    sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
        warn "\u26a0\ufe0f  CONFLICT DETECTED: subconscious-personality-guardian is active in plugins.entries!"
        echo ""
        echo "  Both plugins use the same memory slot. You must disable one of them."
        echo "  Recommended: keep memory-core, disable subconscious-personality-guardian."
        echo ""

        if [ "$DRY_RUN" = false ]; then
            read -r -p "  Auto-disable subconscious-personality-guardian? [Y/n]: " disable_guardian
            if [ "$disable_guardian" != "n" ] && [ "$disable_guardian" != "N" ]; then
                run env OPENCLAW_JSON="$OPENCLAW_JSON" python3 -c "
import json
import os
path = os.environ['OPENCLAW_JSON']
with open(path) as f:
    cfg = json.load(f)
# Remove from entries first
entries = cfg.setdefault('plugins', {}).setdefault('entries', {})
entries.pop('subconscious-personality-guardian', None)
# Add to disabled list
plugins = cfg.setdefault('plugins', {})
disabled = plugins.setdefault('disabled', [])
if 'subconscious-personality-guardian' not in disabled:
    disabled.append('subconscious-personality-guardian')
# Also add to deny list to prevent re-install
deny = plugins.setdefault('deny', [])
if 'subconscious-personality-guardian' not in deny:
    deny.append('subconscious-personality-guardian')
with open(path, 'w') as f:
    json.dump(cfg, f, indent=2)
"
                log "subconscious-personality-guardian disabled"
            else
                warn "Manual action required: disable the conflicting plugin before using memory-core"
            fi
        fi
    else
        log "No plugin conflicts detected"
    fi
fi
echo ""

# ===== Step 4: Install memory-core plugin =====
echo "━━━ Step 4/8: memory-core Plugin ━━━"
if command -v openclaw &>/dev/null; then
    # Check if plugin is already loaded
    if openclaw plugins list 2>/dev/null | grep -q memory-core; then
        log "memory-core plugin already loaded"
    else
        info "Add memory-core to openclaw.json (handled in Step 5)"
    fi
else
    error "openclaw CLI not found in PATH"
fi
echo ""

# ===== Step 5: Configure openclaw.json =====
echo "━━━ Step 5/8: Configuration (openclaw.json) ━━━"
if [ -f "$OPENCLAW_JSON" ]; then
    # JSON-aware check: memory-core in plugins.entries
    if python3 -c "
import json, sys
with open('$OPENCLAW_JSON') as f:
    cfg = json.load(f)
if 'memory-core' in cfg.get('plugins', {}).get('entries', {}):
    sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
        log "memory-core already configured in openclaw.json"
    else
        warn "memory-core not found in openclaw.json"
        info "Add the following to plugins.entries in your openclaw.json:"
        echo ""
        echo '  "memory-core": {'
        echo '    "config": {'
        echo '      "embeddingUrl": "http://127.0.0.1:11434/api/embed",'
        echo '      "embeddingModel": "bge-m3",'
        echo '      "dimension": 1024'
        echo '    }'
        echo '  }'
        echo ""
        echo "  Path: $OPENCLAW_JSON"
        echo ""

        if [ "$DRY_RUN" = false ]; then
            read -r -p "  Auto-insert into openclaw.json? [y/N]: " auto_insert
            if [ "$auto_insert" = "y" ] || [ "$auto_insert" = "Y" ]; then
                # Insertion via env var for injection safety
                run env OPENCLAW_JSON="$OPENCLAW_JSON" python3 -c "
import json
import os
path = os.environ['OPENCLAW_JSON']
with open(path) as f:
    cfg = json.load(f)
plugins = cfg.setdefault('plugins', {})
entries = plugins.setdefault('entries', {})
entries['memory-core'] = {
    'config': {
        'embeddingUrl': 'http://127.0.0.1:11434/api/embed',
        'embeddingModel': 'bge-m3',
        'dimension': 1024
    }
}
with open(path, 'w') as f:
    json.dump(cfg, f, indent=2)
"
                log "memory-core configuration inserted"
            fi
        fi
    fi
else
    warn "openclaw.json not found at $OPENCLAW_JSON"
fi
echo ""

# ===== Step 6: MemOS Cloud Plugin (optional) =====
echo "━━━ Step 6/8: MemOS Cloud Plugin (Optional) ━━━"
if [ "$SKIP_MEMOS" = true ]; then
    info "Skipping (--skip-memos)"
elif [ "$DRY_RUN" = true ]; then
    info "Skipping MemOS Cloud config (dry-run — use without --dry-run to configure)"
else
    read -r -p "  Install MemOS Cloud plugin for cross-device sync? [y/N]: " install_memos
    if [ "$install_memos" = "y" ] || [ "$install_memos" = "Y" ]; then
        echo ""
        echo "  MemOS Cloud requires a running MemOS server instance."
        echo "  Configuration parameters:"
        read -r -p "    Server URL (e.g. https://memos.example.com): " memos_url
        read -r -p "    API Token: " memos_token

        info "MemOS Cloud plugin will be configured in openclaw.json (no separate install needed)"

        run env MEMOS_URL="$memos_url" MEMOS_TOKEN="$memos_token" OPENCLAW_JSON="$OPENCLAW_JSON" python3 -c "
import json
import os
path = os.environ['OPENCLAW_JSON']
with open(path) as f:
    cfg = json.load(f)
entries = cfg.setdefault('plugins', {}).setdefault('entries', {})
entries['memos-cloud-openclaw-plugin'] = {
    'enabled': True,
    'config': {
        'url': os.environ['MEMOS_URL'],
        'token': os.environ['MEMOS_TOKEN'],
        'resetOnNew': True,
        'recallEnabled': True,
        'recallFilterFailOpen': True,
        'asyncMode': True,
        'addEnabled': True,
        'queryPrefix': 'important user context preferences decisions ',
        'memoryLimitNumber': 9,
        'preferenceLimitNumber': 6,
        'relativity': 0.45,
        'maxItemChars': 8000,
        'includeAssistant': True,
        'includePreference': True,
        'tags': ['openclaw', 'memory']
    },
    'hooks': {
        'allowConversationAccess': True
    }
}
with open(path, 'w') as f:
    json.dump(cfg, f, indent=2)
"
        log "MemOS Cloud plugin configured"
    else
        info "Skipping MemOS Cloud"
    fi
fi
echo ""

# ===== Step 7: Create memory directory & template files =====
echo "━━━ Step 7/8: Memory Files ━━━"
run mkdir -p "$MEMORY_DIR"
log "Memory directory: $MEMORY_DIR"

# Create template AGENTS.md memory section
AGENTS_FILE="$WORKSPACE/AGENTS.md"
if [ -f "$AGENTS_FILE" ]; then
    if ! grep -q "memory-core" "$AGENTS_FILE" 2>/dev/null; then
        warn "AGENTS.md exists but may not include memory rules"
        info "Add memory system rules to AGENTS.md (see references/setup-guide.md)"
    else
        log "AGENTS.md already has memory configuration"
    fi
else
    info "AGENTS.md not found — memory rules will be loaded from SKILL.md"
fi
echo ""

# ===== Step 8: Set up cron jobs =====
echo "━━━ Step 8/8: Cron Jobs ━━━"
if command -v openclaw &>/dev/null; then
    # Dreaming pipeline — exact name match
    if openclaw cron list 2>/dev/null | grep -q "memory-dreaming-pipeline"; then
        log "Dreaming cron 'memory-dreaming-pipeline' already exists"
    else
        run openclaw cron add \
            --name "memory-dreaming-pipeline" \
            --cron "0 3 * * *" \
            --agent "default" \
            --announce \
            --message "Run Dreaming pipeline: scan session logs, extract insights via DeepSeek analysis, promote high-scoring candidates" \
            --expect-final || warn "Could not create Dreaming cron (run manually: openclaw cron add --cron '0 3 * * *' --agent default --announce --expect-final)"
        log "Dreaming cron created (03:00 UTC daily)"
    fi
else
    warn "openclaw CLI not found — set up crons manually"
fi
echo ""

# ===== Done =====
echo "============================================"
echo -e "${GREEN}  OpenClaw Memory Hub — Setup Complete${NC}"
echo "============================================"
echo ""
echo "  Next steps:"
echo "    1. Restart Gateway:    openclaw gateway restart"
echo "    2. Verify memory:      openclaw memory status"
echo "    3. Force index:        openclaw memory index --force"
echo "    4. Check cron:         openclaw cron list"
echo ""
echo "  Docs: references/setup-guide.md"
echo "  Repo: https://github.com/VictorQR/anamnesis-hub"
