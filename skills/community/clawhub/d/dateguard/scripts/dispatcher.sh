#!/usr/bin/env bash
# DateGuard -- Main CLI Dispatcher (Entry Point)
# Usage: dispatcher.sh [options]
#
# Options:
#   --path <path>          File or directory to scan (default: .)
#   --format <fmt>         Output format: text, json, html (default: text)
#   --tier <tier>          Override tier: free, pro, team, enterprise
#   --license-key <key>    Provide license key directly
#   --verbose              Show detailed per-match output
#   --category <cat>       Filter to specific category: TZ, NF, EP, DA, CP, ST
#   --help, -h             Show help
#   --version, -v          Show version
#   status                 Show license and configuration info
#   patterns               List all detection patterns

set -euo pipefail

# --- Script location ----------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="1.0.0"

# --- Colors -------------------------------------------------------------------

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# --- Logging helpers ----------------------------------------------------------

log_info()    { echo -e "${BLUE}[DateGuard]${NC} $*"; }
log_success() { echo -e "${GREEN}[DateGuard]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[DateGuard]${NC} $*"; }
log_error()   { echo -e "${RED}[DateGuard]${NC} $*" >&2; }

# --- Version & Help -----------------------------------------------------------

show_version() {
  echo -e "${BOLD}DateGuard${NC} v${VERSION}"
  echo "  Date/time anti-pattern scanner"
  echo "  https://dateguard.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  dispatcher.sh [options]"
  echo "  dispatcher.sh status"
  echo "  dispatcher.sh patterns"
  echo ""
  echo -e "${BOLD}OPTIONS${NC}"
  echo -e "  --path <path>          ${DIM}File or directory to scan (default: .)${NC}"
  echo -e "  --format <fmt>         ${DIM}Output: text, json, html (default: text)${NC}"
  echo -e "  --tier <tier>          ${DIM}Override: free, pro, team, enterprise${NC}"
  echo -e "  --license-key <key>    ${DIM}Provide license key directly${NC}"
  echo -e "  --verbose              ${DIM}Detailed per-match output${NC}"
  echo -e "  --category <cat>       ${DIM}Filter: TZ, NF, EP, DA, CP, ST${NC}"
  echo -e "  --help, -h             ${DIM}Show this help${NC}"
  echo -e "  --version, -v          ${DIM}Show version${NC}"
  echo ""
  echo -e "${BOLD}COMMANDS${NC}"
  echo -e "  status                 ${DIM}Show license and configuration info${NC}"
  echo -e "  patterns               ${DIM}List all detection patterns${NC}"
  echo ""
  echo -e "${BOLD}TIER SYSTEM${NC}"
  echo -e "  ${GREEN}FREE${NC}        30 patterns  TZ, NF categories"
  echo -e "  ${CYAN}PRO${NC}  \$19/mo  60 patterns  TZ, NF, EP, DA"
  echo -e "  ${MAGENTA}TEAM${NC} \$39/mo  90 patterns  TZ, NF, EP, DA, CP, ST"
  echo -e "  ${BOLD}ENTERPRISE${NC}   90 patterns  All + priority support"
  echo ""
  echo -e "${BOLD}CHECK CATEGORIES${NC}"
  echo "  TZ  Timezone Handling        -- missing tzinfo, naive datetime, UTC offsets, DST issues"
  echo "  NF  Naive Formatting         -- ambiguous formats, locale-dependent parsing, deprecated APIs"
  echo "  EP  Epoch & Precision        -- Y2K38, millisecond confusion, precision loss, type overflow"
  echo "  DA  Date Arithmetic          -- manual calculations, leap year bugs, DST-unsafe math"
  echo "  CP  Comparison & Parsing     -- string comparison, ambiguous parsing, reference equality"
  echo "  ST  Storage & Serialization  -- VARCHAR dates, timezone stripping, non-ISO formats"
  echo ""
  echo -e "${BOLD}SCORING${NC}"
  echo "  100 = perfect, 0 = worst"
  echo "  Critical: -25, High: -15, Medium: -8, Low: -3"
  echo "  A(90+), B(80-89), C(70-79), D(60-69), F(<60)"
  echo "  Pass threshold: 70 (exit 0=pass, 1=fail)"
  echo ""
  echo -e "${BOLD}EXAMPLES${NC}"
  echo "  dispatcher.sh --path ."
  echo "  dispatcher.sh --path src/ --format json"
  echo "  dispatcher.sh --path . --category TZ --verbose"
  echo "  dispatcher.sh --path . --format html > report.html"
  echo ""
  echo -e "Get a license at ${CYAN}https://dateguard.pages.dev/pricing${NC}"
}

