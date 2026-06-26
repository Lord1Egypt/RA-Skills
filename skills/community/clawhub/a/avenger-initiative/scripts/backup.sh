#!/usr/bin/env bash
# ============================================================
# AVENGER INITIATIVE — Backup Script v3.1
#
# Branch strategy:
#   main                      → ALWAYS has the latest backup
#   backup/daily/YYYY-MM-DD   → daily snapshot (keep 7)
#   backup/weekly/YYYY-WNN    → weekly snapshot on Sundays (keep 8)
#   backup/monthly/YYYY-MM    → monthly snapshot on 1st (keep 12)
#
# Flow: commit to main → tag as dated branch → prune old branches
#
# Usage: backup.sh ["optional commit message"]
# ============================================================
set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}"
CONFIG_FILE="$OPENCLAW_DIR/credentials/avenger-config.json"
KEY_FILE="$OPENCLAW_DIR/credentials/avenger.key"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace"
LOG_FILE="$WORKSPACE_DIR/memory/avenger-backup.log"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log()  { echo -e "${GREEN}[AVENGER]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; exit 1; }

# ---- Preflight --------------------------------------------
[ -f "$KEY_FILE" ]    || fail "Not configured. Run: bash setup.sh --repo <github-url>"
[ -f "$CONFIG_FILE" ] || fail "Config missing. Run setup.sh first."
AVENGER_KEY=$(cat "$KEY_FILE")
[ -n "$AVENGER_KEY" ] || fail "Encryption key is empty"
command -v git     >/dev/null 2>&1 || fail "git not installed"
command -v gh      >/dev/null 2>&1 || fail "gh CLI not installed"
command -v openssl >/dev/null 2>&1 || fail "openssl not installed"
gh auth status     >/dev/null 2>&1 || fail "gh not authenticated — run: gh auth login"

VAULT_REPO=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['vault_repo'])")
[ -n "$VAULT_REPO" ] || fail "vault_repo not set in avenger-config.json"

# ---- Dates -----------------------------------------------
TODAY=$(date -u '+%Y-%m-%d')
DOW=$(date -u '+%u')      # 1=Mon … 7=Sun
DOM=$(date -u '+%d')      # day of month
WEEK=$(date -u '+%Y-W%V') # ISO week
MONTH=$(date -u '+%Y-%m')

DAILY_BRANCH="backup/daily/$TODAY"
COMMIT_MSG="${1:-"🛡️ Avenger backup — $TODAY"}"
VAULT_DIR="/tmp/avenger-vault-$$"

# ---- Helpers ---------------------------------------------
encrypt_file() {
    openssl enc -aes-256-cbc -pbkdf2 -iter 100000 \
        -pass "pass:$AVENGER_KEY" -in "$1" -out "$2"
}

# ---- Clone repo ------------------------------------------
log "Cloning vault..."
gh repo clone "$VAULT_REPO" "$VAULT_DIR" -- --quiet
cd "$VAULT_DIR"
git config user.email "avenger@openclaw.ai"
git config user.name "Avenger Initiative"

# ---- Ensure main exists ----------------------------------
if git ls-remote --exit-code --heads origin main >/dev/null 2>&1; then
    git checkout main --quiet
else
    warn "main branch missing — creating it now (run setup.sh to avoid this)"
    git checkout -b main --quiet
    echo "# Avenger Vault" > README.md
    git add README.md
    git commit -m "chore: initialize main branch" --quiet
    git push -u origin main --quiet
    log "  ✓ main branch created"
fi

# ---- Create folder structure -----------------------------
mkdir -p config workspace/memory skills

# Auto-detect agent workspaces
AGENT_DIRS=$(find "$OPENCLAW_DIR" -maxdepth 1 -name "workspace-*" -type d 2>/dev/null || true)
for ws in $AGENT_DIRS; do
    agent_name=$(basename "$ws" | sed 's/workspace-//')
    mkdir -p "agents/$agent_name"
done
mkdir -p agents/main

# ---- 1. openclaw.json (ENCRYPTED) -----------------------
log "Encrypting openclaw.json..."
[ -f "$OPENCLAW_DIR/openclaw.json" ] && \
    encrypt_file "$OPENCLAW_DIR/openclaw.json" "config/openclaw.json.enc"

# ---- 2. Cron jobs ----------------------------------------
[ -f "$OPENCLAW_DIR/cron/jobs.json" ] && \
    cp "$OPENCLAW_DIR/cron/jobs.json" "config/cron-jobs.json" && log "  ✓ cron jobs"

