#!/usr/bin/env bash
# CloudGuard -- Main CLI Dispatcher (Entry Point)
# Usage: dispatcher.sh [command] [options]
#
# Commands:
#   scan [--path PATH] [--format text|json|html] [--tier free|pro|team|enterprise]
#        [--category S3|IM|NW|EN|LG|CF] [--verbose] [--license-key KEY]
#   hooks install               Install pre-commit/pre-push hooks (PRO+)
#   hooks uninstall             Remove CloudGuard hooks (PRO+)
#   report [--path PATH]        Generate markdown security report (PRO+)
#   audit [--path PATH]         Deep cloud security audit (PRO+)
#   patterns                    List all detection patterns
#   status                      Show license and config info
#   --help, -h                  Show this help
#   --version, -v               Show version
#
# Exit codes:
#   0 = pass (score >= 70)
#   1 = fail (score < 70)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="1.0.0"

# --- Colors ------------------------------------------------------------------

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# --- Logging helpers ---------------------------------------------------------

log_info()    { echo -e "${BLUE}[CloudGuard]${NC} $*"; }
log_success() { echo -e "${GREEN}[CloudGuard]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[CloudGuard]${NC} $*"; }
log_error()   { echo -e "${RED}[CloudGuard]${NC} $*" >&2; }

# --- Version / Help ----------------------------------------------------------

show_version() {
  echo -e "${BOLD}CloudGuard${NC} v${VERSION}"
  echo "  Cloud infrastructure & IaC security scanner"
  echo "  https://cloudguard.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  cloudguard <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [--path PATH]           ${DIM}[FREE]${NC} Cloud security scan (30 patterns)"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  scan [--path PATH]           ${DIM}[PRO]${NC}  Cloud security scan (60 patterns)"
  echo -e "  hooks install                ${DIM}[PRO]${NC}  Install pre-commit/pre-push hooks"
  echo -e "  hooks uninstall              ${DIM}[PRO]${NC}  Remove CloudGuard hooks"
  echo -e "  report [--path PATH]         ${DIM}[PRO]${NC}  Generate markdown security report"
  echo -e "  audit [--path PATH]          ${DIM}[PRO]${NC}  Deep cloud security audit"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  scan --format json           ${DIM}[TEAM]${NC} JSON output for CI/CD"
  echo -e "  scan --format html           ${DIM}[TEAM]${NC} HTML report output"
  echo -e "  scan --category S3           ${DIM}[TEAM]${NC} Category-filtered scan"
  echo ""
  echo -e "${BOLD}OPTIONS${NC}"
  echo "  --path PATH                  Target directory or file (default: .)"
  echo "  --format text|json|html      Output format (default: text)"
  echo "  --tier free|pro|team         Override tier for pattern limit"
  echo "  --license-key KEY            Provide license key directly"
  echo "  --category S3|IM|NW|EN|LG|CF Filter by category"
  echo "  --verbose                    Show detailed scan progress"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  patterns                     List all detection patterns"
  echo "  status                       Show license and config info"
  echo "  --help, -h                   Show this help"
  echo "  --version, -v                Show version"
  echo ""
  echo -e "${BOLD}CATEGORIES${NC}"
  echo "  S3  Storage Security         (S3 buckets, encryption, access)"
  echo "  IM  IAM & Permissions        (policies, roles, MFA)"
  echo "  NW  Network Security         (security groups, VPC, ports)"
  echo "  EN  Encryption               (at rest, in transit, KMS)"
  echo "  LG  Logging & Monitoring     (CloudTrail, flow logs, alarms)"
  echo "  CF  Configuration & Compliance (tags, backups, naming)"
  echo ""
  echo -e "Get a license at ${CYAN}https://cloudguard.pages.dev${NC}"
}

# --- License -----------------------------------------------------------------

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_cloudguard_license "$required_tier"
}

# --- Hooks management --------------------------------------------------------

