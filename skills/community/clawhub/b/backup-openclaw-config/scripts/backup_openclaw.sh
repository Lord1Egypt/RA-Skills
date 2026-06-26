#!/bin/bash
# OpenClaw Configuration Backup Script
# Usage: ./backup_openclaw.sh [output-directory]

# Default backup directory
DEFAULT_BACKUP_DIR="/data00/backups/openclaw"
BACKUP_DIR="${1:-$DEFAULT_BACKUP_DIR}"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="openclaw_backup_${TIMESTAMP}"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"

echo "=== OpenClaw Configuration Backup ==="
echo "Backup location: $BACKUP_PATH"
echo ""

# Create temporary directory for backup
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Backup function
backup_item() {
    local source="$1"
    local dest="$2"
    local name="$3"
    
    if [ -e "$source" ]; then
        echo "[✓] Backing up $name..."
        
        # Calculate size
        local size=$(du -sh "$source" 2>/dev/null | cut -f1)
        echo "    Size: $size"
        
        # Use rsync for progress and better handling
        rsync -a --progress "$source/" "$dest/" 2>&1 | grep -E "(xfr#|sent)" | tail -1 || {
            # Fallback to cp if rsync fails
            cp -r "$source" "$dest/" 2>/dev/null || {
                echo "[✗] Failed to backup $name"
                return 1
            }
        }
        return 0
    else
        echo "[−] $name not found, skipping..."
        return 0
    fi
}

# Backup OpenClaw configuration directories
backup_item "$HOME/.openclaw" "$TEMP_DIR" ".openclaw (main config)"
backup_item "$HOME/.config/openclaw" "$TEMP_DIR" ".config/openclaw (system config)"
backup_item "$HOME/.local/share/openclaw" "$TEMP_DIR" ".local/share/openclaw (local data)"

# Create backup archive
echo ""
echo "Creating backup archive..."
cd "$TEMP_DIR"
tar -czf "${BACKUP_PATH}.tar.gz" . 2>/dev/null || {
    echo "[✗] Failed to create archive"
    exit 1
}

# Calculate archive size
ARCHIVE_SIZE=$(du -h "${BACKUP_PATH}.tar.gz" | cut -f1)

# Create backup info file
INFO_FILE="${BACKUP_PATH}.info"
cat > "$INFO_FILE" << EOF
OpenClaw Configuration Backup
=============================
Backup Name: $BACKUP_NAME
Created: $(date)
Hostname: $(hostname)
User: $(whoami)
Archive Size: $ARCHIVE_SIZE

Backed up items:
EOF

for item in "$HOME/.openclaw" "$HOME/.config/openclaw" "$HOME/.local/share/openclaw"; do
    if [ -e "$item" ]; then
        echo "  - $item" >> "$INFO_FILE"
    fi
done

echo ""
echo "=== Backup Complete ==="
echo "Archive: ${BACKUP_PATH}.tar.gz"
echo "Info file: ${INFO_FILE}"
echo "Size: ${ARCHIVE_SIZE}"
echo ""

# Clean up old backups (older than 15 days)
echo "=== Cleaning up old backups ==="
DELETED_COUNT=0
find "$BACKUP_DIR" -name "openclaw_backup_*.tar.gz" -type f -mtime +15 | while read -r file; do
    echo "[✓] Deleting old backup: $(basename "$file")"
    rm -f "$file"
    rm -f "${file%.tar.gz}.info" 2>/dev/null
    ((DELETED_COUNT++))
done

if [ $DELETED_COUNT -gt 0 ]; then
    echo "Deleted $DELETED_COUNT old backup(s) (older than 15 days)"
else
    echo "No old backups to clean up"
fi
echo ""

echo "To restore:"
echo "  tar -xzf ${BACKUP_PATH}.tar.gz -C \$HOME"
echo ""
