#!/usr/bin/env bash
# AuthAudit -- Main CLI Entry Point (Dispatcher)
# Authentication & Authorization Pattern Analyzer
#
# Usage: dispatcher.sh [command] [options]
#
# Commands:
#   scan [--path DIR] [--format FMT] [--category CAT]   Auth audit (FREE: 30 patterns / PRO: 60 / TEAM: 90)
#   hooks install                                         Install pre-commit hooks (PRO+)
#   hooks uninstall                                       Remove AuthAudit hooks (PRO+)
#   report [--path DIR]                                   Generate markdown security report (PRO+)
#   status                                                Show license and config info
#   help / --help / -h                                    Show this help
#   version / --version / -v                              Show version
#
# Options:
#   --path <dir|file>     Target path to scan (default: current directory)
#   --format <fmt>        Output format: text, json, html (default: text)
#   --tier <tier>         Override tier: free, pro, team, enterprise
#   --license-key <key>   Provide license key inline
#   --verbose             Show detailed scan progress
#   --category <cat>      Scan specific category: AC, SM, AZ, TK, CS, PW

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

# ─── Logging ─────────────────────────────────────────────────────────────────

log_info()    { echo -e "${BLUE}[AuthAudit]${NC} $*"; }
log_success() { echo -e "${GREEN}[AuthAudit]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[AuthAudit]${NC} $*"; }
log_error()   { echo -e "${RED}[AuthAudit]${NC} $*" >&2; }

# ─── Version / Help ─────────────────────────────────────────────────────────

show_version() {
  echo -e "${BOLD}AuthAudit${NC} v${VERSION}"
  echo "  Authentication & Authorization Pattern Analyzer"
  echo "  https://authaudit.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  authaudit <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [options]              ${DIM}[FREE]${NC}  Auth audit (30 patterns)"
  echo -e "    --path <dir|file>         Target to scan (default: .)"
  echo -e "    --format <text|json>      Output format (default: text)"
  echo -e "    --category <AC|SM|...>    Scan specific category only"
  echo -e "    --verbose                 Show file-by-file progress"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  scan [options]              ${DIM}[PRO]${NC}   Extended audit (60 patterns)"
  echo -e "  hooks install               ${DIM}[PRO]${NC}   Install pre-commit hooks"
  echo -e "  hooks uninstall             ${DIM}[PRO]${NC}   Remove AuthAudit hooks"
  echo -e "  report [--path <dir>]       ${DIM}[PRO]${NC}   Generate security audit report"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  scan [options]              ${DIM}[TEAM]${NC}  Full audit (all 90 patterns)"
  echo -e "    --format <text|json|html> HTML report with filtering"
  echo ""
  echo -e "${BOLD}GLOBAL OPTIONS${NC}"
  echo -e "  --tier <tier>               Override tier detection"
  echo -e "  --license-key <key>         Provide license key inline"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                      Show license and config info"
  echo "  --help, -h, help            Show this help"
  echo "  --version, -v, version      Show version"
  echo ""
  echo -e "${BOLD}CHECK CATEGORIES${NC}"
  echo "  AC   Authentication Checks         (15 patterns)"
  echo "  SM   Session Management             (15 patterns)"
  echo "  AZ   Authorization / Access Control (15 patterns)"
  echo "  TK   Token Handling                 (15 patterns)"
  echo "  CS   CSRF Protection                (15 patterns)"
  echo "  PW   Password & Credential Mgmt    (15 patterns)"
  echo ""
  echo -e "${BOLD}SEVERITY WEIGHTS${NC}"
  echo "  critical  =  25 points"
  echo "  high      =  15 points"
  echo "  medium    =   8 points"
  echo "  low       =   3 points"
  echo ""
  echo -e "${BOLD}SCORING${NC}"
  echo "  Pass threshold: 70   Grades: A(90+) B(80-89) C(70-79) D(60-69) F(<60)"
  echo ""
  echo -e "Get a license at ${CYAN}https://authaudit.dev${NC}"
}

# ─── Argument Parsing ────────────────────────────────────────────────────────

