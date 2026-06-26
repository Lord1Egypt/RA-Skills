#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# BotMark Skill — One-command setup for OpenClaw
#
# Usage:
#   curl -fsSL https://botmark.cc/skill/setup.sh | bash
#   # or after manual download:
#   bash botmark-skill/setup.sh
#
# What it does:
#   1. Detects OpenClaw installation & workspace path
#   2. Copies skill files to the correct directory
#   3. Prompts for API Key (if not already configured)
#   4. Writes API Key to openclaw.json (OpenClaw native config)
#   5. Creates .botmark_env fallback for environments without openclaw.json
#   6. Verifies installation
# ──────────────────────────────────────────────────────────────
set -euo pipefail

# ── Colors ──
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

info()  { echo -e "${CYAN}ℹ${NC} $*"; }
ok()    { echo -e "${GREEN}✓${NC} $*"; }
warn()  { echo -e "${YELLOW}⚠${NC} $*"; }
fail()  { echo -e "${RED}✗${NC} $*"; exit 1; }

# ── Step 0: Detect OpenClaw ──
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
OPENCLAW_CONFIG="$OPENCLAW_HOME/openclaw.json"

if [ ! -d "$OPENCLAW_HOME" ]; then
    fail "OpenClaw not found at $OPENCLAW_HOME. Is OpenClaw installed?"
fi
ok "OpenClaw detected at $OPENCLAW_HOME"

# ── Step 1: Determine skill install path ──
# Priority: workspace/skills (highest) > managed skills
SKILL_DIR=""
WORKSPACE_SKILLS="$OPENCLAW_HOME/workspace/skills/botmark-skill"
MANAGED_SKILLS="$OPENCLAW_HOME/skills/botmark-skill"

if [ -d "$OPENCLAW_HOME/workspace/skills" ]; then
    SKILL_DIR="$WORKSPACE_SKILLS"
    info "Will install to workspace skills (highest priority)"
elif [ -d "$OPENCLAW_HOME/skills" ]; then
    SKILL_DIR="$MANAGED_SKILLS"
    info "Will install to managed skills"
else
    # Create workspace/skills if neither exists
    mkdir -p "$OPENCLAW_HOME/workspace/skills"
    SKILL_DIR="$WORKSPACE_SKILLS"
    info "Created workspace skills directory"
fi

# ── Step 2: Copy skill files ──
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if we're running from the botmark-skill directory
if [ -f "$SCRIPT_DIR/SKILL.md" ]; then
    SOURCE_DIR="$SCRIPT_DIR"
elif [ -f "./SKILL.md" ]; then
    SOURCE_DIR="."
else
    # Download from server
    info "Downloading skill files from botmark.cc..."
    TMPDIR=$(mktemp -d)
    trap "rm -rf $TMPDIR" EXIT
    curl -fsSL "https://botmark.cc/api/v1/bot-benchmark/skill?format=openclaw" -o "$TMPDIR/skill.json"
    # Extract files from JSON response
    python3 -c "
import json, os, base64
with open('$TMPDIR/skill.json') as f:
    data = json.load(f)
skill_dir = '$TMPDIR/botmark-skill'
os.makedirs(skill_dir, exist_ok=True)
# Write SKILL.md
if 'skill_md' in data:
    with open(f'{skill_dir}/SKILL.md', 'w') as f:
        f.write(data['skill_md'])
# Write engine
if 'engine' in data:
    with open(f'{skill_dir}/botmark_engine.py', 'w') as f:
        f.write(data['engine'])
# Write engine_meta
if 'engine_version' in data:
    with open(f'{skill_dir}/engine_meta.json', 'w') as f:
        json.dump({'engine_version': data['engine_version'], 'skill_version': data.get('skill_version', '')}, f, indent=2)
" || fail "Failed to extract skill files"
    SOURCE_DIR="$TMPDIR/botmark-skill"
fi

# Copy files
mkdir -p "$SKILL_DIR"
cp -f "$SOURCE_DIR/SKILL.md" "$SKILL_DIR/" 2>/dev/null || fail "SKILL.md not found in source"
[ -f "$SOURCE_DIR/botmark_engine.py" ]  && cp -f "$SOURCE_DIR/botmark_engine.py" "$SKILL_DIR/"
[ -f "$SOURCE_DIR/engine_meta.json" ]   && cp -f "$SOURCE_DIR/engine_meta.json" "$SKILL_DIR/"
ok "Skill files installed to $SKILL_DIR"

