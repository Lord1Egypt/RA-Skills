#!/usr/bin/env bash
# Auto-fix missing dependencies for project-tunnel.sh
# Detects macOS (brew) or Linux (apt/yum) and installs what's needed.
# Usage: fix_env.sh <tool1> [tool2] ...
# Example: fix_env.sh python3 node

set -euo pipefail

TOOLS=("$@")
if [[ ${#TOOLS[@]} -eq 0 ]]; then
  echo "Usage: fix_env.sh <tool1> [tool2] ..."
  exit 1
fi

OS="$(uname -s)"

install_macos() {
  local tool="$1"
  if ! command -v brew >/dev/null 2>&1; then
    echo "[fix] installing Homebrew first..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
  case "$tool" in
    python3) brew install python3 ;;
    node|npm) brew install node ;;
    curl)    brew install curl ;;
    lsof)    echo "[fix] lsof is part of macOS base — reinstall Xcode CLI tools:" && xcode-select --install ;;
    *)       brew install "$tool" ;;
  esac
}

install_linux() {
  local tool="$1"
  if command -v apt-get >/dev/null 2>&1; then
    case "$tool" in
      python3) sudo apt-get install -y python3 ;;
      node|npm) sudo apt-get install -y nodejs npm ;;
      curl)    sudo apt-get install -y curl ;;
      lsof)    sudo apt-get install -y lsof ;;
      *)       sudo apt-get install -y "$tool" ;;
    esac
  elif command -v yum >/dev/null 2>&1; then
    case "$tool" in
      python3) sudo yum install -y python3 ;;
      node|npm) sudo yum install -y nodejs npm ;;
      curl)    sudo yum install -y curl ;;
      lsof)    sudo yum install -y lsof ;;
      *)       sudo yum install -y "$tool" ;;
    esac
  else
    echo "❌ unknown package manager — please install '$tool' manually" >&2
    exit 1
  fi
}

for tool in "${TOOLS[@]}"; do
  echo "[fix] installing: $tool"
  if [[ "$OS" == "Darwin" ]]; then
    install_macos "$tool"
  else
    install_linux "$tool"
  fi
  echo "[fix] ✅ $tool installed"
done
