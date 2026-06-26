#!/usr/bin/env bash
# BundlePhobia — Main CLI entry point
# Usage: bundlephobia.sh <command> [args...]
#
# Commands:
#   scan [file|dir]           One-shot bundle bloat scan (FREE, 5 file limit)
#   hooks install             Install pre-commit hooks (PRO+)
#   hooks uninstall           Remove BundlePhobia hooks (PRO+)
#   report [dir]              Generate bundle health report (PRO+)
#   audit [dir]               Deep dependency audit (PRO+)
#   budget [dir]              Enforce size budgets (TEAM+)
#   sarif [dir]               SARIF JSON output (TEAM+)
#   ci [dir]                  CI mode scan (TEAM+)
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

log_info()    { echo -e "${BLUE}[BundlePhobia]${NC} $*"; }
log_success() { echo -e "${GREEN}[BundlePhobia]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[BundlePhobia]${NC} $*"; }
log_error()   { echo -e "${RED}[BundlePhobia]${NC} $*" >&2; }

show_version() {
  echo -e "${BOLD}BundlePhobia${NC} v${VERSION}"
  echo "  Bundle size & dependency bloat analyzer"
  echo "  https://bundlephobia.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  bundlephobia <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC} One-shot bundle bloat scan (5 file limit)"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  hooks install             ${DIM}[PRO]${NC}  Install pre-commit hooks"
  echo -e "  hooks uninstall           ${DIM}[PRO]${NC}  Remove BundlePhobia hooks"
  echo -e "  report [dir]              ${DIM}[PRO]${NC}  Generate bundle health report"
  echo -e "  audit [dir]               ${DIM}[PRO]${NC}  Deep dependency audit"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  budget [dir]              ${DIM}[TEAM]${NC} Enforce size budgets"
  echo -e "  sarif [dir]               ${DIM}[TEAM]${NC} SARIF JSON output for CI/CD"
  echo -e "  ci [dir]                  ${DIM}[TEAM]${NC} CI mode (non-interactive)"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                    Show license and config info"
  echo "  patterns                  List all detection patterns"
  echo "  --help, -h                Show this help"
  echo "  --version, -v             Show version"
  echo ""
  echo -e "Get a license at ${CYAN}https://bundlephobia.pages.dev${NC}"
}

# ─── License ────────────────────────────────────────────────────────────────

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_bundlephobia_license "$required_tier"
}

# ─── Hooks management ──────────────────────────────────────────────────────

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
    if grep -q "bundlephobia" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# ─── BundlePhobia hooks ─────────────────────────────
    bundlephobia-scan:
      run: |
        BUNDLEPHOBIA_SKILL_DIR="${BUNDLEPHOBIA_SKILL_DIR:-$HOME/.openclaw/skills/bundlephobia}"
        if [[ -f "$BUNDLEPHOBIA_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$BUNDLEPHOBIA_SKILL_DIR/scripts/patterns.sh"
          source "$BUNDLEPHOBIA_SKILL_DIR/scripts/analyzer.sh"
          hook_bundlephobia_scan
        else
          echo "[BundlePhobia] Skill not found at $BUNDLEPHOBIA_SKILL_DIR — skipping scan"
        fi
      fail_text: |
        Bundle bloat detected in staged files!
        Run 'bundlephobia scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended BundlePhobia hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged JS/TS files will be scanned on every commit."
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
    if grep -q "bundlephobia" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      sed '/# ─── BundlePhobia hooks/,/fail_text:.*$/d' "$config" > "$tmp"
      grep -v "bundlephobia" "$tmp" > "$config" 2>/dev/null || mv "$tmp" "$config"
      rm -f "$tmp"
      echo -e "${GREEN}+${NC} Removed BundlePhobia hooks"
    else
      log_warn "No BundlePhobia hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# ─── Pattern listing ───────────────────────────────────────────────────────

do_list_patterns() {
  source "$SCRIPT_DIR/patterns.sh"

  echo -e "${BOLD}━━━ BundlePhobia Detection Patterns ━━━${NC}"
  echo ""
  echo -e "${BOLD}$(bundlephobia_pattern_count) patterns across 5 categories${NC}"
  echo ""

  local cat_types=("OVERSIZED" "DUPLICATE" "TREESHAKE" "CONFIG" "HYGIENE")
  local cat_labels=("Oversized Dependencies" "Duplicate & Redundant Packages" "Tree-Shaking Failures" "Bundle Configuration Issues" "Dependency Hygiene")

  for i in "${!cat_types[@]}"; do
    local ctype="${cat_types[$i]}"
    local clabel="${cat_labels[$i]}"
    echo -e "${CYAN}${BOLD}$clabel:${NC}"
    bundlephobia_list_patterns "$ctype" | while IFS= read -r line; do
      echo "  $line"
    done
    echo ""
  done
}

# ─── Command dispatch ───────────────────────────────────────────────────────

main() {
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    scan)
      local target="${1:-.}"
      log_info "Scanning for bundle bloat in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      run_bundlephobia_scan "$target" 5
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
          echo "  Usage: bundlephobia hooks [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    report)
      require_license "pro"
      local target="${1:-.}"
      log_info "Generating bundle health report for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_bundlephobia_report "$target"
      ;;

    audit)
      require_license "pro"
      local target="${1:-.}"
      log_info "Running deep dependency audit on ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      run_bundlephobia_audit "$target"
      ;;

    budget)
      require_license "team"
      local target="${1:-.}"
      log_info "Enforcing size budgets in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      enforce_size_budget "$target"
      ;;

    sarif)
      require_license "team"
      local target="${1:-.}"
      log_info "Generating SARIF output for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_sarif_output "$target"
      ;;

    ci)
      require_license "team"
      local target="${1:-.}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      run_bundlephobia_scan "$target" 0
      ;;

    patterns)
      do_list_patterns
      ;;

    status)
      show_version
      echo ""
      source "$SCRIPT_DIR/license.sh"
      show_bundlephobia_status
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
