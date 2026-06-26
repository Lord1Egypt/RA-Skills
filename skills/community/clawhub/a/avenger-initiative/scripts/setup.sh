#!/usr/bin/env bash
# ============================================================
# AVENGER INITIATIVE — Setup Script v3
# Run once per OpenClaw instance
# Usage: setup.sh --repo https://github.com/USER/vault-repo [--key YOUR_KEY]
# ============================================================
set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}"
KEY_FILE="$OPENCLAW_DIR/credentials/avenger.key"
CONFIG_FILE="$OPENCLAW_DIR/credentials/avenger-config.json"
VAULT_REPO=""
PROVIDED_KEY=""

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log()    { echo -e "${GREEN}[AVENGER SETUP]${NC} $1"; }
warn()   { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail()   { echo -e "${RED}[FAIL]${NC} $1"; exit 1; }

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo) VAULT_REPO="$2"; shift 2 ;;
        --key)  PROVIDED_KEY="$2"; shift 2 ;;
        *) fail "Unknown argument: $1" ;;
    esac
done

[ -n "$VAULT_REPO" ] || { echo -e "${BLUE}[?]${NC} GitHub vault repo URL: "; read -r VAULT_REPO; }
[ -n "$VAULT_REPO" ] || fail "Vault repo URL required"

echo ""
echo "🛡️  AVENGER INITIATIVE — SETUP"
echo "================================"

# ---- Preflight checks -------------------------------------
command -v git    >/dev/null 2>&1 || fail "git not installed"
command -v gh     >/dev/null 2>&1 || fail "gh CLI not installed"
command -v openssl >/dev/null 2>&1 || fail "openssl not installed"
gh auth status >/dev/null 2>&1 || fail "gh not authenticated — run: gh auth login"

# ---- Test repo access -------------------------------------
log "Verifying repo access..."
gh repo view "$VAULT_REPO" >/dev/null 2>&1 || fail "Cannot access: $VAULT_REPO — check URL and permissions"
log "  ✓ Repo accessible"

# ---- Credentials dir --------------------------------------
mkdir -p "$OPENCLAW_DIR/credentials"
chmod 700 "$OPENCLAW_DIR/credentials"

# ---- Encryption key ---------------------------------------
if [ -n "$PROVIDED_KEY" ]; then
    echo "$PROVIDED_KEY" > "$KEY_FILE"
    log "  ✓ Using provided key"
elif [ -f "$KEY_FILE" ] && [ -s "$KEY_FILE" ]; then
    log "  ✓ Existing key found at $KEY_FILE"
    echo -e "${BLUE}[?]${NC} Keep existing key? [Y/n] "
    read -r keep
    if [[ "$keep" =~ ^[Nn]$ ]]; then
        echo -e "${BLUE}[?]${NC} Paste key (or press Enter to generate new): "
        read -r new_key
        if [ -n "$new_key" ]; then
            echo "$new_key" > "$KEY_FILE"
        else
            openssl rand -hex 32 > "$KEY_FILE"
            log "  ✓ Generated new key"
        fi
    fi
else
    echo -e "${BLUE}[?]${NC} Paste existing encryption key (or Enter to generate new): "
    read -r user_key
    if [ -n "$user_key" ]; then
        echo "$user_key" > "$KEY_FILE"
        log "  ✓ Saved provided key"
    else
        openssl rand -hex 32 > "$KEY_FILE"
        log "  ✓ Generated new key"
    fi
fi
chmod 600 "$KEY_FILE"

# ---- Save config ------------------------------------------
cat > "$CONFIG_FILE" << JSON
{
  "vault_repo": "$VAULT_REPO",
  "key_file": "$KEY_FILE",
  "setup_at": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "host": "$(hostname)"
}
JSON
chmod 600 "$CONFIG_FILE"
log "  ✓ Config saved"

