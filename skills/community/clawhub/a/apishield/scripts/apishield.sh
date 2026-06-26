#!/usr/bin/env bash
# APIShield -- Main CLI entry point
# Usage: apishield.sh <command> [args...]
#
# Commands:
#   scan [file|dir]           One-shot API security audit (FREE: 5 files / PRO+: unlimited)
#   hooks install             Install pre-commit hooks (PRO+)
#   hooks uninstall           Remove APIShield hooks (PRO+)
#   inventory [dir]           Generate API endpoint inventory (TEAM+)
#   report [dir]              Generate security audit report (PRO+)
#   compliance [dir]          Map findings to OWASP Top 10 (TEAM+)
#   status                    Show license and config info
#   help / --help / -h        Show this help
#   version / --version / -v  Show version

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="1.0.0"

# ─── Colors ──────────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[APIShield]${NC} $*"; }
log_success() { echo -e "${GREEN}[APIShield]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[APIShield]${NC} $*"; }
log_error()   { echo -e "${RED}[APIShield]${NC} $*" >&2; }

# ─── Version / Help ─────────────────────────────────────────────────────────

show_version() {
  echo -e "${BOLD}APIShield${NC} v${VERSION}"
  echo "  API Endpoint Security Auditor"
  echo "  https://apishield.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  apishield <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC}  API security audit (up to 5 route files)"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  scan [file|dir]           ${DIM}[PRO]${NC}   Unlimited route scanning + full checks"
  echo -e "  hooks install             ${DIM}[PRO]${NC}   Install pre-commit hooks"
  echo -e "  hooks uninstall           ${DIM}[PRO]${NC}   Remove APIShield hooks"
  echo -e "  report [dir]              ${DIM}[PRO]${NC}   Generate security audit report"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  inventory [dir]           ${DIM}[TEAM]${NC}  Generate API endpoint inventory"
  echo -e "  compliance [dir]          ${DIM}[TEAM]${NC}  Map findings to OWASP Top 10"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                    Show license and config info"
  echo "  --help, -h, help          Show this help"
  echo "  --version, -v, version    Show version"
  echo ""
  echo -e "Get a license at ${CYAN}https://apishield.pages.dev${NC}"
}

# ─── License ─────────────────────────────────────────────────────────────────

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_apishield_license "$required_tier"
}

get_current_tier() {
  source "$SCRIPT_DIR/license.sh"
  get_apishield_tier
}

# ─── Hooks management ────────────────────────────────────────────────────────

do_hooks_install() {
  if ! command -v lefthook &>/dev/null; then
    log_error "lefthook not installed."
    echo "  Install: brew install lefthook"
    echo "  Or:      npm install -g @arkweid/lefthook"
    return 1
  fi

  if ! git rev-parse --git-dir &>/dev/null 2>&1; then
    log_error "Not inside a git repository."
    return 1
  fi

  local repo_root
  repo_root=$(git rev-parse --show-toplevel)

  log_info "Installing hooks in ${BOLD}$repo_root${NC}"

  local config="$repo_root/lefthook.yml"

  if [[ -f "$config" ]]; then
    if grep -q "apishield" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# --- APIShield hooks -----------------------------------------
    apishield-api-scan:
      glob: "*.{js,ts,jsx,tsx,py,rb}"
      run: |
        APISHIELD_SKILL_DIR="${APISHIELD_SKILL_DIR:-$HOME/.openclaw/skills/apishield}"
        if [[ -f "$APISHIELD_SKILL_DIR/scripts/auditor.sh" ]]; then
          source "$APISHIELD_SKILL_DIR/scripts/auditor.sh"
          hook_api_scan
        else
          echo "[APIShield] Skill not found at $APISHIELD_SKILL_DIR -- skipping scan"
        fi
      fail_text: |
        API security issues detected in staged files!
        Run 'apishield scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended APIShield hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged route files will be scanned for security issues on every commit."
}

do_hooks_uninstall() {
  if ! git rev-parse --git-dir &>/dev/null 2>&1; then
    log_error "Not inside a git repository."
    return 1
  fi

  local repo_root
  repo_root=$(git rev-parse --show-toplevel)
  local config="$repo_root/lefthook.yml"

  if [[ -f "$config" ]]; then
    if grep -q "apishield" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      # Remove the APIShield hook block
      awk '/# --- APIShield hooks/{skip=1} /^[[:space:]]*[a-zA-Z]/ && skip && !/apishield/{skip=0} !skip' "$config" > "$tmp"
      mv "$tmp" "$config"
      echo -e "${GREEN}+${NC} Removed APIShield hooks"
    else
      log_warn "No APIShield hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# ─── Scan command ─────────────────────────────────────────────────────────────

do_scan() {
  local target="${1:-.}"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  # Determine tier for file limits
  local tier="free"
  tier=$(get_current_tier 2>/dev/null) || tier="free"

  source "$SCRIPT_DIR/auditor.sh"

  local max_files=5
  if [[ "$tier" == "pro" || "$tier" == "team" || "$tier" == "enterprise" ]]; then
    max_files=0  # 0 = unlimited
  fi

  log_info "Scanning for API security issues in ${BOLD}$target${NC}"
  do_api_scan "$target" "$max_files"
}

# ─── Report command ──────────────────────────────────────────────────────────

do_report() {
  local target="${1:-.}"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  log_info "Generating security audit report for ${BOLD}$target${NC}"
  source "$SCRIPT_DIR/auditor.sh"
  generate_report "$target"
}

# ─── Inventory command ───────────────────────────────────────────────────────

do_inventory() {
  local target="${1:-.}"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  log_info "Generating API endpoint inventory for ${BOLD}$target${NC}"
  source "$SCRIPT_DIR/auditor.sh"
  generate_inventory "$target"
}

# ─── Compliance command ──────────────────────────────────────────────────────

do_compliance() {
  local target="${1:-.}"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  log_info "Mapping findings to OWASP Top 10 for ${BOLD}$target${NC}"
  source "$SCRIPT_DIR/auditor.sh"
  generate_compliance "$target"
}

# ─── Status command ──────────────────────────────────────────────────────────

do_status() {
  show_version
  echo ""
  source "$SCRIPT_DIR/license.sh"
  show_apishield_status
}

# ─── Command dispatch ────────────────────────────────────────────────────────

main() {
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    scan)
      do_scan "${1:-.}"
      ;;

    hooks)
      require_license "pro"
      local subcmd="${1:-}"
      case "$subcmd" in
        install)
          do_hooks_install
          ;;
        uninstall)
          do_hooks_uninstall
          ;;
        *)
          log_error "Unknown hooks subcommand: $subcmd"
          echo "  Usage: apishield hooks [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    report)
      require_license "pro"
      do_report "${1:-.}"
      ;;

    inventory)
      require_license "team"
      do_inventory "${1:-.}"
      ;;

    compliance)
      require_license "team"
      do_compliance "${1:-.}"
      ;;

    status)
      do_status
      ;;

    --help|-h|help)
      show_help
      ;;

    --version|-v|version)
      show_version
      ;;

    "")
      show_help
      exit 1
      ;;

    *)
      log_error "Unknown command: $cmd"
      echo ""
      show_help
      exit 1
      ;;
  esac
}

main "$@"
