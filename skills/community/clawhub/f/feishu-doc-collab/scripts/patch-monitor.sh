#!/bin/bash
# Feishu Doc Collaboration - Monitor Patch Script (v1.1.0)
# Patches openclaw-lark monitor.js to trigger /hooks/agent on document edit events.
#
# Usage: bash ./skills/feishu-doc-collab/scripts/patch-monitor.sh
#
# Prerequisites:
#   1. hooks must be enabled in openclaw.json
#   2. openclaw-lark extension must be installed
#
# Safe to re-run - idempotent.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Try multiple known locations for monitor.js
MONITOR=""
for candidate in   "$HOME/.openclaw/extensions/openclaw-lark/src/channel/monitor.js"   "/usr/lib/node_modules/openclaw/extensions/feishu/src/monitor.ts"; do
  if [ -f "$candidate" ]; then
    MONITOR="$candidate"
    break
  fi
done

if [ -z "$MONITOR" ]; then
  echo "ERROR: monitor.js/ts not found in any known location."
  echo "Checked:"
  echo "  ~/.openclaw/extensions/openclaw-lark/src/channel/monitor.js"
  echo "  /usr/lib/node_modules/openclaw/extensions/feishu/src/monitor.ts"
  exit 1
fi

echo "Found monitor at: $MONITOR"

CONFIG="$SKILL_DIR/config.json"
if [ ! -f "$CONFIG" ]; then
  echo "ERROR: config.json not found at $CONFIG"
  exit 1
fi

AGENT_NAME=$(python3 -c "import json; print(json.load(open(chr(39)+str('''$CONFIG''')[:0]+'''$CONFIG'''+chr(39)))[chr(39)+'agent_name'+chr(39)])" 2>/dev/null || echo "MyBot")

if grep -q "/hooks/agent" "$MONITOR" 2>/dev/null && grep -q "_editDebounce" "$MONITOR" 2>/dev/null; then
  echo "monitor already patched (hooks + debounce) - no changes needed."
  exit 0
fi

echo "Applying feishu-doc-collab patch..."
echo "  Agent name: $AGENT_NAME"
cp "$MONITOR" "$MONITOR.bak"
echo "  Backup saved: $MONITOR.bak"

# Use the full patched reference file
REF="$SKILL_DIR/references/monitor-full-patched.js"
if [ -f "$REF" ]; then
  cp "$REF" "$MONITOR"
  echo "Applied from reference file: $REF"
else
  echo "ERROR: Reference file not found: $REF"
  echo "Manual patching required. See references/manual-patch.md"
  exit 1
fi

echo ""
echo "Patch applied. Restart the gateway to activate:"
echo "  openclaw gateway restart"
