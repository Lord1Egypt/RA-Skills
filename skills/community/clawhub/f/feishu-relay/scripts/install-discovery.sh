#!/bin/bash
#=============================================================================
# Auto-Discovery Installer
# Opt-in only: Scans for other skills' notify scripts
#=============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DISCOVERY_DIR="${SKILL_DIR}/.discovered"
OPENCLAW_DIR="${HOME}/.openclaw"

usage() {
    echo "Usage: $0 --install | --uninstall | --dry-run | --help"
    echo ""
    echo "Options:"
    echo "  --install     Install discovery links"
    echo "  --uninstall   Remove discovery links"
    echo "  --dry-run     Show what would be done"
    echo "  --help        Show this help"
    echo ""
    echo "This scans for notify scripts in known locations and creates links."
}

if [ $# -eq 0 ]; then
    usage
    exit 1
fi

ACTION=""
DRY_RUN=false

while [ $# -gt 0 ]; do
    case "$1" in
        --install) ACTION="install" ;;
        --uninstall) ACTION="uninstall" ;;
        --dry-run) DRY_RUN=true ;;
        --help) usage; exit 0 ;;
        *) echo "Unknown option: $1"; usage; exit 1 ;;
    esac
    shift
done

# Known locations to scan
SCAN_DIRS=(
    "${OPENCLAW_DIR}/workspace/*/scripts"
    "${OPENCLAW_DIR}/skills/*/scripts"
)

do_install() {
    echo "Scanning for notify scripts..."
    
    # Create discovery directory
    if [ "$DRY_RUN" = false ]; then
        mkdir -p "$DISCOVERY_DIR"
    fi
    
    found=0
    for pattern in "${SCAN_DIRS[@]}"; do
        for dir in $pattern; do
            if [ -d "$dir" ]; then
                for script in "$dir"/*notify*.sh "$dir"/*Notifier*.sh; do
                    if [ -f "$script" ] && [ -x "$script" ]; then
                        basename=$(basename "$script")
                        link="${DISCOVERY_DIR}/${basename}"
                        
                        if [ "$DRY_RUN" = true ]; then
                            echo "  [DRY RUN] Would link: $script -> $link"
                        else
                            if [ ! -L "$link" ]; then
                                ln -sf "$script" "$link"
                                echo "Linked: $basename"
                                found=1
                            fi
                        fi
                    fi
                done
            fi
        done
    done
    
    if [ "$found" = 0 ] && [ "$DRY_RUN" = false ]; then
        echo "No notify scripts found in scan locations"
    fi
    
    if [ "$DRY_RUN" = true ]; then
        echo "Scan complete (dry run)"
    else
        echo "Discovery links installed in: $DISCOVERY_DIR"
    fi
}

do_uninstall() {
    echo "Removing discovery links..."
    
    if [ "$DRY_RUN" = true ]; then
        if [ -d "$DISCOVERY_DIR" ]; then
            echo "  [DRY RUN] Would remove all links in: $DISCOVERY_DIR"
            ls -la "$DISCOVERY_DIR"
        else
            echo "  [DRY RUN] Discovery directory not found"
        fi
    else
        if [ -d "$DISCOVERY_DIR" ]; then
            rm -rf "$DISCOVERY_DIR"
            echo "Removed successfully"
        else
            echo "Discovery directory not found, nothing to remove"
        fi
    fi
}

case "$ACTION" in
    install) do_install ;;
    uninstall) do_uninstall ;;
    *) echo "Error: No action specified"; usage; exit 1 ;;
esac
