#!/usr/bin/env bash
#
# Fast backup verification for Guardian safety skill
# Returns VERIFIED, STALE, UNVERIFIED, or PARTIAL within 2 seconds
#
# Usage: ./verify-backup.sh /path/to/target

set -euo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
    echo '{"verdict":"UNVERIFIED","reason":"No target path provided","checks":[],"elapsed_ms":0}'
    exit 1
fi

if [[ ! -e "$TARGET" ]]; then
    echo '{"verdict":"UNVERIFIED","reason":"Path not found","checks":[],"elapsed_ms":0}'
    exit 1
fi

TARGET="$(cd "$(dirname "$TARGET")" && pwd)/$(basename "$TARGET")"

START_TIME=$(date +%s%N)
RESULTS=()
VERDICT="UNVERIFIED"

add_check() {
    local name="$1"
    local status="$2"
    local detail="$3"
    local recency="${4:-null}"
    RESULTS+=("{\"name\":\"$name\",\"status\":\"$status\",\"detail\":\"$detail\",\"recency_hours\":$recency}")
}

# 1. Git repository
GIT_DIR="$TARGET"
FOUND_GIT=false
while [[ "$GIT_DIR" != "/" && "$GIT_DIR" != "." ]]; do
    if [[ -d "$GIT_DIR/.git" ]]; then
        FOUND_GIT=true
        break
    fi
    GIT_DIR="$(dirname "$GIT_DIR")"
done

if [[ "$FOUND_GIT" == true ]]; then
    # Check if tracked
    REL_PATH="${TARGET#$GIT_DIR/}"
    if git -C "$GIT_DIR" ls-files --error-unmatch "$REL_PATH" &>/dev/null; then
        add_check "git-repository" "VERIFIED" "Git repository detected, file tracked" "null"
        VERDICT="VERIFIED"
    else
        add_check "git-repository" "PARTIAL" "Git repository detected, file NOT tracked" "null"
    fi
fi

# 2. Time Machine (macOS)
if [[ "$VERDICT" != "VERIFIED" && "$OSTYPE" == "darwin"* ]]; then
    if command -v tmutil &>/dev/null; then
        # Check if path is excluded
        EXCLUDED=$(tmutil isexcluded "$TARGET" 2>/dev/null || true)
        if [[ "$EXCLUDED" == *"[Excluded]"* ]]; then
            add_check "time-machine" "PARTIAL" "Time Machine active but path excluded" "null"
        else
            # Check latest backup
            LATEST=$(tmutil latestbackup 2>/dev/null || true)
            if [[ -n "$LATEST" ]]; then
                BACKUP_TIME=$(stat -f %m "$LATEST" 2>/dev/null || true)
                if [[ -n "$BACKUP_TIME" ]]; then
                    NOW=$(date +%s)
                    AGE_HOURS=$(( (NOW - BACKUP_TIME) / 3600 ))
                    if [[ $AGE_HOURS -lt 24 ]]; then
                        add_check "time-machine" "VERIFIED" "Time Machine backup within 24h" "$AGE_HOURS"
                        VERDICT="VERIFIED"
                    else
                        add_check "time-machine" "STALE" "Time Machine backup ${AGE_HOURS}h old" "$AGE_HOURS"
                    fi
                fi
            else
                add_check "time-machine" "UNVERIFIED" "Time Machine not configured" "null"
            fi
        fi
    fi
fi

