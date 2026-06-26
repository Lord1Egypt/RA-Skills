#!/bin/bash
#
# BaiduOCR-LocalFallback one-click installation script
#
set -e

echo "=========================================="
echo "BaiduOCR-LocalFallback - Setup Script"
echo "=========================================="

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Linux"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        echo "Windows"
    else
        echo "Unknown"
    fi
}

OS=$(detect_os)
echo "Detected OS: $OS"

# Check Python
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        echo "✓ Python 3 installed: $PYTHON_VERSION"
        return 0
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
        echo "✓ Python installed: $PYTHON_VERSION"
        return 0
    else
        echo "✗ Python not found. Please install Python 3.8+ first."
        return 1
    fi
}

# Install dependencies
install_dependencies() {
    echo ""
    echo "Installing Python dependencies..."
    
    if pip3 show requests &> /dev/null; then
        echo "  requests already installed, skipping"
    else
        pip3 install requests
    fi
    
    if pip3 show easyocr &> /dev/null; then
        echo "  easyocr already installed, skipping"
    else
        pip3 install easyocr
    fi
    
    if pip3 show Pillow &> /dev/null; then
        echo "  Pillow already installed, skipping"
    else
        pip3 install Pillow
    fi
    
    echo "✓ Dependencies installed"
}

# Create config directory
setup_config_dir() {
    echo ""
    echo "Creating config directory..."
    
    CONFIG_DIR="$HOME/.openclaw/skills/BaiduOCR-LocalFallback"
    mkdir -p "$CONFIG_DIR/cache"
    mkdir -p "$CONFIG_DIR/config"
    
    echo "✓ Config directory: $CONFIG_DIR"
}

# Configure API keys
configure_api_keys() {
    echo ""
    echo "=========================================="
    echo "API Key Configuration"
    echo "=========================================="
    echo ""
    echo "Get your API keys from Baidu Cloud Console:"
    echo "  https://console.bce.baidu.com/"
    echo "  Search 'OCR' -> Create App -> Get AK/SK"
    echo ""
    
    read -p "Enter API Key (press Enter to skip, configure later manually): " API_KEY
    
    if [ -z "$API_KEY" ]; then
        echo "Skipped. Run the following to configure later:"
        echo "  python3 scripts/ocr.py --configure"
        return
    fi
    
    read -p "Enter Secret Key: " SECRET_KEY
    
    if [ -z "$SECRET_KEY" ]; then
        echo "Secret Key cannot be empty"
        exit 1
    fi
    
    CONFIG_FILE="$HOME/.openclaw/skills/BaiduOCR-LocalFallback/config.json"
    cat > "$CONFIG_FILE" << EOF
{
  "api_key": "$API_KEY",
  "secret_key": "$SECRET_KEY"
}
EOF
    
    # Recommend restricting file permissions
    chmod 600 "$CONFIG_FILE" 2>/dev/null || true
    
    echo "✓ API keys saved to: $CONFIG_FILE"
    echo "  (File permissions set to 600 — recommended)"
}

# Test connection
test_connection() {
    echo ""
    echo "Testing API connection..."
    
    CONFIG_FILE="$HOME/.openclaw/skills/BaiduOCR-LocalFallback/config.json"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "⚠ Config file not found, skipping connection test"
        return
    fi
    
    if command -v curl &> /dev/null; then
        API_KEY=$(grep -o '"api_key"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
        SECRET_KEY=$(grep -o '"secret_key"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
        
        if [ -n "$API_KEY" ] && [ -n "$SECRET_KEY" ]; then
            echo "Fetching access_token..."
            RESPONSE=$(curl -s -X POST "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=${API_KEY}&client_secret=${SECRET_KEY}")
            
            if echo "$RESPONSE" | grep -q "access_token"; then
                echo "✓ API connection successful!"
            else
                echo "✗ API connection failed. Please verify your API keys."
                echo "  Response: $RESPONSE"
            fi
        fi
    fi
}

# Main installation flow
main() {
    echo ""
    echo "Starting installation..."
    echo ""
    
    check_python || exit 1
    install_dependencies
    setup_config_dir
    configure_api_keys
    test_connection
    
    echo ""
    echo "=========================================="
    echo "Installation complete!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "  1. Test: python3 scripts/ocr.py --test-connection"
    echo "  2. List APIs: python3 scripts/ocr.py --show-apis"
    echo "  3. Start: python3 scripts/ocr.py --image /path/to/image.jpg"
    echo ""
    echo "Docs: https://github.com/xx235300/BaiduOCR-LocalFallback#readme"
    echo ""
}

main "$@"
