#!/bin/bash

# Calibre OpenClaw Server - Run Script
# This script checks for .env file and installed dependencies before running the server

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Virtual environment path
VENV_DIR="$SCRIPT_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

echo "=========================================="
echo "Calibre OpenClaw Server - Startup Check"
echo "=========================================="
echo ""

# Check or create virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv "$VENV_DIR"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Virtual environment created at $VENV_DIR${NC}"
        # Upgrade pip to avoid PyPI JSON decode bug present in older pip versions
        echo "Upgrading pip in new virtual environment..."
        "$VENV_DIR/bin/python" -m pip install --upgrade pip --no-cache-dir 2>/dev/null
        if [ $? -ne 0 ]; then
            echo -e "${YELLOW}⚠ pip upgrade failed; continuing with the bundled pip${NC}"
        fi
        echo -e "${GREEN}✓ pip upgraded: $($VENV_DIR/bin/pip --version)${NC}"
    else
        echo -e "${RED}ERROR: Failed to create virtual environment${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Virtual environment found at $VENV_DIR${NC}"
    # Check and upgrade pip if needed
    pip_version=$($VENV_PIP --version | awk '{print $2}')
    pip_major=$(echo $pip_version | cut -d. -f1)
    if [ "$pip_major" -lt 25 ]; then
        echo -e "${YELLOW}pip version $pip_version is old, upgrading...${NC}"
        if "$VENV_PYTHON" -m pip install --upgrade pip --no-cache-dir; then
            echo -e "${GREEN}✓ pip upgraded: $($VENV_PIP --version)${NC}"
        else
            echo -e "${YELLOW}⚠ pip upgrade failed; continuing with $pip_version${NC}"
        fi
    else
        echo -e "${GREEN}✓ pip version $pip_version is up to date${NC}"
    fi
fi

# Check if .env exists in multiple locations
ENV_FILE=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CALL_DIR="$(pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# Check in order: script dir, call dir, parent dir
for dir in "$SCRIPT_DIR" "$CALL_DIR" "$PARENT_DIR"; do
    if [ -f "$dir/.env" ]; then
        ENV_FILE="$dir/.env"
        echo -e "${GREEN}✓ .env file found at $ENV_FILE${NC}"
        break
    fi
done

if [ -z "$ENV_FILE" ]; then
    echo -e "${RED}ERROR: .env file not found!${NC}"
    echo "Searched in:"
    echo "  - $SCRIPT_DIR/.env"
    echo "  - $CALL_DIR/.env"
    echo "  - $PARENT_DIR/.env"
    echo ""
    echo "Please create a .env file in one of these locations or specify the path:"
    echo "  cp .env.example /path/to/.env"
    echo "  Then edit it with your configuration."
    echo ""
    read -p "Enter the full path to your .env file (or press Enter to exit): " CUSTOM_ENV
    if [ -n "$CUSTOM_ENV" ] && [ -f "$CUSTOM_ENV" ]; then
        ENV_FILE="$CUSTOM_ENV"
        echo -e "${GREEN}✓ Using .env file at $ENV_FILE${NC}"
    else
        exit 1
    fi
fi

# Export the directory containing .env for the app to find it
export ENV_DIR="$(dirname "$ENV_FILE")"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}ERROR: requirements.txt not found!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ requirements.txt found${NC}"

# Check if virtual environment Python is available
if [ ! -f "$VENV_PYTHON" ]; then
    echo -e "${RED}ERROR: Virtual environment Python not found at $VENV_PYTHON${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment Python found: $($VENV_PYTHON --version)${NC}"

# Check if virtual environment pip is available
if [ ! -f "$VENV_PIP" ]; then
    echo -e "${RED}ERROR: Virtual environment pip not found at $VENV_PIP${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment pip found${NC}"

# Function to check if a package is installed in venv
check_package() {
    local package=$1
    if $VENV_PYTHON -c "import $package" 2>/dev/null; then
        echo -e "${GREEN}✓ $package is installed${NC}"
        return 0
    else
        echo -e "${YELLOW}✗ $package is NOT installed${NC}"
        return 1
    fi
}

