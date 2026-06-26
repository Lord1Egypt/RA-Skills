#!/usr/bin/env bash
# DeadCode -- Main CLI entry point
# Usage: deadcode.sh <command> [args...]
#
# Commands:
#   scan [file|dir]           One-shot dead code scan (FREE, 5 file limit)
#   hooks install             Install pre-commit hooks (PRO+)
#   hooks uninstall           Remove DeadCode hooks (PRO+)
#   report [dir]              Generate dead code report (PRO+)
#   orphans [dir]             Find orphan files (PRO+)
#   ignore [pattern]          Manage ignore rules (TEAM+)
#   sarif [dir]               SARIF output for CI (TEAM+)
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

log_info()    { echo -e "${BLUE}[DeadCode]${NC} $*"; }
log_success() { echo -e "${GREEN}[DeadCode]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[DeadCode]${NC} $*"; }
log_error()   { echo -e "${RED}[DeadCode]${NC} $*" >&2; }

show_version() {
  echo -e "${BOLD}DeadCode${NC} v${VERSION}"
  echo "  Dead code & unused export detector"
  echo "  https://deadcode.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  deadcode <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC} One-shot dead code scan (5 file limit)"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  hooks install             ${DIM}[PRO]${NC}  Install pre-commit hooks"
  echo -e "  hooks uninstall           ${DIM}[PRO]${NC}  Remove DeadCode hooks"
  echo -e "  report [dir]              ${DIM}[PRO]${NC}  Generate dead code report"
  echo -e "  orphans [dir]             ${DIM}[PRO]${NC}  Find orphan files"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  ignore [pattern]          ${DIM}[TEAM]${NC} Manage ignore rules"
  echo -e "  sarif [dir]               ${DIM}[TEAM]${NC} SARIF output for CI"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                    Show license and config info"
  echo "  patterns                  List all detection patterns"
  echo "  --help, -h                Show this help"
  echo "  --version, -v             Show version"
  echo ""
  echo -e "Get a license at ${CYAN}https://deadcode.pages.dev${NC}"
}

# --- License ----------------------------------------------------------------

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_deadcode_license "$required_tier"
}

# --- Hooks management -------------------------------------------------------

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
    if grep -q "deadcode" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# --- DeadCode hooks ------------------------------------------
    deadcode-scan:
      run: |
        DEADCODE_SKILL_DIR="${DEADCODE_SKILL_DIR:-$HOME/.openclaw/skills/deadcode}"
        if [[ -f "$DEADCODE_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$DEADCODE_SKILL_DIR/scripts/patterns.sh"
          source "$DEADCODE_SKILL_DIR/scripts/analyzer.sh"
          hook_deadcode_scan
        else
          echo "[DeadCode] Skill not found at $DEADCODE_SKILL_DIR -- skipping scan"
        fi
      fail_text: |
        Dead code detected in staged source files!
        Run 'deadcode scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended DeadCode hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged source files will be scanned on every commit."
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
    if grep -q "deadcode" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      sed '/# --- DeadCode hooks/,/fail_text:.*$/d' "$config" > "$tmp"
      grep -v "deadcode" "$tmp" > "$config" 2>/dev/null || mv "$tmp" "$config"
      rm -f "$tmp"
      echo -e "${GREEN}+${NC} Removed DeadCode hooks"
    else
      log_warn "No DeadCode hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# --- Pattern listing --------------------------------------------------------

do_list_patterns() {
  source "$SCRIPT_DIR/patterns.sh"

  echo -e "${BOLD}--- DeadCode Detection Patterns ---${NC}"
  echo ""
  echo -e "${BOLD}$(deadcode_pattern_count) patterns across 5 language categories${NC}"
  echo ""

  local lang_types=("JS" "PY" "GO" "CSS" "GENERAL")
  local lang_labels=("JavaScript/TypeScript" "Python" "Go" "CSS/SCSS" "General")

  for i in "${!lang_types[@]}"; do
    local ltype="${lang_types[$i]}"
    local llabel="${lang_labels[$i]}"
    echo -e "${CYAN}${BOLD}$llabel:${NC}"
    deadcode_list_patterns "$ltype" | while IFS= read -r line; do
      echo "  $line"
    done
    echo ""
  done
}

# --- Ignore rules management -----------------------------------------------

do_ignore_add() {
  local pattern="${1:-}"
  if [[ -z "$pattern" ]]; then
    log_error "No pattern provided."
    echo "  Usage: deadcode ignore <pattern>"
    echo "  Example: deadcode ignore '**/generated/**'"
    echo "  Example: deadcode ignore DC-JS-011"
    return 1
  fi

  local config_file="${HOME}/.openclaw/openclaw.json"

  if [[ ! -f "$config_file" ]]; then
    mkdir -p "$(dirname "$config_file")"
    echo '{"skills":{"entries":{"deadcode":{"config":{"ignorePatterns":[]}}}}}' > "$config_file"
  fi

  if command -v python3 &>/dev/null; then
    python3 -c "
import json
try:
    with open('$config_file') as f:
        cfg = json.load(f)
    dc = cfg.setdefault('skills', {}).setdefault('entries', {}).setdefault('deadcode', {}).setdefault('config', {})
    patterns = dc.setdefault('ignorePatterns', [])
    checks = dc.setdefault('ignoreChecks', [])
    p = '$pattern'
    if p.startswith('DC-'):
        if p not in checks:
            checks.append(p)
    else:
        if p not in patterns:
            patterns.append(p)
    with open('$config_file', 'w') as f:
        json.dump(cfg, f, indent=2)
    print('OK')
except Exception as e:
    print(f'ERROR: {e}')
" 2>/dev/null
  elif command -v node &>/dev/null; then
    node -e "
const fs = require('fs');
try {
  let cfg = JSON.parse(fs.readFileSync('$config_file', 'utf8'));
  let dc = ((cfg.skills ||= {}).entries ||= {}).deadcode ||= {};
  (dc.config ||= {});
  const p = '$pattern';
  if (p.startsWith('DC-')) {
    (dc.config.ignoreChecks ||= []).includes(p) || dc.config.ignoreChecks.push(p);
  } else {
    (dc.config.ignorePatterns ||= []).includes(p) || dc.config.ignorePatterns.push(p);
  }
  fs.writeFileSync('$config_file', JSON.stringify(cfg, null, 2));
  console.log('OK');
} catch(e) { console.log('ERROR: ' + e.message); }
" 2>/dev/null
  else
    log_error "python3 or node required to manage ignore rules."
    return 1
  fi

  log_success "Added ignore rule: ${BOLD}$pattern${NC}"
}

# --- Command dispatch -------------------------------------------------------

main() {
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    scan)
      local target="${1:-.}"
      log_info "Scanning for dead code in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      do_deadcode_scan "$target" 5
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
          echo "  Usage: deadcode hooks [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    report)
      require_license "pro"
      local target="${1:-.}"
      log_info "Generating dead code report for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_deadcode_report "$target"
      ;;

    orphans)
      require_license "pro"
      local target="${1:-.}"
      log_info "Finding orphan files in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      find_orphan_files "$target"
      ;;

    ignore)
      require_license "team"
      do_ignore_add "${1:-}"
      ;;

    sarif)
      require_license "team"
      local target="${1:-.}"
      log_info "Generating SARIF output for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_sarif "$target"
      ;;

    patterns)
      do_list_patterns
      ;;

    status)
      show_version
      echo ""
      source "$SCRIPT_DIR/license.sh"
      show_deadcode_status
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
