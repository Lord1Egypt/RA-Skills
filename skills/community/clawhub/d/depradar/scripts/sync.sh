#!/usr/bin/env bash
# sync.sh — Install /depradar to all supported AI assistant locations
#
# Usage:
#   bash scripts/sync.sh              # Install to all detected locations
#   bash scripts/sync.sh --dry-run    # Show what would be installed without doing it
#   bash scripts/sync.sh --uninstall  # Remove from all locations

set -euo pipefail

# ── Config ─────────────────────────────────────────────────────────────────────
SKILL_NAME="depradar-skill"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Install targets
TARGETS=(
  "$HOME/.claude/skills/$SKILL_NAME"           # Claude Code
  "$HOME/.codex/skills/$SKILL_NAME"            # OpenAI Codex CLI
  "$HOME/.agents/skills/$SKILL_NAME"           # Generic agents dir
)

# ── Flags ──────────────────────────────────────────────────────────────────────
DRY_RUN=false
UNINSTALL=false

for arg in "$@"; do
  case "$arg" in
    --dry-run)   DRY_RUN=true ;;
    --uninstall) UNINSTALL=true ;;
    --help|-h)
      echo "Usage: bash scripts/sync.sh [--dry-run] [--uninstall]"
      echo ""
      echo "  --dry-run    Show what would be done without making changes"
      echo "  --uninstall  Remove /depradar from all install locations"
      exit 0
      ;;
    *)
      echo "Unknown flag: $arg"
      exit 1
      ;;
  esac
done

# ── Colours ────────────────────────────────────────────────────────────────────
if [[ -t 1 ]] && command -v tput &>/dev/null && tput colors &>/dev/null && [[ "$(tput colors)" -ge 8 ]]; then
  GREEN="\033[0;32m"
  YELLOW="\033[0;33m"
  RED="\033[0;31m"
  CYAN="\033[0;36m"
  BOLD="\033[1m"
  RESET="\033[0m"
else
  GREEN="" YELLOW="" RED="" CYAN="" BOLD="" RESET=""
fi

info()    { printf "${CYAN}  →${RESET} %s\n" "$1"; }
success() { printf "${GREEN}  ✓${RESET} %s\n" "$1"; }
warn()    { printf "${YELLOW}  !${RESET} %s\n" "$1"; }
error()   { printf "${RED}  ✗${RESET} %s\n" "$1" >&2; }
header()  { printf "\n${BOLD}%s${RESET}\n" "$1"; }

# ── Verify source ──────────────────────────────────────────────────────────────
if [[ ! -f "$SKILL_ROOT/SKILL.md" ]]; then
  error "Could not find SKILL.md in $SKILL_ROOT"
  error "Run this script from the depradar-skill directory: bash scripts/sync.sh"
  exit 1
fi

if [[ ! -f "$SKILL_ROOT/scripts/depradar.py" ]]; then
  error "Could not find scripts/depradar.py in $SKILL_ROOT"
  exit 1
fi

# ── Python check ───────────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
  warn "python3 not found — /depradar requires Python 3.8+. Install from python.org."
else
  PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
  PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
  PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
  if [[ "$PY_MAJOR" -lt 3 ]] || ([[ "$PY_MAJOR" -eq 3 ]] && [[ "$PY_MINOR" -lt 8 ]]); then
    warn "Python $PY_VERSION found but /depradar requires Python 3.8+. Please upgrade."
  else
    success "Python $PY_VERSION OK"
  fi
fi

# ── Determine active targets ───────────────────────────────────────────────────
# Only install to dirs whose parent exists (i.e., the assistant is likely installed)
active_targets=()
for target in "${TARGETS[@]}"; do
  parent="$(dirname "$target")"
  if [[ -d "$parent" ]] || [[ "$DRY_RUN" == true ]]; then
    active_targets+=("$target")
  fi
done

# Always include Claude Code target
CLAUDE_TARGET="$HOME/.claude/skills/$SKILL_NAME"
found_claude=false
for t in "${active_targets[@]}"; do
  [[ "$t" == "$CLAUDE_TARGET" ]] && found_claude=true && break
