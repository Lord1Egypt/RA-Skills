#!/bin/bash
# Backup and Restore Operations
# Usage: backup_account.sh <action> [options...]
# Actions: list, create, restore, download

set -e

ACTION="${1:?Action required (list, create, restore, download)}"
shift 1 2>/dev/null || true

HOST="${CPANEL_HOST:?CPANEL_HOST not set}"
TOKEN="${CPANEL_TOKEN:?CPANEL_TOKEN not set}"

case "$ACTION" in
    list)
        echo "Listing backup files..."
        curl -s -H "Authorization: whm $TOKEN" \
            "${HOST}/json-api/listbackupfiles?api.version=1" | jq '.data'
        ;;
    create)
        USER="${2:?Username required}"
        DEST="${3:-/backup}"
        
        echo "Creating backup for account: $USER..."
        curl -s -H "Authorization: whm $TOKEN" \
            "${HOST}/json-api/backupacct?api.version=1&user=${USER}" | jq .
        ;;
    restore)
        FILE="${2:?Backup file required}"
        USER="${3:-}"
        
        echo "Restoring from backup: $FILE..."
        if [[ -n "$USER" ]]; then
            curl -s -H "Authorization: whm $TOKEN" \
                "${HOST}/json-api/restoreacct?api.version=1&user=${USER}&backup=${FILE}" | jq .
        else
            curl -s -H "Authorization: whm $TOKEN" \
                "${HOST}/json-api/restoreacct?api.version=1&backup=${FILE}" | jq .
        fi
        ;;
    download)
        USER="${2:?Username required}"
        FILE="${3:-backup.tar.gz}"
        
        echo "Downloading backup for $USER..."
        curl -s -H "Authorization: whm $TOKEN" \
            "${HOST}/json-api/downloadbackup?api.version=1&user=${USER}" -o "$FILE"
        echo "Downloaded to: $FILE"
        ;;
    status)
        PID="${2:?Process ID required}"
        
        echo "Checking backup status for PID: $PID..."
        curl -s -H "Authorization: whm $TOKEN" \
            "${HOST}/json-api/backup_status?api.version=1&pid=${PID}" | jq .
        ;;
    *)
        echo "Usage: backup_account.sh <list|create|restore|download|status> [options]"
        exit 1
        ;;
esac