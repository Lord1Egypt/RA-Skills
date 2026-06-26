#!/bin/bash
set -euo pipefail

OS_NAME="$(uname -s)"

case "$OS_NAME" in
  Linux)
    if [[ -f /etc/os-release ]]; then
      . /etc/os-release
      if [[ "${ID:-}" == "ubuntu" ]]; then
        echo "ubuntu"
        exit 0
      fi
    fi
    echo "Unsupported Linux distro. Supported platforms: ubuntu, macos" >&2
    exit 1
    ;;
  Darwin)
    echo "macos"
    exit 0
    ;;
  *)
    echo "Unsupported OS: $OS_NAME. Supported platforms: ubuntu, macos" >&2
    exit 1
    ;;
esac
