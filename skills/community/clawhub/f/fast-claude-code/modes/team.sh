#!/bin/bash
# Team Mode - Start a Claude Code team session with callback
# Usage: team.sh --project <path> --template <name> --task <description> [--callback <type>]
#
# This script is called by OpenClaw after selecting the appropriate template.
# It does NOT auto-select templates - that's done by OpenClaw (LLM).
#
# Flow:
#   User → OpenClaw (LLM) → Understands task → Selects template → Calls this script
#                                                    ↓
#                           team.sh --template xxx --task "xxx"
#                                                    ↓
#                                     Installs hooks + Generates spawn prompt

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$BASE_DIR/templates"

# Default values
PROJECT_DIR=""
TASK=""
TEMPLATE=""
CALLBACK="openclaw"
SESSION_KEY=""
PERMISSION_MODE="auto"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --project)
            PROJECT_DIR="$2"
            shift 2
            ;;
        --task)
            TASK="$2"
            shift 2
            ;;
        --template)
            TEMPLATE="$2"
            shift 2
            ;;
        --callback)
            CALLBACK="$2"
            shift 2
            ;;
        --session-key)
            SESSION_KEY="$2"
            shift 2
            ;;
        --permission-mode)
            PERMISSION_MODE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$PROJECT_DIR" ]]; then
    echo "Error: --project is required"
    exit 1
fi

if [[ -z "$SESSION_KEY" ]]; then
    echo "Error: --session-key is required"
    exit 1
fi

# Validate permission mode
if [[ "$PERMISSION_MODE" != "plan" && "$PERMISSION_MODE" != "auto" ]]; then
    echo "Error: --permission-mode must be 'plan' or 'auto'"
    exit 1
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}ℹ${NC} $*"
}

log_success() {
    echo -e "${GREEN}✅${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}⚠️${NC} $*"
}

log_error() {
    echo -e "${RED}❌${NC} $*"
}

# Expand ~ to home directory
PROJECT_DIR="${PROJECT_DIR/#\~/$HOME}"

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "Error: Project directory does not exist: $PROJECT_DIR"
    exit 1
fi

# Set default template if not specified
if [[ -z "$TEMPLATE" ]]; then
    if [[ -n "$TASK" ]]; then
        # Task provided but no template - OpenClaw should have chosen one
        # Use parallel-review as safe default
        TEMPLATE="parallel-review"
        log_warn "No template specified, using 'parallel-review' as default."
        log_warn "Tip: Let OpenClaw choose the template based on your task."
    else
        # No task and no template - use parallel-review as default
        TEMPLATE="parallel-review"
        log_info "No template specified, using 'parallel-review' as default."
    fi
fi

# Check if CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS is set
if [[ -z "${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:-}" ]]; then
    log_warn "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS is not set"
    log_warn "Team mode may not work without it"
    log_warn "Run: export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1"
    echo ""
fi

# Check if jq is available (required for hooks)
if ! command -v jq &> /dev/null; then
    log_error "jq is required for Team mode but not installed"
    log_error "Install: brew install jq  (macOS)"
    log_error "        sudo apt-get install jq  (Ubuntu/Debian)"
    exit 1
fi

log_info "Starting Team mode..."
log_info "Project: $PROJECT_DIR"
log_info "Template: $TEMPLATE"
log_info "Permission mode: $PERMISSION_MODE"
log_info ""

if [[ "$PERMISSION_MODE" == "auto" ]]; then
    log_warn "⚠️  Auto mode uses --dangerously-skip-permissions"
fi

# Install hooks for team completion detection
log_info "Installing completion hooks..."
HOOKS_DIR="$PROJECT_DIR/.claude/hooks"
mkdir -p "$HOOKS_DIR"

# Settings file path (used regardless of whether hooks are already installed)
SETTINGS_FILE="$PROJECT_DIR/.claude/settings.json"

# Create unique session name for this team run
SESSION="cc-team-$(date +%s)"

echo "[DEBUG] $(date): Creating tmux session $SESSION" >> /tmp/team-debug.log

