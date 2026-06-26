#!/bin/bash
# AI Mother Setup Wizard
# Interactive configuration for first-time users

SKILL_DIR="$HOME/.openclaw/skills/ai-mother"
CONFIG_FILE="$SKILL_DIR/config.json"

echo "👩‍👧‍👦 AI Mother Setup Wizard"
echo "================================"
echo ""

# Check Python dependencies
echo "Checking dependencies..."
if ! python3 -c "import rich" 2>/dev/null; then
    echo "⚠️  Missing dependency: rich"
    read -p "Install rich library? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip3 install rich --user
        echo "✅ rich installed"
    else
        echo "❌ rich is required for TUI dashboard. Install with: pip3 install rich"
    fi
fi
echo ""

# Check if already configured
if [ -f "$CONFIG_FILE" ]; then
    EXISTING_ID=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('owner_feishu_open_id',''))" 2>/dev/null)
    if [ -n "$EXISTING_ID" ] && [ "$EXISTING_ID" != "" ]; then
        echo "⚠️  AI Mother is already configured with open_id: $EXISTING_ID"
        read -p "Do you want to reconfigure? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Setup cancelled."
            exit 0
        fi
    fi
fi

echo "AI Mother needs your Feishu open_id to send you DM notifications."
echo ""
echo "📖 How to get your Feishu open_id:"
echo ""
echo "Method 1: Send a message to the bot on Feishu"
echo "  1. Open Feishu and search for your bot"
echo "  2. Send any message (e.g., 'hello')"
echo "  3. Run: openclaw logs --tail 20 | grep 'ou_'"
echo "  4. Look for: 'received message from ou_xxxxx'"
echo "  5. Copy the ou_xxxxx string"
echo ""
echo "Method 2: Use Feishu API"
echo "  1. Go to: https://open.feishu.cn/app"
echo "  2. Open your app → 'Credentials & Basic Info'"
echo "  3. Find 'Bot Open ID' or use API to get user open_id"
echo ""
echo "Your open_id should start with 'ou_' (e.g., ou_abc123def456xyz789)"
echo ""

# Prompt for open_id
while true; do
    read -p "Enter your Feishu open_id: " OPEN_ID
    
    # Validate format
    if [[ "$OPEN_ID" =~ ^ou_[a-zA-Z0-9]+$ ]]; then
        break
    else
        echo "❌ Invalid format. Open ID must start with 'ou_' followed by alphanumeric characters."
        echo "Example: ou_abc123def456xyz789"
        echo ""
    fi
done

# Save to config
cat > "$CONFIG_FILE" <<EOF
{
  "owner_feishu_open_id": "$OPEN_ID",
  "_comment": "AI Mother configuration. Edit this file to change settings."
}
EOF

echo ""
echo "✅ Configuration saved to: $CONFIG_FILE"
echo ""

# Test notification
echo "🧪 Testing Feishu notification..."
TEST_MSG="👩‍👧‍👦 AI Mother setup complete! I'll notify you when AI agents need attention."

if openclaw message send --channel feishu --target "user:$OPEN_ID" --message "$TEST_MSG" 2>/dev/null; then
    echo "✅ Test message sent! Check your Feishu."
else
    echo "⚠️  Test message failed. Please check:"
    echo "  - Feishu channel is enabled in openclaw config"
    echo "  - Bot has permission to send messages"
    echo "  - open_id is correct"
fi

echo ""
echo "🎉 Setup complete!"
echo ""

# Configure cron job for patrol
echo "⏰ Configuring scheduled patrol..."
CRON_MSG="AI Mother patrol: run ~/.openclaw/skills/ai-mother/scripts/patrol.sh and check all AI agent statuses. If NEEDS_ATTENTION=true, analyze the issue and notify the owner. If everything is fine, no notification needed."

# Check if cron job already exists
EXISTING_CRON=$(openclaw cron list --json 2>/dev/null | grep -c '"name":\s*"ai-mother-patrol"' || echo "0")

if [ "$EXISTING_CRON" -ge "1" ]; then
    echo "✅ Scheduled patrol already configured"
else
    # Create cron job (every 30 minutes)
    if openclaw cron add \
        --name "ai-mother-patrol" \
        --every "30m" \
        --message "$CRON_MSG" \
        --channel "feishu" \
        --to "user:$OPEN_ID" \
        --session "isolated" \
        --timeout-seconds 120 \
        --announce \
        2>/dev/null; then
        echo "✅ Scheduled patrol configured (every 30 minutes)"
    else
        echo "⚠️  Failed to configure cron automatically."
        echo "   Please configure manually or ask Happy to help."
    fi
fi

echo ""

# Optional: Add to HEARTBEAT.md for heartbeat-based patrol
HEARTBEAT_FILE="$HOME/.openclaw/workspace/HEARTBEAT.md"
if [ -f "$HEARTBEAT_FILE" ]; then
    if ! grep -q "ai-mother" "$HEARTBEAT_FILE" 2>/dev/null; then
        echo "📝 Would you like to add AI Mother patrol to HEARTBEAT.md?"
        echo "   This enables heartbeat-based monitoring (alternative to cron)."
        read -p "   Add to HEARTBEAT.md? (y/n): " ADD_HEARTBEAT
        
        if [ "$ADD_HEARTBEAT" = "y" ] || [ "$ADD_HEARTBEAT" = "Y" ]; then
            cat >> "$HEARTBEAT_FILE" << 'EOF'

# AI Mother patrol
# On each heartbeat:
# 1. Run patrol.sh --quiet
# 2. If NEEDS_ATTENTION=true: run auto-heal for each affected PID, then notify owner
# 3. If nothing: stay silent (HEARTBEAT_OK)
EOF
            echo "✅ Added AI Mother patrol to HEARTBEAT.md"
        fi
    else
        echo "✅ AI Mother already configured in HEARTBEAT.md"
    fi
fi

echo ""
echo "Next steps:"
echo "  - AI Mother will patrol every 30 minutes automatically"
echo "  - Run: ~/.openclaw/skills/ai-mother/scripts/patrol.sh (manual check)"
echo "  - Run: ~/.openclaw/skills/ai-mother/scripts/dashboard.sh (TUI dashboard)"
echo ""
