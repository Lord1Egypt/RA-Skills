#!/bin/bash
# Check and install dashboard dependencies if needed

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
  echo "[Dashboard] Dependencies not found. Installing..."
  
  # Check if npm is available
  if ! command -v npm &> /dev/null; then
    echo "[Error] npm not found. Please install Node.js first."
    echo "Visit: https://nodejs.org/"
    exit 1
  fi
  
  # Install dependencies
  npm install
  
  if [ $? -eq 0 ]; then
    echo "[Dashboard] Dependencies installed successfully!"
  else
    echo "[Error] Failed to install dependencies."
    exit 1
  fi
else
  echo "[Dashboard] Dependencies already installed."
fi
