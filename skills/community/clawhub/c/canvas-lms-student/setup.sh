#!/bin/bash
# Setup script for canvas-lms-student skill
# This script installs Python dependencies and checks configuration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="canvas-lms-student"

echo "=========================================="
echo "Setting up $SKILL_NAME skill"
echo "=========================================="

# Check Python version
echo ""
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Found Python $PYTHON_VERSION"
else
    echo "✗ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Install pip dependencies
echo ""
echo "Installing Python dependencies..."
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    pip3 install -q -r "$SCRIPT_DIR/requirements.txt" && echo "✓ Dependencies installed"
else
    echo "⚠ No requirements.txt found, skipping pip install"
fi

# Check configuration
echo ""
echo "Checking Canvas LMS configuration..."

CONFIG_FILE="$HOME/.config/canvas-lms/config.json"
if [ -n "$CANVAS_API_TOKEN" ] && [ -n "$CANVAS_BASE_URL" ]; then
    echo "✓ Configuration found in environment variables"
elif [ -f "$CONFIG_FILE" ]; then
    echo "✓ Configuration found in $CONFIG_FILE"
else
    echo "⚠ Canvas LMS not configured yet"
    echo ""
    echo "Please configure using one of these methods:"
    echo ""
    echo "Method 1: Environment Variables"
    echo '  export CANVAS_BASE_URL="https://your-school.instructure.com"'
    echo '  export CANVAS_API_TOKEN="your-api-token"'
    echo ""
    echo "Method 2: Config File"
    echo "  mkdir -p ~/.config/canvas-lms"
    echo '  echo '\''{"base_url": "https://...", "api_token": "..."}'\'' > ~/.config/canvas-lms/config.json'
    echo ""
    echo "Get your API token from: Canvas → Account → Settings → Approved Integrations"
fi

# Test connection if configured
echo ""
if [ -n "$CANVAS_API_TOKEN" ] || [ -f "$CONFIG_FILE" ]; then
    echo "Testing Canvas connection..."
    if python3 "$SCRIPT_DIR/scripts/canvas_client.py" --test 2>/dev/null; then
        echo "✓ Canvas connection successful"
    else
        echo "✗ Canvas connection failed. Please check your configuration."
    fi
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Available tools:"
echo "  - list_courses: List your Canvas courses"
echo "  - get_assignments: Get course assignments"
echo "  - get_assignment_detail: Get assignment details"
echo "  - search_canvas: Search across courses"
echo "  - download_files: Download course files"
echo "  - export_calendar: Export deadlines to calendar"
echo ""
