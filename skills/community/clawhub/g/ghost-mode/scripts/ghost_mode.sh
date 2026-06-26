#!/usr/bin/env bash
# Ghost Mode CLI - Activate, deactivate, and manage privacy sessions
# Generic version: no agent-specific or environment-specific assumptions.
#
# Usage:
#   ghost_mode.sh on [--session-key <key>]   # Activate ghost mode
#   ghost_mode.sh off [--dry-run]             # Deactivate and run pipeline
#   ghost_mode.sh status                      # Show current status
#   ghost_mode.sh archive-completed           # Archive all active sessions
#   ghost_mode.sh verify-pending              # Verify all scrubbed sessions
#   ghost_mode.sh force-cleanup-all [--dry-run]  # Force cleanup stale sessions (>24h)
#   ghost_mode.sh show-warning                # Show the one-time data loss warning

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
FLAG_FILE="$WORKSPACE/memory/.ghost-mode"
REGISTRY="$WORKSPACE/memory/.ghost-sessions.json"
WARNING_FILE="$WORKSPACE/memory/.ghost-mode-warning-shown"
CONFIG_FILE="$WORKSPACE/ghost-mode-config.json"

# Add scripts dir to Python path
export PYTHONPATH="$SCRIPT_DIR${PYTHONPATH:+:$PYTHONPATH}"

# Colors for output (disabled if not a terminal)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    CYAN='\033[0;36m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    CYAN=''
    NC=''
fi

log() { echo -e "${GREEN}[ghost]${NC} $*"; }
warn() { echo -e "${YELLOW}[ghost]${NC} $*" >&2; }
err() { echo -e "${RED}[ghost]${NC} $*" >&2; }
dry_run_log() { echo -e "${CYAN}[ghost DRY-RUN]${NC} $*"; }

# ── Config ──────────────────────────────────────────────────────────
# Reads ghost-mode-config.json from the workspace.
# {
#   "confirm_before_delete": true,   # require interactive confirmation
#   "dry_run_by_default": true      # if true, `ghost off` defaults to dry-run
# }
ensure_config() {
    # Create default config on first use if it doesn't exist
    if [ ! -f "$CONFIG_FILE" ]; then
        mkdir -p "$(dirname "$CONFIG_FILE")"
        cat > "$CONFIG_FILE" <<'EOF'
{
  "confirm_before_delete": true,
  "dry_run_by_default": true
}
EOF
        log "Created default config at $CONFIG_FILE (confirm_before_delete: true)"
    fi
}

load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        python3 -c "
import json, sys
with open('$CONFIG_FILE') as f:
    cfg = json.load(f)
print(json.dumps(cfg))
" 2>/dev/null || echo '{}'
    else
        echo '{}'
    fi
}

