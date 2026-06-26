#!/bin/bash
# Corkboard Dashboard - OpenClaw Skill Installer
# Installs the dashboard, builds it, starts it with PM2, and registers the skill.
#
# Environment:
#   CORKBOARD_DIR        - Where to clone/find the dashboard (default: ~/.openclaw/dashboard)
#   OPENCLAW_WORKSPACE   - OpenClaw workspace path (default: ~/.openclaw/workspace)
#   CORKBOARD_REPO       - Git repo URL (default: https://github.com/Grooves-n-Grain/carls-corkie.git)
#   CORKBOARD_PORT       - Server port (default: 3010)
#   CORKBOARD_HOST       - Server bind host (default: 0.0.0.0)

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()   { echo -e "${GREEN}[corkboard]${NC} $*"; }
warn()  { echo -e "${YELLOW}[corkboard]${NC} $*"; }
error() { echo -e "${RED}[corkboard]${NC} $*" >&2; }

# --- Configuration ---
INSTALL_DIR="${CORKBOARD_DIR:-$HOME/.openclaw/dashboard}"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
REPO_URL="${CORKBOARD_REPO:-https://github.com/Grooves-n-Grain/carls-corkie.git}"
PORT="${CORKBOARD_PORT:-3010}"
HOST="${CORKBOARD_HOST:-0.0.0.0}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# --- Prerequisites ---
log "Checking prerequisites..."

check_cmd() {
    if ! command -v "$1" &>/dev/null; then
        error "$1 is required but not found. $2"
        return 1
    fi
}

MISSING=0
check_cmd node "Install from https://nodejs.org/" || MISSING=1
check_cmd npm  "Comes with Node.js" || MISSING=1
check_cmd jq   "Install: apt install jq / brew install jq" || MISSING=1
check_cmd curl "Install: apt install curl / brew install curl" || MISSING=1
check_cmd git  "Install: apt install git / brew install git" || MISSING=1

if [[ $MISSING -eq 1 ]]; then
    error "Missing required tools. Install them and re-run."
    exit 1
fi

# Check Node.js version (need 20+)
NODE_VERSION=$(node -v | sed 's/v//' | cut -d. -f1)
if [[ "$NODE_VERSION" -lt 20 ]]; then
    error "Node.js 20+ required (found v$(node -v))"
    exit 1
fi

# PM2 is optional
HAS_PM2=0
if command -v pm2 &>/dev/null; then
    HAS_PM2=1
    log "PM2 found - will use for process management"
else
    warn "PM2 not found - will provide manual start instructions"
    warn "Install PM2: npm install -g pm2"
fi

# --- Clone or locate ---
if [[ -d "$INSTALL_DIR" ]]; then
    log "Dashboard found at $INSTALL_DIR"
    if [[ -d "$INSTALL_DIR/.git" ]]; then
        log "Pulling latest changes..."
        cd "$INSTALL_DIR" && git pull --ff-only 2>/dev/null || warn "Could not pull (may have local changes)"
    fi
else
    log "Cloning dashboard to $INSTALL_DIR..."
    mkdir -p "$(dirname "$INSTALL_DIR")"
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# --- Install dependencies ---
log "Installing dependencies..."
npm install

# --- Environment ---
if [[ ! -f .env ]]; then
    if [[ -f .env.example ]]; then
        log "Creating .env from .env.example..."
        cp .env.example .env
        # Set port
        sed -i "s/^PORT=.*/PORT=$PORT/" .env 2>/dev/null || true
        if grep -q '^CORKBOARD_HOST=' .env; then
            sed -i "s/^CORKBOARD_HOST=.*/CORKBOARD_HOST=$HOST/" .env 2>/dev/null || true
        else
            printf '\nCORKBOARD_HOST=%s\n' "$HOST" >> .env
        fi
    else
        log "Creating minimal .env..."
        cat > .env << EOF
PORT=$PORT
CORKBOARD_HOST=$HOST
CORS_ORIGINS=http://localhost:5180,http://127.0.0.1:5180
EOF
    fi
else
    log ".env already exists, keeping current configuration"
fi

# --- Build ---
log "Building project..."
npm run build

# --- Start ---
if [[ $HAS_PM2 -eq 1 ]]; then
    log "Starting with PM2..."
    # Stop existing instances if running
    pm2 delete corkie-server 2>/dev/null || true
    pm2 delete corkie-client 2>/dev/null || true
    npm run pm2:start
else
    warn "No PM2 - start manually with:"
    warn "  cd $INSTALL_DIR && npm run dev"
    warn ""
    warn "Or install PM2 and run:"
    warn "  npm install -g pm2"
    warn "  cd $INSTALL_DIR && npm run pm2:start"
fi

# --- Health check ---
log "Checking if server is responding..."
HEALTHY=0
HEALTH_TOKEN=""
if [[ -f "$INSTALL_DIR/.env" ]]; then
    HEALTH_TOKEN=$(grep -E '^CORKBOARD_TOKEN=' "$INSTALL_DIR/.env" | tail -n1 | cut -d= -f2- | tr -d '"' | tr -d "'" | xargs || true)
fi
for i in 1 2 3 4 5; do
    if curl -sf -H "Authorization: Bearer $HEALTH_TOKEN" "http://localhost:$PORT/api/pins" >/dev/null 2>&1; then
        HEALTHY=1
        break
    fi
    sleep 2
done

if [[ $HEALTHY -eq 1 ]]; then
    log "Server is healthy at http://localhost:$PORT"
else
    if [[ $HAS_PM2 -eq 1 ]]; then
        warn "Server not responding yet. Check logs: pm2 logs corkie-server"
    else
        warn "Server not responding. Start it manually and verify."
    fi
fi

# --- Register skill ---
SKILL_DEST="$WORKSPACE/skills/corkboard-dashboard"
if [[ -d "$WORKSPACE/skills" ]]; then
    log "Registering skill in workspace..."
    if [[ -d "$SKILL_DEST" ]]; then
        warn "Existing skill found at $SKILL_DEST - backing up to ${SKILL_DEST}.bak"
        rm -rf "${SKILL_DEST}.bak"
        mv "$SKILL_DEST" "${SKILL_DEST}.bak"
    fi
    cp -r "$SKILL_DIR" "$SKILL_DEST"
    log "Skill registered at $SKILL_DEST"
else
    warn "Workspace skills directory not found at $WORKSPACE/skills"
    warn "Create it or set OPENCLAW_WORKSPACE and re-run"
fi

# --- Done ---
echo ""
log "Installation complete!"
echo ""
echo "  Dashboard:  http://localhost:5180"
echo "  API:        http://localhost:$PORT"
echo "  LAN API:    http://<your-lan-ip>:$PORT"
echo "  Skill:      $SKILL_DEST"
echo ""
echo "  Add to your environment:"
echo "    export CORKBOARD_API=\"http://localhost:$PORT\""
if [[ -n "$HEALTH_TOKEN" ]]; then
    echo "    export CORKBOARD_TOKEN=\"$HEALTH_TOKEN\""
fi
echo ""
echo "  Or run the corkboard CLI from $INSTALL_DIR (it auto-loads the token from .env)."
echo ""
echo "  Test it:"
echo "    corkboard add task \"Hello from install\" \"Setup complete\" 2"
echo ""
