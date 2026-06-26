#!/bin/bash
# CFGPU API Environment Setup Script

echo "=== CFGPU API Environment Setup ==="
echo ""

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Installing..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y jq
    elif command -v yum &> /dev/null; then
        sudo yum install -y jq
    elif command -v brew &> /dev/null; then
        brew install jq
    else
        echo "Please install jq manually: https://stedolan.github.io/jq/download/"
        exit 1
    fi
fi

# Create config directory
mkdir -p ~/.cfgpu

# Ask for API token
echo "Please enter your CFGPU API Token:"
echo "(You can get it from https://cfgpu.com)"
read -p "API Token: " api_token

if [ -n "$api_token" ]; then
    # Save token to file
    echo "$api_token" > ~/.cfgpu/token
    chmod 600 ~/.cfgpu/token
    echo "API token saved to ~/.cfgpu/token"
    
    # Add to bashrc/zshrc
    SHELL_RC=""
    if [ -f ~/.bashrc ]; then
        SHELL_RC=~/.bashrc
    elif [ -f ~/.zshrc ]; then
        SHELL_RC=~/.zshrc
    fi
    
    if [ -n "$SHELL_RC" ]; then
        if ! grep -q "CFGPU_API_TOKEN" "$SHELL_RC"; then
            echo "" >> "$SHELL_RC"
            echo "# CFGPU API Configuration" >> "$SHELL_RC"
            echo "export CFGPU_API_TOKEN=\"$api_token\"" >> "$SHELL_RC"
            echo "Added CFGPU_API_TOKEN to $SHELL_RC"
        fi
    fi
    
    # Test API connection
    echo ""
    echo "Testing API connection..."
    export CFGPU_API_TOKEN="$api_token"
    ./cfgpu-helper.sh list-regions 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ API connection successful!"
    else
        echo "❌ API connection failed. Please check your token."
    fi
else
    echo "No token provided. You can set it later with:"
    echo "  export CFGPU_API_TOKEN='your-token'"
    echo "  or"
    echo "  echo 'your-token' > ~/.cfgpu/token"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Usage examples:"
echo "  ./cfgpu-helper.sh list-regions"
echo "  ./cfgpu-helper.sh list-gpus"
echo "  ./cfgpu-helper.sh quick-create"
echo ""
echo "For more details, see the SKILL.md file."