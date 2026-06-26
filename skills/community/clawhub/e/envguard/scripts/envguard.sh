#!/usr/bin/env bash
# EnvGuard — Main CLI entry point
# Usage: envguard.sh <command> [args...]
#
# Commands:
#   scan [file|dir]           One-shot secret scan (FREE)
#   hooks install             Install pre-commit hooks (PRO+)
#   hooks uninstall           Remove EnvGuard hooks (PRO+)
#   allowlist [add|remove|list] Manage false positives (PRO+)
#   diff                      Scan staged changes only (PRO+)
#   history [dir]             Full git history scan (TEAM+)
#   report [dir]              Generate compliance report (TEAM+)
#   policy [dir]              Custom patterns + enforcement (TEAM+)
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
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[EnvGuard]${NC} $*"; }
log_success() { echo -e "${GREEN}[EnvGuard]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[EnvGuard]${NC} $*"; }
log_error()   { echo -e "${RED}[EnvGuard]${NC} $*" >&2; }

show_version() {
  echo -e "${BOLD}EnvGuard${NC} v${VERSION}"
  echo "  Pre-commit secret detection"
  echo "  https://envguard.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  envguard <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC} One-shot secret scan"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  hooks install             ${DIM}[PRO]${NC}  Install pre-commit hooks"
  echo -e "  hooks uninstall           ${DIM}[PRO]${NC}  Remove EnvGuard hooks"
  echo -e "  allowlist add <pattern>   ${DIM}[PRO]${NC}  Allow a known-safe pattern"
  echo -e "  allowlist remove <pat>    ${DIM}[PRO]${NC}  Remove from allowlist"
  echo -e "  allowlist list            ${DIM}[PRO]${NC}  Show allowlisted patterns"
  echo -e "  diff                      ${DIM}[PRO]${NC}  Scan staged changes only"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  history [dir]             ${DIM}[TEAM]${NC} Full git history scan"
  echo -e "  report [dir]              ${DIM}[TEAM]${NC} Generate compliance report"
  echo -e "  policy [dir]              ${DIM}[TEAM]${NC} Custom patterns + enforcement"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                    Show license and config info"
  echo "  patterns                  List all detection patterns"
  echo "  --help, -h                Show this help"
  echo "  --version, -v             Show version"
  echo ""
  echo -e "Get a license at ${CYAN}https://envguard.pages.dev${NC}"
}

# ─── License ────────────────────────────────────────────────────────────────

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_envguard_license "$required_tier"
}

# ─── Allowlist management ──────────────────────────────────────────────────

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

do_allowlist() {
  local subcmd="${1:-list}"
  local pattern="${2:-}"

  case "$subcmd" in
    add)
      if [[ -z "$pattern" ]]; then
        log_error "Usage: envguard allowlist add <pattern>"
        return 1
      fi

      # Ensure config directory exists
      mkdir -p "$(dirname "$OPENCLAW_CONFIG")"

      if command -v python3 &>/dev/null; then
        python3 -c "
import json, os

config_path = os.path.expanduser('$OPENCLAW_CONFIG')
cfg = {}
if os.path.exists(config_path):
    with open(config_path) as f:
        cfg = json.load(f)

# Navigate/create nested structure
cfg.setdefault('skills', {}).setdefault('entries', {}).setdefault('envguard', {}).setdefault('config', {}).setdefault('allowlist', [])

allowlist = cfg['skills']['entries']['envguard']['config']['allowlist']
pattern = '$pattern'
if pattern not in allowlist:
    allowlist.append(pattern)

with open(config_path, 'w') as f:
    json.dump(cfg, f, indent=2)
print('added')
" 2>/dev/null
        log_success "Added to allowlist: ${BOLD}$pattern${NC}"
      elif command -v node &>/dev/null; then
        node -e "
