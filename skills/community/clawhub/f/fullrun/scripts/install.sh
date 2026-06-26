#!/bin/bash

# Fullrun - Install Script
# Sets up fullrun skill in the current project directory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FULLRUN_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_CLAUDE_DIR="$(pwd)/.claude"
PROJECT_SETTINGS="$PROJECT_CLAUDE_DIR/settings.local.json"

echo "=== Fullrun Skill - Project Setup ==="
echo ""

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    echo "Install with: brew install jq"
    exit 1
fi

# Create .claude directory in project
echo "[1/4] Creating .claude directory in project..."
mkdir -p "$PROJECT_CLAUDE_DIR"

# Create symlink to scripts or copy them
echo "[2/4] Setting up scripts..."
if [ -d "$PROJECT_CLAUDE_DIR/fullrun" ]; then
    echo "      Project scripts already exist, skipping"
else
    mkdir -p "$PROJECT_CLAUDE_DIR/fullrun/scripts"
    cp "$FULLRUN_DIR/scripts/main.sh" "$PROJECT_CLAUDE_DIR/fullrun/scripts/"
    cp "$FULLRUN_DIR/scripts/fullrun.sh" "$PROJECT_CLAUDE_DIR/fullrun/scripts/"
    cp "$FULLRUN_DIR/scripts/cron-manager.sh" "$PROJECT_CLAUDE_DIR/fullrun/scripts/"
    chmod +x "$PROJECT_CLAUDE_DIR/fullrun/scripts"/*.sh
    echo "      Copied scripts to: $PROJECT_CLAUDE_DIR/fullrun/scripts/"
fi

# Create or update project settings.local.json
echo "[3/4] Configuring project settings..."

# Create settings.local.json if it doesn't exist
if [ ! -f "$PROJECT_SETTINGS" ]; then
    echo '{}' > "$PROJECT_SETTINGS"
    echo "      Created: $PROJECT_SETTINGS"
else
    echo "      Found existing: $PROJECT_SETTINGS"
fi

# Add permissions for project scripts
current_allow=$(jq -r '.permissions.allow // [] | .[]' "$PROJECT_SETTINGS" 2>/dev/null || echo "")
project_script_pattern="Bash($PROJECT_CLAUDE_DIR/fullrun/scripts/*.sh)"

if ! echo "$current_allow" | grep -qF "$project_script_pattern"; then
    jq --arg pattern "$project_script_pattern" '.permissions.allow += [$pattern]' "$PROJECT_SETTINGS" > "$PROJECT_SETTINGS.tmp" && \
    mv "$PROJECT_SETTINGS.tmp" "$PROJECT_SETTINGS"
    echo "      Added permission: $project_script_pattern"
else
    echo "      Permission already exists, skipping"
fi

# Add SessionStart hook for auto-monitoring
# The hook checks for checklist.md and .claude-status.txt in current directory at runtime
# Build hook JSON using jq to ensure proper escaping
HOOK_NAME="fullrun-auto-monitor"
HOOK_COMMAND="if [ -f \"\$(pwd)/checklist.md\" ] && [ ! -f \"\$(pwd)/.claude-status.txt\" ]; then echo \"Starting fullrun monitoring...\" && $PROJECT_CLAUDE_DIR/fullrun/scripts/main.sh start 2>/dev/null || true; fi"

has_session_start=$(jq 'has("hooks") and (.hooks | has("SessionStart"))' "$PROJECT_SETTINGS" 2>/dev/null || echo "false")
has_fullrun_hook=$(jq --arg name "$HOOK_NAME" '.hooks.SessionStart // [] | map(.name // "") | index($name) != null' "$PROJECT_SETTINGS" 2>/dev/null || echo "false")

if [ "$has_fullrun_hook" = "true" ]; then
    echo "      Fullrun hook already exists, skipping"
elif [ "$has_session_start" = "true" ] && [ "$(jq '.hooks.SessionStart | length' "$PROJECT_SETTINGS" 2>/dev/null)" -gt 0 ]; then
    # Append to existing SessionStart
    jq --arg name "$HOOK_NAME" --arg cmd "$HOOK_COMMAND" \
       '.hooks.SessionStart += [{"name": $name, "hooks": [{"type": "command", "command": $cmd, "timeout": 10, "statusMessage": "Initializing fullrun task executor"}]}]' \
       "$PROJECT_SETTINGS" > "$PROJECT_SETTINGS.tmp" && \
    mv "$PROJECT_SETTINGS.tmp" "$PROJECT_SETTINGS"
    echo "      Appended hook to existing SessionStart"
else
    # Create new SessionStart array
    jq --arg name "$HOOK_NAME" --arg cmd "$HOOK_COMMAND" \
       '.hooks.SessionStart = [{"name": $name, "hooks": [{"type": "command", "command": $cmd, "timeout": 10, "statusMessage": "Initializing fullrun task executor"}]}]' \
       "$PROJECT_SETTINGS" > "$PROJECT_SETTINGS.tmp" && \
    mv "$PROJECT_SETTINGS.tmp" "$PROJECT_SETTINGS"
    echo "      Created SessionStart with hook"
fi

# Validate JSON
echo "[4/4] Validating settings..."
if ! jq empty "$PROJECT_SETTINGS" 2>/dev/null; then
    echo "Error: Invalid JSON in $PROJECT_SETTINGS"
    exit 1
fi
echo "      JSON validation passed"

echo ""
echo "=== Project Setup Complete ==="
echo ""
echo "Project directory: $(pwd)"
echo "Settings file: $PROJECT_SETTINGS"
echo "Scripts directory: $PROJECT_CLAUDE_DIR/fullrun/scripts/"
echo ""
echo "Usage in this project:"
echo "  /fullrun - Start task execution"
echo "  ./.claude/fullrun/scripts/main.sh start - Start background monitoring"
echo "  ./.claude/fullrun/scripts/main.sh status - Check status"
echo ""
echo "To uninstall from this project, run: ./scripts/uninstall.sh"
echo ""
