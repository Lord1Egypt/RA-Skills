#!/bin/bash

# Install hevycli for Hevy fitness tracking
set -e

INSTALL_DIR="$HOME/.local/bin"
BINARY_NAME="hevycli"
TEMP_DIR="/tmp/hevycli-install"

echo "🏋️ Installing hevycli..."

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$TEMP_DIR"

# Get latest release URL
RELEASE_URL=$(curl -sL https://api.github.com/repos/obay/hevycli/releases/latest | grep "browser_download_url.*linux.*amd64" | cut -d '"' -f 4 | head -1)

if [ -z "$RELEASE_URL" ]; then
    echo "❌ Failed to get download URL"
    exit 1
fi

echo "📥 Downloading from: $RELEASE_URL"

# Download and extract
cd "$TEMP_DIR"
curl -sL "$RELEASE_URL" | tar -xz

# Install binary
if [ -f "$BINARY_NAME" ]; then
    mv "$BINARY_NAME" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/$BINARY_NAME"
    echo "✅ hevycli installed to $INSTALL_DIR/$BINARY_NAME"
else
    echo "❌ Binary not found in archive"
    exit 1
fi

# Add to PATH if not already
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "📝 Add to your shell profile:"
    echo "export PATH=\"\$PATH:$INSTALL_DIR\""
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo "🎉 Installation complete!"
echo "💡 Next: Run 'hevycli config init' to set up your API key"