#!/bin/bash
#
# CtrlZ Skill Demo
#

CTRLZ="$HOME/.openclaw/skills/ctrlz/scripts/ctrlz.sh"
TEST_DIR="/tmp/ctrlz_demo_$$"

echo "=== CtrlZ Skill Feature Test ==="
echo ""

# Use separate database
export CTRLZ_DB="$TEST_DIR/undo.db"
mkdir -p "$TEST_DIR"

echo "1. Initialize database..."
bash "$CTRLZ" init
echo ""

echo "2. Create test file..."
echo "This is original content" > "$TEST_DIR/myfile.txt"
cat "$TEST_DIR/myfile.txt"
echo ""

echo "3. Start Undo Session..."
SESSION=$(bash "$CTRLZ" start "Modify myfile.txt" | jq -r '.session_id')
echo "Session ID: $SESSION"
echo ""

echo "4. Record operation to be performed..."
bash "$CTRLZ" record "$SESSION" file_edit "$TEST_DIR/myfile.txt"
echo ""

echo "5. Execute actual modification..."
echo "This is modified content" > "$TEST_DIR/myfile.txt"
cat "$TEST_DIR/myfile.txt"
echo ""

echo "6. View undoable operations..."
bash "$CTRLZ" list
echo ""

echo "7. Execute undo (CtrlZ)..."
bash "$CTRLZ" undo
echo ""

echo "8. Verify file restored..."
cat "$TEST_DIR/myfile.txt"
echo ""

echo "9. View statistics..."
bash "$CTRLZ" stats
echo ""

echo "10. Set Stack size to 3..."
bash "$CTRLZ" set-stack 3
bash "$CTRLZ" get-stack
echo ""

# Cleanup
rm -rf "$TEST_DIR"

echo "=== Test Complete ==="