# ---- 3. Workspace .md files ------------------------------
BACKED=0
for f in "$WORKSPACE_DIR"/*.md; do
    [ -f "$f" ] || continue
    cp "$f" "workspace/$(basename "$f")"
    BACKED=$((BACKED+1))
done
log "  ✓ $BACKED workspace files"

# ---- 4. Memory logs --------------------------------------
COUNT=0
for mf in "$WORKSPACE_DIR/memory"/*.md; do
    [ -f "$mf" ] || continue
    cp "$mf" "workspace/memory/$(basename "$mf")"
    COUNT=$((COUNT+1))
done
log "  ✓ $COUNT memory logs"

# ---- 5. Agent workspaces ---------------------------------
for ws in $AGENT_DIRS; do
    agent_name=$(basename "$ws" | sed 's/workspace-//')
    COUNT=0
    for f in SOUL.md IDENTITY.md MEMORY.md HEARTBEAT.md TOOLS.md AGENTS.md USER.md BOOTSTRAP.md; do
        [ -f "$ws/$f" ] && cp "$ws/$f" "agents/$agent_name/$f" && COUNT=$((COUNT+1)) || true
    done
    [ $COUNT -gt 0 ] && log "  ✓ agent:$agent_name ($COUNT files)"
done
for f in SOUL.md IDENTITY.md MEMORY.md HEARTBEAT.md TOOLS.md; do
    [ -f "$WORKSPACE_DIR/$f" ] && cp "$WORKSPACE_DIR/$f" "agents/main/$f" || true
done

# ---- 6. Custom skills ------------------------------------
SKILLS_DIR="$WORKSPACE_DIR/skills"
if [ -d "$SKILLS_DIR" ]; then
    SKILL_COUNT=0
    for skill_dir in "$SKILLS_DIR"/*/; do
        skill_name=$(basename "$skill_dir")
        mkdir -p "skills/$skill_name"
        [ -f "$skill_dir/SKILL.md" ]   && cp "$skill_dir/SKILL.md" "skills/$skill_name/"
        [ -d "$skill_dir/scripts" ]    && cp -r "$skill_dir/scripts"    "skills/$skill_name/" 2>/dev/null || true
        [ -d "$skill_dir/references" ] && cp -r "$skill_dir/references" "skills/$skill_name/" 2>/dev/null || true
        SKILL_COUNT=$((SKILL_COUNT+1))
    done
    log "  ✓ $SKILL_COUNT skills"
fi

# ---- 7. README + Manifest --------------------------------
HOSTNAME=$(hostname 2>/dev/null || echo "unknown")
OC_VER=$(python3 -c "import json; print(json.load(open('$OPENCLAW_DIR/update-check.json')).get('current','?'))" 2>/dev/null || echo "?")
BACKUP_TS=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
BACKUP_DATE=$(date -u '+%B %d, %Y at %H:%M UTC')

cat > README.md << README
# 🛡️ Avenger Initiative — Encrypted Backup Vault

