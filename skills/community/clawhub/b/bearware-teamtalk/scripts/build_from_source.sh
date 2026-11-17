#!/usr/bin/env bash
set -euo pipefail

# Build TeamTalk 5 from GitHub source
REPO_URL="${REPO_URL:-https://github.com/BearWare/TeamTalk5.git}"
BUILD_DIR="${BUILD_DIR:-./TeamTalk5}"
BRANCH="${BRANCH:-master}"
TARGET="${TARGET:-auto}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== TeamTalk 5 Build from Source ==="
echo "Build dir: $BUILD_DIR"
echo "Target: $TARGET"

# Detect target
if [ "$TARGET" = "auto" ]; then
    case "$(uname -s)" in
        Linux*)  TARGET="linux" ;;
        Darwin*) TARGET="mac" ;;
        CYGWIN*|MINGW*|MSYS*) TARGET="win" ;;
        *)       echo "Unknown OS"; exit 1 ;;
    esac
fi

# Clone if not exists
if [ ! -d "$BUILD_DIR" ]; then
    echo "Cloning TeamTalk5 from $REPO_URL"
    git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$BUILD_DIR"
else
    echo "TeamTalk5 already cloned at $BUILD_DIR"
    if [ -d "$BUILD_DIR/.git" ]; then
        git -C "$BUILD_DIR" pull --depth 1
    fi
fi

cd "$BUILD_DIR"

# Install dependencies
case "$TARGET" in
    linux)
        echo "Detecting Linux distro..."
        if grep -qi ubuntu /etc/os-release 2>/dev/null; then
            UBUNTU_VER=$(grep VERSION_ID /etc/os-release | cut -d= -f2 | tr -d '"' | tr -d '.')
            echo "Installing deps for Ubuntu $UBUNTU_VER..."
            sudo make -C Build depend-ubuntu${UBUNTU_VER} || \
                sudo make -C Build depend-ubuntu22
            echo "Building..."
            make -C Build ubuntu${UBUNTU_VER} || make -C Build ubuntu22
        elif grep -qi debian /etc/os-release 2>/dev/null; then
            sudo make -C Build depend-raspios12
            make -C Build raspios12
        else
            echo "Unsupported Linux distro. Trying direct CMake build..."
            mkdir -p Library/TeamTalkLib/build && cd Library/TeamTalkLib/build
            cmake .. -DCMAKE_BUILD_TYPE=Release
            make -j$(nproc)
        fi
        ;;
    mac)
        brew install qt openssl 2>/dev/null || true
        make -C Build depend-mac
        make -C Build mac
        ;;
    win)
        echo "Windows build requires Visual Studio. See:"
        echo "  https://github.com/BearWare/TeamTalk5#readme"
        exit 1
        ;;
esac

echo ""
echo "=== Build complete ==="
echo "Binaries in: $BUILD_DIR/Build/output"
$SCRIPT_DIR/check_sdk.py