# --- Tier hierarchy -----------------------------------------------------------

declare -A TIER_LEVELS=(
  [free]=0
  [pro]=1
  [team]=2
  [enterprise]=3
)

# --- License integration ------------------------------------------------------

# Source license module and determine the effective tier.
# Priority: --tier flag > --license-key flag > env var > config file > free
resolve_tier() {
  local tier_override="$1"
  local license_key_flag="$2"

  # If tier is explicitly overridden, validate license for that tier
  if [[ -n "$tier_override" ]]; then
    local required_level="${TIER_LEVELS[$tier_override]:-0}"
    if [[ $required_level -gt 0 ]]; then
      # Need to validate license
      source "$SCRIPT_DIR/license.sh"

      # If a key was provided via flag, set it in env
      if [[ -n "$license_key_flag" ]]; then
        export DATEGUARD_LICENSE_KEY="$license_key_flag"
      fi

      if ! check_dateguard_license "$tier_override"; then
        exit 1
      fi
    fi
    echo "$required_level"
    return
  fi

  # Auto-detect tier from license
  source "$SCRIPT_DIR/license.sh"

  # If a key was provided via flag, set it in env
  if [[ -n "$license_key_flag" ]]; then
    export DATEGUARD_LICENSE_KEY="$license_key_flag"
  fi

  local detected_tier
  detected_tier=$(get_dateguard_tier)
  echo "${TIER_LEVELS[$detected_tier]:-0}"
}

# --- Pattern listing ----------------------------------------------------------

do_list_patterns() {
  source "$SCRIPT_DIR/patterns.sh"

  echo -e "${BOLD}--- DateGuard Detection Patterns ---${NC}"
  echo ""
  echo -e "${BOLD}$(dateguard_pattern_count) patterns across 6 categories${NC}"
  echo ""

  dateguard_list_patterns "all"
}

# --- Status display -----------------------------------------------------------

do_show_status() {
  show_version
  echo ""
  source "$SCRIPT_DIR/license.sh"
  show_dateguard_status
}

# --- Hooks management ---------------------------------------------------------