This is an automated encrypted backup of an [OpenClaw](https://openclaw.ai) agent system,
managed by the [Avenger Initiative](https://proskills.md/skills/avenger-initiative) skill.

**Last backup:** $BACKUP_DATE
**Host:** \`$HOSTNAME\` | **OpenClaw:** $OC_VER

---

## What's in this vault?

Everything needed to fully restore an OpenClaw agent system from zero:

| Path | Encrypted | Contents |
|------|-----------|----------|
| \`config/openclaw.json.enc\` | ✅ AES-256-CBC | All API keys, bot tokens, plugin config |
| \`config/cron-jobs.json\` | No | Scheduled jobs and heartbeats |
| \`workspace/*.md\` | No | SOUL.md, IDENTITY.md, MEMORY.md, AGENTS.md, etc. |
| \`workspace/memory/\` | No | Daily memory logs |
| \`agents/<name>/\` | No | Per-agent SOUL, IDENTITY, MEMORY, HEARTBEAT files |
| \`skills/<name>/\` | No | Custom skill definitions, scripts, and references |

> **Note:** \`openclaw.json\` contains all secrets and is the only encrypted file.
> Everything else is plain text — safe to read directly in GitHub.

---

## Branch structure

| Branch | Purpose | Retention |
|--------|---------|-----------|
| \`main\` | ✅ **Always the latest backup** — start here | Forever |
| \`backup/daily/YYYY-MM-DD\` | Daily point-in-time snapshots | Last 7 kept |
| \`backup/weekly/YYYY-WNN\` | Weekly snapshots (created Sundays) | Last 8 kept |
| \`backup/monthly/YYYY-MM\` | Monthly snapshots (created on 1st) | Last 12 kept |

---

## How to restore

### Full restore (latest)

\`\`\`bash
# 1. Clone this vault
git clone <this-repo-url> vault && cd vault

# 2. Run the restore script
bash skills/avenger-initiative/scripts/restore.sh --vault .

# 3. Restart OpenClaw
openclaw gateway restart
\`\`\`

### Restore from a specific date

\`\`\`bash
git clone <this-repo-url> vault && cd vault
git checkout backup/daily/2026-03-10
bash skills/avenger-initiative/scripts/restore.sh --vault .
openclaw gateway restart
\`\`\`

### Decrypt openclaw.json manually

\`\`\`bash
# You need the encryption key (64-char hex, stored in your password manager)
openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 \
  -pass "pass:<YOUR_KEY>" \
  -in config/openclaw.json.enc \
  -out openclaw.json
\`\`\`

---

## Avenger Initiative commands

Tell your OpenClaw agent any of these:

| Command | What it does |
|---------|-------------|
| \`"avenger backup"\` | Run a backup right now |
| \`"avenger status"\` | Show last backup time, branch, and vault URL |
| \`"restore from vault"\` | Start guided restore flow |
| \`"avenger setup"\` | First-time setup wizard (new machine) |

Or run scripts directly:

\`\`\`bash
# Manual backup
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/backup.sh

# Manual restore (latest)
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/restore.sh

# Setup on a new machine
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/setup.sh --repo <vault-url>
\`\`\`

---

## Security

- Encryption: AES-256-CBC · PBKDF2 · 100,000 iterations
- Key storage: Local only (\`~/.openclaw/credentials/avenger.key\`) — never committed
- Everything else in this repo is intentionally plaintext (no secrets)

---

*Managed by [Avenger Initiative](https://proskills.md/skills/avenger-initiative) · Runs nightly at 02:00 UTC*
README

# Also keep a compact machine-readable manifest
cat > AVENGER-MANIFEST.json << MANIFEST
{
  "backup_at": "$BACKUP_TS",
  "host": "$HOSTNAME",
  "openclaw_version": "$OC_VER",
  "daily_branch": "$DAILY_BRANCH",
  "vault_repo": "$VAULT_REPO"
}
MANIFEST

# ---- .gitignore ------------------------------------------
cat > .gitignore << 'GITIGNORE'
*.key
*.pem
.env
credentials/
node_modules/
__pycache__/
*.pyc
.DS_Store
GITIGNORE

# ---- Commit to main --------------------------------------
log "Committing to main..."
git add -A
if git diff --cached --quiet; then
    warn "No changes since last backup."
    cd /; rm -rf "$VAULT_DIR"
    exit 0
fi
git commit -m "$COMMIT_MSG" --quiet
git push origin main --quiet
log "  ✓ main updated"

# ---- Create dated snapshot branch from current main ------
log "Creating snapshot branch $DAILY_BRANCH..."
git checkout -b "$DAILY_BRANCH" --quiet
git push origin "$DAILY_BRANCH" --force --quiet
log "  ✓ Snapshot: $DAILY_BRANCH"

# ---- Weekly snapshot (Sundays) ---------------------------
if [ "$DOW" = "7" ]; then
    WEEKLY_BRANCH="backup/weekly/$WEEK"
    git checkout -b "$WEEKLY_BRANCH" --quiet 2>/dev/null || git checkout "$WEEKLY_BRANCH" --quiet
    git push origin "$WEEKLY_BRANCH" --force --quiet
    git checkout main --quiet
    log "  ✓ Weekly: $WEEKLY_BRANCH"
fi

# ---- Monthly snapshot (1st of month) ---------------------
if [ "$DOM" = "01" ]; then
    MONTHLY_BRANCH="backup/monthly/$MONTH"
    git checkout -b "$MONTHLY_BRANCH" --quiet 2>/dev/null || git checkout "$MONTHLY_BRANCH" --quiet
    git push origin "$MONTHLY_BRANCH" --force --quiet
    git checkout main --quiet
    log "  ✓ Monthly: $MONTHLY_BRANCH"
fi

# ---- Prune old dated branches ----------------------------
log "Pruning old branches..."
git fetch --prune --quiet

prune_branches() {
    local pattern="$1" keep="$2"
    local count=0
    git branch -r --list "origin/$pattern" | sed 's|origin/||' | sort -r | while read -r b; do
        count=$((count+1))
        if [ $count -gt $keep ]; then
            git push origin --delete "$b" --quiet 2>/dev/null && echo -e "\033[1;33m[WARN]\033[0m  🗑 Pruned $b" || true
        fi
    done
}

prune_branches "backup/daily/*"   7
prune_branches "backup/weekly/*"  8
prune_branches "backup/monthly/*" 12

# ---- Done ------------------------------------------------
cd /; rm -rf "$VAULT_DIR"
mkdir -p "$(dirname "$LOG_FILE")"
echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') OK | branch=main+$DAILY_BRANCH | $VAULT_REPO" >> "$LOG_FILE"
log "✅ Backup complete → $VAULT_REPO"
log "   main = latest | snapshot = $DAILY_BRANCH"
