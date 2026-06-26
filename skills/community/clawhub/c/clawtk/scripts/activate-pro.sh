#!/usr/bin/env bash
# ClawTK Pro Activation
# Validates a license key and unlocks Pro features.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
STATE_FILE="$OPENCLAW_DIR/clawtk-state.json"
API_BASE="https://api.clawtk.co/v1"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

log()  { echo -e "${GREEN}[clawtk]${NC} $1"; }
warn() { echo -e "${YELLOW}[clawtk]${NC} $1"; }
err()  { echo -e "${RED}[clawtk]${NC} $1" >&2; }

# ── Validate Key Format ─────────────────────────────────────────────────────

validate_format() {
    local key="$1"
    # Expected format: XXXX-XXXX-XXXX or XXXX-XXXX-XXXX-XXXX
    if [[ ! "$key" =~ ^[A-Z0-9]{4}(-[A-Z0-9]{4}){2,3}$ ]]; then
        err "Invalid key format: $key"
        err "Expected format: XXXX-XXXX-XXXX"
        exit 1
    fi
}

# ── Validate Against API ────────────────────────────────────────────────────

validate_key() {
    local key="$1"
    local response

    log "Validating license key..."

    if command -v curl &>/dev/null; then
        response=$(curl -sS --max-time 10 \
            -H "Content-Type: application/json" \
            -d "{\"key\": \"$key\"}" \
            "$API_BASE/validate" 2>&1) || {
            err "Could not reach activation server."
            err "Check your internet connection and try again."
            err "If the problem persists, contact support@clawtk.co"
            exit 1
        }
    elif command -v wget &>/dev/null; then
        response=$(wget -qO- --timeout=10 \
            --header="Content-Type: application/json" \
            --post-data="{\"key\": \"$key\"}" \
            "$API_BASE/validate" 2>&1) || {
            err "Could not reach activation server."
            exit 1
        }
    else
        err "Neither curl nor wget found."
        exit 1
    fi

    # Parse response
    local valid tier
    valid=$(echo "$response" | jq -r '.valid // false' 2>/dev/null)
    tier=$(echo "$response" | jq -r '.tier // "pro"' 2>/dev/null)

    if [ "$valid" != "true" ]; then
        local message
        message=$(echo "$response" | jq -r '.message // "Invalid or expired license key."' 2>/dev/null)
        err "$message"
        err ""
        err "Purchase a key at https://clawtk.co/pro"
        exit 1
    fi

    echo "$tier"
}

# ── Update State ─────────────────────────────────────────────────────────────

activate_state() {
    local tier="$1"
    local key="$2"

    if [ ! -f "$STATE_FILE" ]; then
        err "ClawTK is not set up. Run /clawtk setup first."
        exit 1
    fi

    local updated
    updated=$(jq \
        --arg tier "$tier" \
        --arg key "$key" \
        --arg date "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        '.tier = $tier | .licenseKey = $key | .activatedAt = $date' \
        "$STATE_FILE")
    echo "$updated" > "$STATE_FILE"
}

# ── Install Pro Features ────────────────────────────────────────────────────

install_pro_features() {
    echo ""
    log "Installing Pro features..."

    # Install ClawTK Engine
    log "Setting up ClawTK Engine token compression..."
    bash "$SCRIPT_DIR/install-engine.sh" install || {
        warn "Engine installation failed. You can install it manually later."
        warn "Run: /clawtk setup (it will retry Engine installation)"
    }

    echo ""
    echo -e "${BOLD}${GREEN}Pro activated!${NC}"
    echo ""
    echo "New features unlocked:"
    echo "  [x] ClawTK Engine token compression (60-90% savings on CLI output)"
    echo "  [x] Custom spend caps (edit via /clawtk config)"
    echo "  [x] Semantic task caching"
    echo ""
    echo "Run /clawtk savings after your next session to see the difference."
}

# ── Main ─────────────────────────────────────────────────────────────────────

main() {
    local key="${1:-}"

    if [ -z "$key" ]; then
        err "Usage: activate-pro.sh <license-key>"
        err "Example: activate-pro.sh ABCD-1234-EFGH"
        err ""
        err "Purchase a key at https://clawtk.co/pro"
        exit 1
    fi

    # Normalize to uppercase
    key=$(echo "$key" | tr '[:lower:]' '[:upper:]')

    validate_format "$key"

    local tier
    tier=$(validate_key "$key")

    activate_state "$tier" "$key"
    log "License validated. Tier: $(echo "$tier" | tr '[:lower:]' '[:upper:]')"

    install_pro_features
}

main "$@"
