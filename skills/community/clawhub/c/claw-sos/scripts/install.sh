#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Claw-SOS Installer
# ═══════════════════════════════════════════════════════════════
# Usage: curl -fsSL https://raw.githubusercontent.com/clawsos/claw-sos/main/install.sh | bash
# Or:    wget -qO- https://raw.githubusercontent.com/clawsos/claw-sos/main/install.sh | bash

set -euo pipefail

REPO="clawsos/claw-sos"
BRANCH="main"
INSTALL_DIR="/usr/local/bin"
SCRIPT_NAME="sos"
RAW_URL="https://raw.githubusercontent.com/${REPO}/${BRANCH}/sos.sh"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}╔═══════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     🔧 Claw-SOS Installer             ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════╝${NC}"
echo ""

# Check if running as root or can write to install dir
if [[ -w "$INSTALL_DIR" ]]; then
  SUDO=""
elif command -v sudo &>/dev/null; then
  SUDO="sudo"
  echo -e "${YELLOW}Need sudo to install to ${INSTALL_DIR}${NC}"
else
  echo -e "${RED}Error: Can't write to ${INSTALL_DIR} and sudo not available.${NC}"
  echo -e "${YELLOW}Try: INSTALL_DIR=~/.local/bin bash <(curl -fsSL ...)${NC}"
  exit 1
fi

# Allow custom install dir
INSTALL_DIR="${INSTALL_DIR:-/usr/local/bin}"
mkdir -p "$INSTALL_DIR" 2>/dev/null || $SUDO mkdir -p "$INSTALL_DIR"

# Detect OS
OS="$(uname -s)"
echo -e "  OS: ${GREEN}${OS}${NC}"

# Download
echo -ne "  Downloading sos.sh... "
if command -v curl &>/dev/null; then
  $SUDO curl -fsSL "$RAW_URL" -o "${INSTALL_DIR}/${SCRIPT_NAME}"
elif command -v wget &>/dev/null; then
  $SUDO wget -qO "${INSTALL_DIR}/${SCRIPT_NAME}" "$RAW_URL"
else
  echo -e "${RED}Error: curl or wget required${NC}"
  exit 1
fi
echo -e "${GREEN}✓${NC}"

# Make executable
$SUDO chmod +x "${INSTALL_DIR}/${SCRIPT_NAME}"

# Check whiptail/dialog for arrow-key menu
echo -ne "  Checking menu support... "
if command -v whiptail &>/dev/null; then
  echo -e "${GREEN}whiptail ✓${NC}"
elif command -v dialog &>/dev/null; then
  echo -e "${GREEN}dialog ✓${NC}"
else
  echo -e "${YELLOW}not found${NC}"
  echo -e "  ${YELLOW}Arrow-key menu won't work. Install for best experience:${NC}"
  if [[ "$OS" == "Darwin" ]]; then
    echo -e "    ${CYAN}brew install dialog${NC}"
  else
    echo -e "    ${CYAN}apt install whiptail${NC}  or  ${CYAN}yum install newt${NC}"
  fi
  echo -e "  ${GREEN}Text menu will work fine without it.${NC}"
fi

# Check OpenClaw
echo -ne "  Checking OpenClaw... "
if command -v openclaw &>/dev/null; then
  echo -e "${GREEN}$(openclaw --version 2>/dev/null | head -1)${NC}"
else
  echo -e "${YELLOW}not found (sos will still install but some features need OpenClaw)${NC}"
fi

# Verify installation
echo ""
VERSION=$("${INSTALL_DIR}/${SCRIPT_NAME}" --version 2>/dev/null || echo "unknown")
if [[ "$VERSION" != "unknown" ]]; then
  echo -e "${GREEN}╔═══════════════════════════════════════╗${NC}"
  echo -e "${GREEN}║  ✅ Installed: ${VERSION}               ║${NC}"
  echo -e "${GREEN}║  Location: ${INSTALL_DIR}/${SCRIPT_NAME}              ║${NC}"
  echo -e "${GREEN}╚═══════════════════════════════════════╝${NC}"
  echo ""
  echo -e "  Run ${CYAN}sos${NC} to start"
  echo -e "  Run ${CYAN}sos auto${NC} for automatic repair"
  echo -e "  Run ${CYAN}sos --help${NC} for all options"
else
  echo -e "${RED}Installation may have failed. Check ${INSTALL_DIR}/${SCRIPT_NAME}${NC}"
  exit 1
fi
