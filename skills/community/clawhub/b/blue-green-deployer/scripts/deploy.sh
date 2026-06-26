#!/bin/bash
# Blue/Green Deployment Script for OpenClaw Config
# Implements: Clone -> Experiment -> Audit (via Symlink) -> Promote/Rollback
# Version 2.0 (Refactored for safety and reliability)

# Exit on error, undefined variables, and pipe failures
set -euo pipefail

# Paths
BLUE_CONFIG="$HOME/.openclaw/openclaw.json"
GREEN_CONFIG="$HOME/.openclaw/openclaw.json.green"
BACKUP_CONFIG="$HOME/.openclaw/openclaw.json.bak"
AUDIT_LINK="$HOME/.openclaw/openclaw.json.audit"

# Cleanup function to be called on error or exit
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo "⚠️  An error occurred. Performing emergency cleanup..."
        # If we left a .tmp file, try to restore it
        if [ -f "${BLUE_CONFIG}.tmp" ]; then
            mv "${BLUE_LONG_NAME:-${BLUE_CONFIG}.tmp}" "$BLUE_CONFIG" 2>/dev/null || true
        fi
    fi
    # Remove the audit symlink if it exists
    [ -L "$AUDIT_LINK" ] && rm "$AUDIT_LINK"
}

trap cleanup EXIT

echo "🚀 Starting Blue/Green Deployment Process (v2)..."

# 1. Setup: Ensure Green exists and is a clone of Blue
if [ ! -f "$BLUE_CONFIG" ]; then
    echo "❌ Error: Blue configuration ($BLUE_CONFIG) not found!"
    exit 1
fi

if [ ! -f "$GREEN_CONFIG" ]; then
    echo "📂 Creating Green (Tester) config from Blue..."
    cp "$BLUE_CONFIG" "$GREEN_CONFIG"
fi

# 2. The Audit (The core logic)
echo "🔍 Preparing Audit link..."

# Create a robust backup of the current Blue
cp "$BLUE_CONFIG" "$BACKUP_CONFIG"

# Create the audit symlink pointing to Green
ln -sf "$GREEN_CONFIG" "$AUDIT_LINK"

# 3. Validation
# We use a temporary file to perform the swap safely.
echo "🧪 Running validation against the Audit link..."

# Create a temporary copy of Blue to swap in
cp "$BLUE_CONFIG" "${BLUE_CONFIG}.tmp"

# Point Blue to the Audit link (which points to Green)
# Note: We are effectively making the 'real' config file a symlink to Green for the test
rm "$BLUE_CONFIG"
ln -s "$AUDIT_LINK" "$BLUE_CONFIG"

# Execute the check
# We use 'openclaw status' - we assume this command exists in the PATH/environment
if openclaw status > /dev/null 2>&1; then
    echo "✅ SUCCESS: Green configuration is valid!"
    echo "🎉 Promoting Green to Blue..."
    
    # To promote, we replace the symlink with the actual content of Green
    rm "$BLUE_CONFIG"
    cp "$GREEN_CONFIG" "$BLUE_CONFIG"
    
    echo "🚀 Deployment complete. Blue is now updated."
else
    echo "❌ FAILURE: Green configuration is invalid!"
    echo "🚨 Rolling back Blue to original state..."
    
    # Restore from backup
    rm "$BLUE_CONFIG"
    cp "$BACKUP_CONFIG" "$BLUE_CONFIG"
    
    echo "🔄 Rollback complete. Blue is restored."
    exit 1
fi
