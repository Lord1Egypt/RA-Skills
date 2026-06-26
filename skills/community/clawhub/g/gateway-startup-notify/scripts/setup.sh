#!/bin/bash
set -e

# Gateway Notify Setup Script
# Configures a hook to send notifications when the OpenClaw gateway starts up.

SUPPORTED_CHANNELS="telegram whatsapp discord slack signal imessage googlechat irc line openclaw-weixin feishu qqbot"

usage() {
  echo "Usage: $0 <channel> <address>"
  echo ""
  echo "Supported channels: $SUPPORTED_CHANNELS"
  echo ""
  echo "Examples:"
  echo "  $0 telegram @username"
  echo "  $0 whatsapp +1234567890"
  echo "  $0 discord 1234567890"
  echo "  $0 slack #general"
  echo "  $0 signal +1234567890"
  echo "  $0 imessage user@icloud.com"
  echo "  $0 googlechat spaces/xxx"
  echo "  $0 irc #channel"
  echo "  $0 line user_id"
  echo "  $0 openclaw-weixin openid@im.wechat"
  echo "  $0 feishu chat_id"
  echo "  $0 qqbot chat_id"
  exit 1
}

if [ $# -lt 2 ]; then
  usage
fi

# Check dependencies
if ! command -v python3 &>/dev/null; then
  echo "Error: python3 required but not found. Please install python3."
  exit 1
fi

CHANNEL="$1"
ADDRESS="$2"
HOOK_DIR="$HOME/.openclaw/hooks/gateway-notify"

# Validate channel
VALID=false
for ch in $SUPPORTED_CHANNELS; do
  if [ "$ch" = "$CHANNEL" ]; then
    VALID=true
    break
  fi
done

if [ "$VALID" = false ]; then
  echo "Error: Unsupported channel '$CHANNEL'"
  echo "Supported: $SUPPORTED_CHANNELS"
  exit 1
fi

# Address validation
case "$CHANNEL" in
  telegram)
    if [[ ! "$ADDRESS" =~ ^@[a-zA-Z0-9_]{5,32}$ ]] && [[ ! "$ADDRESS" =~ ^-?[0-9]+$ ]]; then
      echo "Error: Invalid Telegram address (use @username or chat ID)"
      exit 1
    fi
    ;;
  whatsapp|signal)
    if [[ ! "$ADDRESS" =~ ^\+[0-9]{10,15}$ ]]; then
      echo "Error: Invalid phone format for $CHANNEL (use +countrycodenumber)"
      exit 1
    fi
    ;;
  imessage)
    if [[ ! "$ADDRESS" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]] && [[ ! "$ADDRESS" =~ ^\+[0-9]{10,15}$ ]]; then
      echo "Error: Invalid address for iMessage (use email or +phone)"
      exit 1
    fi
    ;;
  discord)
    if [[ ! "$ADDRESS" =~ ^[0-9]+$ ]]; then
      echo "Error: Invalid Discord address (use numeric channel ID)"
      exit 1
    fi
    ;;
  slack)
    if [[ ! "$ADDRESS" =~ ^#[a-zA-Z0-9_-]+$ ]] && [[ ! "$ADDRESS" =~ ^[A-Z][A-Z0-9]+$ ]]; then
      echo "Error: Invalid Slack address (use #channel or channel ID)"
      exit 1
    fi
    ;;
  googlechat)
    if [[ ! "$ADDRESS" =~ ^spaces/ ]]; then
      echo "Error: Invalid Google Chat address (use spaces/xxx format)"
      exit 1
    fi
    ;;
  irc)
    if [[ ! "$ADDRESS" =~ ^#[a-zA-Z0-9_-]+$ ]]; then
      echo "Error: Invalid IRC address (use #channel)"
      exit 1
    fi
    ;;
  line)
    if [[ -z "$ADDRESS" ]]; then
      echo "Error: Line user ID required"
      exit 1
    fi
    ;;
  openclaw-weixin)
    if [[ ! "$ADDRESS" =~ ^[a-zA-Z0-9_-]+@im\.wechat$ ]]; then
      echo "Error: Invalid WeChat address (expected: openid@im.wechat)"
      exit 1
    fi
    ;;
  feishu)
    if [[ -z "$ADDRESS" ]]; then
      echo "Error: Feishu chat_id required (e.g. oc_xxx or user_id)"
      exit 1
    fi
    ;;
  qqbot)
    if [[ ! "$ADDRESS" =~ ^[0-9]+$ ]]; then
      echo "Error: Invalid QQ address (use numeric chat ID)"
      exit 1
    fi
    ;;
