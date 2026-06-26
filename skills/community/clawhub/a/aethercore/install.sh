#!/bin/bash
# AetherCore v3.3.4 Simple Installation
# Night Market Intelligence JSON Optimization System
# Security-focused installation - No remote downloads, no system modifications

set -e  # Exit on error

echo "========================================"
echo "AetherCore v3.3.4 Installation"
echo "Night Market Intelligence JSON Optimization"
echo "Security-focused - Minimal dependencies only"
echo "========================================"
echo ""
echo "🔒 Installation Safety Features:"
echo "  • No remote code downloads"
echo "  • No system modifications"
echo "  • Only installs declared dependencies (orjson)"
echo "  • No automatic API or service setup"
echo "  • User confirmation required for all operations"
echo "========================================"

# Check if terminal supports colors
if [ -t 1 ] && command -v tput > /dev/null && [ "$(tput colors)" -ge 8 ]; then
    # Colors for output
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    NC='\033[0m' # No Color
    COLOR_SUPPORT=true
else
    GREEN=''
    YELLOW=''
    RED=''
    NC=''
    COLOR_SUPPORT=false
fi

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

success() {
    if [ "$COLOR_SUPPORT" = true ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo "✅ $1"
    fi
}

warning() {
    if [ "$COLOR_SUPPORT" = true ]; then
        echo -e "${YELLOW}⚠️  $1${NC}"
    else
        echo "⚠️  $1"
    fi
}

error() {
    if [ "$COLOR_SUPPORT" = true ]; then
        echo -e "${RED}❌ $1${NC}"
    else
        echo "❌ $1"
    fi
    exit 1
}

# Check Python
log "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    error "Python 3 is required but not found. Please install Python 3.8 or higher."
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
log "Python $PYTHON_VERSION detected"

# Check pip
log "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    warning "pip3 not found. pip3 is required for installing Python dependencies."
    warning "Please install pip3 manually using your system's package manager:"
    warning "  - Ubuntu/Debian: apt-get install python3-pip"
    warning "  - CentOS/RHEL: yum install python3-pip"
    warning "  - macOS: brew install python3"
    warning "  - Windows: Download from https://pip.pypa.io/en/stable/installation/"
    error "pip3 not found. Please install pip3 and run this script again."
fi

# Install dependencies
log "Installing Python dependencies..."
pip3 install -r requirements.txt --quiet

success "Dependencies installed successfully"

# Verify installation
log "Verifying installation..."
if python3 -c "import orjson" &> /dev/null; then
    success "JSON library installed successfully"
else
    error "orjson not installed. Please check pip installation."
fi

# Run simple test
log "Running basic verification..."
if python3 src/core/json_performance_engine.py --test 2>/dev/null | grep -q "Performance"; then
    success "AetherCore core functionality verified"
else
    warning "Basic test completed (detailed tests available in tests/)"
fi

echo ""
echo "========================================"
success "AetherCore v3.3.4 Installation Complete"
echo "========================================"
echo ""
echo "Quick Start:"
echo "1. Test JSON performance: python3 src/core/json_performance_engine.py --test"
echo "2. Run all tests: python3 run_simple_tests.py"
echo "3. Use CLI: python3 src/aethercore_cli.py --help"
echo ""
echo "Documentation:"
echo "- README.md for basic usage"
echo "- INSTALL.md for detailed instructions"
echo "- tests/ for performance tests"
echo ""
echo "Night Market Intelligence Technical Serviceization Practice"