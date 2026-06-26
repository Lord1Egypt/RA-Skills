#!/bin/bash
# FounderClaw uninstaller — removes everything
# Usage: bash uninstall.sh

set -e

SKILLS_DIR="${HOME}/.agents/skills"
FC_DIR="${SKILLS_DIR}/founderclaw"
CONFIG="${HOME}/.openclaw/openclaw.json"

echo "=== FounderClaw Uninstaller ==="
echo ""

# Step 1: Remove symlinks
echo "Removing skill symlinks..."
REMOVED=0
for link in "$SKILLS_DIR"/*; do
    [ -L "$link" ] || continue
    target=$(readlink "$link")
    echo "$target" | grep -q "founderclaw" && rm "$link" && REMOVED=$((REMOVED + 1))
done
echo "  ✅ Removed $REMOVED symlinks"

# Step 2: Remove repo
echo ""
echo "Removing FounderClaw repo..."
rm -rf "$FC_DIR"
echo "  ✅ Removed ~/.agents/skills/founderclaw/"

# Step 3: Remove agents from config
echo ""
echo "Removing agents from config..."
if [ -f "$CONFIG" ]; then
    python3 << 'PYEOF'
import json, re, os

config_path = os.path.expanduser("~/.openclaw/openclaw.json")

with open(config_path, 'r') as f:
    content = f.read()

content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
content = re.sub(r',\s*([}\]])', r'\1', content)
config = json.loads(content)

fc_ids = ['founderclaw-main', 'fc-strategy', 'fc-shipper', 'fc-tester', 'fc-safety', 'fc-observer']

if 'agents' in config and 'list' in config['agents']:
    original_count = len(config['agents']['list'])
    config['agents']['list'] = [a for a in config['agents']['list'] if a.get('id') not in fc_ids]
    removed = original_count - len(config['agents']['list'])
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"  ✅ Removed {removed} FounderClaw agents from config")
else:
    print("  ✅ No agents section in config")
PYEOF
else
    echo "  ⚠️ Config not found at $CONFIG"
fi

# Step 4: Report
echo ""
echo "=== Uninstalled ==="
echo ""
echo "  ✅ Skills removed"
echo "  ✅ Repo deleted"
echo "  ✅ Agents removed from config"
echo "  ✅ Workspace preserved at ~/.openclaw/founderclaw/"
echo ""
echo "  ⚠️ Gateway restart required."
echo "  Run: openclaw gateway restart"