# 3. Linux snapshot systems (snapper, timeshift, btrbk)
if [[ "$VERDICT" != "VERIFIED" && "$OSTYPE" == "linux"* ]]; then
    # Check for snapper
    if command -v snapper &>/dev/null; then
        MOUNT_POINT=$(findmnt -T "$TARGET" -n -o TARGET 2>/dev/null || true)
        if [[ -n "$MOUNT_POINT" ]]; then
            CONFIG=$(snapper list-configs 2>/dev/null | grep -m1 "$MOUNT_POINT" || true)
            if [[ -n "$CONFIG" ]]; then
                SNAPSHOTS=$(snapper -c "$MOUNT_POINT" list -t single 2>/dev/null | tail -n +3 | wc -l || true)
                if [[ "$SNAPSHOTS" -gt 0 ]]; then
                    add_check "snapper" "VERIFIED" "Snapper snapshots exist for filesystem" "null"
                    VERDICT="VERIFIED"
                fi
            fi
        fi
    fi

    # Check for timeshift
    if [[ "$VERDICT" != "VERIFIED" ]] && command -v timeshift &>/dev/null; then
        TIMESHIFT_STATUS=$(timeshift --list 2>/dev/null | head -5 || true)
        if [[ "$TIMESHIFT_STATUS" == *"snapshot"* ]]; then
            add_check "timeshift" "VERIFIED" "Timeshift snapshots detected" "null"
            VERDICT="VERIFIED"
        fi
    fi

    # Check for btrbk
    if [[ "$VERDICT" != "VERIFIED" ]] && [[ -d "/var/log/btrbk" ]]; then
        add_check "btrbk" "VERIFIED" "btrbk logs present" "null"
        VERDICT="VERIFIED"
    fi
fi

# 4. Cloud sync (iCloud, Dropbox, Google Drive, OneDrive)
if [[ "$VERDICT" != "VERIFIED" ]]; then
    PARENT_DIR="$(dirname "$TARGET")"
    
    # Check for cloud sync markers
    if [[ "$PARENT_DIR" == *"iCloud Drive"* ]] || [[ "$PARENT_DIR" == *"Dropbox"* ]] || \
       [[ "$PARENT_DIR" == *"Google Drive"* ]] || [[ "$PARENT_DIR" == *"OneDrive"* ]]; then
        add_check "cloud-sync" "VERIFIED" "Path in cloud sync directory" "null"
        VERDICT="VERIFIED"
    fi
    
    # Check for .cloud files (unsynced markers)
    if find "$PARENT_DIR" -maxdepth 1 -name "*.cloud" -print -quit 2>/dev/null | grep -q .; then
        add_check "cloud-sync" "PARTIAL" "Cloud sync active but unsynced files present" "null"
    fi
fi

# 5. Explicit backup tools (restic, borg, duplicity)
if [[ "$VERDICT" != "VERIFIED" ]]; then
    PARENT_DIR="$(dirname "$TARGET")"
    
    for marker in ".restic" ".borg" ".snapshots" "backup" ".backups"; do
        if [[ -d "$PARENT_DIR/$marker" ]] || [[ -d "$HOME/$marker" ]]; then
            add_check "explicit-backup" "VERIFIED" "Backup marker found: $marker" "null"
            VERDICT="VERIFIED"
            break
        fi
    done
fi

# 6. ZFS snapshots (Linux/FreeBSD)
if [[ "$VERDICT" != "VERIFIED" ]] && command -v zfs &>/dev/null; then
    ZFS_DATASET=$(df "$TARGET" 2>/dev/null | tail -1 | awk '{print $1}' || true)
    if [[ "$ZFS_DATASET" == *"/"* ]]; then
        SNAPSHOTS=$(zfs list -t snapshot "$ZFS_DATASET" 2>/dev/null | wc -l || true)
        if [[ "$SNAPSHOTS" -gt 1 ]]; then
            add_check "zfs-snapshots" "VERIFIED" "ZFS snapshots exist" "null"
            VERDICT="VERIFIED"
        fi
    fi
fi

# Calculate elapsed time
END_TIME=$(date +%s%N)
ELAPSED_MS=$(( (END_TIME - START_TIME) / 1000000 ))

# Build JSON output
checks_json="[$(IFS=,; echo "${RESULTS[*]}")]"

echo "{\"verdict\":\"$VERDICT\",\"target\":\"$TARGET\",\"checks\":$checks_json,\"elapsed_ms\":$ELAPSED_MS}"
exit 0
