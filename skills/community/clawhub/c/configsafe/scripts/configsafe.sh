#!/usr/bin/env bash
# ConfigSafe — Main CLI entry point
# Usage: configsafe.sh <command> [args...]
#
# Commands:
#   scan [file|dir]           One-shot config scan (FREE, 5 file limit)
#   hooks install             Install pre-commit hooks (PRO+)
#   hooks uninstall           Remove ConfigSafe hooks (PRO+)
#   report [dir]              Generate security report (PRO+)
#   benchmark [dir]           CIS benchmark checks (PRO+)
#   policy [dir]              Enforce security policies (TEAM+)
#   compliance [dir]          Full compliance report (TEAM+)
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

log_info()    { echo -e "${BLUE}[ConfigSafe]${NC} $*"; }
log_success() { echo -e "${GREEN}[ConfigSafe]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[ConfigSafe]${NC} $*"; }
log_error()   { echo -e "${RED}[ConfigSafe]${NC} $*" >&2; }

show_version() {
  echo -e "${BOLD}ConfigSafe${NC} v${VERSION}"
  echo "  Infrastructure configuration auditor"
  echo "  https://configsafe.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  configsafe <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC} One-shot config scan (5 file limit)"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  hooks install             ${DIM}[PRO]${NC}  Install pre-commit hooks"
  echo -e "  hooks uninstall           ${DIM}[PRO]${NC}  Remove ConfigSafe hooks"
  echo -e "  report [dir]              ${DIM}[PRO]${NC}  Generate security report"
  echo -e "  benchmark [dir]           ${DIM}[PRO]${NC}  CIS benchmark checks"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  policy [dir]              ${DIM}[TEAM]${NC} Enforce security policies"
  echo -e "  compliance [dir]          ${DIM}[TEAM]${NC} Full compliance report (CIS, NIST)"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                    Show license and config info"
  echo "  patterns                  List all detection patterns"
  echo "  --help, -h                Show this help"
  echo "  --version, -v             Show version"
  echo ""
  echo -e "Get a license at ${CYAN}https://configsafe.pages.dev${NC}"
}

# ─── License ────────────────────────────────────────────────────────────────

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_configsafe_license "$required_tier"
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
    if grep -q "configsafe" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# ─── ConfigSafe hooks ─────────────────────────────
    configsafe-config-scan:
      run: |
        CONFIGSAFE_SKILL_DIR="${CONFIGSAFE_SKILL_DIR:-$HOME/.openclaw/skills/configsafe}"
        if [[ -f "$CONFIGSAFE_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$CONFIGSAFE_SKILL_DIR/scripts/patterns.sh"
          source "$CONFIGSAFE_SKILL_DIR/scripts/analyzer.sh"
          hook_config_scan
        else
          echo "[ConfigSafe] Skill not found at $CONFIGSAFE_SKILL_DIR — skipping scan"
        fi
      fail_text: |
        Misconfigurations detected in staged config files!
        Run 'configsafe scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended ConfigSafe hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged config files will be scanned on every commit."
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
    if grep -q "configsafe" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      sed '/# ─── ConfigSafe hooks/,/fail_text:.*$/d' "$config" > "$tmp"
      grep -v "configsafe" "$tmp" > "$config" 2>/dev/null || mv "$tmp" "$config"
      rm -f "$tmp"
      echo -e "${GREEN}+${NC} Removed ConfigSafe hooks"
    else
      log_warn "No ConfigSafe hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# ─── Pattern listing ───────────────────────────────────────────────────────

do_list_patterns() {
  source "$SCRIPT_DIR/patterns.sh"

  echo -e "${BOLD}━━━ ConfigSafe Detection Patterns ━━━${NC}"
  echo ""
  echo -e "${BOLD}$(configsafe_pattern_count) patterns across 6 config types${NC}"
  echo ""

  local config_types=("DOCKERFILE" "COMPOSE" "KUBERNETES" "TERRAFORM" "CICD" "NGINX")
  local config_labels=("Dockerfile" "docker-compose" "Kubernetes" "Terraform" "CI/CD Pipelines" "Nginx/Apache")

  for i in "${!config_types[@]}"; do
    local ctype="${config_types[$i]}"
    local clabel="${config_labels[$i]}"
    echo -e "${CYAN}${BOLD}$clabel:${NC}"
    configsafe_list_patterns "$ctype" | while IFS= read -r line; do
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
      log_info "Scanning configurations in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      do_config_scan "$target" 5
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
          echo "  Usage: configsafe hooks [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    report)
      require_license "pro"
      local target="${1:-.}"
      log_info "Generating security report for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_report "$target"
      ;;

    benchmark)
      require_license "pro"
      local target="${1:-.}"
      log_info "Running CIS benchmark checks on ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      run_benchmark "$target"
      ;;

    policy)
      require_license "team"
      local target="${1:-.}"
      log_info "Enforcing security policies on ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      enforce_policy "$target"
      ;;

    compliance)
      require_license "team"
      local target="${1:-.}"
      log_info "Generating compliance report for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_compliance "$target"
      ;;

    patterns)
      do_list_patterns
      ;;

    status)
      show_version
      echo ""
      source "$SCRIPT_DIR/license.sh"
      show_configsafe_status
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
