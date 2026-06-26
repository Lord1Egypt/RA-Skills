#!/bin/bash
# Claw-SOS Uninstaller

set -euo pipefail

INSTALL_DIR="/usr/local/bin"
SCRIPT_NAME="sos"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

if [[ -w "$INSTALL_DIR" ]]; then
  SUDO=""
elif command -v sudo &>/dev/null; then
  SUDO="sudo"
else
  echo -e "${RED}Can't write to ${INSTALL_DIR}. Run as root or with sudo.${NC}"
  exit 1
fi

if [[ -f "${INSTALL_DIR}/${SCRIPT_NAME}" ]]; then
  $SUDO rm -f "${INSTALL_DIR}/${SCRIPT_NAME}"
  echo -e "${GREEN}✓ Removed ${INSTALL_DIR}/${SCRIPT_NAME}${NC}"
  echo -e "  Log file kept at: ~/.openclaw/backups/sos.log"
  echo -e "  Config backups kept at: ~/.openclaw/backups/"
else
  echo -e "${RED}sos not found at ${INSTALL_DIR}/${SCRIPT_NAME}${NC}"
fi
