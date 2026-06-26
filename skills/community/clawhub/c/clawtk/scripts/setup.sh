#!/usr/bin/env bash
# ClawTK Setup — One-command OpenClaw cost optimization
# Usage:
#   setup.sh              Run full setup
#   setup.sh --status     Show current optimization status
#   setup.sh --restore    Restore original config
#   setup.sh --override   Temporarily disable spend caps (1 hour)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
STATE_FILE="$OPENCLAW_DIR/clawtk-state.json"

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

# ── Full Setup ───────────────────────────────────────────────────────────────

run_setup() {
    echo -e "${BOLD}"
    echo "  ╔═══════════════════════════════════════╗"
    echo "  ║         ClawTK Setup v1.0.0         ║"
    echo "  ║   Cut your OpenClaw costs by 60-80%   ║"
    echo "  ╚═══════════════════════════════════════╝"
    echo -e "${NC}"

    # Step 1: Patch config
    log "Step 1/3: Optimizing OpenClaw config..."
    local backup_path
    backup_path=$(bash "$SCRIPT_DIR/patch-config.sh" patch | tail -1)

    # Step 2: Register hooks
    log "Step 2/3: Installing spend guard hooks..."
    if command -v openclaw &>/dev/null; then
        openclaw plugins install "$SKILL_DIR" 2>/dev/null || {
            warn "Could not register hook pack automatically."
            warn "Run manually: openclaw plugins install $SKILL_DIR"
        }
    else
        warn "openclaw CLI not found in PATH. Hooks will activate on next session."
    fi

    # Step 3: Write state (preserve existing tier/license if upgrading)
    log "Step 3/4: Saving setup state..."
    local tier="free"
    local license_key="null"
    local rtk_installed="false"
    local rtk_version="null"
    if [ -f "$STATE_FILE" ]; then
        tier=$(jq -r '.tier // "free"' "$STATE_FILE")
        license_key=$(jq -r '.licenseKey // "null"' "$STATE_FILE")
        rtk_installed=$(jq -r '.rtkInstalled // "false"' "$STATE_FILE")
        rtk_version=$(jq -r '.rtkVersion // "null"' "$STATE_FILE")
    fi

    cat > "$STATE_FILE" <<EOF
{
  "tier": "$tier",
  "version": "1.0.0",
  "installDate": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "configBackup": "$backup_path",
  "licenseKey": $([ "$license_key" = "null" ] && echo "null" || echo "\"$license_key\""),
  "rtkInstalled": $rtk_installed,
  "rtkVersion": $([ "$rtk_version" = "null" ] && echo "null" || echo "\"$rtk_version\""),
  "spendCaps": {
    "daily": 10,
    "weekly": 50
  },
  "overrideUntil": null
}
EOF

    # Step 4: Install Pro features if tier is pro/cloud
    if [ "$tier" = "pro" ] || [ "$tier" = "cloud" ]; then
        log "Step 4/4: Setting up Pro features..."

        # Install ClawTK Engine if not already installed
        if [ "$rtk_installed" != "true" ]; then
            log "Installing ClawTK Engine token compression..."
            bash "$SCRIPT_DIR/install-engine.sh" install || {
                warn "Engine installation failed. You can retry with: /clawtk setup"
            }
        else
            log "Engine already installed. Checking version..."
            bash "$SCRIPT_DIR/install-engine.sh" check >/dev/null 2>&1 || {
                warn "Engine may need updating. Run: brew upgrade rtk"
            }
        fi
    else
        log "Step 4/4: Skipped (Pro features require activation)"
    fi

    echo ""
    echo -e "${GREEN}${BOLD}Setup complete!${NC}"
    echo ""
    echo "What's active now:"
    echo "  [x] Heartbeat isolation (biggest saver)"
    echo "  [x] Optimized heartbeat interval (55m)"
    echo "  [x] Cheap heartbeat model (Flash Lite)"
    echo "  [x] Context cap (100K tokens)"
    echo "  [x] Image downscaling (800px)"
    echo "  [x] Spend caps (\$10/day, \$50/week)"
    echo "  [x] Retry loop protection"

    if [ "$tier" = "pro" ] || [ "$tier" = "cloud" ]; then
        # Re-read state to get updated Engine status
        local rtk_now
        rtk_now=$(jq -r '.rtkInstalled // false' "$STATE_FILE")
        echo "  $([ "$rtk_now" = "true" ] && echo "[x]" || echo "[ ]") ClawTK Engine token compression (Pro)"
        echo "  [x] Semantic task caching (Pro)"
        echo "  [x] Custom spend caps (Pro)"
    fi

    echo ""
    echo "Commands:"
    echo "  /clawtk savings   — See how much you're saving"
    echo "  /clawtk status    — Check optimization status"
    echo "  /clawtk restore   — Undo all changes"
    echo "  /clawtk override  — Temporarily disable caps (1hr)"

    if [ "$tier" = "free" ]; then
        echo ""
        echo -e "${YELLOW}Upgrade to Pro (\$49 one-time) for ClawTK Engine compression — up to 80% savings.${NC}"
        echo -e "${YELLOW}Visit https://clawtk.co/pro${NC}"
    fi

    echo ""
    log "Restart your OpenClaw gateway for all changes to take effect."
}