do_hooks_install() {
  if ! command -v lefthook &>/dev/null; then
    log_error "lefthook not installed."
    echo "  Install: brew install lefthook"
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
    if grep -q "dateguard" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# --- DateGuard hooks ----------------------------------------
    dateguard-check:
      run: |
        DATEGUARD_SKILL_DIR="${DATEGUARD_SKILL_DIR:-$HOME/.openclaw/skills/dateguard}"
        if [[ -f "$DATEGUARD_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$DATEGUARD_SKILL_DIR/scripts/patterns.sh"
          source "$DATEGUARD_SKILL_DIR/scripts/analyzer.sh"
          hook_dateguard_check
        else
          echo "[DateGuard] Skill not found at $DATEGUARD_SKILL_DIR -- skipping scan"
        fi
      fail_text: |
        Date/time issues detected in staged files!
        Run 'dateguard scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended DateGuard hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged files will be scanned for date/time issues on every commit."
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
    if grep -q "dateguard" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      sed '/# --- DateGuard hooks/,/fail_text:.*$/d' "$config" > "$tmp"
      grep -v "dateguard" "$tmp" > "$config" 2>/dev/null || mv "$tmp" "$config"
      rm -f "$tmp"
      echo -e "${GREEN}+${NC} Removed DateGuard hooks"
    else
      log_warn "No DateGuard hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# --- Main scan dispatch -------------------------------------------------------

do_scan() {
  local target="$1"
  local tier_level="$2"
  local format="$3"
  local verbose="$4"
  local category_filter="$5"

  # Source dependencies
  source "$SCRIPT_DIR/patterns.sh"
  source "$SCRIPT_DIR/analyzer.sh"

  # Run the scan
  do_dateguard_scan "$target" "$tier_level" "$format" "$verbose" "$category_filter"
}

# --- CLI Argument Parsing -----------------------------------------------------

main() {
  local scan_path="."
  local format="text"
  local tier_override=""
  local license_key_flag=""
  local verbose="false"
  local category_filter=""
  local command=""

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --path)
        shift
        scan_path="${1:-.}"
        ;;
      --format)
        shift
        format="${1:-text}"
        ;;
      --tier)
        shift
        tier_override="${1:-}"
        ;;
      --license-key)
        shift
        license_key_flag="${1:-}"
        ;;
      --verbose)
        verbose="true"
        ;;
      --category)
        shift
        category_filter="${1:-}"
        ;;
      --help|-h|help)
        show_help
        exit 0
        ;;
      --version|-v)
        show_version
        exit 0
        ;;
      status)
        command="status"
        ;;
      patterns)
        command="patterns"
        ;;
      scan)
        # "scan" is the default; just consume the word
        ;;
      check|audit)
        # Aliases for scan
        ;;
      hooks)
        shift
        local subcmd="${1:-}"
        case "$subcmd" in
          install)
            source "$SCRIPT_DIR/license.sh"
            if [[ -n "$license_key_flag" ]]; then
              export DATEGUARD_LICENSE_KEY="$license_key_flag"
            fi
            check_dateguard_license "pro" || exit 1
            do_hooks_install
            exit $?
            ;;
          uninstall)
            do_hooks_uninstall
            exit $?
            ;;
          *)
            log_error "Unknown hooks subcommand: $subcmd"
            echo "  Usage: dispatcher.sh hooks [install|uninstall]"
            exit 1
            ;;
        esac
        ;;
      report)
        # Generate markdown report
        shift || true
        local report_target="${1:-.}"
        source "$SCRIPT_DIR/license.sh"
        if [[ -n "$license_key_flag" ]]; then
          export DATEGUARD_LICENSE_KEY="$license_key_flag"
        fi
        check_dateguard_license "pro" || exit 1
        source "$SCRIPT_DIR/patterns.sh"
        source "$SCRIPT_DIR/analyzer.sh"
        local tier_num
        tier_num=$(get_tier_level "$(get_dateguard_tier)")
        local categories
        categories=$(get_dateguard_categories_for_tier "$tier_num")
        # Discover and scan files
        local -a files=()
        find_scannable_files "$report_target" files
        for filepath in "${files[@]}"; do
          scan_file "$filepath" "$categories" ""
        done
        generate_markdown_report "$report_target" "${#files[@]}"
        exit 0
        ;;
      -*)
        log_error "Unknown option: $1"
        echo ""
        show_help
        exit 1
        ;;
      *)
        # Treat as path if no command matched
        if [[ -z "$command" && ("$1" == "." || -e "$1") ]]; then
          scan_path="$1"
        else
          log_error "Unknown command: $1"
          echo ""
          show_help
          exit 1
        fi
        ;;
    esac
    shift || true
  done

  # Handle special commands
  case "${command:-}" in
    status)
      do_show_status
      exit 0
      ;;
    patterns)
      do_list_patterns
      exit 0
      ;;
  esac

  # Validate format
  case "$format" in
    text|json|html) ;;
    *)
      log_error "Invalid format: $format. Use text, json, or html."
      exit 1
      ;;
  esac

  # Validate tier override if provided
  if [[ -n "$tier_override" ]]; then
    case "$tier_override" in
      free|pro|team|enterprise) ;;
      *)
        log_error "Invalid tier: $tier_override. Use free, pro, team, or enterprise."
        exit 1
        ;;
    esac
  fi

  # Resolve tier level
  local tier_level
  tier_level=$(resolve_tier "$tier_override" "$license_key_flag")

  # Show banner for text output
  if [[ "$format" == "text" ]]; then
    show_version
    echo ""

    # Show tier info
    local tier_name="Free"
    case "$tier_level" in
      0) tier_name="Free (30 patterns)" ;;
      1) tier_name="Pro (60 patterns)" ;;
      2) tier_name="Team (90 patterns)" ;;
      3) tier_name="Enterprise (90 patterns)" ;;
    esac
    echo -e "  Tier: ${BOLD}$tier_name${NC}"
    echo ""
  fi

  # Run scan
  do_scan "$scan_path" "$tier_level" "$format" "$verbose" "$category_filter"
  exit $?
}

main "$@"
