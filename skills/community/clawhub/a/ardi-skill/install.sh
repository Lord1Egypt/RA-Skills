#!/bin/sh
# Install ardi-agent binary from GitHub releases.
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/awp-worknet/ardi-skill/main/install.sh | sh
# or
#   sh install.sh
#
# ⚠ Production install URL: github.com/awp-worknet/ardi-skill (canonical org).
# Releases tagged on awp-worknet/ardi-skill main; binaries built by CI.
#
# Runtime requirements — any ONE of: curl, wget, or python3 (stdlib).

set -e

# ─────────────────────────────────────────────────────────────────────
# Production repo. Forks of this skill should re-point this constant.
REPO="awp-worknet/ardi-skill"
# ─────────────────────────────────────────────────────────────────────

# Default install dir: ~/.local/bin if writable (no sudo needed); fall
# back to /usr/local/bin only if user explicitly opts in via INSTALL_DIR.
# Pre-v0.5.9 default was /usr/local/bin which prompted for sudo on macOS
# the first time anyone ran the curl|sh one-liner — broke the
# unattended-install path that LLM agents follow.
if [ -z "${INSTALL_DIR:-}" ]; then
  if [ -w "${HOME}/.local/bin" ] 2>/dev/null || mkdir -p "${HOME}/.local/bin" 2>/dev/null; then
    INSTALL_DIR="${HOME}/.local/bin"
  else
    INSTALL_DIR="/usr/local/bin"
  fi
fi

OS="$(uname -s)"
ARCH="$(uname -m)"

case "${OS}" in
  Linux)   OS_NAME="linux" ;;
  Darwin)  OS_NAME="darwin" ;;
  *)       echo "Error: unsupported OS: ${OS}"; exit 1 ;;
esac

case "${ARCH}" in
  x86_64|amd64)   ARCH_NAME="x86_64" ;;
  aarch64|arm64)  ARCH_NAME="aarch64" ;;
  *)              echo "Error: unsupported architecture: ${ARCH}"; exit 1 ;;
esac

if [ "${OS_NAME}" = "linux" ] && [ "${ARCH_NAME}" = "x86_64" ]; then
  BINARY_NAME="ardi-agent-linux-x86_64-musl"
else
  BINARY_NAME="ardi-agent-${OS_NAME}-${ARCH_NAME}"
fi

fetch() {
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$1"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO- "$1"
  elif command -v python3 >/dev/null 2>&1; then
    python3 -c "
import sys, urllib.request
try:
    with urllib.request.urlopen(sys.argv[1], timeout=60) as r:
        sys.stdout.buffer.write(r.read())
except Exception as e:
    print('fetch failed:', e, file=sys.stderr); sys.exit(1)
" "$1"
  else
    echo "Error: need curl, wget, or python3 to download — none found" >&2
    return 1
  fi
}

save() {
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL -o "$2" "$1"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "$2" "$1"
  elif command -v python3 >/dev/null 2>&1; then
    python3 -c "
import sys, urllib.request
try:
    urllib.request.urlretrieve(sys.argv[1], sys.argv[2])
except Exception as e:
    print('download failed:', e, file=sys.stderr); sys.exit(1)
" "$1" "$2"
  else
    return 1
  fi
}

echo "Fetching latest ardi-agent release from ${REPO}..."
LATEST="$(fetch "https://api.github.com/repos/${REPO}/releases/latest" \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["tag_name"])' 2>/dev/null \
  || fetch "https://api.github.com/repos/${REPO}/releases/latest" \
       | grep '"tag_name"' | head -1 | sed 's/.*: "\(.*\)".*/\1/')"

if [ -z "${LATEST}" ]; then
  echo "Error: could not find latest release of ${REPO}" >&2
  echo "  Check https://github.com/${REPO}/releases" >&2
  exit 1
fi

URL="https://github.com/${REPO}/releases/download/${LATEST}/${BINARY_NAME}"

echo "Downloading ardi-agent ${LATEST} (${OS_NAME}/${ARCH_NAME})..."
TMPFILE="$(mktemp)"
if ! save "${URL}" "${TMPFILE}"; then
  rm -f "${TMPFILE}"
  echo "Error: download failed from ${URL}" >&2
  exit 1
fi

chmod +x "${TMPFILE}"
mkdir -p "${INSTALL_DIR}"

if [ -w "${INSTALL_DIR}" ] || [ "${INSTALL_DIR}" = "${HOME}/.local/bin" ]; then
  mv "${TMPFILE}" "${INSTALL_DIR}/ardi-agent"
elif command -v sudo >/dev/null 2>&1; then
  echo "Installing to ${INSTALL_DIR} (requires sudo)..."
  sudo mv "${TMPFILE}" "${INSTALL_DIR}/ardi-agent"
else
  mkdir -p "${HOME}/.local/bin"
  mv "${TMPFILE}" "${HOME}/.local/bin/ardi-agent"
  INSTALL_DIR="${HOME}/.local/bin"
  echo "Note: installed to ${HOME}/.local/bin — add it to PATH if not already"
fi

if [ "${OS_NAME}" = "darwin" ]; then
  xattr -d com.apple.quarantine "${INSTALL_DIR}/ardi-agent" 2>/dev/null || true
fi

echo ""
echo "✓ ardi-agent ${LATEST} installed to ${INSTALL_DIR}/ardi-agent"
if ! command -v ardi-agent >/dev/null 2>&1; then
  echo ""
  echo "⚠ ${INSTALL_DIR} is not in PATH. Add this to your shell rc:"
  echo "    export PATH=\"${INSTALL_DIR}:\$PATH\""
fi

echo ""
echo "Next:"
echo "  1. Install awp-wallet (for tx signing):"
echo "     git clone https://github.com/awp-core/awp-wallet ~/awp-wallet && cd ~/awp-wallet && bash install.sh"
echo "  2. Run preflight:"
echo "     ardi-agent preflight"
