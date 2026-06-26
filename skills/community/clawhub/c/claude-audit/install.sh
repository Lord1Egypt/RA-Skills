#!/usr/bin/env bash
set -euo pipefail

# claude-audit installer
# Usage: curl -fsSL https://raw.githubusercontent.com/atobones/claude-audit/main/install.sh | bash

REPO="atobones/claude-audit"
BRANCH="main"
RAW="https://raw.githubusercontent.com/${REPO}/${BRANCH}"
SKILL_FILE="audit.md"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

header() {
  echo ""
  echo -e "${CYAN}${BOLD}  claude-audit installer${NC}"
  echo -e "${CYAN}  ----------------------${NC}"
  echo ""
}

success() { echo -e "  ${GREEN}$1${NC}"; }
warn()    { echo -e "  ${YELLOW}$1${NC}"; }
error()   { echo -e "  ${RED}$1${NC}"; exit 1; }
info()    { echo -e "  $1"; }

header

# Determine install mode
MODE="${1:-}"
if [[ "$MODE" == "--global" || "$MODE" == "-g" ]]; then
  TARGET_DIR="$HOME/.claude/commands"
  MODE_LABEL="global"
elif [[ "$MODE" == "--project" || "$MODE" == "-p" ]]; then
  TARGET_DIR=".claude/commands"
  MODE_LABEL="project"
else
  echo -e "  ${BOLD}Where do you want to install?${NC}"
  echo ""
  echo "  1) Global  (~/.claude/commands/) - available in all projects"
  echo "  2) Project  (./.claude/commands/) - available in this project only"
  echo ""
  read -rp "  Choice [1/2]: " choice
  echo ""
  case "$choice" in
    1) TARGET_DIR="$HOME/.claude/commands"; MODE_LABEL="global" ;;
    2) TARGET_DIR=".claude/commands"; MODE_LABEL="project" ;;
    *) error "Invalid choice. Run again and pick 1 or 2." ;;
  esac
fi

# Create target directory
mkdir -p "$TARGET_DIR" || error "Failed to create $TARGET_DIR"

# Download skill file
info "Downloading audit.md..."
if command -v curl &>/dev/null; then
  curl -fsSL "${RAW}/${SKILL_FILE}" -o "${TARGET_DIR}/${SKILL_FILE}"
elif command -v wget &>/dev/null; then
  wget -q "${RAW}/${SKILL_FILE}" -O "${TARGET_DIR}/${SKILL_FILE}"
else
  error "Neither curl nor wget found. Install one and retry."
fi

# Verify
if [[ -f "${TARGET_DIR}/${SKILL_FILE}" ]]; then
  echo ""
  success "Installed successfully! (${MODE_LABEL})"
  echo ""
  info "Location: ${TARGET_DIR}/${SKILL_FILE}"
  echo ""
  echo -e "  ${BOLD}Usage:${NC}"
  echo "    /audit                    Full audit of current project"
  echo "    /audit --focus security   Security scan only"
  echo "    /audit --changed          Audit only changed files"
  echo "    /audit --fix              Auto-fix after scan"
  echo "    /audit src/               Audit specific directory"
  echo ""
  success "Open Claude Code and type /audit to start."
  echo ""
else
  error "Installation failed. File not found at ${TARGET_DIR}/${SKILL_FILE}"
fi
