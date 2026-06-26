#!/bin/bash
# coding-with-cursor-ai.sh - Execute coding tasks using Cursor AI agent

# Exit on any error
set -e

# Parse input arguments
PROJECT_PATH=""
TASK=""
FILES=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --project)
      PROJECT_PATH="$2"
      shift 2
      ;;
    --task)
      TASK="$2"
      shift 2
      ;;
    --files)
      FILES="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required inputs
if [ -z "$PROJECT_PATH" ] || [ -z "$TASK" ]; then
  echo "Error: Both --project and --task are required."
  echo "Usage: $0 --project <path> --task <description> [--files <file-list>]"
  exit 1
fi

# Check if project directory exists
if [ ! -d "$PROJECT_PATH" ]; then
  echo "Error: Project directory not found: $PROJECT_PATH"
  exit 1
fi

# Change to project directory
cd "$PROJECT_PATH"

# Ensure Cursor CLI is available
if ! command -v cursor-agent &> /dev/null; then
  echo "Error: cursor-agent is not installed or not in PATH."
  echo "Please install Cursor CLI from https://cursor.com"  
  exit 1
fi

# Export API key if available
if [ -n "$CURSOR_API_KEY" ]; then
  export CURSOR_API_KEY
fi

# Create a temporary task file for Cursor
TASK_FILE="/tmp/cursor-task-$(date +%s).txt"
echo "# Task Request" > "$TASK_FILE"
echo "" >> "$TASK_FILE"
echo "## Project: $PROJECT_PATH" >> "$TASK_FILE"
echo "" >> "$TASK_FILE"
echo "## Task:" >> "$TASK_FILE"
echo "$TASK" >> "$TASK_FILE"

echo "" >> "$TASK_FILE"
echo "## Instructions:" >> "$TASK_FILE"
echo "- Make precise, minimal changes to accomplish the task." >> "$TASK_FILE"
echo "- Follow existing code style and patterns." >> "$TASK_FILE"
echo "- Add comments only if necessary for clarity." >> "$TASK_FILE"
echo "- Create new files if needed." >> "$TASK_FILE"
echo "- Commit message should start with 'feat:', 'fix:', or 'refactor:' based on task nature." >> "$TASK_FILE"

echo "" >> "$TASK_FILE"
echo "## Files to focus on:" >> "$TASK_FILE"
if [ -n "$FILES" ]; then
  echo "$FILES" | tr ',' '\n' | sed 's/^/  - /' >> "$TASK_FILE"
else
  echo "  - All relevant files" >> "$TASK_FILE"
fi

echo "" >> "$TASK_FILE"
echo "## Output:" >> "$TASK_FILE"
echo "- Generate a pull request summary at the end." >> "$TASK_FILE"
echo "- Confirm when task is completed." >> "$TASK_FILE"

echo "" >> "$TASK_FILE"
echo "---" >> "$TASK_FILE"
echo "Task created on $(date)" >> "$TASK_FILE"

echo "" >> "$TASK_FILE"

echo "Executing Cursor AI agent for task..."
echo "Project: $PROJECT_PATH"
echo "Task: $TASK"

echo ""

cursor-agent --task-file "$TASK_FILE" --project-root "$PROJECT_PATH"

# Cleanup
echo ""
echo "Task completed. Cleaning up temporary files..."
rm -f "$TASK_FILE"

echo ""
echo "Cursor AI agent task finished successfully."
