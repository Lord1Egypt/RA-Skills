#!/usr/bin/env bash
set -euo pipefail

echo "Installing dfseo-cli..."

if command -v pip &> /dev/null; then
    pip install dfseo
elif command -v pip3 &> /dev/null; then
    pip3 install dfseo
else
    echo "Error: pip not found. Install Python 3.11+ first." >&2
    exit 1
fi

if command -v dfseo &> /dev/null; then
    echo "✓ dfseo-cli installed successfully"
    dfseo --version
else
    echo "Error: dfseo command not found after installation." >&2
    echo "Make sure ~/.local/bin is in your PATH:" >&2
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\"" >&2
    exit 1
fi

echo ""
echo "Next steps:"
echo "  1. Set credentials:"
echo "     export DATAFORSEO_LOGIN='your@email.com'"
echo "     export DATAFORSEO_PASSWORD='your_api_password'"
echo ""
echo "  2. Verify:"
echo "     dfseo auth status"
echo ""
echo "  3. Try it:"
echo "     dfseo serp google 'test keyword'"
echo ""
echo "  4. Set defaults (optional):"
echo "     dfseo config set location 'Italy'"
echo "     dfseo config set language 'Italian'"
echo ""
echo "Get your DataForSEO API credentials at: https://app.dataforseo.com/api-access"
