#!/bin/bash
# FounderClaw installer — ONE command, does EVERYTHING
# Usage: curl -fsSL https://raw.githubusercontent.com/ashish797/FounderClaw/main/install.sh | bash

set -e

SKILLS_DIR="${HOME}/.agents/skills"
FC_DIR="${SKILLS_DIR}/founderclaw"
REPO_URL="https://github.com/ashish797/FounderClaw.git"
CONFIG="${HOME}/.openclaw/openclaw.json"

echo "=== FounderClaw Installer ==="
echo ""

# Step 1: Clone
if [ -d "$FC_DIR" ]; then
    echo "Updating FounderClaw..."
    cd "$FC_DIR" && git stash 2>/dev/null && git fetch origin && git reset --hard origin/main
else
    echo "Cloning FounderClaw..."
    git clone --single-branch --depth 1 "$REPO_URL" "$FC_DIR"
fi

# Step 2: Symlink skills
echo ""
echo "Installing skills..."
mkdir -p "$SKILLS_DIR"
INSTALLED=0
SKIPPED=0
for skill_dir in "$FC_DIR"/*/; do
    [ ! -f "$skill_dir/SKILL.md" ] && continue
    skill_name=$(basename "$skill_dir")
    target="$SKILLS_DIR/$skill_name"
    if [ -e "$target" ] || [ -L "$target" ]; then
        if [ -L "$target" ] && [ "$(readlink "$target")" = "$skill_dir" ]; then
            : # already linked
        else
            SKIPPED=$((SKIPPED + 1))
        fi
    else
        ln -sf "$skill_dir" "$target"
        INSTALLED=$((INSTALLED + 1))
    fi
done
echo "  ✅ $INSTALLED skills installed ($SKIPPED skipped)"

# Step 3: Create workspace
echo ""
echo "Creating workspace..."
if [ ! -d "${HOME}/.openclaw/founderclaw" ]; then
    cp -r "$FC_DIR/workspace-template" "${HOME}/.openclaw/founderclaw"
    echo "  ✅ Workspace created at ~/.openclaw/founderclaw/"
else
    echo "  ✅ Workspace already exists"
fi

# Step 4: Build browse binary (optional)
echo ""
if command -v bun >/dev/null 2>&1; then
    echo "Building browse binary..."
    cd "$FC_DIR/browse"
    bun install --silent 2>/dev/null
    if bun build src/cli.ts --compile --outfile dist/browse 2>/dev/null; then
        echo "  ✅ Browse binary built"
    else
        echo "  ⚠️ Browse build failed (non-critical)"
    fi
else
    echo "  ⏭️ Bun not found — browse binary skipped"
fi

# Step 5: Apply multi-agent config (THE KEY STEP)
echo ""
echo "Applying multi-agent config..."

if [ ! -f "$CONFIG" ]; then
    echo "  ⚠️ openclaw.json not found at $CONFIG"
    echo "  Run: openclaw setup first"
    echo ""
    echo "After setup, add these agents manually:"
    cat "$FC_DIR/install-founderclaw/agents-config.json"
    exit 1
fi

# Use Python to patch the config
python3 << 'PYEOF'
import json
import sys
import os

config_path = os.path.expanduser("~/.openclaw/openclaw.json")

try:
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Parse JSON (handle JSON5-like content by removing comments)
    import re
    # Remove single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Remove trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
    
    config = json.loads(content)
except Exception as e:
    print(f"  ⚠️ Could not parse config: {e}")
    print("  Falling back to manual install.")
    sys.exit(1)

# Check if agents already exist
existing_ids = [a.get('id') for a in config.get('agents', {}).get('list', [])]
fc_agents = ['founderclaw-main', 'fc-strategy', 'fc-shipper', 'fc-tester', 'fc-safety', 'fc-observer']

if all(aid in existing_ids for aid in fc_agents):
    print("  ✅ All 6 FounderClaw agents already in config")
    sys.exit(0)

# Read agents config
fc_config_path = os.path.expanduser("~/.agents/skills/founderclaw/install-founderclaw/agents-config.json")
with open(fc_config_path, 'r') as f:
    fc_agents_list = json.load(f)

# Add agents to config
if 'agents' not in config:
    config['agents'] = {}
if 'list' not in config['agents']:
    config['agents']['list'] = []

for fc_agent in fc_agents_list:
    # Check if already exists
    if fc_agent['id'] not in existing_ids:
        config['agents']['list'].append(fc_agent)
        print(f"  ✅ Added agent: {fc_agent['id']} ({fc_agent['name']})")
    else:
        print(f"  ✅ Agent already exists: {fc_agent['id']}")

# Write back
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("  ✅ Config updated")
PYEOF

# Step 6: Add proactive rules to AGENTS.md
echo ""
WORKSPACE="${HOME}/.openclaw/workspace"
AGENTS_MD="${WORKSPACE}/AGENTS.md"
if [ -f "$AGENTS_MD" ]; then
    if ! grep -q "FOUNDERCLAW" "$AGENTS_MD" 2>/dev/null; then
        echo "" >> "$AGENTS_MD"
        echo "# FounderClaw Skills" >> "$AGENTS_MD"
        echo "FounderClaw installed. 30 skills available. Say 'what skills do you have?' to list them." >> "$AGENTS_MD"
        echo "  ✅ Added proactive rules to AGENTS.md"
    fi
fi

# Step 7: Verify
echo ""
echo "=== Verifying installation ==="

# Count skills
SKILL_COUNT=$(find "$FC_DIR" -maxdepth 2 -name SKILL.md | wc -l)
echo "  Skills: $SKILL_COUNT"

# Check workspace
if [ -d "${HOME}/.openclaw/founderclaw/ceo" ]; then
    echo "  Workspace: ✅"
else
    echo "  Workspace: ❌"
fi

# Check config
if python3 -c "
import json, re, os
with open(os.path.expanduser('~/.openclaw/openclaw.json'), 'r') as f:
    c = re.sub(r',\s*([}\]])', r'\1', re.sub(r'//.*$', '', f.read(), flags=2))
config = json.loads(c)
ids = [a['id'] for a in config.get('agents',{}).get('list',[])]
fc = ['founderclaw-main','fc-strategy','fc-shipper','fc-tester','fc-safety','fc-observer']
found = sum(1 for a in fc if a in ids)
print(f'  Agents: {found}/6 configured')
" 2>/dev/null; then
    :
else
    echo "  Agents: ⚠️ Could not verify"
fi

# Step 8: Report
echo ""
echo "=== FounderClaw Installed ==="
echo ""
echo "  ✅ $SKILL_COUNT skills"
echo "  ✅ Workspace at ~/.openclaw/founderclaw/"
echo "  ✅ Multi-agent config applied"
echo ""
echo "  ⚠️ Gateway restart required for agents to activate."
echo "  Run: openclaw gateway restart"
echo ""
echo "  Quick start:"
echo "    - Say 'what skills do you have?'"
echo "    - Say 'I have an idea'"
echo "    - Say 'review my code'"
echo ""
echo "  Uninstall: bash ~/.agents/skills/founderclaw/uninstall.sh"
