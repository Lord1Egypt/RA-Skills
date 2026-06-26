#!/usr/bin/env bash
# inject-gateway-env.sh — Bake API keys from 1Password into the OpenClaw gateway plist.
# Run whenever a key changes, or after a fresh bootstrap.
# 
# Requires: op CLI + ~/.config/openclaw/.op-service-token
#
# Usage: bash scripts/inject-gateway-env.sh

set -euo pipefail

PLIST="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
TOKEN_FILE="$HOME/.config/openclaw/.op-service-token"

if [ ! -f "$TOKEN_FILE" ]; then
    echo "❌ No 1Password token at $TOKEN_FILE"
    echo "   Get it from 1Password and run: echo <TOKEN> > $TOKEN_FILE && chmod 600 $TOKEN_FILE"
    exit 1
fi

export OP_SERVICE_ACCOUNT_TOKEN=$(cat "$TOKEN_FILE")

echo "Reading keys from 1Password..."
OPENAI_API_KEY=$(op read "op://OpenClaw/OpenAI API Key/credential" 2>/dev/null) || { echo "❌ OpenAI key read failed"; exit 1; }
ANTHROPIC_API_KEY=$(op read "op://OpenClaw/Anthropic API Key/notesPlain" 2>/dev/null) || { echo "❌ Anthropic key read failed"; exit 1; }
GEMINI_API_KEY=$(op read "op://OpenClaw/Gemini API Key/notesPlain" 2>/dev/null) || { echo "❌ Gemini key read failed"; exit 1; }
MISTRAL_API_KEY=$(op read "op://OpenClaw/Mistral API Key/credential" 2>/dev/null) || { echo "❌ Mistral key read failed"; exit 1; }
VOYAGE_API_KEY=$(op read "op://OpenClaw/Voyage API Key/credential" 2>/dev/null) || { echo "⚠️ Voyage key read failed (optional)"; VOYAGE_API_KEY=""; }
HF_TOKEN=$(op read "op://OpenClaw/Hugging Face API Credentials/credential" 2>/dev/null) || { echo "⚠️ HuggingFace token read failed (optional)"; HF_TOKEN=""; }

if [ ! -f "$PLIST" ]; then
    echo "❌ Gateway plist not found at $PLIST"
    echo "   Run: openclaw gateway start (once) to create it, then re-run this script"
    exit 1
fi

echo "Injecting into $PLIST ..."
BUDDY="/usr/libexec/PlistBuddy"

inject_key() {
    local key="$1" val="$2"
    [ -z "$val" ] && return
    $BUDDY -c "Delete :EnvironmentVariables:$key" "$PLIST" 2>/dev/null || true
    $BUDDY -c "Add :EnvironmentVariables:$key string $val" "$PLIST"
    echo "  ✅ $key"
}

inject_key "OPENAI_API_KEY"       "$OPENAI_API_KEY"
inject_key "ANTHROPIC_API_KEY"    "$ANTHROPIC_API_KEY"
inject_key "GEMINI_API_KEY"       "$GEMINI_API_KEY"
inject_key "MISTRAL_API_KEY"      "$MISTRAL_API_KEY"
inject_key "VOYAGE_API_KEY"       "$VOYAGE_API_KEY"
inject_key "HF_TOKEN"             "$HF_TOKEN"
inject_key "OP_SERVICE_ACCOUNT_TOKEN" "$(cat "$TOKEN_FILE")"
inject_key "SHERPA_ONNX_RUNTIME_DIR" "$HOME/.openclaw/sherpa-onnx/runtime"
inject_key "SHERPA_ONNX_MODEL_DIR"   "$HOME/.openclaw/sherpa-onnx/models/vits-piper-en_US-lessac-high"
inject_key "OTLP_ENDPOINT"           "localhost:4317"

echo ""
echo "Restarting gateway..."
launchctl stop ai.openclaw.gateway 2>/dev/null || true
sleep 2
launchctl start ai.openclaw.gateway
echo "✅ Gateway restarted"
echo ""
echo "Verify: launchctl print gui/\$UID/ai.openclaw.gateway | grep -E 'OPENAI|ANTHROPIC|OP_SERVICE'"