esac

echo "Setting up gateway-notify hook..."
echo "Channel: $CHANNEL"
echo "Address: $ADDRESS"
echo ""

# Back up existing hook if present
if [ -d "$HOOK_DIR" ]; then
  BACKUP="$HOOK_DIR.bak.$(date +%Y%m%d%H%M%S).$$"
  echo "⚠ Existing hook found. Backing up to $BACKUP"
  cp -r "$HOOK_DIR" "$BACKUP"
fi

mkdir -p "$HOOK_DIR"

# Create HOOK.md
cat > "$HOOK_DIR/HOOK.md" << 'HOOKEOF'
---
name: gateway-notify
description: "Send notification when gateway starts"
metadata:
  openclaw:
    emoji: "🚀"
    events: ["gateway:startup"]
---

# Gateway Notify

Sends a notification to the configured channel when the gateway starts up.
HOOKEOF

echo "✓ Created HOOK.md"

# Write config to a separate JSON file (safe from injection)
# Generate config.json safely using Python (handles all escaping)
python3 -c "
import json, sys
config = {'channel': sys.argv[1], 'address': sys.argv[2]}
print(json.dumps(config, indent=2))
" "$CHANNEL" "$ADDRESS" > "$HOOK_DIR/config.json"

echo "✓ Created config.json"

# Create handler.ts — reads config at runtime, no embedded user input
cat > "$HOOK_DIR/handler.ts" << 'HANDLEREOF'
import { execFile } from "child_process";
import { promisify } from "util";
import { readFileSync } from "fs";
import { join } from "path";

const execFileAsync = promisify(execFile);

// Read config from separate file — no user input embedded in code
const configPath = join(__dirname, "config.json");
let config: { channel: string; address: string };
try {
  config = JSON.parse(readFileSync(configPath, "utf-8"));
} catch (err) {
  console.error("[gateway-notify] Failed to load config.json:", err);
  return;
}

const handler = async (event: any) => {
  if (event.type !== "gateway" || event.action !== "startup") return;

  try {
    const now = new Date();
    const timeStr = now.toLocaleString("en-US", { hour12: false });
    const port = String(event.data?.port || "18789");

    const message = [
      "🚀 Gateway Started",
      "⏰ " + timeStr,
      "🌐 127.0.0.1:" + port,
    ].join("\n");

    await execFileAsync("openclaw", [
      "message", "send",
      "--channel", config.channel,
      "--target", config.address,
      "--message", message,
    ]);

    console.log("[gateway-notify] Notification sent to " + config.channel);
  } catch (err) {
    console.error("[gateway-notify] Failed to send notification:", err);
  }
};

export default handler;
HANDLEREOF

echo "✓ Created handler.ts"

# Enable hook
if command -v openclaw &>/dev/null; then
  openclaw hooks enable gateway-notify
  echo "✓ Hook enabled"
else
  echo "⚠ openclaw not found in PATH. Enable the hook manually:"
  echo "  openclaw hooks enable gateway-notify"
fi

echo ""
echo "Setup complete! Restart the gateway to activate:"
echo "  openclaw gateway restart"
echo ""
echo "Tip: Review the generated files before restarting:"
echo "  cat $HOOK_DIR/config.json"
echo "  cat $HOOK_DIR/handler.ts"
