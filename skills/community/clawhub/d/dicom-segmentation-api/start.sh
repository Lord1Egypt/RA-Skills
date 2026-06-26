#!/bin/bash
# DICOM Segmentation API - Quick Start

set -e

PORT="${1:-8000}"
HOST="${2:-0.0.0.0}"

echo "🚀 Starting DICOM Segmentation API..."
echo "📦 Port: $PORT"
echo "🌐 Host: $HOST"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Check dependencies
echo "📋 Checking dependencies..."
python3 -c "import fastapi, torch, monai" 2>/dev/null || {
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
}

# Create output directory
mkdir -p output

# Start server
echo "🚀 Starting server..."
python3 api_server.py --host $HOST --port $PORT
