#!/bin/bash
# GitHub Bounty Hunter - PR Tracker

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Load config
source "${SCRIPT_DIR}/config.sh"

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG_FILE"
}

# Check PR status
check_pr_status() {
    local pr_url="$1"
    
    # Extract owner/repo/number from URL
    local path="${pr_url#https://github.com/}"
    local owner="${path%%/*}"
    path="${path#*/}"
    local repo="${path%%/*}"
    local number="${path##*/}"
    
    # Get PR status
    gh pr view "$number" \
        --repo "$owner/$repo" \
        --json state,merged,mergedAt \
        2>/dev/null || echo '{"state":"unknown"}'
}

# Update queue status
update_queue() {
    [ ! -f "$QUEUE_FILE" ] && return 0
    
    local updated=false
    
    jq -c '.[]' "$QUEUE_FILE" | while read -r entry; do
        local url=$(echo "$entry" | jq -r '.url')
        local pr_url=$(echo "$entry" | jq -r '.pr_url // empty')
        local status=$(echo "$entry" | jq -r '.status')
        
        # Skip if no PR or already merged
        [ -z "$pr_url" ] && continue
        [ "$status" = "merged" ] && continue
        
        # Check PR status
        local pr_status=$(check_pr_status "$pr_url")
        local state=$(echo "$pr_status" | jq -r '.state')
        local merged=$(echo "$pr_status" | jq -r '.merged')
        
        if [ "$merged" = "true" ]; then
            log "✅ MERGED: $url"
            # Update status in queue
            jq --arg url "$url" \
               '(.[] | select(.url == $url) | .status) = "merged"' \
               "$QUEUE_FILE" > "${QUEUE_FILE}.tmp"
            mv "${QUEUE_FILE}.tmp" "$QUEUE_FILE"
            updated=true
            
            # Move to history
            echo "$entry" | jq --arg merged_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
                '. + {merged_at: $merged_at}' >> "$HISTORY_FILE"
        fi
    done
    
    if [ "$updated" = true ]; then
        log "Queue updated"
    fi
}

# Show stats
show_stats() {
    local total=$(jq 'length' "$QUEUE_FILE" 2>/dev/null || echo 0)
    local pending=$(jq '[.[] | select(.status == "pending")] | length' "$QUEUE_FILE" 2>/dev/null || echo 0)
    local submitted=$(jq '[.[] | select(.status == "submitted")] | length' "$QUEUE_FILE" 2>/dev/null || echo 0)
    local merged=$(jq 'length' "$HISTORY_FILE" 2>/dev/null || echo 0)
    
    log "=== Stats ==="
    log "Total in queue: $total"
    log "Pending: $pending"
    log "Submitted: $submitted"
    log "Merged (all time): $merged"
}

# Main
main() {
    log "=== PR Tracker ==="
    
    update_queue
    show_stats
    
    log "=== Tracking complete ==="
}

main "$@"
