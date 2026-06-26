#!/usr/bin/env bash
# ErrorLens -- Main CLI entry point
# Usage: errorlens.sh <command> [args...]
#
# Commands:
#   scan [file|dir]           One-shot error handling scan (FREE, 5 file limit)
#   hook install              Install pre-commit hooks (FREE)
#   hook uninstall            Remove ErrorLens hooks (FREE)
#   report [dir]              Generate error handling report (FREE)
#   watch [dir]               Continuous monitoring mode (PRO+)
#   ci [dir]                  CI/CD integration mode (PRO+)
#   team-report [dir]         Aggregate team metrics (TEAM+)
#   baseline [dir]            Baseline known issues for allowlisting (TEAM+)
#   status                    Show license and config info

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="1.0.0"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[ErrorLens]${NC} $*"; }
log_success() { echo -e "${GREEN}[ErrorLens]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[ErrorLens]${NC} $*"; }
log_error()   { echo -e "${RED}[ErrorLens]${NC} $*" >&2; }

show_version() {
  echo -e "${BOLD}ErrorLens${NC} v${VERSION}"
  echo "  Error handling & exception safety analyzer"
  echo "  https://errorlens.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  errorlens <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC} One-shot error handling scan (5 file limit)"
  echo -e "  hook install              ${DIM}[FREE]${NC} Install pre-commit hooks"
  echo -e "  hook uninstall            ${DIM}[FREE]${NC} Remove ErrorLens hooks"
  echo -e "  report [dir]              ${DIM}[FREE]${NC} Generate error handling report"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  watch [dir]               ${DIM}[PRO]${NC}  Continuous monitoring mode"
  echo -e "  ci [dir]                  ${DIM}[PRO]${NC}  CI/CD integration with exit codes"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  team-report [dir]         ${DIM}[TEAM]${NC} Aggregate team error handling metrics"
  echo -e "  baseline [dir]            ${DIM}[TEAM]${NC} Baseline known issues for allowlisting"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                    Show license and config info"
  echo "  patterns                  List all detection patterns"
  echo "  --help, -h                Show this help"
  echo "  --version, -v             Show version"
  echo ""
  echo -e "Get a license at ${CYAN}https://errorlens.pages.dev${NC}"
}

# --- License ----------------------------------------------------------------

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_errorlens_license "$required_tier"
}

# --- Hooks management -------------------------------------------------------

do_hooks_install() {
  if ! command -v lefthook &>/dev/null; then
    log_error "lefthook not installed."
    echo "  Install: brew install lefthook"
    echo "  Or:      npm install -g lefthook"
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
    if grep -q "errorlens" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# --- ErrorLens hooks ----------------------------------------
    errorlens-error-scan:
      run: |
        ERRORLENS_SKILL_DIR="${ERRORLENS_SKILL_DIR:-$HOME/.openclaw/skills/errorlens}"
        if [[ -f "$ERRORLENS_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$ERRORLENS_SKILL_DIR/scripts/patterns.sh"
          source "$ERRORLENS_SKILL_DIR/scripts/analyzer.sh"
          hook_error_scan
        else
          echo "[ErrorLens] Skill not found at $ERRORLENS_SKILL_DIR -- skipping scan"
        fi
      fail_text: |
        Error handling issues detected in staged files!
        Run 'errorlens scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended ErrorLens hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged files will be scanned for error handling issues on every commit."
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
    if grep -q "errorlens" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      sed '/# --- ErrorLens hooks/,/fail_text:.*$/d' "$config" > "$tmp"
      grep -v "errorlens" "$tmp" > "$config" 2>/dev/null || mv "$tmp" "$config"
      rm -f "$tmp"
      echo -e "${GREEN}+${NC} Removed ErrorLens hooks"
    else
      log_warn "No ErrorLens hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# --- Pattern listing --------------------------------------------------------

do_list_patterns() {
  source "$SCRIPT_DIR/patterns.sh"

  echo -e "${BOLD}--- ErrorLens Detection Patterns ---${NC}"
  echo ""
  echo -e "${BOLD}$(errorlens_pattern_count) patterns across 6 categories${NC}"
  echo ""

  local cat_types=("EMPTY_CATCH" "SWALLOWED" "BOUNDARY" "GENERIC" "RESOURCE" "INFOLEAK")
  local cat_labels=("Empty Catches" "Swallowed Exceptions" "Error Boundaries" "Generic Errors" "Resource & Propagation" "Information Leak")

  for i in "${!cat_types[@]}"; do
    local ctype="${cat_types[$i]}"
    local clabel="${cat_labels[$i]}"
    echo -e "${CYAN}${BOLD}$clabel:${NC}"
    errorlens_list_patterns "$ctype" | while IFS= read -r line; do
      echo "  $line"
    done
    echo ""
  done
}

# --- Command dispatch -------------------------------------------------------

main() {
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    scan)
      local target="${1:-.}"
      log_info "Scanning for error handling issues in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      do_errorlens_scan "$target" 5
      ;;

    hook)
      local subcmd="${1:-}"
      case "$subcmd" in
        install)
          do_hooks_install
          ;;
        uninstall)
          do_hooks_uninstall
          ;;
        *)
          log_error "Unknown hook subcommand: $subcmd"
          echo "  Usage: errorlens hook [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    report)
      local target="${1:-.}"
      log_info "Generating error handling report for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_errorlens_report "$target"
      ;;

    watch)
      require_license "pro"
      local target="${1:-.}"
      log_info "Starting watch mode on ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      watch_mode "$target"
      ;;

    ci)
      require_license "pro"
      local target="${1:-.}"
      log_info "Running CI mode on ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      ci_mode "$target"
      ;;

    team-report)
      require_license "team"
      local target="${1:-.}"
      log_info "Generating team report for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      team_report "$target"
      ;;

    baseline)
      require_license "team"
      local target="${1:-.}"
      log_info "Creating error handling baseline for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      baseline_mode "$target"
      ;;

    patterns)
      do_list_patterns
      ;;

    status)
      show_version
      echo ""
      source "$SCRIPT_DIR/license.sh"
      show_errorlens_status
      ;;

    --help|-h|help)
      show_help
      ;;

    --version|-v)
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