do_hooks_install() {
  if ! command -v lefthook &>/dev/null; then
    log_error "lefthook not installed."
    echo "  Install: brew install lefthook"
    echo "  Or: npm install -g @evilmartians/lefthook"
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
    if grep -q "cloudguard" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# --- CloudGuard hooks ----------------------------------------
    cloudguard-check:
      run: |
        CLOUDGUARD_SKILL_DIR="${CLOUDGUARD_SKILL_DIR:-$HOME/.openclaw/skills/cloudguard}"
        if [[ -f "$CLOUDGUARD_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$CLOUDGUARD_SKILL_DIR/scripts/patterns.sh"
          source "$CLOUDGUARD_SKILL_DIR/scripts/analyzer.sh"
          hook_cloudguard_check
        else
          echo "[CloudGuard] Skill not found at $CLOUDGUARD_SKILL_DIR -- skipping scan"
        fi
      fail_text: |
        Cloud security issues detected in staged files!
        Run 'cloudguard scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended CloudGuard hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged IaC files will be scanned on every commit."
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
    if grep -q "cloudguard" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      sed '/# --- CloudGuard hooks/,/fail_text:.*$/d' "$config" > "$tmp"
      grep -v "cloudguard" "$tmp" > "$config" 2>/dev/null || mv "$tmp" "$config"
      rm -f "$tmp"
      echo -e "${GREEN}+${NC} Removed CloudGuard hooks"
    else
      log_warn "No CloudGuard hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# --- Command Dispatch --------------------------------------------------------

main() {
  # Parse global options and command
  local cmd=""
  local target_path="."
  local format="text"
  local tier_override=""
  local license_key_override=""
  local verbose="false"
  local category_filter="all"

  # Parse all arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --path)
        target_path="${2:-.}"
        shift 2
        ;;
      --format)
        format="${2:-text}"
        shift 2
        ;;
      --tier)
        tier_override="${2:-}"
        shift 2
        ;;
      --license-key)
        license_key_override="${2:-}"
        shift 2
        ;;
      --verbose)
        verbose="true"
        shift
        ;;
      --category)
        category_filter="${2:-all}"
        shift 2
        ;;
      --help|-h|help)
        show_help
        return 0
        ;;
      --version|-v)
        show_version
        return 0
        ;;
      -*)
        log_error "Unknown option: $1"
        echo ""
        show_help
        return 1
        ;;
      *)
        if [[ -z "$cmd" ]]; then
          cmd="$1"
        fi
        shift
        ;;
    esac
  done

  # Apply license key override if provided
  if [[ -n "$license_key_override" ]]; then
    export CLOUDGUARD_LICENSE_KEY="$license_key_override"
  fi

  # Source dependencies
  source "$SCRIPT_DIR/license.sh"
  source "$SCRIPT_DIR/patterns.sh"
  source "$SCRIPT_DIR/analyzer.sh"

  # Determine tier and pattern limit
  local current_tier
  if [[ -n "$tier_override" ]]; then
    current_tier="$tier_override"
  else
    current_tier=$(get_cloudguard_tier)
  fi

  local pattern_limit="${TIER_PATTERN_LIMITS[$current_tier]:-30}"

  # Validate category filter
  if [[ "$category_filter" != "all" ]]; then
    case "$category_filter" in
      S3|IM|NW|EN|LG|CF) ;; # valid
      *)
        log_error "Unknown category: $category_filter"
        echo "  Available: S3, IM, NW, EN, LG, CF"
        return 1
        ;;
    esac
  fi

  # Validate format
  case "$format" in
    text|json|html) ;; # valid
    *)
      log_error "Unknown format: $format"
      echo "  Available: text, json, html"
      return 1
      ;;
  esac

  # Dispatch command
  case "${cmd:-scan}" in
    scan)
      # Check tier requirements for advanced features
      if [[ "$format" == "json" || "$format" == "html" ]]; then
        check_cloudguard_license "team" || return 1
      fi
      if [[ "$category_filter" != "all" ]]; then
        check_cloudguard_license "team" || return 1
      fi

      if [[ "$format" == "text" ]]; then
        log_info "Scanning for cloud security issues in ${BOLD}$target_path${NC}"
      fi

      do_cloudguard_scan "$target_path" "$pattern_limit" "$format" "$category_filter" "$verbose"
      ;;

    hooks)
      # Parse subcommand from remaining args
      # Since we consumed args above, check what we have
      log_error "Usage: cloudguard hooks install|uninstall"
      echo "  Specify: hooks install or hooks uninstall as command"
      return 1
      ;;

    install)
      check_cloudguard_license "pro" || return 1
      do_hooks_install
      ;;

    uninstall)
      check_cloudguard_license "pro" || return 1
      do_hooks_uninstall
      ;;

    report)
      check_cloudguard_license "pro" || return 1
      log_info "Generating cloud security report for ${BOLD}$target_path${NC}"
      generate_cloudguard_report "$target_path" "$pattern_limit" "$category_filter"
      ;;

    audit)
      check_cloudguard_license "pro" || return 1
      log_info "Running deep cloud security audit on ${BOLD}$target_path${NC}"
      do_cloudguard_audit "$target_path" "$pattern_limit" "$category_filter"
      ;;

    patterns)
      do_list_patterns
      ;;

    status)
      show_version
      echo ""
      show_cloudguard_status
      ;;

    "")
      show_help
      return 1
      ;;

    *)
      log_error "Unknown command: $cmd"
      echo ""
      show_help
      return 1
      ;;
  esac
}

main "$@"
