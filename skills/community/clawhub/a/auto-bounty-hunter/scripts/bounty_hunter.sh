#!/bin/bash
# GitHub Bounty Hunter - Main Script

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Load config
source "${SCRIPT_DIR}/config.sh"

# Create data directory
mkdir -p "${SKILL_DIR}/data"

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG_FILE"
}

# Scan for 0-comment issues
scan_issues() {
    log "Scanning for 0-comment issues..."
    
    gh search issues \
        --limit "$MAX_ISSUES_PER_SCAN" \
        --json url,title,repository,createdAt \
        "is:issue is:open comments:0 language:${LANGUAGES// /,}" \
        2>/dev/null || echo "[]"
}

# Evaluate issue value
evaluate_issue() {
    local issue_url="$1"
    local repo="${issue_url#https://github.com/}"
    repo="${repo%/issues/*}"
    
    # Get repo info
    local stars=$(gh repo view "$repo" --json stargazersCount -q .stargazersCount 2>/dev/null || echo 0)
    
    # Skip low-star repos
    if [ "$stars" -lt "$MIN_REPO_STARS" ]; then
        echo "SKIP: Low stars ($stars)"
        return 1
    fi
    
    # Skip blacklisted orgs
    local org="${repo%%/*}"
    if [[ ",$SKIP_ORGS," == *",$org,"* ]]; then
        echo "SKIP: Blacklisted org ($org)"
        return 1
    fi
    
    echo "PROCESS: Stars=$stars"
    return 0
}

# Add to queue
add_to_queue() {
    local issue_url="$1"
    local title="$2"
    
    # Initialize queue if needed
    [ ! -f "$QUEUE_FILE" ] && echo "[]" > "$QUEUE_FILE"
    
    # Check if already in queue
    if jq -e --arg url "$issue_url" '.[] | select(.url == $url)' "$QUEUE_FILE" >/dev/null 2>&1; then
        log "Already in queue: $issue_url"
        return 0
    fi
    
    # Add to queue
    local entry=$(jq -n \
        --arg url "$issue_url" \
        --arg title "$title" \
        --arg added "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        '{url: $url, title: $title, added: $added, status: "pending"}')
    
    jq --argjson entry "$entry" '. += [$entry]' "$QUEUE_FILE" > "${QUEUE_FILE}.tmp"
    mv "${QUEUE_FILE}.tmp" "$QUEUE_FILE"
    
    log "Added to queue: $title"
}

# Main
main() {
    log "=== GitHub Bounty Hunter v1.0 ==="
    
    if [ "$DRY_RUN" = true ]; then
        log "DRY RUN MODE - No actions will be taken"
    fi
    
    # Scan for issues
    local issues=$(scan_issues)
    local count=$(echo "$issues" | jq 'length')
    
    log "Found $count issues"
    
    if [ "$count" -eq 0 ]; then
        log "No issues found"
        return 0
    fi
    
    # Process each issue
    echo "$issues" | jq -c '.[]' | while read -r issue; do
        local url=$(echo "$issue" | jq -r '.url')
        local title=$(echo "$issue" | jq -r '.title')
        
        log "Evaluating: $title"
        
        if evaluate_issue "$url"; then
            add_to_queue "$url" "$title"
        fi
    done
    
    log "=== Scan complete ==="
}

main "$@"