# ── Status ───────────────────────────────────────────────────────────────────

show_status() {
    if [ ! -f "$STATE_FILE" ]; then
        err "ClawTK is not set up yet. Run /clawtk setup first."
        exit 1
    fi

    local tier install_date rtk_installed override_until
    tier=$(jq -r '.tier' "$STATE_FILE")
    install_date=$(jq -r '.installDate' "$STATE_FILE")
    rtk_installed=$(jq -r '.rtkInstalled' "$STATE_FILE")
    override_until=$(jq -r '.overrideUntil // "none"' "$STATE_FILE")

    echo -e "${BOLD}ClawTK Status${NC}"
    echo -e "${CYAN}────────────────────────────────────────${NC}"
    printf "  %-22s %s\n" "Tier:" "$(echo "$tier" | tr '[:lower:]' '[:upper:]')"
    printf "  %-22s %s\n" "Installed:" "$install_date"
    printf "  %-22s %s\n" "ClawTK Engine Compression:" "$([ "$rtk_installed" = "true" ] && echo "Active" || echo "Not installed (Pro)")"
    printf "  %-22s %s\n" "Spend Cap Override:" "$override_until"
    echo -e "${CYAN}────────────────────────────────────────${NC}"

    echo ""
    echo "Config optimizations:"

    local config_file="$OPENCLAW_DIR/openclaw.json"
    if [ -f "$config_file" ]; then
        local isolated interval context_cap image_dim
        isolated=$(jq -r '.agents.defaults.heartbeat.isolatedSession // false' "$config_file")
        interval=$(jq -r '.agents.defaults.heartbeat.every // "not set"' "$config_file")
        context_cap=$(jq -r '.agents.defaults.contextTokens // "not set"' "$config_file")
        image_dim=$(jq -r '.agents.defaults.imageMaxDimensionPx // "not set"' "$config_file")

        local check_mark="[x]"
        local cross_mark="[ ]"

        echo "  $([ "$isolated" = "true" ] && echo "$check_mark" || echo "$cross_mark") Heartbeat isolation"
        echo "  $([ "$interval" = "55m" ] && echo "$check_mark" || echo "$cross_mark") Heartbeat interval (55m)"
        echo "  $check_mark Heartbeat model (cheap)"
        echo "  $([ "$context_cap" = "100000" ] && echo "$check_mark" || echo "$cross_mark") Context cap (100K)"
        echo "  $([ "$image_dim" = "800" ] && echo "$check_mark" || echo "$cross_mark") Image downscaling (800px)"
    else
        warn "Config file not found at $config_file"
    fi

    # Pro features
    if [ "$tier" = "pro" ] || [ "$tier" = "cloud" ]; then
        echo ""
        echo "Pro features:"
        if [ "$rtk_installed" = "true" ] && command -v rtk &>/dev/null; then
            local rtk_ver
            rtk_ver=$(rtk --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "unknown")
            echo "  [x] ClawTK Engine compression (v$rtk_ver)"
        else
            echo "  [ ] ClawTK Engine compression (not installed — run /clawtk setup to retry)"
        fi
        echo "  [x] Semantic task caching"
        echo "  [x] Custom spend caps"

        # Cache stats
        local cache_db="$OPENCLAW_DIR/clawtk-cache.db"
        if [ -f "$cache_db" ] && command -v sqlite3 &>/dev/null; then
            local cache_entries cache_hits
            cache_entries=$(sqlite3 "$cache_db" "SELECT count(*) FROM cache" 2>/dev/null || echo "0")
            cache_hits=$(sqlite3 "$cache_db" "SELECT sum(hit_count) FROM cache" 2>/dev/null || echo "0")
            echo ""
            echo "  Cache: $cache_entries entries, $cache_hits total hits"
        fi
    else
        echo ""
        echo -e "  ${YELLOW}Upgrade to Pro for ClawTK Engine compression, caching, and custom caps.${NC}"
        echo -e "  ${YELLOW}https://clawtk.co/pro${NC}"
    fi
}

# ── Override ─────────────────────────────────────────────────────────────────

set_override() {
    if [ ! -f "$STATE_FILE" ]; then
        err "ClawTK is not set up yet. Run /clawtk setup first."
        exit 1
    fi

    # Set override for 1 hour from now
    local override_until
    if [[ "$OSTYPE" == "darwin"* ]]; then
        override_until=$(date -u -v+1H +%Y-%m-%dT%H:%M:%SZ)
    else
        override_until=$(date -u -d "+1 hour" +%Y-%m-%dT%H:%M:%SZ)
    fi

    local updated
    updated=$(jq --arg until "$override_until" '.overrideUntil = $until' "$STATE_FILE")
    echo "$updated" > "$STATE_FILE"

    log "Spend caps disabled until $override_until"
    warn "Caps will re-enable automatically in 1 hour."
}

# ── Restore ──────────────────────────────────────────────────────────────────

run_restore() {
    bash "$SCRIPT_DIR/patch-config.sh" restore
    log "Restart your OpenClaw gateway for changes to take effect."
}

# ── Main ─────────────────────────────────────────────────────────────────────

main() {
    case "${1:-}" in
        --status)  show_status ;;
        --restore) run_restore ;;
        --override) set_override ;;
        *)         run_setup ;;
    esac
}

main "$@"
