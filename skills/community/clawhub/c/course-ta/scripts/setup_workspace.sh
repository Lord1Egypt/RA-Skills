#!/usr/bin/env bash
# Setup script for Course TA skill
# Creates workspace directories, config, and AGENTS.md on macOS (Mac Mini)

set -euo pipefail

# Resolve workspace directory
if [ -n "${OPENCLAW_WORKSPACE_DIR:-}" ]; then
  WORKSPACE="$OPENCLAW_WORKSPACE_DIR"
else
  WORKSPACE="$HOME/.openclaw/workspace"
fi

echo "==> Using workspace: $WORKSPACE"

# Create memory directory (course materials go here directly, not in subdirectories)
MEMORY_DIR="$WORKSPACE/memory"
mkdir -p "$MEMORY_DIR"
echo "==> Created $MEMORY_DIR"

# Create course-ta.json config if not present
CONFIG_FILE="$WORKSPACE/course-ta.json"
if [ ! -f "$CONFIG_FILE" ]; then
  cat > "$CONFIG_FILE" << 'JSONEOF'
{
  "allowed_channels": [],
  "course_name": "AI Essentials",
  "professor_name": "Professor",
  "semester": "Spring 2026"
}
JSONEOF
  echo "==> Created $CONFIG_FILE (edit with your channel IDs and course info)"
else
  echo "==> $CONFIG_FILE already exists, skipping"
fi

# Create or update AGENTS.md
AGENTS_FILE="$WORKSPACE/AGENTS.md"
if [ ! -f "$AGENTS_FILE" ]; then
  cat > "$AGENTS_FILE" << 'MDEOF'
# Agent Instructions

## Role

You are a course teaching assistant. Your primary function is to help students understand course material by answering questions based on indexed course documents.

## Behavior

- Always search memory before answering course-related questions.
- Only provide information grounded in course materials.
- Be helpful, patient, and pedagogical.
- Do not provide direct answers to homework or exams.
- Do not discuss grades or evaluation criteria.
- Refuse off-topic requests politely.
- Respond in the student's language (default English, Chinese if asked in Chinese).

## Channel Policy

Check `course-ta.json` in the workspace root for allowed Discord channel IDs. If the file lists specific channels, only respond in those channels.
MDEOF
  echo "==> Created $AGENTS_FILE"
else
  echo "==> $AGENTS_FILE already exists, skipping (check it includes TA instructions)"
fi

echo ""
echo "Setup complete. Next steps:"
echo "  1. Place course materials (PDF, PPTX, MD) directly in: $MEMORY_DIR"
echo "  2. Run: openclaw memory index --force"
echo "  3. Edit $CONFIG_FILE with your Discord channel IDs and course info"
echo "  4. Ensure your Discord bot permissions are set (see references/setup-guide.md)"
