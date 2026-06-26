#!/bin/bash
# review-work — independent self-review via Claude CLI
# Usage: review-work "<task_summary>" --context <file_or_folder> [--skill <file_or_folder>]
#
# Sends work to a separate Claude instance for quality review.
# Claude reads all files itself (including images and PDFs) using its own tools.
# Returns issues with severity (critical/major/minor) and a PASS/FAIL verdict.
# Auto-logs issues to LESSONS.md when the review fails.
# Auto-includes LESSONS.md (if it exists) so the reviewer checks for repeat mistakes.

set -eo pipefail

LESSONS_FILE="${LESSONS_FILE:-$HOME/.openclaw/workspace/LESSONS.md}"

# --- Parse arguments ---

TASK=""
CONTEXT_PATH=""
SKILL_PATH=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --context)
      CONTEXT_PATH="$2"
      shift 2
      ;;
    --skill)
      SKILL_PATH="$2"
      shift 2
      ;;
    --help|-h)
      echo "Usage: review-work \"<task_summary>\" --context <file_or_folder> [--skill <file_or_folder>]"
      echo ""
      echo "Arguments:"
      echo "  task_summary          What the work was supposed to accomplish"
      echo "  --context <path>      File or folder to review (required)"
      echo "  --skill <path>        SKILL.md or skill folder used for the task (optional)"
      echo ""
      echo "Examples:"
      echo "  review-work \"Write a Python email validator\" --context /tmp/email.py"
      echo "  review-work \"Write an SEO blog\" --context /tmp/blog.md --skill ~/skills/seo-content-writer/SKILL.md"
      echo "  review-work \"Build a todo app\" --context /tmp/my-app/ --skill ~/skills/fullstack/SKILL.md"
      echo ""
      echo "Environment:"
      echo "  LESSONS_FILE    Path to lessons file (default: ~/.openclaw/workspace/LESSONS.md)"
      exit 0
      ;;
    *)
      if [ -z "$TASK" ]; then
        TASK="$1"
      else
        echo "Error: Unexpected argument: $1"
        echo "Usage: review-work \"<task_summary>\" --context <file_or_folder> [--skill <file_or_folder>]"
        exit 1
      fi
      shift
      ;;
  esac
done

if [ -z "$TASK" ]; then
  echo "Error: Task summary is required."
  echo "Usage: review-work \"<task_summary>\" --context <file_or_folder> [--skill <file_or_folder>]"
  exit 1
fi

if [ -z "$CONTEXT_PATH" ]; then
  echo "Error: --context is required."
  echo "Usage: review-work \"<task_summary>\" --context <file_or_folder> [--skill <file_or_folder>]"
  exit 1
fi

# Resolve to absolute path
CONTEXT_PATH=$(realpath "$CONTEXT_PATH" 2>/dev/null || echo "$CONTEXT_PATH")

if [ ! -e "$CONTEXT_PATH" ]; then
  echo "Error: Context path not found: $CONTEXT_PATH"
  exit 1
fi

# Resolve skill name to path if not a valid file/folder
# Accepts: "seo-content-writer", "seo-content-writer/SKILL.md", or full path
SKILLS_DIR="${SKILLS_DIR:-$HOME/.openclaw/workspace/skills}"
if [ -n "$SKILL_PATH" ] && [ ! -e "$SKILL_PATH" ]; then
  if [ -f "$SKILLS_DIR/$SKILL_PATH/SKILL.md" ]; then
    SKILL_PATH="$SKILLS_DIR/$SKILL_PATH"
  elif [ -f "$SKILLS_DIR/$SKILL_PATH" ]; then
    SKILL_PATH="$SKILLS_DIR/$SKILL_PATH"
  fi
fi

if [ -n "$SKILL_PATH" ]; then
  SKILL_PATH=$(realpath "$SKILL_PATH" 2>/dev/null || echo "$SKILL_PATH")
  if [ ! -e "$SKILL_PATH" ]; then
    echo "Warning: Skill path not found: $SKILL_PATH (continuing without skill context)"
    SKILL_PATH=""
  fi
fi

# Check if claude CLI is available
if ! command -v claude &> /dev/null; then
  echo "Error: claude CLI not found. Install with: npm install -g @anthropic-ai/claude-code"
  exit 1
