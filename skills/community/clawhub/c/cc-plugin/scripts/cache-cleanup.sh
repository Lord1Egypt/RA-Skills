#!/bin/bash
# Plugin cache cleanup script
# Keeps only the latest version directory for each plugin
# Latest = most recently created directory (by birthtime)

set -euo pipefail

CACHE_DIR="${HOME}/.claude/plugins/cache"
DRY_RUN=false
VERBOSE=false

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -n, --dry-run    Show what would be deleted without actually deleting"
    echo "  -v, --verbose    Show detailed information"
    echo "  -h, --help       Show this help message"
}

usage_exit() {
    usage
    exit "${1:-2}"
}

while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--dry-run) DRY_RUN=true; shift ;;
        -v|--verbose) VERBOSE=true; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Unknown option: $1" >&2; usage_exit 2 ;;
    esac
done

log() {
    if [[ "$VERBOSE" == true ]]; then
        echo "$@"
    fi
}

cleanup_marketplace() {
    local marketplace_dir="$1"
    local marketplace_name
    marketplace_name=$(basename "$marketplace_dir")

    log "Processing marketplace: $marketplace_name"

    # Skip if not a directory
    [[ -d "$marketplace_dir" ]] || return 0

    # Skip temp directories
    if [[ "$marketplace_name" == temp_git_* ]]; then
        if [[ "$DRY_RUN" == true ]]; then
            echo "[DRY-RUN] Would delete temp directory: $marketplace_dir"
        else
            echo "Deleting temp directory: $marketplace_dir"
            rm -rf "$marketplace_dir"
        fi
        return 0
    fi

    # Process each plugin in the marketplace
    for plugin_dir in "$marketplace_dir"/*/; do
        [[ -d "$plugin_dir" ]] || continue

        local plugin_name=$(basename "$plugin_dir")
        log "  Processing plugin: $plugin_name"

        # Get all version directories with their birthtime
        local versions=()
        local times=()

        for version_dir in "$plugin_dir"/*/; do
            [[ -d "$version_dir" ]] || continue
            local version_name=$(basename "$version_dir")

            # Get a creation/modification time (portable best-effort).
            # 1) macOS/BSD: birthtime via `stat -f "%B"`
            # 2) Linux: birthtime via `stat -c "%W"` (returns 0 when filesystem doesn't track it)
            # 3) Fallback (any platform): modification time via `stat -c "%Y"` so versions are still ordered
            local birthtime
            if birthtime=$(stat -f "%B" "$version_dir" 2>/dev/null); then
                :
            elif birthtime=$(stat -c "%W" "$version_dir" 2>/dev/null) && [[ "$birthtime" != "0" ]]; then
                :
            elif birthtime=$(stat -c "%Y" "$version_dir" 2>/dev/null); then
                :
            else
                birthtime=0
            fi

            versions+=("$version_name")
            times+=("$birthtime")
        done

        # Skip if only one or no versions
        if [[ ${#versions[@]} -le 1 ]]; then
            log "    Only ${#versions[@]} version(s), skipping"
            continue
        fi

        # Find the latest version (highest birthtime)
        local latest_idx=0
        local latest_time=${times[0]}

        for i in "${!times[@]}"; do
            if [[ ${times[$i]} -gt $latest_time ]]; then
                latest_time=${times[$i]}
                latest_idx=$i
            fi
        done

        local latest_version=${versions[$latest_idx]}
        log "    Latest version: $latest_version (birthtime: $latest_time)"

        # Delete old versions
        for i in "${!versions[@]}"; do
            if [[ $i -ne $latest_idx ]]; then
                local old_version=${versions[$i]}
                local old_dir="${plugin_dir}${old_version}"

                if [[ "$DRY_RUN" == true ]]; then
                    echo "[DRY-RUN] Would delete: $old_dir"
                else
                    echo "Deleting old cache: $old_dir"
                    rm -rf "$old_dir"
                fi
            fi
        done
    done
}

main() {
    if [[ ! -d "$CACHE_DIR" ]]; then
        echo "Cache directory not found: $CACHE_DIR"
        exit 1
    fi

    echo "Plugin cache cleanup"
    echo "===================="
    if [[ "$DRY_RUN" == true ]]; then
        echo "Mode: DRY-RUN (no changes will be made)"
    fi
    echo ""

    # Process each marketplace
    for marketplace_dir in "$CACHE_DIR"/*/; do
        cleanup_marketplace "$marketplace_dir"
    done

    echo ""
    echo "Done!"
}

main