const fs = require('fs');
const path = '$OPENCLAW_CONFIG';
let cfg = {};
try { cfg = JSON.parse(fs.readFileSync(path, 'utf8')); } catch(e) {}
if (!cfg.skills) cfg.skills = {};
if (!cfg.skills.entries) cfg.skills.entries = {};
if (!cfg.skills.entries.envguard) cfg.skills.entries.envguard = {};
if (!cfg.skills.entries.envguard.config) cfg.skills.entries.envguard.config = {};
if (!cfg.skills.entries.envguard.config.allowlist) cfg.skills.entries.envguard.config.allowlist = [];
const al = cfg.skills.entries.envguard.config.allowlist;
if (!al.includes('$pattern')) al.push('$pattern');
fs.writeFileSync(path, JSON.stringify(cfg, null, 2));
" 2>/dev/null
        log_success "Added to allowlist: ${BOLD}$pattern${NC}"
      else
        log_error "Requires python3 or node to manage allowlist."
        return 1
      fi
      ;;

    remove)
      if [[ -z "$pattern" ]]; then
        log_error "Usage: envguard allowlist remove <pattern>"
        return 1
      fi

      if [[ ! -f "$OPENCLAW_CONFIG" ]]; then
        log_warn "No config file found. Allowlist is empty."
        return 0
      fi

      if command -v python3 &>/dev/null; then
        python3 -c "
import json, os

config_path = os.path.expanduser('$OPENCLAW_CONFIG')
if not os.path.exists(config_path):
    print('not_found')
    exit()

with open(config_path) as f:
    cfg = json.load(f)

try:
    allowlist = cfg['skills']['entries']['envguard']['config']['allowlist']
    pattern = '$pattern'
    if pattern in allowlist:
        allowlist.remove(pattern)
        with open(config_path, 'w') as f:
            json.dump(cfg, f, indent=2)
        print('removed')
    else:
        print('not_found')
except (KeyError, TypeError):
    print('not_found')
" 2>/dev/null | {
          read -r result
          if [[ "$result" == "removed" ]]; then
            log_success "Removed from allowlist: ${BOLD}$pattern${NC}"
          else
            log_warn "Pattern not found in allowlist: $pattern"
          fi
        }
      elif command -v node &>/dev/null; then
        node -e "
const fs = require('fs');
const path = '$OPENCLAW_CONFIG';
let cfg = {};
try { cfg = JSON.parse(fs.readFileSync(path, 'utf8')); } catch(e) {}
const al = cfg?.skills?.entries?.envguard?.config?.allowlist || [];
const idx = al.indexOf('$pattern');
if (idx >= 0) {
  al.splice(idx, 1);
  fs.writeFileSync(path, JSON.stringify(cfg, null, 2));
  console.log('removed');
} else {
  console.log('not_found');
}
" 2>/dev/null | {
          read -r result
          if [[ "$result" == "removed" ]]; then
            log_success "Removed from allowlist: ${BOLD}$pattern${NC}"
          else
            log_warn "Pattern not found in allowlist: $pattern"
          fi
        }
      else
        log_error "Requires python3 or node to manage allowlist."
        return 1
      fi
      ;;

    list)
      echo -e "${BOLD}━━━ EnvGuard Allowlist ━━━${NC}"
      echo ""

      local items=""
      if [[ -f "$OPENCLAW_CONFIG" ]]; then
        if command -v python3 &>/dev/null; then
          items=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    for item in cfg.get('skills', {}).get('entries', {}).get('envguard', {}).get('config', {}).get('allowlist', []):
        print(item)
