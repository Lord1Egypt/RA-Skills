#!/bin/bash

# ClawSaver Publication Script
# Publishes ClawSaver to ClawHub

set -e

SKILL_DIR=$(dirname "$0")
cd "$SKILL_DIR"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         ClawSaver v1.0.0 — Publishing to ClawHub              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo

# Step 1: Verify tests pass
echo "Step 1: Verifying tests..."
npm test > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✅ All tests passing"
else
  echo "❌ Tests failed. Aborting."
  exit 1
fi
echo

# Step 2: Check npm login
echo "Step 2: Checking ClawHub authentication..."
npm whoami --registry=https://registry.clawhub.com > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✅ Authenticated with ClawHub"
else
  echo "⚠️  Not authenticated with ClawHub. Running: npm login"
  npm login --registry=https://registry.clawhub.com
fi
echo

# Step 3: Publish
echo "Step 3: Publishing to ClawHub..."
npm publish --registry=https://registry.clawhub.com

if [ $? -eq 0 ]; then
  echo "✅ Successfully published!"
else
  echo "❌ Publication failed."
  exit 1
fi
echo

# Step 4: Verify
echo "Step 4: Verifying publication..."
npm view clawsaver --registry=https://registry.clawhub.com > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✅ Package verified on ClawHub"
else
  echo "❌ Package not found on ClawHub."
  exit 1
fi
echo

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  ✅ Publication Complete!                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo
echo "Next steps:"
echo "  1. Users can install with: npm install clawsaver"
echo "  2. Or use ClawHub: openclaw skill install clawsaver"
echo "  3. See README.md for integration instructions"
echo
echo "Documentation: https://clawhub.com/skills/clawsaver"
echo
