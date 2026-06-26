#!/bin/bash

# Fullrun - Uninstall Script
# Removes fullrun skill configuration from the current project

set -e

PROJECT_CLAUDE_DIR="$(pwd)/.claude"
PROJECT_SETTINGS="$PROJECT_CLAUDE_DIR/settings.local.json"

echo "=== Fullrun Skill - Project Uninstall ==="
echo ""

# Check if settings file exists
if [ ! -f "$PROJECT_SETTINGS" ]; then
    echo "No project settings file found: $PROJECT_SETTINGS"
    echo "Nothing to uninstall"
    exit 0
fi

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    echo "Install with: brew install jq"
    exit 1
fi

# Step 1: Remove fullrun permissions
echo "[1/3] Removing permissions..."
project_script_pattern="Bash($(pwd)/.claude/fullrun/scripts/*.sh)"
before_count=$(jq '.permissions.allow // [] | length' "$PROJECT_SETTINGS" 2>/dev/null || echo "0")
jq --arg pattern "$project_script_pattern" '.permissions.allow = (.permissions.allow // [] | map(select(. != $pattern)))' "$PROJECT_SETTINGS" > "$PROJECT_SETTINGS.tmp" && \
mv "$PROJECT_SETTINGS.tmp" "$PROJECT_SETTINGS"
after_count=$(jq '.permissions.allow // [] | length' "$PROJECT_SETTINGS" 2>/dev/null || echo "0")
removed=$((before_count - after_count))
if [ "$removed" -gt 0 ]; then
    echo "      Removed $removed permission rule(s)"
else
    echo "      No permissions to remove"
fi

# Step 2: Remove fullrun hook from SessionStart
echo "[2/3] Removing SessionStart hook..."
has_session_start=$(jq 'has("hooks") and (.hooks | has("SessionStart"))' "$PROJECT_SETTINGS" 2>/dev/null || echo "false")

if [ "$has_session_start" = "true" ]; then
    # Filter out only the fullrun hook by name, preserve others
    jq '.hooks.SessionStart = (.hooks.SessionStart // [] | map(select(.name != "fullrun-auto-monitor")))' "$PROJECT_SETTINGS" > "$PROJECT_SETTINGS.tmp" && \
    mv "$PROJECT_SETTINGS.tmp" "$PROJECT_SETTINGS"

    # Check if SessionStart is now empty, if so remove the key entirely
    remaining_count=$(jq '.hooks.SessionStart | length' "$PROJECT_SETTINGS" 2>/dev/null || echo "0")
    if [ "$remaining_count" = "0" ]; then
        jq 'del(.hooks.SessionStart)' "$PROJECT_SETTINGS" > "$PROJECT_SETTINGS.tmp" && \
        mv "$PROJECT_SETTINGS.tmp" "$PROJECT_SETTINGS"
        echo "      Removed empty SessionStart section"
    else
        echo "      Removed fullrun hook, $remaining_count other hook(s) preserved"
    fi
else
    echo "      No SessionStart hooks found, skipping"
fi

# Validate JSON
if ! jq empty "$PROJECT_SETTINGS" 2>/dev/null; then
    echo "Error: Invalid JSON in $PROJECT_SETTINGS"
    exit 1
fi
echo "      JSON validation passed"

# Step 3: Remove installed files
echo "[3/3] Removing installed files..."

if [ -d "$PROJECT_CLAUDE_DIR/fullrun" ]; then
    rm -rf "$PROJECT_CLAUDE_DIR/fullrun"
    echo "      Removed: $PROJECT_CLAUDE_DIR/fullrun"
else
    echo "      Skipped: $PROJECT_CLAUDE_DIR/fullrun (not found)"
fi

# Clean up settings.local.json if it's empty or has only empty sections
# Check if permissions.allow is empty and hooks is empty or missing
is_empty=$(jq '((.permissions.allow // []) | length) == 0 and ((.hooks.SessionStart // []) | length) == 0' "$PROJECT_SETTINGS" 2>/dev/null || echo "false")
if [ "$is_empty" = "true" ]; then
    rm "$PROJECT_SETTINGS"
    echo "      Removed empty settings file: $PROJECT_SETTINGS"
fi

echo ""
echo "=== Uninstall Complete ==="
echo ""
echo "Project directory: $(pwd)"
echo "Settings file: $PROJECT_SETTINGS"
echo ""
echo "To reinstall, run: ./scripts/install.sh"
echo ""
