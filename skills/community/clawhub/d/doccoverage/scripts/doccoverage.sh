#!/usr/bin/env bash
# DocCoverage -- Main CLI entry point
# Usage: doccoverage.sh <command> [args...]
#
# Commands:
#   scan [file|dir]           One-shot doc coverage scan (FREE, 5 file limit)
#   hooks install             Install pre-commit hooks (PRO+)
#   hooks uninstall           Remove DocCoverage hooks (PRO+)
#   report [dir]              Generate coverage report (PRO+)
#   coverage [dir]            Calculate doc coverage percentage (PRO+)
#   policy [dir]              Enforce doc policies (TEAM+)
#   sarif [dir]               Generate SARIF JSON output (TEAM+)
#   changelog [dir]           Verify CHANGELOG completeness (TEAM+)
#   status                    Show license and config info
#   patterns                  List all detection patterns

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

log_info()    { echo -e "${BLUE}[DocCoverage]${NC} $*"; }
log_success() { echo -e "${GREEN}[DocCoverage]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[DocCoverage]${NC} $*"; }
log_error()   { echo -e "${RED}[DocCoverage]${NC} $*" >&2; }

show_version() {
  echo -e "${BOLD}DocCoverage${NC} v${VERSION}"
  echo "  Documentation coverage & quality analyzer"
  echo "  https://doccoverage.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  doccoverage <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC} One-shot doc coverage scan (5 file limit)"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  hooks install             ${DIM}[PRO]${NC}  Install pre-commit hooks"
  echo -e "  hooks uninstall           ${DIM}[PRO]${NC}  Remove DocCoverage hooks"
  echo -e "  report [dir]              ${DIM}[PRO]${NC}  Generate coverage report"
  echo -e "  coverage [dir]            ${DIM}[PRO]${NC}  Calculate doc coverage percentage"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  policy [dir]              ${DIM}[TEAM]${NC} Enforce doc policies"
  echo -e "  sarif [dir]               ${DIM}[TEAM]${NC} Generate SARIF JSON output"
  echo -e "  changelog [dir]           ${DIM}[TEAM]${NC} Verify CHANGELOG completeness"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                    Show license and config info"
  echo "  patterns                  List all detection patterns"
  echo "  --help, -h                Show this help"
  echo "  --version, -v             Show version"
  echo ""
  echo -e "Get a license at ${CYAN}https://doccoverage.pages.dev${NC}"
}

# -- License -------------------------------------------------------------------

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_doccoverage_license "$required_tier"
}

# -- Hooks management ----------------------------------------------------------

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
    if grep -q "doccoverage" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# -- DocCoverage hooks ----------------------------------------
    doccoverage-doc-scan:
      run: |
        DOCCOVERAGE_SKILL_DIR="${DOCCOVERAGE_SKILL_DIR:-$HOME/.openclaw/skills/doccoverage}"
        if [[ -f "$DOCCOVERAGE_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$DOCCOVERAGE_SKILL_DIR/scripts/patterns.sh"
          source "$DOCCOVERAGE_SKILL_DIR/scripts/analyzer.sh"
          hook_doccoverage_scan
        else
          echo "[DocCoverage] Skill not found at $DOCCOVERAGE_SKILL_DIR -- skipping scan"
        fi
      fail_text: |
        Documentation gaps detected in staged files!
        Run 'doccoverage scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended DocCoverage hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged files will be scanned for documentation gaps on every commit."
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
    if grep -q "doccoverage" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      sed '/# -- DocCoverage hooks/,/fail_text:.*$/d' "$config" > "$tmp"
      grep -v "doccoverage" "$tmp" > "$config" 2>/dev/null || mv "$tmp" "$config"
      rm -f "$tmp"
      echo -e "${GREEN}+${NC} Removed DocCoverage hooks"
    else
      log_warn "No DocCoverage hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# -- Pattern listing -----------------------------------------------------------

do_list_patterns() {
  source "$SCRIPT_DIR/patterns.sh"

  echo -e "${BOLD}--- DocCoverage Detection Patterns ---${NC}"
  echo ""
  echo -e "${BOLD}$(doccoverage_pattern_count) patterns across 6 categories${NC}"
  echo ""

  local categories=("MISSING" "INCOMPLETE" "README" "API" "TYPE" "QUALITY")
  local labels=(
    "Missing Function/Method Docs"
    "Incomplete Documentation"
    "README & Project Docs"
    "API Documentation"
    "Type & Interface Docs"
    "Comment Quality"
  )

  for i in "${!categories[@]}"; do
    local ctype="${categories[$i]}"
    local clabel="${labels[$i]}"
    echo -e "${CYAN}${BOLD}$clabel:${NC}"
    doccoverage_list_patterns "$ctype" | while IFS= read -r line; do
      echo "  $line"
    done
    echo ""
  done
}

# -- Command dispatch ----------------------------------------------------------

main() {
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    scan)
      local target="${1:-.}"
      log_info "Scanning for documentation gaps in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      run_doccoverage_scan "$target" 5
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
          echo "  Usage: doccoverage hooks [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    report)
      require_license "pro"
      local target="${1:-.}"
      log_info "Generating documentation coverage report for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_doccoverage_report "$target"
      ;;

    coverage)
      require_license "pro"
      local target="${1:-.}"
      log_info "Calculating documentation coverage for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      run_doccoverage_coverage "$target"
      ;;

    policy)
      require_license "team"
      local target="${1:-.}"
      log_info "Enforcing documentation policies on ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      enforce_doc_policy "$target"
      ;;

    sarif)
      require_license "team"
      local target="${1:-.}"
      log_info "Generating SARIF output for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_sarif_output "$target"
      ;;

    changelog)
      require_license "team"
      local target="${1:-.}"
      log_info "Verifying CHANGELOG completeness for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      verify_changelog "$target"
      ;;

    patterns)
      do_list_patterns
      ;;

    status)
      show_version
      echo ""
      source "$SCRIPT_DIR/license.sh"
      show_doccoverage_status
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
