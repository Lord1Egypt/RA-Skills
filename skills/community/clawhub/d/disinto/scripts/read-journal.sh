#!/usr/bin/env bash
set -euo pipefail

# read-journal.sh — read agent journal entries
#
# Usage: read-journal.sh AGENT [--date YYYY-MM-DD] [--list] [--help]
#   AGENT: planner, supervisor, or exec
#   --date: specific date (default: today)
#   --list: list available journal dates instead of reading
#
# Required env: PROJECT_REPO_ROOT

usage() {
    cat <<'USAGE'
read-journal.sh AGENT [--date YYYY-MM-DD] [--list] [--help]
  AGENT: planner, supervisor, or exec
  --date: specific date (default: today)
  --list: list available journal dates instead of reading
USAGE
    exit 0
}

agent=""
target_date=$(date +%Y-%m-%d)
list_mode=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --date)  target_date="$2"; shift 2 ;;
        --list)  list_mode=true;   shift ;;
        --help|-h) usage ;;
        -*)      echo "Unknown option: $1" >&2; exit 1 ;;
        *)
            if [[ -z "$agent" ]]; then
                agent="$1"
            else
                echo "Unexpected argument: $1" >&2; exit 1
            fi
            shift
            ;;
    esac
done

: "${PROJECT_REPO_ROOT:?PROJECT_REPO_ROOT is required}"

if [[ -z "$agent" ]]; then
    echo "Error: agent name is required (planner, supervisor, exec)" >&2
    echo "" >&2
    usage
fi

# --- Resolve journal directory ---
case "$agent" in
    planner)    journal_dir="${PROJECT_REPO_ROOT}/planner/journal" ;;
    supervisor) journal_dir="${PROJECT_REPO_ROOT}/supervisor/journal" ;;
    exec)       journal_dir="${PROJECT_REPO_ROOT}/exec/journal" ;;
    predictor)
        echo "The predictor does not write journal files."
        echo "Its memory lives in forge issues labeled 'prediction/unreviewed' and 'prediction/actioned'."
        echo ""
        echo "Query predictions with:"
        echo "  curl -sH 'Authorization: token \${FORGE_TOKEN}' '\${FORGE_API}/issues?state=open&labels=prediction%2Funreviewed'"
        exit 0
        ;;
    *)
        echo "Error: unknown agent '${agent}'" >&2
        echo "Available: planner, supervisor, exec, predictor" >&2
        exit 1
        ;;
esac

if [[ ! -d "$journal_dir" ]]; then
    echo "No journal directory found at ${journal_dir}" >&2
    exit 1
fi

# --- List mode ---
if $list_mode; then
    echo "Available journal dates for ${agent}:"
    find "$journal_dir" -maxdepth 1 -name '*.md' -printf '%f\n' 2>/dev/null | sed 's|\.md$||' | sort -r | head -20
    exit 0
fi

# --- Read specific date ---
journal_file="${journal_dir}/${target_date}.md"
if [[ -f "$journal_file" ]]; then
    cat "$journal_file"
else
    echo "No journal entry for ${agent} on ${target_date}" >&2
    echo "" >&2
    echo "Recent entries:" >&2
    find "$journal_dir" -maxdepth 1 -name '*.md' -printf '%f\n' 2>/dev/null | sed 's|\.md$||' | sort -r | head -5 >&2
    exit 1
fi
