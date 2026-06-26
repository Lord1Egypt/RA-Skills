#!/usr/bin/env bash
#
# OpenClaw wrapper for cross-border-intel TypeScript skill
# This script provides the interface for OpenClaw to call the TypeScript skill
#

# Set environment variables
export OPENCLAW_CONFIG_PATH="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
export OPENCLAW_STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"

# Path to the TypeScript skill (adjust if needed)
SKILL_DIR="/Users/zhuqiangyi/Beansmile/beansmile-claw-skills/packages/cross-border-intel"
TEST_WRAPPER="$SKILL_DIR/test-wrapper.mjs"

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "Error: node is not installed" >&2
    exit 1
fi

# Check if the test wrapper exists
if [ ! -f "$TEST_WRAPPER" ]; then
    echo "Error: TypeScript skill not found at $TEST_WRAPPER" >&2
    echo "Please run 'pnpm build' in the skill directory first" >&2
    exit 1
fi

# Execute the TypeScript skill
node "$TEST_WRAPPER" "$@"
