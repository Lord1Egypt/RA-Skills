#!/bin/bash
# Patch openclaw-lark plugin to force reply_in_thread=true for group chats.
# Usage: bash patch-lark-thread.sh [--check-only]
#
# --check-only: Only check if patch is applied, exit 0 if yes, 1 if no.

set -euo pipefail

PLUGIN_DIR="${OPENCLAW_LARK_DIR:-$HOME/.openclaw/extensions/openclaw-lark/src/messaging/inbound}"
DISPATCH="$PLUGIN_DIR/dispatch.js"
DISPATCH_CMD="$PLUGIN_DIR/dispatch-commands.js"

check_only=false
if [[ "${1:-}" == "--check-only" ]]; then
    check_only=true
fi

patched=0
needs_patch=0

for f in "$DISPATCH" "$DISPATCH_CMD"; do
    if [ ! -f "$f" ]; then
        echo "❌ Not found: $f"
        needs_patch=1
        continue
    fi
    if grep -q "dc\.isGroup || dc\.isThread" "$f"; then
        patched=$((patched + 1))
    elif grep -q "replyInThread: dc\.isThread" "$f"; then
        needs_patch=1
    fi
done

if [ "$check_only" = true ]; then
    if [ "$needs_patch" -gt 0 ]; then
        echo "❌ Patch NOT applied (found $needs_patch file(s) needing patch)"
        exit 1
    else
        echo "✅ Patch is applied ($patched file(s) verified)"
        exit 0
    fi
fi

# Apply patch
echo "🔧 Patching openclaw-lark for group thread replies..."

for f in "$DISPATCH" "$DISPATCH_CMD"; do
    if [ ! -f "$f" ]; then
        echo "  ❌ Not found: $f"
        continue
    fi
    if grep -q "replyInThread: dc\.isThread" "$f"; then
        sed -i '' 's/replyInThread: dc\.isThread/replyInThread: dc.isGroup || dc.isThread/g' "$f"
        echo "  ✅ Patched: $(basename "$f")"
    else
        echo "  ⏭️  Already patched or changed: $(basename "$f")"
    fi
done

echo ""
echo "Done. Restart gateway to apply:"
echo "  openclaw gateway restart"
echo "  -- or --"
echo "  Use gateway tool: action=restart"
