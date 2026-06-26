#!/usr/bin/env bash
# NOTE: On CIFS/SMB mounts, run with: bash git-bisect-example.sh
# Demonstrates automated git bisect to find the commit that introduced a bug
#
# Usage:
#   bash git-bisect-example.sh <good-ref> <bad-ref> <test-command>
#
# Examples:
#   bash git-bisect-example.sh v1.0.0 HEAD "npm test"
#   bash git-bisect-example.sh abc123 HEAD "node -e 'require(\"./dist\").validate(\"test\")'"
#   bash git-bisect-example.sh v2.0 main "python -m pytest tests/test_auth.py -x"

set -euo pipefail

GOOD_REF="${1:-}"
BAD_REF="${2:-HEAD}"
TEST_CMD="${3:-}"

if [ -z "$GOOD_REF" ] || [ -z "$TEST_CMD" ]; then
  echo "Usage: bash git-bisect-example.sh <good-ref> <bad-ref> <test-command>"
  echo ""
  echo "Arguments:"
  echo "  good-ref     A commit/tag where the code works correctly"
  echo "  bad-ref      A commit/tag where the bug exists (default: HEAD)"
  echo "  test-command  Command that exits 0 if OK, non-zero if bug present"
  echo ""
  echo "Examples:"
  echo "  bash git-bisect-example.sh v1.0.0 HEAD 'npm test'"
  echo "  bash git-bisect-example.sh abc123 main 'python -m pytest tests/ -x'"
  echo ""
  exit 1
fi

echo "========================================="
echo "  Git Bisect — Automated Bug Finder"
echo "========================================="
echo ""
echo "Good commit:  $GOOD_REF"
echo "Bad commit:   $BAD_REF"
echo "Test command: $TEST_CMD"
echo ""

# Ensure we're in a git repo
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  echo "ERROR: Not inside a git repository."
  exit 1
fi

# Check for uncommitted changes
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "WARNING: You have uncommitted changes."
  echo "Stashing changes before bisect..."
  git stash push -m "bisect-auto-stash"
  STASHED=true
else
  STASHED=false
fi

# Start bisect
echo ""
echo "Starting bisect..."
git bisect start "$BAD_REF" "$GOOD_REF"

# Create a temporary test script that handles build + test
BISECT_SCRIPT=$(mktemp /tmp/bisect-test-XXXXXX.sh)
cat > "$BISECT_SCRIPT" << SCRIPTEOF
#!/usr/bin/env bash
set -e

# If there's a build step, try it (but skip commit if build fails)
if [ -f "package.json" ] && grep -q '"build"' package.json 2>/dev/null; then
  npm run build 2>/dev/null || exit 125  # 125 = skip this commit
fi

if [ -f "Makefile" ] && grep -q '^build:' Makefile 2>/dev/null; then
  make build 2>/dev/null || exit 125
fi

# Run the actual test
$TEST_CMD
SCRIPTEOF
chmod +x "$BISECT_SCRIPT" 2>/dev/null || true

echo "Running automated bisect..."
echo ""

# Run bisect with the test script
git bisect run bash "$BISECT_SCRIPT"

# Capture the result
RESULT=$?

echo ""
echo "========================================="
if [ $RESULT -eq 0 ]; then
  echo "  Bisect complete!"
  echo ""
  echo "  First bad commit:"
  git bisect log | tail -1
  echo ""
  echo "  Commit details:"
  git log --oneline -1
else
  echo "  Bisect encountered an error (exit code: $RESULT)"
fi
echo "========================================="

# Clean up
rm -f "$BISECT_SCRIPT"
git bisect reset

# Restore stashed changes
if [ "$STASHED" = true ]; then
  echo ""
  echo "Restoring stashed changes..."
  git stash pop
fi

echo ""
echo "Done. Working tree restored to original state."
