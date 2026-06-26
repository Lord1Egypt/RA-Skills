#!/bin/bash
# post-create-validate.sh — Run AFTER creating/editing a Python file
# Checks for function duplication, missing imports, and bypass patterns.
# Usage: bash post-create-validate.sh <file_path>

set -euo pipefail

NEW_FILE="${1:-}"

if [ -z "$NEW_FILE" ] || [ ! -f "$NEW_FILE" ]; then
    echo "❌ File not found: $NEW_FILE"
    echo "Usage: bash post-create-validate.sh <file_path>"
    exit 1
fi

PROJECT_DIR=$(dirname "$NEW_FILE")
NEW_BASENAME=$(basename "$NEW_FILE")
WARNINGS=0

echo "╔══════════════════════════════════════════════════╗"
echo "║          POST-CREATION VALIDATION                ║"
echo "╚══════════════════════════════════════════════════╝"
echo "  File: $NEW_FILE"
echo ""

# 1. Extract function names from new file
NEW_FUNCS=$(grep "^def " "$NEW_FILE" 2>/dev/null | sed 's/def \([a-zA-Z_]*\).*/\1/' || true)

if [ -z "$NEW_FUNCS" ]; then
    echo "ℹ️  No function definitions found in new file."
else
    # 2. Check for duplicate function names in other project files
    echo "🔍 Checking for function duplication..."
    echo "─────────────────────────────────────"
    
    for func_name in $NEW_FUNCS; do
        EXISTING=$(grep -rn "^def ${func_name}\b" "$PROJECT_DIR"/*.py 2>/dev/null | grep -v "$NEW_BASENAME" || true)
        if [ -n "$EXISTING" ]; then
            echo "  ⚠️  DUPLICATE: '$func_name' already exists!"
            echo "     $EXISTING"
            WARNINGS=$((WARNINGS + 1))
        fi
    done
    
    if [ "$WARNINGS" -eq 0 ]; then
        echo "  ✅ No duplicate functions found."
    fi
    echo ""
fi

# 3. Check if new file imports from established modules
echo "🔗 Checking imports from established modules..."
echo "─────────────────────────────────────────────"

# Find established modules (files with >5 functions = likely a core module)
ESTABLISHED=""
for pyfile in "$PROJECT_DIR"/*.py; do
    [ "$pyfile" = "$NEW_FILE" ] && continue
    [ ! -f "$pyfile" ] && continue
    func_count=$(grep -c "^def " "$pyfile" 2>/dev/null || true)
    func_count=${func_count:-0}
    func_count=$(echo "$func_count" | tr -d '[:space:]')
    if [ "$func_count" -gt 5 ]; then
        mod_name=$(basename "$pyfile" .py)
        ESTABLISHED="$ESTABLISHED $mod_name"
    fi
done

if [ -n "$ESTABLISHED" ]; then
    IMPORTS_FOUND=0
    for mod in $ESTABLISHED; do
        if grep -q "from ${mod}\|import ${mod}\|from \.${mod}" "$NEW_FILE" 2>/dev/null; then
            echo "  ✅ Imports from established module: $mod"
            IMPORTS_FOUND=1
        fi
    done
    
    if [ "$IMPORTS_FOUND" -eq 0 ]; then
        echo "  ⚠️  WARNING: Does not import from any established module!"
        echo "     Established modules:$ESTABLISHED"
        echo "     Consider importing validated functions instead of reimplementing."
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "  ℹ️  No established modules (>5 functions) found in project."
fi
echo ""

# 4. Check for bypass patterns
echo "🚫 Checking for bypass patterns..."
echo "──────────────────────────────────"
BYPASS_PATTERNS=("simplified version" "quick version" "temporary" "TODO: integrate" "hack" "workaround")
for pattern in "${BYPASS_PATTERNS[@]}"; do
    MATCH=$(grep -in "$pattern" "$NEW_FILE" 2>/dev/null || true)
    if [ -n "$MATCH" ]; then
        echo "  ⚠️  BYPASS PATTERN: '$pattern'"
        echo "     $MATCH"
        WARNINGS=$((WARNINGS + 1))
    fi
done
echo ""

# 5. Summary
if [ "$WARNINGS" -gt 0 ]; then
    echo "╔══════════════════════════════════════════════════╗"
    echo "║  ⚠️  $WARNINGS WARNING(S) — Review before proceeding   ║"
    echo "╚══════════════════════════════════════════════════╝"
    exit 1
else
    echo "╔══════════════════════════════════════════════════╗"
    echo "║  ✅ All checks passed                            ║"
    echo "╚══════════════════════════════════════════════════╝"
    exit 0
fi
