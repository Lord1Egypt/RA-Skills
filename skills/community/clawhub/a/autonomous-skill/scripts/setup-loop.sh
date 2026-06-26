#!/bin/bash
#
# Autonomous Skill - Loop Setup Script
# Creates state file for in-session hook-based autonomous loop.
# Called by SKILL.md when user wants hook mode instead of headless mode.
#
# Usage:
#   setup-loop.sh "task description" [OPTIONS]
#
# Options:
#   --mode structured|lightweight    Loop mode (default: structured)
#   --max-iterations N               Max iterations (default: 0 = unlimited)
#   --completion-promise TEXT        Promise phrase (default: DONE)
#   --task-name NAME                 Explicit task name
#

set -euo pipefail

# ── Parse arguments ────────────────────────────────────────────────────
PROMPT_PARTS=()
MAX_ITERATIONS=0
COMPLETION_PROMISE="DONE"
MODE="structured"
TASK_NAME=""

while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      cat <<'EOF'
Autonomous Loop Setup

Usage:
  setup-loop.sh "task description" [OPTIONS]

Options:
  --mode structured|lightweight  Loop mode (default: structured)
  --max-iterations N             Max iterations (0 = unlimited)
  --completion-promise TEXT       Promise phrase (default: DONE)
  --task-name NAME               Explicit task name

Modes:
  structured   - Full task decomposition with task_list.md tracking
  lightweight  - Same prompt repeated, Ralph-style iteration
EOF
      exit 0
      ;;
    --max-iterations)
      [[ -z "${2:-}" ]] && { echo "Error: --max-iterations requires a number" >&2; exit 1; }
      MAX_ITERATIONS="$2"; shift 2 ;;
    --completion-promise)
      [[ -z "${2:-}" ]] && { echo "Error: --completion-promise requires text" >&2; exit 1; }
      COMPLETION_PROMISE="$2"; shift 2 ;;
    --mode)
      [[ -z "${2:-}" ]] && { echo "Error: --mode requires structured or lightweight" >&2; exit 1; }
      MODE="$2"; shift 2 ;;
    --task-name)
      [[ -z "${2:-}" ]] && { echo "Error: --task-name requires a name" >&2; exit 1; }
      TASK_NAME="$2"; shift 2 ;;
    *)
      PROMPT_PARTS+=("$1"); shift ;;
  esac
done

PROMPT="${PROMPT_PARTS[*]}"

if [[ -z "$PROMPT" ]]; then
  echo "Error: No task description provided" >&2
  echo "Usage: setup-loop.sh \"Your task description\" [OPTIONS]" >&2
  exit 1
fi

# Generate task name if not provided
if [[ -z "$TASK_NAME" ]]; then
  TASK_NAME=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | cut -c1-30 | sed 's/^-//' | sed 's/-$//')
  [[ -z "$TASK_NAME" ]] && TASK_NAME="task-$(date +%Y%m%d-%H%M%S)"
fi

TASK_DIR=".autonomous/$TASK_NAME"

# Set up task directory for structured mode
if [[ "$MODE" == "structured" ]]; then
  mkdir -p "$TASK_DIR/sessions"
fi

# Create state file
mkdir -p .claude

# Quote values for YAML
if [[ -n "$COMPLETION_PROMISE" ]]; then
  PROMISE_YAML="\"$COMPLETION_PROMISE\""
else
  PROMISE_YAML="null"
fi

cat > .claude/autonomous-loop.local.md <<EOF
---
active: true
iteration: 1
max_iterations: $MAX_ITERATIONS
completion_promise: $PROMISE_YAML
mode: $MODE
task_name: "$TASK_NAME"
task_dir: "$TASK_DIR"
started_at: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
---

$PROMPT
EOF

# Output setup message
cat <<EOF
Autonomous loop activated in this session.

Mode: $MODE
Task: $TASK_NAME
Iteration: 1
Max iterations: $(if [[ $MAX_ITERATIONS -gt 0 ]]; then echo $MAX_ITERATIONS; else echo "unlimited"; fi)
Completion: output <promise>$COMPLETION_PROMISE</promise> when genuinely done

The stop hook is now active. When you try to exit, the same prompt
will be fed back. Your previous work persists in files, creating an
iterative improvement loop.

To cancel: delete .claude/autonomous-loop.local.md

EOF

# Build the prompt with mode-appropriate context
if [[ "$MODE" == "structured" ]]; then
  if [[ -f "$TASK_DIR/task_list.md" ]]; then
    echo "Continuing structured task. Read $TASK_DIR/task_list.md and $TASK_DIR/progress.md for current state."
  else
    echo "New structured task. Create $TASK_DIR/task_list.md with phased sub-tasks, then begin work."
  fi
  echo ""
  echo "Task directory: $TASK_DIR"
else
  echo "Lightweight mode: iterate on the task until complete."
fi

echo ""
echo "When ALL work is complete and verified, output:"
echo "  <promise>$COMPLETION_PROMISE</promise>"
echo ""
echo "ONLY output the promise when it is genuinely true. Do not lie to exit the loop."
echo ""
echo "$PROMPT"