parse_args() {
  # Defaults
  SCAN_PATH="."
  OUTPUT_FORMAT="text"
  OVERRIDE_TIER=""
  INLINE_KEY=""
  VERBOSE="false"
  TARGET_CATEGORY=""
  COMMAND=""
  SUBCOMMAND=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      scan|hooks|report|status|help|version)
        COMMAND="$1"
        shift
        # Check for subcommand (hooks install / hooks uninstall)
        if [[ "$COMMAND" == "hooks" && $# -gt 0 ]]; then
          SUBCOMMAND="$1"
          shift
        fi
        ;;
      --path)
        SCAN_PATH="${2:-.}"
        shift 2
        ;;
      --format)
        OUTPUT_FORMAT="${2:-text}"
        shift 2
        ;;
      --tier)
        OVERRIDE_TIER="${2:-}"
        shift 2
        ;;
      --license-key)
        INLINE_KEY="${2:-}"
        shift 2
        ;;
      --verbose)
        VERBOSE="true"
        shift
        ;;
      --category)
        TARGET_CATEGORY="${2:-}"
        shift 2
        ;;
      --help|-h)
        COMMAND="help"
        shift
        ;;
      --version|-v)
        COMMAND="version"
        shift
        ;;
      -*)
        log_error "Unknown option: $1"
        echo "  Run 'authaudit --help' for usage."
        exit 1
        ;;
      *)
        # If no command set yet, treat first positional as command
        if [[ -z "$COMMAND" ]]; then
          COMMAND="$1"
        elif [[ -z "$SUBCOMMAND" && "$COMMAND" == "hooks" ]]; then
          SUBCOMMAND="$1"
        else
          # Treat as path
          SCAN_PATH="$1"
        fi
        shift
        ;;
    esac
  done

  # Default command
  [[ -z "$COMMAND" ]] && COMMAND=""
}

# ─── License Integration ────────────────────────────────────────────────────

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_authaudit_license "$required_tier"
}

get_current_tier() {
  source "$SCRIPT_DIR/license.sh"
  get_authaudit_tier
}

get_current_pattern_limit() {
  source "$SCRIPT_DIR/license.sh"
  get_pattern_limit
}

# ─── Tier Resolution ────────────────────────────────────────────────────────
# Resolves the effective tier from: --tier override > --license-key > env/config

resolve_tier() {
  # If --license-key was provided inline, set it as env var for license.sh
  if [[ -n "$INLINE_KEY" ]]; then
    export AUTHAUDIT_LICENSE_KEY="$INLINE_KEY"
  fi

  # If --tier was provided, use it directly
  if [[ -n "$OVERRIDE_TIER" ]]; then
    case "$OVERRIDE_TIER" in
      free|pro|team|enterprise) echo "$OVERRIDE_TIER" ;;
      *)
        log_error "Invalid tier: $OVERRIDE_TIER"
        echo "  Valid tiers: free, pro, team, enterprise"
        exit 1
        ;;
    esac
    return
  fi

  # Otherwise detect from license
  local tier
  tier=$(get_current_tier 2>/dev/null) || tier="free"
  echo "$tier"
}

# Map tier to pattern limit per category
tier_to_pattern_limit() {
  local tier="$1"
  case "$tier" in
    enterprise|team) echo 15 ;;
    pro)             echo 10 ;;
    *)               echo 5  ;;
  esac
}

# ─── Category Validation ────────────────────────────────────────────────────

validate_category() {
  local cat="$1"
  case "$cat" in
    AC|SM|AZ|TK|CS|PW) return 0 ;;
    *)
      log_error "Invalid category: $cat"
      echo "  Valid categories: AC, SM, AZ, TK, CS, PW"
      echo ""
      echo "  AC  Authentication Checks"
      echo "  SM  Session Management"
      echo "  AZ  Authorization / Access Control"
      echo "  TK  Token Handling"
      echo "  CS  CSRF Protection"
      echo "  PW  Password & Credential Management"
      return 1
      ;;
  esac
}