# ---- Initialize vault repo with main branch ---------------
log "Initializing vault repo..."
GH_TOKEN=$(gh auth token)
REPO_URL=$(echo "$VAULT_REPO" | sed "s|https://|https://${GH_TOKEN}@|")
VAULT_DIR="/tmp/avenger-setup-$$"
git clone --quiet "$REPO_URL" "$VAULT_DIR"
cd "$VAULT_DIR"
git config user.email "avenger@openclaw.ai"
git config user.name "Avenger Initiative"

# Check if main branch exists
if git ls-remote --exit-code --heads origin main >/dev/null 2>&1; then
    log "  ✓ main branch already exists"
else
    warn "  main branch not found — creating it now..."
    # Switch to main (or create it)
    git checkout -b main 2>/dev/null || git checkout main
    cat > README.md << 'VAULTREADME'
# 🛡️ Avenger Initiative Vault

This is an encrypted backup vault managed by [Avenger Initiative](https://proskills.md/skills/avenger-initiative).

## Branch Structure

| Branch | Purpose |
|--------|---------|
| `main` | ✅ Always contains the **latest backup** |
| `backup/daily/YYYY-MM-DD` | Point-in-time daily snapshots (last 7 kept) |
| `backup/weekly/YYYY-WNN` | Weekly snapshots (last 8 kept) |
| `backup/monthly/YYYY-MM` | Monthly snapshots (last 12 kept) |

## Restore

```bash
# Latest (default)
bash restore.sh

# From a specific date
bash restore.sh --branch backup/daily/2026-03-10
```

## Security

`openclaw.json` is AES-256-CBC encrypted. Encryption key is stored locally only — never in this repo.
VAULTREADME
    git add README.md
    git commit -m "chore: initialize vault with main branch" --quiet
    git push -u origin main --quiet
    log "  ✓ main branch created and pushed"
fi

cd /; rm -rf "$VAULT_DIR"

# ---- Make scripts executable ------------------------------
SKILL_DIR="$OPENCLAW_DIR/workspace/skills/avenger-initiative/scripts"
chmod +x "$SKILL_DIR"/*.sh 2>/dev/null || true

# ---- Schedule daily backup cron ---------------------------
log "Setting up daily backup cron (02:00 UTC)..."
CRON_FILE="$OPENCLAW_DIR/cron/jobs.json"

if [ -f "$CRON_FILE" ]; then
    # Check if avenger job already exists
    if python3 -c "import json,sys; d=json.load(open('$CRON_FILE')); sys.exit(0 if any('avenger' in j.get('name','').lower() for j in d.get('jobs',[])) else 1)" 2>/dev/null; then
        log "  ✓ Backup cron already exists"
    else
        python3 << PYEOF
import json, uuid
path = "$CRON_FILE"
data = json.load(open(path))
data["jobs"].append({
    "id": str(uuid.uuid4()),
    "name": "Avenger Initiative — Nightly Backup",
    "enabled": True,
    "schedule": {"kind": "cron", "expr": "0 2 * * *", "tz": "UTC"},
    "sessionTarget": "main",
    "wakeMode": "now",
    "payload": {
        "kind": "systemEvent",
        "text": "🛡️ Avenger nightly backup: Run this exact command now and confirm when done: bash $SKILL_DIR/backup.sh"
    }
})
open(path, "w").write(json.dumps(data, indent=2))
print("  ✓ Daily backup cron added (02:00 UTC)")
PYEOF
    fi
else
    warn "  Cron file not found at $CRON_FILE — add backup cron manually via OpenClaw"
fi

# ---- Show key to save -------------------------------------
KEY=$(cat "$KEY_FILE")
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          🔐 SAVE THIS ENCRYPTION KEY NOW                    ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo ""
echo "   $KEY"
echo ""
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  Save in 1Password / Bitwarden / secure notes.              ║"
echo "║  Without this key, openclaw.json.enc cannot be decrypted.   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

log "✅ Setup complete!"
log ""
log "   Run your first backup:"
log "   bash $SKILL_DIR/backup.sh"
