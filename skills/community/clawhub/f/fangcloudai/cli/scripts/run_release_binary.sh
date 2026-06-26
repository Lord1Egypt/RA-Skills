#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]:-$0}"
SCRIPT_DIR="$(cd "$(dirname "${SCRIPT_PATH}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
RELEASE_DIR="${ROOT_DIR}/release"
BIN_DIR="${ROOT_DIR}/bin"

if [ "$#" -lt 1 ]; then
  echo "Usage: run_release_binary.sh <subcommand> [args...]" >&2
  echo "Example: ./cli/scripts/run_release_binary.sh api GET /v2/user/info" >&2
  exit 1
fi

os="$(uname -s)"
arch="$(uname -m)"

case "${os}" in
  Darwin)
    # On Apple Silicon running a Rosetta x86_64 shell, prefer arm64 binary.
    if [ "${arch}" = "arm64" ]; then
      file="fangcloud-macos-arm64"
    elif [ "${arch}" = "x86_64" ] && [ "$(sysctl -in hw.optional.arm64 2>/dev/null || echo 0)" = "1" ]; then
      file="fangcloud-macos-arm64"
    else
      file="fangcloud-macos-amd64"
    fi
    ;;
  Linux)
    if [ "${arch}" = "aarch64" ]; then
      file="fangcloud-linux-arm64"
    else
      file="fangcloud-linux-amd64"
    fi
    ;;
  *)
    echo "Unsupported OS for this script: ${os}" >&2
    echo "Use PowerShell script on Windows: .\\cli\\scripts\\run_release_binary.ps1" >&2
    exit 1
    ;;
esac

target="${BIN_DIR}/${file}"

is_healthy() {
  local bin_path="$1"
  if [ "${os}" = "Darwin" ]; then
    codesign --verify --verbose=2 "${bin_path}" >/dev/null 2>&1
  else
    "${bin_path}" --help >/dev/null 2>&1
  fi
}

if [ ! -x "${target}" ] || ! is_healthy "${target}"; then
  "${SCRIPT_DIR}/download_release_binary.sh" "${file}"
fi

exec "${target}" "$@"