except: pass
" 2>/dev/null) || true
        elif command -v node &>/dev/null; then
          items=$(node -e "
try {
  const cfg = require('$OPENCLAW_CONFIG');
  (cfg?.skills?.entries?.envguard?.config?.allowlist || []).forEach(i => console.log(i));
} catch(e) {}
" 2>/dev/null) || true
        elif command -v jq &>/dev/null; then
          items=$(jq -r '.skills.entries.envguard.config.allowlist[]? // empty' "$OPENCLAW_CONFIG" 2>/dev/null) || true
        fi
      fi

      if [[ -z "$items" ]]; then
        echo -e "  ${DIM}(empty)${NC}"
        echo ""
        echo -e "Add patterns: ${CYAN}envguard allowlist add <pattern>${NC}"
      else
        local count=0
        while IFS= read -r item; do
          [[ -z "$item" ]] && continue
          ((count++)) || true
          echo -e "  ${GREEN}*${NC} $item"
        done <<< "$items"
        echo ""
        echo -e "  ${DIM}$count pattern(s) allowlisted${NC}"
      fi
      ;;

    *)
      log_error "Unknown allowlist subcommand: $subcmd"
      echo "  Usage: envguard allowlist [add|remove|list] [pattern]"
      return 1
      ;;
  esac
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
    if grep -q "envguard" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# ─── EnvGuard hooks ─────────────────────────────
    envguard-secret-scan:
      run: |
        ENVGUARD_SKILL_DIR="${ENVGUARD_SKILL_DIR:-$HOME/.openclaw/skills/envguard}"
        if [[ -f "$ENVGUARD_SKILL_DIR/scripts/scanner.sh" ]]; then
          source "$ENVGUARD_SKILL_DIR/scripts/scanner.sh"
          hook_secret_scan
        else
          echo "[EnvGuard] Skill not found at $ENVGUARD_SKILL_DIR — skipping scan"
        fi
      fail_text: |
        Secrets detected in staged files!
        Run 'envguard scan' to see details.
        Run 'envguard allowlist add <pattern>' to allow known-safe patterns.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended EnvGuard hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged files will be scanned for secrets on every commit."
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
    if grep -q "envguard" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      sed '/# ─── EnvGuard hooks/,/fail_text:.*$/d' "$config" > "$tmp"
      grep -v "envguard" "$tmp" > "$config" 2>/dev/null || mv "$tmp" "$config"
      rm -f "$tmp"
      echo -e "${GREEN}+${NC} Removed EnvGuard hooks"
    else
      log_warn "No EnvGuard hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# ─── Pattern listing ───────────────────────────────────────────────────────

do_list_patterns() {
  source "$SCRIPT_DIR/patterns.sh"

  echo -e "${BOLD}━━━ EnvGuard Detection Patterns ━━━${NC}"
  echo ""
  echo -e "${BOLD}$(envguard_pattern_count) patterns across 20+ services${NC}"
  echo ""

  echo -e "${RED}${BOLD}CRITICAL:${NC}"
  envguard_list_patterns "critical" | while IFS= read -r line; do
    echo "  $line"
  done
  echo ""

  echo -e "${RED}HIGH:${NC}"
  envguard_list_patterns "high" | while IFS= read -r line; do
    echo "  $line"
  done
  echo ""

  echo -e "${YELLOW}MEDIUM:${NC}"
  envguard_list_patterns "medium" | while IFS= read -r line; do
    echo "  $line"
  done
  echo ""

  echo -e "${BLUE}LOW:${NC}"
  envguard_list_patterns "low" | while IFS= read -r line; do
    echo "  $line"
  done
}

# ─── Command dispatch ───────────────────────────────────────────────────────

main() {
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    scan)
      local target="${1:-.}"
      log_info "Scanning for secrets in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/scanner.sh"
      do_secret_scan "$target"
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
          echo "  Usage: envguard hooks [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    allowlist)
      require_license "pro"
      local subcmd="${1:-list}"
      shift || true
      local pattern="${1:-}"
      do_allowlist "$subcmd" "$pattern"
      ;;

    diff)
      require_license "pro"
      log_info "Scanning staged changes for secrets..."
      source "$SCRIPT_DIR/scanner.sh"
      do_diff_scan
      ;;

    history)
      require_license "team"
      local target="${1:-.}"
      log_info "Scanning git history in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/scanner.sh"
      do_history_scan "$target"
      ;;

    report)
      require_license "team"
      local target="${1:-.}"
      log_info "Generating security report for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/scanner.sh"
      do_secret_report "$target"
      ;;

    policy)
      require_license "team"
      local target="${1:-.}"
      log_info "Running policy enforcement in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/scanner.sh"
      do_policy_scan "$target"
      ;;

    patterns)
      do_list_patterns
      ;;

    status)
      show_version
      echo ""
      source "$SCRIPT_DIR/license.sh"
      show_envguard_status
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