# Create on-stop hook
# Use unquoted heredoc so $BASE_DIR gets substituted with actual path
# Disable nounset for heredoc parsing (variables like $1 are from case statement)
set +u
cat > "$HOOKS_DIR/on-stop.sh" << EOF
#!/bin/bash
# Team completion detection hook
# This hook fires when Claude Code stops

TMUX_SESSION="${SESSION}"

# 读取 tmux 输出
OUTPUT=\$(tmux -L "cc" capture-pane -p -S -10 -t "\$TMUX_SESSION" 2>/dev/null || echo "")

# 检查是否有 session marker，如果有只检测之后的内容
if grep -q "=== START \${TMUX_SESSION} ===" <<< "\$OUTPUT"; then
    OUTPUT=\$(sed -n "/=== START \${TMUX_SESSION} ===/,\\\$p" <<< "\$OUTPUT")
fi

# 检测 marker
if ! grep -q "CC_CALLBACK_DONE" <<< "\$OUTPUT"; then
    # 中途 stop → 忽略
    echo "Intermediate stop, ignoring"
    exit 0
fi

# 最终完成 → 调 callback
CALLBACK_SCRIPT="$BASE_DIR/callbacks/$CALLBACK.sh"

INPUT=\$(cat)
SESSION_ID=\$(echo "\$INPUT" | jq -r '.session_id // "unknown"')
CWD=\$(echo "\$INPUT" | jq -r '.cwd // "unknown"')

# Read original task from file (saved by team.sh)
if [[ -f ".claude/team-task.txt" ]]; then
    ORIGINAL_TASK=\$(cat ".claude/team-task.txt")
else
    ORIGINAL_TASK="\$CWD"
fi

# List all non-hidden files and directories (expand folders)
TEAM_OUTPUTS="Team 任务完成！\n项目目录: \$CWD\n\n文件列表：\n\n"

MAX_FILE_COUNT=20
FILE_COUNT=0

