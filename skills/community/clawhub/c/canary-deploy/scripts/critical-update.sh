#!/bin/bash
# =============================================================================
# critical-update.sh — Automated safe change pipeline
# =============================================================================
# Usage: bash critical-update.sh --name "description" --backup /path/to/config \
#        --command "your change command" --validate "validation command"
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CANARY_DIR="${CANARY_DIR:-/tmp/canary-deploy}"
BACKUP_DIR="$CANARY_DIR/backups"

# Parse arguments
NAME=""
BACKUP_FILES=()
COMMAND=""
VALIDATE_CMD=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --name) NAME="$2"; shift 2;;
        --backup) BACKUP_FILES+=("$2"); shift 2;;
        --command) COMMAND="$2"; shift 2;;
        --validate) VALIDATE_CMD="$2"; shift 2;;
        --dry-run) DRY_RUN=true; shift;;
        *) echo "Unknown option: $1"; exit 1;;
    esac
done

if [ -z "$NAME" ] || [ -z "$COMMAND" ]; then
    echo "Usage: bash $0 --name 'change name' --command 'change cmd' [--backup /path] [--validate 'cmd'] [--dry-run]"
    exit 1
fi

mkdir -p "$CANARY_DIR" "$BACKUP_DIR"

echo "============================================"
echo "  Critical Update: $NAME"
echo "  $(date)"
echo "============================================"
echo

# --- Step 1: Baseline -------------------------------------------------------
echo "📸 Step 1: Capturing baseline..."
bash "$SCRIPT_DIR/canary-test.sh" baseline
echo

# --- Step 2: Backup config files --------------------------------------------
if [ ${#BACKUP_FILES[@]} -gt 0 ]; then
    echo "💾 Step 2: Backing up config files..."
    for f in "${BACKUP_FILES[@]}"; do
        if [ -f "$f" ]; then
            SAFE_NAME=$(echo "$f" | tr '/' '_')
            cp "$f" "$BACKUP_DIR/$SAFE_NAME"
            echo "$f" > "$BACKUP_DIR/$SAFE_NAME.path"
            echo "  ✅ Backed up: $f"
        else
            echo "  ⚠️  File not found: $f"
        fi
    done
else
    echo "💾 Step 2: No config files to backup (skipped)"
fi
echo

# --- Step 3: Apply change ----------------------------------------------------
if [ "$DRY_RUN" = "true" ]; then
    echo "🏃 Step 3: DRY RUN — Would execute:"
    echo "  $COMMAND"
    echo
    echo "  Skipping execution (--dry-run)"
    exit 0
fi

echo "🏃 Step 3: Applying change..."
echo "  Command: $COMMAND"
if eval "$COMMAND"; then
    echo "  ✅ Command executed successfully"
else
    echo "  ❌ Command FAILED (exit code $?)"
    echo "  ⏪ Auto-rolling back..."
    bash "$SCRIPT_DIR/canary-test.sh" rollback
    exit 1
fi
echo

# --- Step 4: Validate -------------------------------------------------------
echo "🔍 Step 4: Validating..."

# System-level validation
if bash "$SCRIPT_DIR/canary-test.sh" validate; then
    echo "  ✅ System checks passed"
else
    echo "  ❌ System checks FAILED"
    echo "  ⏪ Auto-rolling back..."
    bash "$SCRIPT_DIR/canary-test.sh" rollback
    echo "  ❌ Change reverted. System restored to baseline."
    exit 1
fi

# Custom validation
if [ -n "$VALIDATE_CMD" ]; then
    echo "  Running custom validation: $VALIDATE_CMD"
    if eval "$VALIDATE_CMD"; then
        echo "  ✅ Custom validation passed"
    else
        echo "  ❌ Custom validation FAILED"
        echo "  ⏪ Auto-rolling back..."
        bash "$SCRIPT_DIR/canary-test.sh" rollback
        echo "  ❌ Change reverted. System restored to baseline."
        exit 1
    fi
fi

echo
echo "============================================"
echo "  ✅ Critical Update Complete: $NAME"
echo "  All validations passed."
echo "============================================"

# Log the change
echo "$(date -Iseconds) | $NAME | SUCCESS | $COMMAND" >> "$CANARY_DIR/changelog.log"
