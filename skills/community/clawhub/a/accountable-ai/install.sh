#!/bin/bash

# Accountable AI Installation Script
# Creates ~/.accountable-ai/ directory and copies documentation files

set -e

INSTALL_DIR="$HOME/.accountable-ai"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Copy documentation files
cp "$SOURCE_DIR/GOVERNANCE.md" "$INSTALL_DIR/"
cp "$SOURCE_DIR/PROCEDURES.md" "$INSTALL_DIR/"
cp "$SOURCE_DIR/DELEGATION.md" "$INSTALL_DIR/"
cp "$SOURCE_DIR/README.md" "$INSTALL_DIR/"

# Make the install script itself executable
chmod +x "$0"

# Print success message
echo "Accountable AI successfully installed!"
echo ""
echo "Installation directory: $INSTALL_DIR"
echo ""
echo "Installed files:"
echo "  - GOVERNANCE.md"
echo "  - PROCEDURES.md"
echo "  - DELEGATION.md"
echo "  - README.md"
echo ""
echo "Usage:"
echo "  View documentation: cat $INSTALL_DIR/README.md"
echo "  Read governance: cat $INSTALL_DIR/GOVERNANCE.md"
echo "  Check procedures: cat $INSTALL_DIR/PROCEDURES.md"
echo "  Review delegation: cat $INSTALL_DIR/DELEGATION.md"
