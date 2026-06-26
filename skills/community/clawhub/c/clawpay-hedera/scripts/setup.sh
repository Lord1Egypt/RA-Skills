#!/bin/bash
# ClawPay OpenClaw Skill Setup
# Installs the ClawPay CLI for autonomous MCP payments on Hedera

set -e

echo "🦞 Setting up ClawPay..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is required. Install from https://nodejs.org"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 20 ]; then
    echo "Error: Node.js 20+ required (found v$NODE_VERSION)"
    exit 1
fi

# Verify ClawPay CLI is accessible
echo "Checking ClawPay CLI..."
npx @clawpay-hedera/sdk --version

# Check for Hedera key
if [ -z "$HEDERA_PRIVATE_KEY" ]; then
    echo ""
    echo "⚠️  HEDERA_PRIVATE_KEY not set."
    echo "Set it in your environment to enable autonomous payments:"
    echo "  export HEDERA_PRIVATE_KEY=\"0x...\""
    echo ""
    echo "Get a testnet key from https://portal.hedera.com"
else
    echo "✓ HEDERA_PRIVATE_KEY is set"
fi

echo ""
echo "✓ ClawPay setup complete"
echo "Usage: npx @clawpay-hedera/sdk connect --urls <server-url> --hedera-key \$HEDERA_PRIVATE_KEY"
