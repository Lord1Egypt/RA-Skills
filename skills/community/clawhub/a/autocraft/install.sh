#!/bin/bash

# AutoCraft One-Click Installation Script
# Automatically downloads complete system, installs dependencies, and starts services

set -e

echo "=========================================="
echo "  AutoCraft One-Click Installation"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check required tools
echo -e "${BLUE}[1/5] Checking system environment...${NC}"
command -v git >/dev/null 2>&1 || { echo "Error: git is required"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Error: python3 is required"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "Error: npm is required"; exit 1; }
echo -e "${GREEN}✓ Environment check passed${NC}"
echo ""

# Download complete system code
echo -e "${BLUE}[2/5] Downloading AutoCraft complete system...${NC}"
if [ ! -d "autocraft-opensource" ]; then
    echo "Downloading from GitHub..."
    git clone https://github.com/Robin-Chen2025/autocraft-opensource.git || {
        echo "GitHub download failed, trying Gitee..."
        git clone https://gitee.com/Robin-Chen2025/autocraft-opensource.git
    }
else
    echo "autocraft-opensource directory already exists, skipping download"
fi
cd autocraft-opensource
echo -e "${GREEN}✓ Code download complete${NC}"
echo ""

# Install backend dependencies
echo -e "${BLUE}[3/5] Installing backend dependencies (Python + FastAPI)...${NC}"
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..
echo -e "${GREEN}✓ Backend dependencies installed${NC}"
echo ""

# Install frontend dependencies
echo -e "${BLUE}[4/5] Installing frontend dependencies (Node.js + Vue3)...${NC}"
npm install
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
echo ""

# Start services
echo -e "${BLUE}[5/5] Starting AutoCraft services...${NC}"
echo ""

# Start backend
echo "Starting backend service (port 9001)..."
cd backend
source venv/bin/activate
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 9001 > /tmp/autocraft_backend.log 2>&1 &
BACKEND_PID=$!
deactivate
cd ..
echo -e "${GREEN}✓ Backend service started (PID: $BACKEND_PID)${NC}"

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting frontend service (port 8080)..."
nohup npm run dev > /tmp/autocraft_frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend service started (PID: $FRONTEND_PID)${NC}"

# Wait for frontend to start
sleep 5

echo ""
echo "=========================================="
echo -e "${GREEN}  ✓ AutoCraft installed and started!${NC}"
echo "=========================================="
echo ""
echo "Access URLs:"
echo "  🌐 Frontend UI: http://localhost:8080"
echo "  📚 API Docs:    http://localhost:9001/docs"
echo ""
echo "Service Processes:"
echo "  Backend PID:  $BACKEND_PID"
echo "  Frontend PID: $FRONTEND_PID"
echo ""
echo "Log Files:"
echo "  Backend log:  /tmp/autocraft_backend.log"
echo "  Frontend log: /tmp/autocraft_frontend.log"
echo ""
echo "Stop Services:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Documentation:"
echo "  README.md - Project overview"
echo "  DEPLOYMENT.md - Deployment guide"
echo "  docs/OPERATION_MANUAL.md - Operation manual"
echo ""
