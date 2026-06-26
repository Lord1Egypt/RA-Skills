#!/usr/bin/env bash
# ClawTK ClawTK Engine Installer
# Downloads and installs the ClawTK Engine binary for token compression.
# Tries Homebrew first, falls back to official curl installer.
# Verifies binary after install.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
STATE_FILE="$OPENCLAW_DIR/clawtk-state.json"
RTK_VERSION_FILE="$SKILL_DIR/templates/rtk-version.txt"
RTK_MIN_VERSION="0.28.0"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${GREEN}[clawtk]${NC} $1"; }
warn() { echo -e "${YELLOW}[clawtk]${NC} $1"; }
err()  { echo -e "${RED}[clawtk]${NC} $1" >&2; }

# ── Version Check ────────────────────────────────────────────────────────────

# Compare semver: returns 0 if $1 >= $2
version_gte() {
    local IFS=.
    local i ver1=($1) ver2=($2)
    for ((i = 0; i < ${#ver2[@]}; i++)); do
        local v1="${ver1[i]:-0}"
        local v2="${ver2[i]:-0}"
        if ((v1 > v2)); then return 0; fi
        if ((v1 < v2)); then return 1; fi
    done
    return 0
}

get_rtk_version() {
    rtk --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1
}

# ── Detect Platform ──────────────────────────────────────────────────────────

detect_platform() {
    local os arch

    case "$(uname -s)" in
        Darwin) os="macos" ;;
        Linux)  os="linux" ;;
        *)
            err "Unsupported OS: $(uname -s)"
            err "Engine supports macOS and Linux."
            exit 1
            ;;
    esac

    case "$(uname -m)" in
        x86_64|amd64)  arch="x86_64" ;;
        arm64|aarch64) arch="arm64" ;;
        *)
            err "Unsupported architecture: $(uname -m)"
            exit 1
            ;;
    esac

    echo "${os}_${arch}"
}

# ── Install via Homebrew ─────────────────────────────────────────────────────

install_brew() {
    if ! command -v brew &>/dev/null; then
        return 1
    fi

    log "Installing Engine via Homebrew..."
    brew install rtk

    if command -v rtk &>/dev/null; then
        log "Engine installed via Homebrew."
        return 0
    fi

    warn "Homebrew install completed but rtk not found in PATH."
    return 1
}

# ── Install via Official Script ──────────────────────────────────────────────

install_curl() {
    local rtk_version
    rtk_version=$(cat "$RTK_VERSION_FILE" 2>/dev/null | tr -d '[:space:]')
    rtk_version="${rtk_version:-$RTK_MIN_VERSION}"

    local installer_url="https://raw.githubusercontent.com/rtk-ai/rtk/refs/tags/v${rtk_version}/install.sh"

    warn "Engine is not available via Homebrew on this system."
    warn "The installer will download and run a shell script from:"
    warn "  $installer_url"
    warn ""
    warn "If you prefer, you can install manually instead:"
    warn "  cargo install rtk@$rtk_version"
    warn "  # or download from: https://github.com/rtk-ai/rtk/releases/tag/v${rtk_version}"
    warn ""

    log "Installing Engine v$rtk_version via official installer..."

    local tmp_installer
    tmp_installer=$(mktemp "${TMPDIR:-/tmp}/rtk-install-XXXXXX.sh")

    if command -v curl &>/dev/null; then
        curl -fsSL "$installer_url" -o "$tmp_installer"
    elif command -v wget &>/dev/null; then
        wget -qO "$tmp_installer" "$installer_url"
    else
        err "Neither curl nor wget found. Cannot download ClawTK Engine."
        rm -f "$tmp_installer"
        exit 1
    fi

    # Show what will be executed so the user/reviewer can inspect
    log "Installer downloaded to $tmp_installer ($(wc -c < "$tmp_installer" | tr -d ' ') bytes)"

    sh "$tmp_installer"
    rm -f "$tmp_installer"

    # The official installer puts the binary in ~/.local/bin
    local local_bin="$HOME/.local/bin"

    if [ -f "$local_bin/rtk" ] && ! command -v rtk &>/dev/null; then
        warn "Engine installed to $local_bin but it's not in your PATH."
        warn "Add this to your shell profile (~/.zshrc or ~/.bashrc):"
        warn '  export PATH="$HOME/.local/bin:$PATH"'
        warn ""
        warn "Then restart your terminal or run: source ~/.zshrc"

        # Temporarily add to PATH for this session
        export PATH="$local_bin:$PATH"
    fi

    if command -v rtk &>/dev/null; then
        log "Engine installed via official installer."
        return 0
    fi

    err "Engine installation failed."
    return 1
}

