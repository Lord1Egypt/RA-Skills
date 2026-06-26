#!/bin/bash
#
# Emergency Restore Script for OpenClaw Backups
# Usage: ./restore.sh <backup_file_or_directory>
#
# This script DOES NOT require OpenClaw to be running.
# It can be used when OpenClaw is completely broken.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if backup argument is provided
if [ $# -eq 0 ]; then
    print_error "No backup specified!"
    echo ""
    echo "Usage: $0 <backup_file_or_directory>"
    echo ""
    echo "Examples:"
    echo "  $0 ~/.openclaw/backups/critical/before-upgrade-20260402_063835.tar.gz"
    echo "  $0 ~/.openclaw/backups/daily/2026/04/06/config_20260406_120000/"
    echo ""
    echo "To list available backups:"
    echo "  ls -lht ~/.openclaw/backups/critical/"
    echo "  ls -lht ~/.openclaw/backups/daily/"
    exit 1
fi

BACKUP_PATH="$1"

# Check if backup exists
if [ ! -e "$BACKUP_PATH" ]; then
    print_error "Backup not found: $BACKUP_PATH"
    exit 1
fi

print_info "Starting restore process..."
print_info "Backup: $BACKUP_PATH"

# Confirm restore
echo ""
print_warn "WARNING: This will overwrite your current OpenClaw configuration!"
echo -n "Type 'yes' to continue: "
read -r CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    print_warn "Restore cancelled."
    exit 0
fi

# Create backup of current state BEFORE restore
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CURRENT_BACKUP="$HOME/.openclaw/backups/critical/pre-restore-${TIMESTAMP}.tar.gz"
print_info "Creating backup of current state: $CURRENT_BACKUP"

mkdir -p "$HOME/.openclaw/backups/critical"
tar -czf "$CURRENT_BACKUP" \
    ~/.openclaw/openclaw.json \
    ~/.openclaw/agents \
    ~/.openclaw/memory \
    ~/.openclaw/workspace 2>/dev/null || true

print_info "Current state backed up successfully."

# Restore from backup
print_info "Restoring from backup..."

if [ -f "$BACKUP_PATH" ]; then
    # It's a tar.gz file
    print_info "Extracting tar.gz file..."
    cd "$HOME/.openclaw"
    tar -xzf "$BACKUP_PATH"
    print_info "Extraction completed."
elif [ -d "$BACKUP_PATH" ]; then
    # It's a directory
    print_info "Copying from directory..."
    cp -R "$BACKUP_PATH"/. "$HOME/.openclaw/"
    print_info "Copy completed."
else
    print_error "Unknown backup format: $BACKUP_PATH"
    exit 1
fi

# Verify restore
print_info "Verifying restore..."

if [ -f "$HOME/.openclaw/openclaw.json" ]; then
    print_info "Configuration file restored."
else
    print_warn "Configuration file not found in backup."
fi

if [ -f "$HOME/.openclaw/workspace/MEMORY.md" ]; then
    print_info "Workspace files restored."
else
    print_warn "Workspace files not found in backup."
fi

# Summary
echo ""
print_info "========================================="
print_info "Restore completed successfully!"
print_info "========================================="
echo ""
echo "Restored from: $BACKUP_PATH"
echo "Current state backup: $CURRENT_BACKUP"
echo ""
echo "Next steps:"
echo "  1. Restart OpenClaw: openclaw gateway restart"
echo "  2. Check status: openclaw gateway status"
echo "  3. If issues persist, restore from current state backup:"
echo "     tar -xzf $CURRENT_BACKUP -C \$HOME/.openclaw"
echo ""
print_info "Please review your restored configuration."
