#!/bin/bash

# Configure Hevy API key
set -e

API_KEY="${1:-}"
CONFIG_DIR="$HOME/.hevycli"
CONFIG_FILE="$CONFIG_DIR/config.yaml"

if [ -z "$API_KEY" ]; then
    echo "❌ Usage: $0 <api-key>"
    echo "💡 Get your API key from: https://hevy.com/settings?developer"
    exit 1
fi

echo "🔧 Configuring hevycli..."

# Create config directory
mkdir -p "$CONFIG_DIR"

# Create config file
cat > "$CONFIG_FILE" << EOF
api:
  key: "$API_KEY"

display:
  output_format: json
  color: false
  units: metric

EOF

echo "✅ Configuration saved to $CONFIG_FILE"
echo "🧪 Testing API connection..."

# Test the configuration
if command -v hevycli >/dev/null 2>&1; then
    if hevycli workout count >/dev/null 2>&1; then
        echo "✅ API key working correctly!"
    else
        echo "⚠️ API key may not be working. Check your Hevy Pro subscription and key."
    fi
else
    echo "⚠️ hevycli not found. Run install_hevycli.sh first."
fi