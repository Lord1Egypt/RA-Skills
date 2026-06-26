#!/bin/bash
# Thin wrapper that keeps the old CLI shape while delegating to workflow.py.

set -euo pipefail

QUERY=""
EPISODE=""
PREFER_4K=false
LATEST_SEASON=false
SEARCH_ONLY=false
DOWNLOADER="transmission"
DOWNLOAD_DIR="${DOWNLOAD_DIR:-$HOME/Downloads}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --search-only) SEARCH_ONLY=true; shift ;;
        --prefer-4k) PREFER_4K=true; shift ;;
        --latest-season) LATEST_SEASON=true; shift ;;
        --episode) EPISODE="$2"; shift 2 ;;
        --downloader) DOWNLOADER="$2"; shift 2 ;;
        --download-dir) DOWNLOAD_DIR="$2"; shift 2 ;;
        -*) echo "未知选项：$1" >&2; exit 1 ;;
        *) [ -z "$QUERY" ] && QUERY="$1" || EPISODE="$1"; shift ;;
    esac
done

if [ -z "$QUERY" ]; then
    echo '{"error": "未提供番剧名"}'
    exit 1
fi

ARGS=()
[ -n "$EPISODE" ] && ARGS+=(--episode "$EPISODE")
[ "$PREFER_4K" = true ] && ARGS+=(--prefer-4k)
[ "$LATEST_SEASON" = true ] && ARGS+=(--latest-season)
[ "$SEARCH_ONLY" = false ] && ARGS+=(--download --downloader "$DOWNLOADER" --download-dir "$DOWNLOAD_DIR")

python3 "$SCRIPT_DIR/scripts/workflow.py" "$QUERY" "${ARGS[@]}" --json
