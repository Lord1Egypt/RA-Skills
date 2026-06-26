#!/usr/bin/env bash
set -euo pipefail

# factory-status.sh — query agent status, open issues, and CI pipelines
#
# Usage: factory-status.sh [--agents] [--issues] [--ci] [--help]
#   No flags: show all sections
#   --agents: show only agent activity status
#   --issues: show only open issues summary
#   --ci:     show only CI pipeline status
#
# Required env: FORGE_TOKEN, FORGE_API, PROJECT_REPO_ROOT
# Optional env: WOODPECKER_SERVER, WOODPECKER_TOKEN, WOODPECKER_REPO_ID

usage() {
    sed -n '3,10s/^# //p' "$0"
    exit 0
}

show_agents=false
show_issues=false
show_ci=false
show_all=true

while [[ $# -gt 0 ]]; do
    case "$1" in
        --agents) show_agents=true; show_all=false; shift ;;
        --issues) show_issues=true; show_all=false; shift ;;
        --ci)     show_ci=true;     show_all=false; shift ;;
        --help|-h) usage ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

: "${FORGE_TOKEN:?FORGE_TOKEN is required}"
: "${FORGE_API:?FORGE_API is required}"
: "${PROJECT_REPO_ROOT:?PROJECT_REPO_ROOT is required}"

forge_get() {
    curl -sf -H "Authorization: token ${FORGE_TOKEN}" \
        -H "Accept: application/json" \
        "${FORGE_API}$1"
}

# --- Agent status ---
print_agent_status() {
    echo "## Agent Status"
    echo ""
    local state_dir="${PROJECT_REPO_ROOT}/state"
    local agents=(dev review gardener supervisor planner predictor action vault exec)
    for agent in "${agents[@]}"; do
        local state_file="${state_dir}/.${agent}-active"
        if [[ -f "$state_file" ]]; then
            echo "  ${agent}: ACTIVE (since $(stat -c '%y' "$state_file" 2>/dev/null | cut -d. -f1 || echo 'unknown'))"
        else
            echo "  ${agent}: idle"
        fi
    done
    echo ""
}

# --- Open issues ---
print_open_issues() {
    echo "## Open Issues"
    echo ""
    local issues
    issues=$(forge_get "/issues?state=open&type=issues&limit=50&sort=created&direction=desc" 2>/dev/null) || {
        echo "  (failed to fetch issues from forge)"
        echo ""
        return
    }
    local count
    count=$(echo "$issues" | jq 'length')
    echo "  Total open: ${count}"
    echo ""

    # Group by key labels
    for label in backlog priority in-progress blocked; do
        local labeled
        labeled=$(echo "$issues" | jq --arg l "$label" '[.[] | select(.labels[]?.name == $l)]')
        local n
        n=$(echo "$labeled" | jq 'length')
        if [[ "$n" -gt 0 ]]; then
            echo "  [${label}] (${n}):"
            echo "$labeled" | jq -r '.[] | "    #\(.number) \(.title)"' | head -10
            echo ""
        fi
    done
}

# --- CI pipelines ---
print_ci_status() {
    echo "## CI Pipelines"
    echo ""
    if [[ -z "${WOODPECKER_SERVER:-}" || -z "${WOODPECKER_TOKEN:-}" || -z "${WOODPECKER_REPO_ID:-}" ]]; then
        echo "  (Woodpecker not configured — set WOODPECKER_SERVER, WOODPECKER_TOKEN, WOODPECKER_REPO_ID)"
        echo ""
        return
    fi
    local pipelines
    pipelines=$(curl -sf -H "Authorization: Bearer ${WOODPECKER_TOKEN}" \
        "${WOODPECKER_SERVER}/api/repos/${WOODPECKER_REPO_ID}/pipelines?per_page=10" 2>/dev/null) || {
        echo "  (failed to fetch pipelines from Woodpecker)"
        echo ""
        return
    }
    echo "$pipelines" | jq -r '.[] | "  #\(.number) [\(.status)] \(.branch) \(.commit[:8]) — \(.message // "" | split("\n")[0])"' | head -10
    echo ""
}

# --- Output ---
if $show_all || $show_agents; then print_agent_status; fi
if $show_all || $show_issues; then print_open_issues; fi
if $show_all || $show_ci;     then print_ci_status; fi