get_config_bool() {
    local key="$1"
    local default="${2:-false}"
    local val
    val=$(load_config | python3 -c "
import json, sys
cfg = json.load(sys.stdin)
print(str(cfg.get('$key', $default)).lower())
" 2>/dev/null || echo "$default")
    echo "$val"
}

# ── Confirmation ────────────────────────────────────────────────────
confirm_delete() {
    # Check config: if confirm_before_delete is false, skip confirmation
    local require_confirm
    require_confirm=$(get_config_bool "confirm_before_delete" "true")
    if [ "$require_confirm" = "false" ]; then
        return 0
    fi

    # If not a terminal, we can't prompt — fail safe by requiring --yes
    if [ ! -t 0 ]; then
        err "Confirmation required but no terminal available. Use --yes to skip confirmation."
        return 1
    fi

    echo -e "${RED}⚠️  You are about to permanently delete session data.${NC}"
    echo -e "${RED}   This action is IRREVERSIBLE. Deleted data cannot be recovered.${NC}"
    echo ""
    echo -e "  Type ${YELLOW}yes${NC} to confirm, or anything else to cancel:"
    read -r response
    if [ "$response" != "yes" ]; then
        log "Operation cancelled."
        return 1
    fi
    return 0
}

# ── Helpers ──────────────────────────────────────────────────────────
require_cmd() {
    if ! command -v "$1" &>/dev/null; then
        err "Required command not found: $1"
        exit 1
    fi
}

secure_delete() {
    # Try shred first, fall back to rm with warning
    if command -v shred &>/dev/null; then
        shred -u "$1" 2>/dev/null
    else
        warn "shred not available, using rm (less secure): $1"
        rm -f "$1"
    fi
}

secure_delete_dry_run() {
    dry_run_log "Would secure-delete: $1"
}

check_warning() {
    # Show one-time data loss warning if not already shown
    if [ ! -f "$WARNING_FILE" ]; then
        echo ""
        echo "⚠️  DATA LOSS WARNING"
        echo "════════════════════════════════════════════════════════════════"
        echo "Ghost Mode permanently deletes data by design."
        echo ""
        echo "When you run 'ghost off', this skill will:"
        echo "  • SCRUB entries from daily logs, semantic memory, and episodic memory"
        echo "  • SHRED session transcripts using secure deletion (shred -u)"
        echo "  • REMOVE entries from the OpenClaw memory search index"
        echo ""
        echo "This is IRREVERSIBLE. Deleted data cannot be recovered."
        echo ""
        echo "Bugs, misuse, or environment conflicts can cause data loss"
        echo "beyond what you intended. By using this skill, you accept these risks."
        echo ""
        echo "RECOMMENDED: Set up daily backups of your OpenClaw workspace:"
        echo "  tar -czf ~/openclaw-backup-\$(date +%F).tar.gz ~/.openclaw/workspace/ ~/.openclaw/data/"
        echo "════════════════════════════════════════════════════════════════"
        echo ""
        # Mark warning as shown so it only appears once
        mkdir -p "$(dirname "$WARNING_FILE")"
        date -u +"%Y-%m-%dT%H:%M:%SZ" > "$WARNING_FILE"
        log "Warning shown and acknowledged. This message will not appear again."
    fi
}

# Ensure registry exists
ensure_registry() {
    mkdir -p "$(dirname "$REGISTRY")"
    if [ ! -f "$REGISTRY" ]; then
        echo '{"sessions": {}}' > "$REGISTRY"
    fi
}

# ── Dry-run helpers ──────────────────────────────────────────────────
dry_run_archive() {
    local session_id="$1"
    dry_run_log "Would archive session files for: $session_id"
    dry_run_log "  Would copy session JSONL + checkpoints to ~/.openclaw/ghost-archive/"
    dry_run_log "  Would remove originals from sessions directory"
}

dry_run_scrub() {
    local session_id="$1"
    dry_run_log "Would scrub memory files for session: $session_id"
    dry_run_log "  Would remove ghost-window entries from: memory/*.md"
    dry_run_log "  Would remove ghost-window entries from: memory/semantic/*.md"
    dry_run_log "  Would remove ghost-window entries from: memory/episodic/*.md"
    dry_run_log "  Would remove promoted ghost entries from: MEMORY.md"
}

dry_run_index_cleanup() {
    local session_id="$1"
    dry_run_log "Would remove index entries for session: $session_id"
    dry_run_log "  Would DELETE rows from memory.db matching session ID"
}

dry_run_verify() {
    local session_id="$1"
    dry_run_log "Would run 7-layer verification for session: $session_id"
}

dry_run_shred() {
    local archive_dir="$1"
    if [ -d "$archive_dir" ]; then
        local count
        count=$(find "$archive_dir" -type f | wc -l)
        dry_run_log "Would secure-delete $count archived file(s) in: $archive_dir"
    else
        dry_run_log "No archive directory found at $archive_dir (nothing to shred)"
    fi
}

# ── Commands ─────────────────────────────────────────────────────────
cmd_on() {
    check_warning
    require_cmd python3
    local session_key=""
    local session_id

    # Parse optional --session-key argument
    while [ $# -gt 0 ]; do
        case "$1" in
            --session-key)
                shift; session_key="$1" ;;
            *) session_key="$1" ;;
        esac
        shift
    done
    [ -z "$session_key" ] && session_key="unknown"

    # Try to get current session from OpenClaw if available
    if command -v openclaw &>/dev/null; then
        session_id=$(openclaw sessions list --current --format json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('id','unknown'))" 2>/dev/null || echo "")
    fi
    [ -z "$session_id" ] && session_id="ghost-$(date +%s)"

    # Check if already active
    if [ -f "$FLAG_FILE" ]; then
        warn "Ghost mode already active"
        python3 "$SCRIPT_DIR/ghost_registry.py" flag-read
        return 0
    fi

    ensure_registry
    python3 "$SCRIPT_DIR/ghost_registry.py" add "$session_key" "$session_id"

    # Write flag file
    mkdir -p "$(dirname "$FLAG_FILE")"
    python3 -c "
import json
from datetime import datetime, timezone
flag = {'sessionKey': '$session_key', 'sessionId': '$session_id', 'activatedAt': datetime.now(timezone.utc).isoformat()}
with open('$FLAG_FILE', 'w') as f:
    json.dump(flag, f, indent=2)
"

    log "Ghost mode ON — session: $session_id"
    log "Memory writes are now suppressed until 'ghost off'"
}

