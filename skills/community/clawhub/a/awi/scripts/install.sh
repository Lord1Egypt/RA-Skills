#!/bin/bash
set -e

VERSION="v0.1.0"
REPO="jzOcb/awi"
INSTALL_DIR="${HOME}/bin"

# Detect OS and architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

case "$ARCH" in
  x86_64|amd64) ARCH="amd64" ;;
  arm64|aarch64) ARCH="arm64" ;;
  *) echo "❌ Unsupported architecture: $ARCH"; exit 1 ;;
esac

case "$OS" in
  darwin) PLATFORM="darwin" ;;
  linux) PLATFORM="linux" ;;
  *) echo "❌ Unsupported OS: $OS"; exit 1 ;;
esac

BINARY="awi-${PLATFORM}-${ARCH}"
URL="https://github.com/${REPO}/releases/download/${VERSION}/${BINARY}"

echo "📦 Installing AWI ${VERSION} (${PLATFORM}/${ARCH})..."
echo "   From: ${URL}"

mkdir -p "$INSTALL_DIR"

if command -v curl &>/dev/null; then
  curl -fSL "$URL" -o "${INSTALL_DIR}/awi"
elif command -v wget &>/dev/null; then
  wget -q "$URL" -O "${INSTALL_DIR}/awi"
else
  echo "❌ Need curl or wget"; exit 1
fi

chmod +x "${INSTALL_DIR}/awi"

# Verify
if "${INSTALL_DIR}/awi" --help &>/dev/null; then
  echo "✅ AWI installed to ${INSTALL_DIR}/awi"
  echo "   Run: awi read <url>"
else
  echo "❌ Installation failed"
  exit 1
fi