fi

# --- Build prompts ---

# System prompt: static reviewer instructions (appended to Claude's defaults)
SYSTEM_PROMPT="You are a code and content reviewer. You can ONLY read files — never edit, write, or execute anything.

## How to review
1. Read ALL files at the given path. If it's a folder, read every file in it (skip node_modules, .git, __pycache__, dist, build, .next, vendor, venv, .cache directories). For images, view them. For PDFs, read them.
2. Review for: accuracy, completeness, quality, errors, and missed requirements.
3. If a skill definition is provided, use its requirements as the definition of done. Generate a verification checklist and check each item. A missing requirement is a major issue.
4. If a lessons file is provided, check if any past mistakes are repeated.
5. List every issue with severity:
   - **critical** — Blocks correctness or usability. Must fix.
   - **major** — Significant quality or completeness gap. Should fix.
   - **minor** — Style, polish, or optional improvement. Nice to fix.
6. End with a verdict line in exactly this format:
   VERDICT: PASS (if zero critical and zero major issues)
   VERDICT: FAIL — X critical, Y major, Z minor (if any critical or major issues exist)"

# User prompt: task-specific info
USER_PROMPT="Review the work at \`$CONTEXT_PATH\`.

**Original task:** ${TASK}"

if [ -n "$SKILL_PATH" ] && [ -e "$SKILL_PATH" ]; then
  USER_PROMPT="${USER_PROMPT}

**Skill definition:** \`$SKILL_PATH\` — read this and verify the work meets every requirement."
fi

if [ -f "$LESSONS_FILE" ]; then
  USER_PROMPT="${USER_PROMPT}

**Past mistakes:** \`$LESSONS_FILE\` — read this and check for repeat mistakes."
fi

# Run the review (read-only tools, no session persistence)
STDERR_LOG=$(mktemp /tmp/review-work-stderr.XXXXXX)
trap 'rm -f "$STDERR_LOG"' EXIT

set +e
REVIEW_OUTPUT=$(claude --print \
  --model sonnet \
  --dangerously-skip-permissions \
  --tools "Read,Glob,Grep" \
  --no-session-persistence \
  --append-system-prompt "$SYSTEM_PROMPT" \
  "$USER_PROMPT" 2>"$STDERR_LOG")
CLAUDE_EXIT=$?
set -e

if [ "$CLAUDE_EXIT" -ne 0 ] || [ -z "$REVIEW_OUTPUT" ]; then
  echo "Error: claude --print failed (exit code $CLAUDE_EXIT)."
  [ -n "$REVIEW_OUTPUT" ] && echo "$REVIEW_OUTPUT"
  [ -s "$STDERR_LOG" ] && cat "$STDERR_LOG"
  echo "Check your API key and network connection. Test with: claude --print 'hello'"
  exit 1
fi

# Print the review output
echo "$REVIEW_OUTPUT"

# Auto-log to LESSONS.md if the review failed
if echo "$REVIEW_OUTPUT" | grep -q "VERDICT: FAIL"; then
  VERDICT_LINE=$(echo "$REVIEW_OUTPUT" | grep "VERDICT: FAIL" | tail -1)
  DATE=$(date +%Y-%m-%d)

  # Extract critical and major issues (skip minor)
  ISSUES=$(echo "$REVIEW_OUTPUT" | grep -iE '(critical|major)\b' | grep -v 'VERDICT' | grep -v '0 critical' | grep -v '0 major' | head -10)

  # Create directory if needed
  LESSONS_DIR=$(dirname "$LESSONS_FILE")
  mkdir -p "$LESSONS_DIR"

  # Append learning entry (quoted heredoc prevents command injection from backticks in variables)
  {
    echo ""
    echo "### [$DATE] REVIEW-FAIL: $(basename "$CONTEXT_PATH")"
    echo ""
    printf 'TASK: %s\n' "$TASK"
    printf 'CONTEXT: %s\n' "$CONTEXT_PATH"
    printf '%s\n' "$VERDICT_LINE"
    echo "ISSUES:"
    printf '%s\n' "$ISSUES"
    echo ""
    echo "---"
  } >> "$LESSONS_FILE"
fi