# ── Step 3: API Key configuration ──
EXISTING_KEY=""

# Check 1: openclaw.json skills.entries
if [ -f "$OPENCLAW_CONFIG" ] && command -v python3 &>/dev/null; then
    EXISTING_KEY=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    key = cfg.get('skills', {}).get('entries', {}).get('botmark-skill', {}).get('apiKey', '')
    print(key)
except: pass
" 2>/dev/null)
fi

# Check 2: environment variable
if [ -z "$EXISTING_KEY" ] && [ -n "${BOTMARK_API_KEY:-}" ]; then
    EXISTING_KEY="$BOTMARK_API_KEY"
fi

# Check 3: .botmark_env file
if [ -z "$EXISTING_KEY" ] && [ -f "$SKILL_DIR/.botmark_env" ]; then
    source "$SKILL_DIR/.botmark_env" 2>/dev/null
    EXISTING_KEY="${BOTMARK_API_KEY:-}"
fi

if [ -n "$EXISTING_KEY" ]; then
    MASKED="${EXISTING_KEY:0:8}***"
    ok "API Key already configured ($MASKED)"
else
    echo ""
    echo -e "${CYAN}━━━ API Key Setup ━━━${NC}"
    echo "BotMark needs an API Key to run evaluations."
    echo "Get one free at: https://botmark.cc"
    echo ""
    read -rp "$(echo -e "${CYAN}?${NC}") Enter your BotMark API Key: " INPUT_KEY

    if [ -z "$INPUT_KEY" ]; then
        warn "No API Key provided. You can configure it later:"
        warn "  Edit $OPENCLAW_CONFIG"
        warn "  Or run this setup script again"
    else
        # Validate format
        if [[ ! "$INPUT_KEY" =~ ^bm_(live|test)_ ]]; then
            warn "Key doesn't start with bm_live_ or bm_test_ — saving anyway"
        fi

        # Save to openclaw.json (primary — OpenClaw native)
        if command -v python3 &>/dev/null; then
            python3 -c "
import json, os

config_path = '$OPENCLAW_CONFIG'

# Read existing or create new
if os.path.exists(config_path):
    with open(config_path) as f:
        cfg = json.load(f)
else:
    cfg = {}

# Ensure skills.entries.botmark-skill exists
cfg.setdefault('skills', {}).setdefault('entries', {})
cfg['skills']['entries'].setdefault('botmark-skill', {})
cfg['skills']['entries']['botmark-skill']['apiKey'] = '$INPUT_KEY'

# Write back
with open(config_path, 'w') as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
" && ok "API Key saved to openclaw.json (OpenClaw native config)"
        fi

        # Save to .botmark_env (fallback — for non-openclaw.json environments)
        cat > "$SKILL_DIR/.botmark_env" << ENVEOF
BOTMARK_API_KEY="$INPUT_KEY"
ENVEOF
        chmod 600 "$SKILL_DIR/.botmark_env"
        ok "API Key saved to .botmark_env (fallback)"
    fi
fi

# ── Step 4: Verify installation ──
echo ""
echo -e "${CYAN}━━━ Verification ━━━${NC}"

ISSUES=0

# Check SKILL.md
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    ok "SKILL.md present"
else
    warn "SKILL.md missing"; ISSUES=$((ISSUES+1))
fi

# Check engine
if [ -f "$SKILL_DIR/botmark_engine.py" ]; then
    ok "botmark_engine.py present"
else
    warn "botmark_engine.py missing (will be downloaded on first evaluation)"
fi

# Check python3
if command -v python3 &>/dev/null; then
    ok "python3 available"
else
    warn "python3 not found on PATH"; ISSUES=$((ISSUES+1))
fi

# Check curl
if command -v curl &>/dev/null; then
    ok "curl available"
else
    warn "curl not found on PATH"; ISSUES=$((ISSUES+1))
fi

# Check API Key
if [ -n "$EXISTING_KEY" ] || [ -n "${INPUT_KEY:-}" ]; then
    ok "API Key configured"
else
    warn "API Key not configured"; ISSUES=$((ISSUES+1))
fi

echo ""
if [ "$ISSUES" -eq 0 ]; then
    echo -e "${GREEN}━━━ Setup complete! ━━━${NC}"
    echo "Start a new OpenClaw session and say \"跑个分\" or \"benchmark\" to begin."
else
    echo -e "${YELLOW}━━━ Setup complete with $ISSUES warning(s) ━━━${NC}"
    echo "Fix the warnings above, then start a new OpenClaw session."
fi