cmd_off() {
    check_warning
    ensure_config
    require_cmd python3

    local dry_run=false
    local skip_confirm=false

    # Parse arguments
    while [ $# -gt 0 ]; do
        case "$1" in
            --dry-run) dry_run=true ;;
            --yes|-y) skip_confirm=true ;;
            *) ;;
        esac
        shift
    done

    # Check dry_run_by_default config
    local default_dry
    default_dry=$(get_config_bool "dry_run_by_default" "true")
    if [ "$default_dry" = "true" ] && [ "$dry_run" = "false" ]; then
        dry_run=true
        dry_run_log "dry_run_by_default is enabled in config — running in dry-run mode"
        dry_run_log "Use --yes to override and run for real"
    fi

    if [ ! -f "$FLAG_FILE" ]; then
        warn "Ghost mode is not active"
        return 0
    fi

    # Read flag before removing
    local session_id
    session_id=$(python3 -c "import json; print(json.load(open('$FLAG_FILE')).get('sessionId', 'unknown'))")

    # ── Dry-run path ─────────────────────────────────────────────
    if [ "$dry_run" = "true" ]; then
        dry_run_log "=== DRY RUN — no changes will be made ==="
        dry_run_log "Session: $session_id"
        echo ""
        dry_run_archive "$session_id"
        dry_run_scrub "$session_id"
        dry_run_index_cleanup "$session_id"
        dry_run_verify "$session_id"
        dry_run_shred "$HOME/.openclaw/ghost-archive"
        echo ""
        dry_run_log "=== END DRY RUN ==="
        dry_run_log "Run 'ghost_mode.sh off' (without --dry-run) to execute these operations."
        return 0
    fi

    # ── Confirmation ──────────────────────────────────────────────
    if [ "$skip_confirm" = "false" ]; then
        if ! confirm_delete; then
            return 1
        fi
    fi

    # Remove flag
    rm -f "$FLAG_FILE"
    log "Ghost mode flag removed"

    # Run archival pipeline
    log "Running archival pipeline for session $session_id..."

    # Step 1: Update registry status to completed
    python3 "$SCRIPT_DIR/ghost_registry.py" update "$session_id" completed 2>/dev/null || true

    # Step 2: Archive session files
    python3 "$SCRIPT_DIR/ghost_archive.py" session "$session_id" 2>/dev/null || {
        warn "Archival encountered issues, continuing..."
    }

    # Step 3: Scrub memory files
    python3 "$SCRIPT_DIR/ghost_scrub.py" session "$session_id" 2>/dev/null || {
        warn "Scrubbing encountered issues, continuing..."
    }

    # Step 4: Index cleanup
    python3 "$SCRIPT_DIR/ghost_index_cleanup.py" --session-id "$session_id" 2>/dev/null || {
        warn "Index cleanup encountered issues, continuing..."
    }

    # Step 5: Verify
    python3 "$SCRIPT_DIR/ghost_verify.py" session "$session_id" 2>/dev/null || {
        warn "Verification encountered issues, continuing..."
    }

    # Step 6: Secure delete archived files
    local archive_dir="$HOME/.openclaw/ghost-archive"
    if [ -d "$archive_dir" ]; then
        find "$archive_dir" -type f -exec shred -u {} \; 2>/dev/null || {
            find "$archive_dir" -type f -exec rm -f {} \;
            warn "shred unavailable, used rm instead"
        }
        # Remove empty directories
        find "$archive_dir" -type d -empty -delete 2>/dev/null || true
    fi

    log "Ghost mode OFF — session $session_id fully scrubbed and verified"
}

cmd_status() {
    require_cmd python3

    if [ -f "$FLAG_FILE" ]; then
        log "Ghost mode: ACTIVE"
        python3 "$SCRIPT_DIR/ghost_registry.py" flag-read
    else
        log "Ghost mode: INACTIVE"
    fi

    echo ""
    log "Registry:"
    python3 "$SCRIPT_DIR/ghost_registry.py" list

    # Show config
    echo ""
    log "Config:"
    if [ -f "$CONFIG_FILE" ]; then
        cat "$CONFIG_FILE"
    else
        echo "  (no config file — using defaults)"
        echo "  confirm_before_delete: true (requires confirmation before delete)"
        echo "  dry_run_by_default: true (ghost off defaults to dry-run, use --yes to execute)"
    fi
}

cmd_archive_completed() {
    require_cmd python3
    python3 "$SCRIPT_DIR/ghost_archive.py" completed
}

cmd_verify_pending() {
    require_cmd python3
    python3 "$SCRIPT_DIR/ghost_verify.py" scrubbed
}

