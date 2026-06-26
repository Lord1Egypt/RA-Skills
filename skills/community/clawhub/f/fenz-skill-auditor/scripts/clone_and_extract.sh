#!/usr/bin/env bash
# clone_and_extract.sh - Clone a GitHub repo and find all SKILL.md files
# Usage: clone_and_extract.sh <github-repo-url>
# Exit codes: 0=success, 1=bad args, 2=clone failed, 3=no SKILL.md found

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Error: Missing repository URL" >&2
  echo "Usage: $0 <github-repo-url>" >&2
  exit 1
fi

REPO_URL="$1"

# Validate GitHub URL
if ! echo "$REPO_URL" | grep -qE '^https?://github\.com/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+'; then
  echo "Error: Invalid GitHub URL: $REPO_URL" >&2
  echo "Expected format: https://github.com/<owner>/<repo>" >&2
  exit 1
fi

# Clean trailing .git or slashes
REPO_URL="${REPO_URL%.git}"
REPO_URL="${REPO_URL%/}"

# Create temp directory
TEMP_DIR=$(mktemp -d)
trap 'echo "Temp dir: $TEMP_DIR (cleanup is caller responsibility)" >&2' EXIT

echo "Cloning $REPO_URL (shallow)..." >&2

if ! git clone --depth 1 "$REPO_URL" "$TEMP_DIR/repo" 2>&1 | sed 's/^/  /' >&2; then
  echo "Error: Failed to clone repository" >&2
  rm -rf "$TEMP_DIR"
  exit 2
fi

# Find all SKILL.md files
SKILL_FILES=$(find "$TEMP_DIR/repo" -name "SKILL.md" -type f 2>/dev/null)

if [ -z "$SKILL_FILES" ]; then
  echo "Error: No SKILL.md files found in repository" >&2
  rm -rf "$TEMP_DIR"
  exit 3
fi

# Count skills found
SKILL_COUNT=$(echo "$SKILL_FILES" | wc -l | tr -d ' ')
echo "Found $SKILL_COUNT SKILL.md file(s)" >&2

# Output JSON with skill file paths (relative to repo root)
echo "{"
echo "  \"temp_dir\": \"$TEMP_DIR/repo\","
echo "  \"skill_count\": $SKILL_COUNT,"
echo "  \"skills\": ["

FIRST=true
while IFS= read -r skill_path; do
  # Get path relative to repo root
  REL_PATH="${skill_path#$TEMP_DIR/repo/}"
  # Get the directory containing SKILL.md
  SKILL_DIR=$(dirname "$REL_PATH")
  # Extract skill name from SKILL.md frontmatter if possible
  SKILL_NAME=$(grep -A5 '^---' "$skill_path" | grep '^name:' | sed 's/^name:[[:space:]]*//' | head -1)
  if [ -z "$SKILL_NAME" ]; then
    SKILL_NAME=$(basename "$SKILL_DIR")
  fi

  if [ "$FIRST" = true ]; then
    FIRST=false
  else
    echo ","
  fi

  printf '    {"name": "%s", "path": "%s", "dir": "%s"}' "$SKILL_NAME" "$REL_PATH" "$SKILL_DIR"
done <<< "$SKILL_FILES"

echo ""
echo "  ]"
echo "}"