done
if [[ "$found_claude" == false ]]; then
  active_targets=("$CLAUDE_TARGET" "${active_targets[@]}")
fi

# ── Uninstall mode ─────────────────────────────────────────────────────────────
if [[ "$UNINSTALL" == true ]]; then
  header "Uninstalling /depradar"
  removed=0
  for target in "${TARGETS[@]}"; do
    if [[ -d "$target" ]]; then
      info "Removing $target"
      if [[ "$DRY_RUN" == false ]]; then
        rm -rf "$target"
        success "Removed $target"
      else
        warn "[dry-run] Would remove $target"
      fi
      ((removed++)) || true
    fi
  done
  if [[ "$removed" -eq 0 ]]; then
    info "/depradar was not installed in any known location."
  fi
  exit 0
fi

# ── Install ────────────────────────────────────────────────────────────────────
header "Installing /depradar v$(python3 -c "import json; d=open('$SKILL_ROOT/.claude-plugin/plugin.json').read(); import json; print(json.loads(d)['version'])" 2>/dev/null || echo "1.0.0")"

printf "  Source: ${CYAN}%s${RESET}\n\n" "$SKILL_ROOT"

installed=0
for target in "${active_targets[@]}"; do
  info "Installing to $target ..."

  if [[ "$DRY_RUN" == true ]]; then
    warn "[dry-run] Would sync to $target"
    continue
  fi

  # Create parent directory
  mkdir -p "$(dirname "$target")"

  # Rsync if available, otherwise cp -r
  if command -v rsync &>/dev/null; then
    rsync -a --delete \
      --exclude='__pycache__' \
      --exclude='*.pyc' \
      --exclude='.git' \
      --exclude='*.egg-info' \
      "$SKILL_ROOT/" "$target/"
  else
    # Fallback: remove old install and copy fresh
    rm -rf "$target"
    cp -r "$SKILL_ROOT" "$target"
    # Remove pycache after copy
    find "$target" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
    find "$target" -name '*.pyc' -delete 2>/dev/null || true
  fi

  # Make hooks executable
  if [[ -f "$target/hooks/scripts/check-config.sh" ]]; then
    chmod +x "$target/hooks/scripts/check-config.sh"
  fi

  # Install JS AST dependencies (acorn) if npm is available
  if command -v npm &>/dev/null && [[ -f "$target/scripts/lib/package.json" ]]; then
    npm install --prefix "$target/scripts/lib/" --silent 2>/dev/null \
      && success "Installed JS AST dependencies (acorn) in $target/scripts/lib/" \
      || warn "npm install for JS AST deps failed — regex fallback will be used"
  fi

  success "Installed to $target"
  ((installed++)) || true
done

# ── Config tip ────────────────────────────────────────────────────────────────
if [[ "$DRY_RUN" == false ]] && [[ "$installed" -gt 0 ]]; then
  echo ""
  header "Optional: Add API keys for better coverage"

  GLOBAL_ENV="$HOME/.config/depradar/.env"
  if [[ -f "$GLOBAL_ENV" ]]; then
    success "Config file already exists at $GLOBAL_ENV"
  else
    printf "  Create ${CYAN}%s${RESET}:\n\n" "$GLOBAL_ENV"
    cat << 'EXAMPLE'
    mkdir -p ~/.config/depradar
    cat > ~/.config/depradar/.env << 'EOF'
    # github.com/settings/tokens — no scopes needed for public repos
    GITHUB_TOKEN=ghp_...

    # scrapecreators.com — enables Reddit community signals
    SCRAPECREATORS_API_KEY=sc_...
    EOF
EXAMPLE
  fi

  echo ""
  printf "  Run ${BOLD}/depradar --diagnose${RESET} to check your configuration.\n"
  printf "  Run ${BOLD}/depradar --mock${RESET} to test with fixture data.\n"
  echo ""
fi

# ── Summary ───────────────────────────────────────────────────────────────────
if [[ "$DRY_RUN" == true ]]; then
  echo ""
  warn "Dry run complete. No files were changed."
elif [[ "$installed" -gt 0 ]]; then
  echo ""
  printf "${GREEN}${BOLD}✓ /depradar installed successfully${RESET} to $installed location(s).\n"
  echo ""
fi
