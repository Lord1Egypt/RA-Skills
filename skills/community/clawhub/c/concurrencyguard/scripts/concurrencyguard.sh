#!/usr/bin/env bash
# ConcurrencyGuard -- Main CLI entry point
# Usage: concurrencyguard.sh <command> [args...]
#
# Commands:
#   scan [file|dir]           One-shot concurrency safety scan (FREE, 5 file limit)
#   hook install              Install pre-commit hooks (FREE)
#   hook uninstall            Remove ConcurrencyGuard hooks (FREE)
#   report [dir]              Generate concurrency safety report (FREE)
#   watch [dir]               Continuous file-watching mode (PRO+)
#   ci [dir]                  CI/CD integration with exit codes (PRO+)
#   team-report [dir]         Aggregate team-level report (TEAM+)
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

log_info()    { echo -e "${BLUE}[ConcurrencyGuard]${NC} $*"; }
log_success() { echo -e "${GREEN}[ConcurrencyGuard]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[ConcurrencyGuard]${NC} $*"; }
log_error()   { echo -e "${RED}[ConcurrencyGuard]${NC} $*" >&2; }

show_version() {
  echo -e "${BOLD}ConcurrencyGuard${NC} v${VERSION}"
  echo "  Race condition & concurrency safety analyzer"
  echo "  https://concurrencyguard.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  concurrencyguard <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC} One-shot concurrency scan (5 file limit)"
  echo -e "  hook install              ${DIM}[FREE]${NC} Install pre-commit hooks"
  echo -e "  hook uninstall            ${DIM}[FREE]${NC} Remove ConcurrencyGuard hooks"
  echo -e "  report [dir]              ${DIM}[FREE]${NC} Generate concurrency safety report"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  watch [dir]               ${DIM}[PRO]${NC}  Continuous file-watching mode"
  echo -e "  ci [dir]                  ${DIM}[PRO]${NC}  CI/CD integration with exit codes"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  team-report [dir]         ${DIM}[TEAM]${NC} Aggregate team-level report"
  echo -e "  baseline [dir]            ${DIM}[TEAM]${NC} Baseline known issues for allowlisting"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                    Show license and config info"
  echo "  patterns                  List all detection patterns"
  echo "  --help, -h                Show this help"
  echo "  --version, -v             Show version"
  echo ""
  echo -e "Get a license at ${CYAN}https://concurrencyguard.pages.dev${NC}"
}

# --- License ----------------------------------------------------------------

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_concurrencyguard_license "$required_tier"
}

# --- Hooks management -------------------------------------------------------

do_hooks_install() {
  if ! command -v lefthook &>/dev/null; then
    log_error "lefthook not installed."
    echo "  Install: brew install lefthook"
    echo "  Or: npm install -g lefthook"
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
    if grep -q "concurrencyguard" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# --- ConcurrencyGuard hooks ----------------------------------------
    concurrencyguard-concurrency-scan:
      run: |
        CONCURRENCYGUARD_SKILL_DIR="${CONCURRENCYGUARD_SKILL_DIR:-$HOME/.openclaw/skills/concurrencyguard}"
        if [[ -f "$CONCURRENCYGUARD_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$CONCURRENCYGUARD_SKILL_DIR/scripts/patterns.sh"
          source "$CONCURRENCYGUARD_SKILL_DIR/scripts/analyzer.sh"
          hook_concurrency_scan
        else
          echo "[ConcurrencyGuard] Skill not found at $CONCURRENCYGUARD_SKILL_DIR -- skipping scan"
        fi
      fail_text: |
        Concurrency safety issues detected in staged files!
        Run 'concurrencyguard scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended ConcurrencyGuard hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged files will be scanned for concurrency issues on every commit."
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
    if grep -q "concurrencyguard" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      sed '/# --- ConcurrencyGuard hooks/,/fail_text:.*$/d' "$config" > "$tmp"
      grep -v "concurrencyguard" "$tmp" > "$config" 2>/dev/null || mv "$tmp" "$config"
      rm -f "$tmp"
      echo -e "${GREEN}+${NC} Removed ConcurrencyGuard hooks"
    else
      log_warn "No ConcurrencyGuard hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# --- Pattern listing --------------------------------------------------------

do_list_patterns() {
  source "$SCRIPT_DIR/patterns.sh"

  echo -e "${BOLD}--- ConcurrencyGuard Detection Patterns ---${NC}"
  echo ""
  echo -e "${BOLD}$(concurrencyguard_pattern_count) patterns across 6 categories${NC}"
  echo ""

  local cat_types=("SS" "LK" "TC" "AW" "TS" "DL")
  local cat_labels=("Shared State" "Locking & Mutex" "TOCTOU & Atomicity" "Async/Await Pitfalls" "Thread Safety" "Deadlock & Starvation")

  for i in "${!cat_types[@]}"; do
    local ctype="${cat_types[$i]}"
    local clabel="${cat_labels[$i]}"
    echo -e "${CYAN}${BOLD}$clabel:${NC}"
    concurrencyguard_list_patterns "$ctype" | while IFS= read -r line; do
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
      log_info "Scanning for concurrency issues in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      do_concurrency_scan "$target" 5
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
          echo "  Usage: concurrencyguard hook [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    report)
      local target="${1:-.}"
      log_info "Generating concurrency safety report for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_concurrency_report "$target"
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
      log_info "Creating baseline for ${BOLD}$target${NC}"
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
      show_concurrencyguard_status
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