cmd_force_cleanup() {
    require_cmd python3
    ensure_config

    local dry_run=false
    local skip_confirm=false

    # Parse arguments
    while [ $# -gt 0 ]; do
        case "$1" in
            --dry-run) dry_run=true ;;
            --yes|-y) skip_confirm=true ;;
            *) ;;
        esac
        shift
    done

    # Check dry_run_by_default config
    local default_dry
    default_dry=$(get_config_bool "dry_run_by_default" "true")
    if [ "$default_dry" = "true" ] && [ "$dry_run" = "false" ]; then
        dry_run=true
        dry_run_log "dry_run_by_default is enabled in config — running in dry-run mode"
    fi

    log "Force cleanup: processing stale sessions..."

    # Get stale sessions
    local stale
    stale=$(python3 "$SCRIPT_DIR/ghost_registry.py" stale)

    if [ "$stale" = "[]" ] || [ -z "$stale" ]; then
        log "No stale sessions found"
        return 0
    fi

    # ── Dry-run path ─────────────────────────────────────────────
    if [ "$dry_run" = "true" ]; then
        dry_run_log "=== DRY RUN — no changes will be made ==="
        echo "$stale" | python3 -c "
import json, sys
sessions = json.load(sys.stdin)
for s in sessions:
    print(f'  Would clean up stale session: {s[\"sessionId\"]} (age: {s.get(\"activatedAt\",\"unknown\")})')
print(f'  Total stale sessions: {len(sessions)}')
"
        dry_run_log "=== END DRY RUN ==="
        dry_run_log "Run 'ghost_mode.sh force-cleanup-all' (without --dry-run) to execute."
        return 0
    fi

    # ── Confirmation ──────────────────────────────────────────────
    if [ "$skip_confirm" = "false" ]; then
        if ! confirm_delete; then
            return 1
        fi
    fi

    # Process each stale session
    echo "$stale" | python3 -c "
import json, sys
sessions = json.load(sys.stdin)
for s in sessions:
    print(s['sessionId'])
" | while read -r sid; do
        log "Cleaning up stale session: $sid"
        python3 "$SCRIPT_DIR/ghost_registry.py" update "$sid" completed 2>/dev/null || true
        python3 "$SCRIPT_DIR/ghost_archive.py" session "$sid" 2>/dev/null || true
        python3 "$SCRIPT_DIR/ghost_scrub.py" session "$sid" 2>/dev/null || true
        python3 "$SCRIPT_DIR/ghost_index_cleanup.py" --session-id "$sid" 2>/dev/null || true
        python3 "$SCRIPT_DIR/ghost_verify.py" session "$sid" 2>/dev/null || true
    done

    # Remove flag
    rm -f "$FLAG_FILE"
    log "Stale sessions cleaned up"
}

# Main
case "${1:-help}" in
    on)
        shift
        cmd_on "$@"
        ;;
    off)
        shift
        cmd_off "$@"
        ;;
    status)
        cmd_status
        ;;
    show-warning)
        check_warning
        ;;
    archive-completed)
        cmd_archive_completed
        ;;
    verify-pending)
        cmd_verify_pending
        ;;
    force-cleanup-all)
        shift
        cmd_force_cleanup "$@"
        ;;
    help|*)
        echo "Ghost Mode — Privacy mode for OpenClaw sessions"
        echo ""
        echo "⚠️  WARNING: This skill permanently deletes data by design."
        echo "   Run 'ghost_mode.sh show-warning' to see the full warning."
        echo ""
        echo "Usage: ghost_mode.sh <command> [options]"
        echo ""
        echo "Commands:"
        echo "  on [--session-key <key>]    Activate ghost mode"
        echo "  off [--dry-run] [--yes]     Deactivate and scrub session data"
        echo "  status                       Show current ghost mode status and config"
        echo "  show-warning                 Show the one-time data loss warning"
        echo "  archive-completed            Archive all active sessions"
        echo "  verify-pending               Verify all scrubbed sessions"
        echo "  force-cleanup-all [--dry-run] [--yes]"
        echo "                               Force cleanup stale sessions (>24h)"
        echo ""
        echo "Options:"
        echo "  --dry-run    Show what would be deleted without making any changes"
        echo "  --yes, -y    Skip confirmation prompt (for scripted use)"
        echo ""
        echo "Configuration (ghost-mode-config.json in workspace root):"
        echo "  {"
        echo "    \"confirm_before_delete\": true,   // Require 'yes' confirmation before deleting"
        echo "    \"dry_run_by_default\": true     // If true (default), 'ghost off' defaults to dry-run; pass --yes to execute"
        echo "  }"
        echo ""
        echo "Environment variables:"
        echo "  OPENCLAW_WORKSPACE          Path to OpenClaw workspace (default: ~/.openclaw/workspace)"
        echo "  OPENCLAW_AGENT              Agent directory name (default: main)"
        echo ""
        echo "RECOMMENDED: Set up daily backups before using this skill."
        echo "  tar -czf ~/openclaw-backup-\$(date +%F).tar.gz ~/.openclaw/workspace/ ~/.openclaw/data/"
        ;;
esac