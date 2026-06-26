#!/bin/bash

# EkyBot Workspace Registration Script
# Registers OpenClaw workspace with EkyBot platform

set -e

CONFIG_DIR="$HOME/.openclaw/ekybot-connector"
CONFIG_FILE="$CONFIG_DIR/config.json"
EKYBOT_API_BASE="https://www.ekybot.com/api"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

print_status "🔌 EkyBot Workspace Registration"
echo

# Check if already configured
if [[ -f "$CONFIG_FILE" ]]; then
    print_warning "Configuration already exists at $CONFIG_FILE"
    read -p "Do you want to re-register? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Registration cancelled."
        exit 0
    fi
fi

# Gather workspace information
print_status "Gathering workspace information..."

# Get OpenClaw gateway info
if ! command -v openclaw &> /dev/null; then
    print_error "OpenClaw CLI not found. Please ensure OpenClaw is installed and in PATH."
    exit 1
fi

# Get workspace name (user input)
read -p "Workspace name: " WORKSPACE_NAME
if [[ -z "$WORKSPACE_NAME" ]]; then
    print_error "Workspace name is required."
    exit 1
fi

# Get user email for registration
read -p "Email address: " USER_EMAIL
if [[ -z "$USER_EMAIL" ]]; then
    print_error "Email address is required."
    exit 1
fi

# Get gateway URL (default to common endpoint)
read -p "Gateway URL (default: https://gateway.ekybot.com): " GATEWAY_URL
GATEWAY_URL=${GATEWAY_URL:-"https://gateway.ekybot.com"}

# Prepare registration payload
REGISTRATION_DATA=$(cat <<EOF
{
  "name": "$WORKSPACE_NAME",
  "email": "$USER_EMAIL",
  "type": "openclaw",
  "gatewayUrl": "$GATEWAY_URL",
  "metadata": {
    "platform": "$(uname -s)",
    "registered_at": "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)"
  }
}
EOF
)

print_status "Registering workspace with EkyBot..."

# Make registration request
RESPONSE=$(curl -s -X POST "$EKYBOT_API_BASE/workspaces/register" \
  -H "Content-Type: application/json" \
  -d "$REGISTRATION_DATA")

# Check if registration was successful
if [[ $? -ne 0 ]]; then
    print_error "Failed to connect to EkyBot API"
    exit 1
fi

# Parse response
WORKSPACE_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('workspaceId', ''))" 2>/dev/null)
API_KEY=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('apiKey', ''))" 2>/dev/null)
SUCCESS=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(str(data.get('success', False)).lower())" 2>/dev/null)

if [[ "$SUCCESS" != "true" ]] || [[ -z "$WORKSPACE_ID" ]] || [[ -z "$API_KEY" ]]; then
    print_error "Registration failed. Server response:"
    echo "$RESPONSE"
    exit 1
fi

# Create configuration file
CONFIG_DATA=$(cat <<EOF
{
  "workspace_id": "$WORKSPACE_ID",
  "api_key": "$API_KEY",
  "workspace_name": "$WORKSPACE_NAME",
  "user_email": "$USER_EMAIL",
  "telemetry_interval": 300,
  "endpoints": {
    "base_url": "$EKYBOT_API_BASE",
    "health": "$EKYBOT_API_BASE/workspaces/$WORKSPACE_ID/health",
    "telemetry": "$EKYBOT_API_BASE/workspaces/$WORKSPACE_ID/telemetry"
  },
  "registered_at": "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)"
}
EOF
)

echo "$CONFIG_DATA" > "$CONFIG_FILE"
chmod 600 "$CONFIG_FILE"  # Protect API key

print_status "✅ Registration successful!"
echo
echo "Workspace ID: $WORKSPACE_ID"
echo "API Key: ${API_KEY:0:12}..."
echo "Configuration saved to: $CONFIG_FILE"
echo
print_status "Next steps:"
echo "  1. Test connection: scripts/health_check.sh"
echo "  2. Start telemetry: runtime/src/telemetry.js (via Node.js)"