# Check critical packages
echo ""
echo "Checking required packages..."
echo "----------------------------"

missing_packages=0

# List of packages to check (import names, not pip names)
declare -a packages=(
    "fastapi"
    "uvicorn"
    "pydantic"
    "psycopg2"
    "fitz"
    "httpx"
)

for package in "${packages[@]}"; do
    if ! check_package "$package"; then
        missing_packages=$((missing_packages + 1))
    fi
done

# If packages are missing, offer to install
if [ $missing_packages -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}WARNING: $missing_packages required package(s) are missing${NC}"
    echo ""
    read -p "Do you want to install missing packages now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Installing packages from requirements.txt in virtual environment..."
        $VENV_PIP install -r requirements.txt
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Packages installed successfully${NC}"
        else
            echo -e "${RED}ERROR: Failed to install packages${NC}"
            exit 1
        fi
    else
        echo -e "${RED}ERROR: Cannot start server without required packages${NC}"
        echo "Please install them manually:"
        echo "  $VENV_PIP install -r requirements.txt"
        exit 1
    fi
else
    echo -e "${GREEN}✓ All required packages are installed${NC}"
fi

# Check if Ollama is running
echo ""
echo "Checking Ollama..."
echo "-------------------"

if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓ Ollama is installed${NC}"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Ollama is running${NC}"
        
        # Check if model is available
        if curl -s http://localhost:11434/api/tags | grep -q "nomic-embed-text-v2-moe"; then
            echo -e "${GREEN}✓ nomic-embed-text-v2-moe model is available${NC}"
        else
            echo -e "${YELLOW}⚠ nomic-embed-text-v2-moe model is not downloaded${NC}"
            echo "  You can download it with: ollama pull nomic-embed-text-v2-moe:latest"
        fi
    else
        echo -e "${YELLOW}⚠ Ollama is not running${NC}"
        echo "  Start it with: ollama serve"
    fi
else
    echo -e "${YELLOW}⚠ Ollama is not installed${NC}"
    echo "  Install it from: https://ollama.ai"
fi

# Check if PostgreSQL is accessible
echo ""
echo "Checking PostgreSQL..."
echo "----------------------"

PGUSER="$(env_value POSTGRESQL_DB_USER)"
PGPASSWORD="$(env_value POSTGRESQL_DB_PASSWD)"
PGDATABASE="$(env_value POSTGRESQL_DB_DATABASE)"
PGHOST="$(env_value POSTGRESQL_DB_HOST)"
PGHOST="${PGHOST:-localhost}"
PGPORT="$(env_value POSTGRESQL_DB_PORT)"
PGPORT="${PGPORT:-5432}"

if [ -z "$PGUSER" ] || [ -z "$PGDATABASE" ]; then
    echo -e "${YELLOW}⚠ POSTGRESQL_DB_USER and POSTGRESQL_DB_DATABASE must be configured in .env${NC}"
elif PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c "SELECT 1" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PostgreSQL is accessible${NC}"
else
    echo -e "${YELLOW}⚠ PostgreSQL is not accessible${NC}"
    echo "  Make sure PostgreSQL is running and credentials are correct in .env"
fi

# Check if Calibre metadata.db exists
echo ""
echo "Checking Calibre database..."
echo "----------------------------"

if [ -f "/mnt/Backup_2/Biblioteca/metadata.db" ]; then
    echo -e "${GREEN}✓ Calibre metadata.db found${NC}"
else
    echo -e "${RED}ERROR: Calibre metadata.db not found at /mnt/Backup_2/Biblioteca/metadata.db${NC}"
    echo "  Please check the CALIBRE_DB_PATH in .env"
    exit 1
fi

# All checks passed
echo ""
echo -e "${GREEN}=========================================="
echo "All checks passed! Starting server..."
echo "==========================================${NC}"
echo ""

# Start the server using virtual environment. Use exec so SIGINT/SIGTERM reach
# Uvicorn directly and its lifespan shutdown handlers can complete.
exec "$VENV_PYTHON" -m app.main
