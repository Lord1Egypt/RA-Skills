#!/usr/bin/env bash
# AVENGER INITIATIVE — Restore Script v3.1
# ============================================================
# AVENGER INITIATIVE — Restore Script v2
# Restores from any branch (daily/weekly/monthly/main)
# Usage: restore.sh [--vault /path] [--branch backup/daily/YYYY-MM-DD]
# ============================================================
set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}"
KEY_FILE="$OPENCLAW_DIR/credentials/avenger.key"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace"
VAULT_DIR=""
BRANCH="main"
CLEANUP_VAULT=false

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log()  { echo -e "${GREEN}[AVENGER]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; exit 1; }

while [[ $# -gt 0 ]]; do
    case "$1" in
        --vault)  VAULT_DIR="$2"; shift 2 ;;
        --branch) BRANCH="$2"; shift 2 ;;
        *) fail "Unknown argument: $1" ;;
    esac
done

echo ""
echo "🛡️  AVENGER INITIATIVE — RESTORE"
echo "================================="

# ---- Preflight --------------------------------------------
[ -f "$KEY_FILE" ] || fail "Encryption key not found at $KEY_FILE"
AVENGER_KEY=$(cat "$KEY_FILE")
[ -n "$AVENGER_KEY" ] || fail "Encryption key is empty"
command -v openssl >/dev/null 2>&1 || fail "openssl not installed"
command -v git >/dev/null 2>&1 || fail "git not installed"

# ---- Clone if not provided --------------------------------
if [ -z "$VAULT_DIR" ] || [ ! -d "$VAULT_DIR" ]; then
    CONFIG_FILE="$OPENCLAW_DIR/credentials/avenger-config.json"
    [ -f "$CONFIG_FILE" ] || fail "No vault configured. Run setup.sh first."
    VAULT_REPO=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['vault_repo'])")
    VAULT_DIR="/tmp/avenger-restore-$$"
    log "Cloning vault from $VAULT_REPO..."
    gh repo clone "$VAULT_REPO" "$VAULT_DIR" -- --quiet
    CLEANUP_VAULT=true
fi

cd "$VAULT_DIR"

# ---- Show available branches if user wants to choose ------
if [ "$BRANCH" = "list" ]; then
    echo ""
    echo "Available backup branches:"
    git branch -r | grep 'backup/' | sed 's|origin/||' | sort -r | head -30
    echo ""
    echo -e "${BLUE}[?]${NC} Enter branch name (or 'main' for latest): "
    read -r BRANCH
fi

# ---- Checkout branch --------------------------------------
log "Checking out branch: $BRANCH"
git checkout "$BRANCH" --quiet 2>/dev/null || \
    git checkout "origin/$BRANCH" --quiet 2>/dev/null || \
    fail "Branch not found: $BRANCH"

# ---- Show manifest ----------------------------------------
[ -f "AVENGER-MANIFEST.md" ] && echo "" && cat "AVENGER-MANIFEST.md" && echo ""

# ---- Confirm ----------------------------------------------
echo -e "${BLUE}[?]${NC} Overwrite current OpenClaw files with this snapshot? [y/N] "
read -r confirm
[[ "$confirm" =~ ^[Yy]$ ]] || { log "Aborted."; exit 0; }

# ---- Safety backup ----------------------------------------
TS=$(date +%Y%m%d%H%M%S)
[ -f "$OPENCLAW_DIR/openclaw.json" ] && \
    cp "$OPENCLAW_DIR/openclaw.json" "$OPENCLAW_DIR/openclaw.json.pre-restore-$TS" && \
    log "Safety copy saved: openclaw.json.pre-restore-$TS"

# ---- Decrypt openclaw.json --------------------------------
if [ -f "config/openclaw.json.enc" ]; then
    log "Decrypting openclaw.json..."
    openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 \
        -pass "pass:$AVENGER_KEY" \
        -in "config/openclaw.json.enc" \
        -out "$OPENCLAW_DIR/openclaw.json" || fail "Decryption failed — wrong key?"
    log "  ✓ openclaw.json"
fi

# ---- Cron jobs --------------------------------------------
if [ -f "config/cron-jobs.json" ]; then
    mkdir -p "$OPENCLAW_DIR/cron"
    cp "config/cron-jobs.json" "$OPENCLAW_DIR/cron/jobs.json"
    log "  ✓ cron jobs"
fi

# ---- Workspace files --------------------------------------
mkdir -p "$WORKSPACE_DIR/memory"
for f in workspace/*.md; do [ -f "$f" ] && cp "$f" "$WORKSPACE_DIR/$(basename $f)" || true; done
for mf in workspace/memory/*.md; do [ -f "$mf" ] && cp "$mf" "$WORKSPACE_DIR/memory/$(basename $mf)" || true; done
log "  ✓ workspace + memory logs"

# ---- Agent workspaces -------------------------------------
for agent_dir in agents/*/; do
    [ -d "$agent_dir" ] || continue
    agent_name=$(basename "$agent_dir")
    [ "$agent_name" = "main" ] && continue
    ws="$OPENCLAW_DIR/workspace-$agent_name"
    mkdir -p "$ws"
    for f in "$agent_dir"*.md; do [ -f "$f" ] && cp "$f" "$ws/$(basename $f)" || true; done
    log "  ✓ agent:$agent_name"
done

# ---- Custom skills ----------------------------------------
if [ -d "skills" ] && [ "$(ls -A skills 2>/dev/null)" ]; then
    mkdir -p "$WORKSPACE_DIR/skills"
    for skill_dir in skills/*/; do
        skill_name=$(basename "$skill_dir")
        mkdir -p "$WORKSPACE_DIR/skills/$skill_name"
        cp -r "$skill_dir"* "$WORKSPACE_DIR/skills/$skill_name/" 2>/dev/null || true
    done
    log "  ✓ skills"
fi

# ---- Cleanup ----------------------------------------------
$CLEANUP_VAULT && rm -rf "$VAULT_DIR"

echo ""
log "✅ Restore complete from branch: $BRANCH"
echo ""
echo "  Run: openclaw gateway restart"
echo ""