# ── Configure ClawTK Engine for OpenClaw ───────────────────────────────────────────────

configure_rtk() {
    log "Configuring Engine for OpenClaw..."

    # Initialize Engine globally with auto-patch (no prompts)
    # This installs the PreToolUse hook that transparently rewrites bash commands
    rtk init -g --auto-patch 2>/dev/null || {
        warn "Could not auto-configure Engine hooks."
        warn "Run manually: rtk init -g"
        return 1
    }

    log "Engine hooks configured. Bash commands will be compressed automatically."
}

# ── Update State File ────────────────────────────────────────────────────────

update_state() {
    local version="$1"

    if [ ! -f "$STATE_FILE" ]; then
        warn "ClawTK state file not found. Run /clawtk setup first."
        return
    fi

    local updated
    updated=$(jq \
        --arg ver "$version" \
        '.rtkInstalled = true | .rtkVersion = $ver' \
        "$STATE_FILE")
    echo "$updated" > "$STATE_FILE"
}

# ── Main ─────────────────────────────────────────────────────────────────────

main() {
    local action="${1:-install}"

    case "$action" in
        install)
            # Check if already installed and sufficient version
            if command -v rtk &>/dev/null; then
                local current_version
                current_version=$(get_rtk_version)

                if [ -n "$current_version" ]; then
                    if version_gte "$current_version" "$RTK_MIN_VERSION"; then
                        log "Engine v$current_version already installed (meets minimum v$RTK_MIN_VERSION)."
                        configure_rtk
                        update_state "$current_version"
                        return 0
                    else
                        warn "Engine v$current_version installed but v$RTK_MIN_VERSION+ required. Upgrading..."
                    fi
                fi
            fi

            local platform
            platform=$(detect_platform)
            log "Detected platform: $platform"

            # Try Homebrew first, fall back to curl installer
            if install_brew; then
                true  # success
            elif install_curl; then
                true  # success
            else
                err "Failed to install Engine."
                err ""
                err "Manual install options:"
                err "  Homebrew:  brew install rtk"
                err "  Cargo:    cargo install rtk"
                err "  Binary:   https://github.com/rtk-ai/rtk/releases"
                exit 1
            fi

            # Verify
            local installed_version
            installed_version=$(get_rtk_version)

            if [ -z "$installed_version" ]; then
                err "Engine installed but version check failed."
                exit 1
            fi

            log "Engine v$installed_version installed successfully."

            # Configure hooks
            configure_rtk

            # Update state
            update_state "$installed_version"

            echo ""
            log "Engine is ready. CLI output will be compressed by 60-90%."
            log "Run 'rtk gain' after a session to see your token savings."
            ;;

        check)
            # Version check only (used by /clawtk status)
            if ! command -v rtk &>/dev/null; then
                echo "not_installed"
                return 1
            fi

            local version
            version=$(get_rtk_version)

            if [ -z "$version" ]; then
                echo "unknown"
                return 1
            fi

            if version_gte "$version" "$RTK_MIN_VERSION"; then
                echo "$version"
                return 0
            else
                echo "outdated:$version"
                return 1
            fi
            ;;

        *)
            err "Unknown action: $action"
            echo "Usage: install-engine.sh [install|check]"
            exit 1
            ;;
    esac
}

main "$@"
