#!/bin/bash

# Daily News Brief skill installer for OpenClaw

echo "Installing Daily News Brief skill..."

# Check if OpenClaw skills directory exists
if [ ! -d "$OPENCLAW_SKILLS_DIR" ]; then
    echo "Error: OPENCLAW_SKILLS_DIR environment variable not set"
    echo "Please set the OpenClaw skills directory path"
    exit 1
fi

# Copy skill files to OpenClaw skills directory
echo "Copying skill files to $OPENCLAW_SKILLS_DIR/daily-news-brief..."
mkdir -p "$OPENCLAW_SKILLS_DIR/daily-news-brief"
cp -r * "$OPENCLAW_SKILLS_DIR/daily-news-brief/"

echo "Installation completed!"
echo ""
echo "Next steps:"
echo "1. Configure Telegram settings:"
echo "   set config.telegram_chat_id \"YOUR_CHAT_ID\""
echo "   set config.telegram_bot_token \"YOUR_BOT_TOKEN\""
echo "2. Register the skill:"
echo "   daily-news-brief register"
echo "3. Test the skill:"
echo "   daily-news-brief test"