# Function to list files recursively (max 3 levels deep, 200 files total)
list_dir() {
    local dir="\$1"
    local indent="\$2"
    local depth="\$3"
    if [[ "\$depth" -ge 3 ]] || [[ "\$FILE_COUNT" -ge "\$MAX_FILE_COUNT" ]]; then
        return
    fi
    for item in "\$dir"/*; do
        if [[ "\$FILE_COUNT" -ge "\$MAX_FILE_COUNT" ]]; then
            break
        fi
        if [[ -e "\$item" ]]; then
            FILE_COUNT=\$((FILE_COUNT + 1))
            name=\$(basename "\$item")
            if [[ -d "\$item" ]]; then
                TEAM_OUTPUTS="\$TEAM_OUTPUTS\${indent}📁 \$name/\n"
                list_dir "\$item" "  \$indent" "\$((depth + 1))"
            else
                size=\$(stat -f %z -- "\$item" 2>/dev/null || stat --format=%s -- "\$item" 2>/dev/null || echo "?")
                TEAM_OUTPUTS="\$TEAM_OUTPUTS\${indent}📄 \$name (\$size bytes)\n"
            fi
        fi
    done
}

list_dir "\$CWD" "" 0

if [[ "\$FILE_COUNT" -ge "\$MAX_FILE_COUNT" ]]; then
    TEAM_OUTPUTS="\$TEAM_OUTPUTS\n(文件数量已达上限 \$MAX_FILE_COUNT，更多文件未显示)\n"
fi

# Trigger callback with file list
"\$CALLBACK_SCRIPT" \
    --status done \
    --mode team \
    --task "team-session-\$SESSION_ID" \
    --message "\$ORIGINAL_TASK" \
    --output "\$TEAM_OUTPUTS" \
    --session-key "$SESSION_KEY"
# Cleanup: Remove team hooks after callback completes
# 1. Delete on-stop.sh hook file
rm -f ".claude/hooks/on-stop.sh"

# 2. Clean up settings.json - remove on-stop.sh references
if [ -f ".claude/settings.json" ] && command -v jq &> /dev/null; then
    if jq -e '.. | objects | select(.command? == ".claude/hooks/on-stop.sh")' ".claude/settings.json" > /dev/null 2>&1; then
        jq '.hooks.Stop |= (map(.hooks |= map(select(.command != ".claude/hooks/on-stop.sh"))))' ".claude/settings.json" > ".claude/settings.json.tmp" 2>/dev/null && \\
            mv ".claude/settings.json.tmp" ".claude/settings.json"
    fi
fi

# 3. Remove team task file
rm -f ".claude/team-task.txt"
EOF

chmod +x "$HOOKS_DIR/on-stop.sh"
# Re-enable nounset
set -u

# Create or update .claude/settings.json with hooks configuration (always run, not just on fresh install)
HOOKS_CONFIG=$(cat <<'HOOKSJSON'
{
  "Stop": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": ".claude/hooks/on-stop.sh"
        }
      ]
    }
  ]
}
HOOKSJSON
)

mkdir -p "$PROJECT_DIR/.claude"

# Upsert Stop hook in settings.json
if [ -f "$SETTINGS_FILE" ]; then
    # Settings file exists, merge Stop hook (replace entire Stop array)
    jq --argjson newHooks "$HOOKS_CONFIG" '
    .hooks = (.hooks // {}) |
    .hooks.Stop = $newHooks.Stop
    ' "$SETTINGS_FILE" > "$SETTINGS_FILE.tmp"
    mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"
    log_success "Upserted Stop hook"
else
    # No settings file, create fresh
    jq -n --argjson newHooks "$HOOKS_CONFIG" '
    {hooks: {Stop: $newHooks.Stop}}
    ' > "$SETTINGS_FILE"
    log_success "Created settings with Stop hook"
fi

log_success "Hooks installed to $HOOKS_DIR/"
log_info "Settings updated: $SETTINGS_FILE"
log_info ""

# Generate spawn prompt based on task
SPAWN_PROMPT=""
if [[ -n "$TASK" ]]; then
    log_info "Starting Claude Code in Team mode..."
    log_info "Task: $TASK"
    log_info "Template: $TEMPLATE"
    log_info "Main Session: $SESSION"
    log_info ""

    # Get template-specific spawn prompt
    if [[ -f "$TEMPLATES_DIR/$TEMPLATE.sh" ]]; then
        SPAWN_PROMPT=$(bash "$TEMPLATES_DIR/$TEMPLATE.sh")
        # Substitute variables using sed (handles special chars correctly)
        SPAWN_PROMPT=$(echo "$SPAWN_PROMPT" | sed "s/\${TASK_DESCRIPTION}/$TASK/g")
        SPAWN_PROMPT=$(echo "$SPAWN_PROMPT" | sed "s|\${TARGET_DIR}|$PROJECT_DIR|g")
        # Integrate CC_CALLBACK_DONE into the final reporting step
        # Replace "Report completion with summary" with instructions to output marker
        SPAWN_PROMPT=$(echo "$SPAWN_PROMPT" | sed "s/Report completion with summary/Report completion with summary. ⚠️ CRITICAL: After reporting, you MUST output exactly CC_CALLBACK_DONE on its own line./")
        # Add Session Id
        SPAWN_PROMPT=$(echo -e "$SPAWN_PROMPT\n\n=== START ${SESSION} ===")
    else
        log_warn "Template not found: $TEMPLATE, using default"
        SPAWN_PROMPT="I need to complete a complex task using a team approach.

Task: ${TASK}
Target: ${PROJECT_DIR}

Template approach: ${TEMPLATE}

Please spawn a team to handle this task efficiently. Consider:
1. What roles/teammates are needed for this task
2. How to divide the work to avoid conflicts
3. What each teammate should focus on
4. How to coordinate and synthesize results

Use delegate mode: I coordinate, teammates execute.

When ready, spawn the team and begin working on the task.

⚠️ CRITICAL INSTRUCTION: After completing the task and reporting the summary, you MUST output exactly CC_CALLBACK_DONE on its own line. This is required for automated completion detection."

        SPAWN_PROMPT=$(echo -e "$SPAWN_PROMPT\n\n=== START ${SESSION} ===")
    fi

    log_info "Spawning team..."
    log_info ""
else
    log_error "Error: --task is required for Team mode"
    log_info "Team mode requires a task description to spawn the team."
    exit 1
fi

# Change to project directory
cd "$PROJECT_DIR"

# DEBUG: Log start
echo "[DEBUG] $(date): Team mode starting" >> /tmp/team-debug.log
echo "[DEBUG] PROJECT_DIR=$PROJECT_DIR" >> /tmp/team-debug.log
echo "[DEBUG] TEMPLATE=$TEMPLATE" >> /tmp/team-debug.log
echo "[DEBUG] TASK=$TASK" >> /tmp/team-debug.log
echo "[DEBUG] PERMISSION_MODE=$PERMISSION_MODE" >> /tmp/team-debug.log

# Execute team spawn using tmux (PTY mode required for agent teams)
log_info "Team will work on the task and exit when complete."
log_info "Completion will be detected by hooks automatically."
log_info ""
log_info "⏳ Team execution in progress (this may take some time)..."
log_info "    No output during this time is normal - agents are working."
log_info ""

# Save original task for callback
echo "$TASK" > "$PROJECT_DIR/.claude/team-task.txt"

TMUX_SERVER="cc"

# Kill existing session if any
tmux -L "$TMUX_SERVER" kill-session -t "$SESSION" 2>/dev/null || true

# Create tmux session in project directory
tmux -L "$TMUX_SERVER" new-session -d -s "$SESSION" -c "$PROJECT_DIR"
sleep 0.5

echo "[DEBUG] $(date): Tmux session created, starting Claude Code" >> /tmp/team-debug.log

# Start Claude Code (same as interactive.sh)
if [[ "$PERMISSION_MODE" == "auto" ]]; then
    CLAUDE_CMD="claude --dangerously-skip-permissions"
    echo "[DEBUG] CLAUDE_CMD=$CLAUDE_CMD" >> /tmp/team-debug.log

    tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" "$CLAUDE_CMD" Enter
    sleep 4

    # Auto-accept safety confirmation
    OUTPUT=$(tmux -L "$TMUX_SERVER" capture-pane -p -t "$SESSION" 2>>/tmp/team-debug.log || echo "")
    echo "[DEBUG] $(date): Initial output captured" >> /tmp/team-debug.log
    echo "[DEBUG] Output: $OUTPUT" >> /tmp/team-debug.log
    
    # Check for new version: bypass permissions prompt (v2.0+)
    if grep -q "bypass permissions" <<< "$OUTPUT"; then
        log_info "Auto-accepting permissions with 'y'..."
        tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" "y"
        sleep 0.5
        tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" Enter
        sleep 5
    # Check for old version: "Yes, I trust this folder" (v1.x)
    elif grep -q "Yes, I trust this folder" <<< "$OUTPUT"; then
        log_info "Auto-accepting permissions with '1'..."
        tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" 1
        sleep 0.5
        tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" Enter
        sleep 5
    fi
else
    CLAUDE_CMD="claude --permission-mode $PERMISSION_MODE"
    echo "[DEBUG] CLAUDE_CMD=$CLAUDE_CMD" >> /tmp/team-debug.log

    tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" "$CLAUDE_CMD" Enter
    sleep 4
fi

# Send spawn prompt via temp file (handles multi-line)
TMPFILE=$(mktemp /tmp/cc-spawn-XXXXXX.txt)
printf '%s' "$SPAWN_PROMPT" > "$TMPFILE"
tmux -L "$TMUX_SERVER" load-buffer "$TMPFILE"
tmux -L "$TMUX_SERVER" paste-buffer -t "$SESSION"
rm -f "$TMPFILE"
sleep 0.3
tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" Enter

echo "[DEBUG] $(date): Spawn prompt sent, exiting" >> /tmp/team-debug.log

log_info "✅ Team spawn prompt sent"

# Exit immediately - hook will handle callback and cleanup on completion
log_success "Team started in background. Callback will notify on completion."
exit 0