# ─── Hooks Management ───────────────────────────────────────────────────────

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
    if grep -q "authaudit" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# --- AuthAudit hooks -----------------------------------------
    authaudit-scan:
      glob: "*.{js,ts,jsx,tsx,py,rb,go,java,php,cs}"
      run: |
        AUTHAUDIT_SKILL_DIR="${AUTHAUDIT_SKILL_DIR:-$HOME/.openclaw/skills/authaudit}"
        if [[ -f "$AUTHAUDIT_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$AUTHAUDIT_SKILL_DIR/scripts/patterns.sh"
          source "$AUTHAUDIT_SKILL_DIR/scripts/analyzer.sh"
          hook_scan
        else
          echo "[AuthAudit] Skill not found at $AUTHAUDIT_SKILL_DIR -- skipping scan"
        fi
      fail_text: |
        Authentication/authorization issues detected in staged files!
        Run 'authaudit scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended AuthAudit hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged source files will be scanned for auth issues on every commit."
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
    if grep -q "authaudit" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      # Remove the AuthAudit hook block
      awk '/# --- AuthAudit hooks/{skip=1} /^[[:space:]]*[a-zA-Z]/ && skip && !/authaudit/{skip=0} !skip' "$config" > "$tmp"
      mv "$tmp" "$config"
      echo -e "${GREEN}+${NC} Removed AuthAudit hooks from lefthook.yml"
    else
      log_warn "No AuthAudit hooks found in lefthook.yml"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# ─── Scan Command ───────────────────────────────────────────────────────────

do_scan() {
  local target="$SCAN_PATH"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  # Resolve tier and pattern limit
  local tier
  tier=$(resolve_tier)
  local pattern_limit
  pattern_limit=$(tier_to_pattern_limit "$tier")

  # Validate category if specified
  if [[ -n "$TARGET_CATEGORY" ]]; then
    validate_category "$TARGET_CATEGORY" || return 1
  fi

  # HTML format requires team tier
  if [[ "$OUTPUT_FORMAT" == "html" ]]; then
    local tier_level=0
    case "$tier" in
      enterprise) tier_level=3 ;;
      team)       tier_level=2 ;;
      pro)        tier_level=1 ;;
      *)          tier_level=0 ;;
    esac
    if [[ $tier_level -lt 2 ]]; then
      log_error "HTML output requires ${BOLD}team${NC} tier or higher."
      echo -e "  Upgrade at: ${CYAN}https://authaudit.dev/pricing${NC}"
      return 1
    fi
  fi

  # Load analyzer
  source "$SCRIPT_DIR/analyzer.sh"

  if [[ "$OUTPUT_FORMAT" == "text" ]]; then
    log_info "Scanning for auth/authz issues in ${BOLD}$target${NC}"
    echo -e "  ${DIM}Tier: ${tier} (${pattern_limit} patterns per category)${NC}"
  fi

  run_scan "$target" "$OUTPUT_FORMAT" "$pattern_limit" "$VERBOSE" "$TARGET_CATEGORY"
}

# ─── Report Command ─────────────────────────────────────────────────────────

do_report() {
  local target="$SCAN_PATH"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  local tier
  tier=$(resolve_tier)
  local pattern_limit
  pattern_limit=$(tier_to_pattern_limit "$tier")

  log_info "Generating security audit report for ${BOLD}$target${NC}"
  source "$SCRIPT_DIR/analyzer.sh"
  generate_report "$target" "$pattern_limit"
}

# ─── Status Command ─────────────────────────────────────────────────────────

do_status() {
  show_version
  echo ""
  source "$SCRIPT_DIR/license.sh"
  show_authaudit_status
}

# ─── Command Dispatch ───────────────────────────────────────────────────────

main() {
  parse_args "$@"

  case "$COMMAND" in
    scan)
      do_scan
      ;;

    hooks)
      require_license "pro"
      case "$SUBCOMMAND" in
        install)
          do_hooks_install
          ;;
        uninstall)
          do_hooks_uninstall
          ;;
        *)
          log_error "Unknown hooks subcommand: $SUBCOMMAND"
          echo "  Usage: authaudit hooks [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    report)
      require_license "pro"
      do_report
      ;;

    status)
      do_status
      ;;

    help|--help|-h)
      show_help
      ;;

    version|--version|-v)
      show_version
      ;;

    "")
      show_help
      exit 1
      ;;

    *)
      log_error "Unknown command: $COMMAND"
      echo ""
      show_help
      exit 1
      ;;
  esac
}

main "$@"
