#!/usr/bin/env bash
# hermes-restore: Restore from a Hermes Backup archive
# Usage: restore.sh <backup.tar.gz[.enc]> [--dry-run] [--force]

set -euo pipefail

ARCHIVE="${1:-}"
DRY_RUN=false
FORCE=false

for arg in "${@:2}"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --force) FORCE=true ;;
  esac
done

# ── Colors ───────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { echo -e "${GREEN}[✓]${NC} $*"; }
warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
error() { echo -e "${RED}[✗]${NC} $*"; exit 1; }
dry()   { echo -e "${CYAN}[DRY]${NC} $*"; }

# ── Validate ─────────────────────────────────────────────────────────────────
[[ -z "$ARCHIVE" ]] && error "Usage: restore.sh <backup.tar.gz[.enc]> [--dry-run] [--force]"
[[ ! -f "$ARCHIVE" ]] && error "Archive not found: $ARCHIVE"

echo ""
echo "🦞 Hermes Restore"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$DRY_RUN && echo -e "${CYAN}[DRY RUN — no changes will be made]${NC}\n"

# ── Check if encrypted ───────────────────────────────────────────────────────
IS_ENCRYPTED=false
if [[ "$ARCHIVE" == *.enc ]]; then
  IS_ENCRYPTED=true
  warn "Encrypted backup detected"
  echo -n "Enter decryption password: "
  read -s PASSWORD
  echo ""
  
  # Decrypt to temp
  TEMP_ARCHIVE="/tmp/hermes-restore-$$.tar.gz"
  if ! openssl enc -aes-256-cbc -d -salt -pbkdf2 -in "$ARCHIVE" -out "$TEMP_ARCHIVE" -pass pass:"$PASSWORD" 2>/dev/null; then
    error "Decryption failed — wrong password?"
  fi
  ARCHIVE="$TEMP_ARCHIVE"
  trap "rm -f $TEMP_ARCHIVE" EXIT
fi

# ── Extract and validate ─────────────────────────────────────────────────────
WORK_DIR="/tmp/hermes-restore-$$"
mkdir -p "$WORK_DIR"
trap "rm -rf $WORK_DIR" EXIT

info "Extracting archive..."
tar -xzf "$ARCHIVE" -C "$WORK_DIR"

BACKUP_DIR=$(find "$WORK_DIR" -maxdepth 1 -name "hermes-backup_*" -type d | head -1)
[[ -z "$BACKUP_DIR" ]] && error "Invalid archive: no hermes-backup_* directory found"

# ── Read Manifest ─────────────────────────────────────────────────────────────
MANIFEST="${BACKUP_DIR}/MANIFEST.json"
if [[ -f "$MANIFEST" ]]; then
  echo ""
  echo "📋 Backup Info:"
  python3 -c "
import json
d = json.load(open('${MANIFEST}'))
print(f\"  Platform: {d.get('platform', 'unknown')}\")
print(f\"  Agent: {d.get('agent_name', 'unknown')}\")
print(f\"  Created: {d.get('timestamp', 'unknown')}\")
print(f\"  From: {d.get('hostname', 'unknown')}\")
print(f\"  Encrypted: {d.get('encrypted', False)}\")
" 2>/dev/null || true
  echo ""
fi

# ── Detect Target Platform ───────────────────────────────────────────────────
HERMES_HOME="${HOME}/.hermes"
OPENCLAW_HOME="${HOME}/.openclaw"

if [[ -d "$HERMES_HOME" ]]; then
  TARGET_PLATFORM="hermes"
  TARGET_HOME="$HERMES_HOME"
elif [[ -d "$OPENCLAW_HOME" ]]; then
  TARGET_PLATFORM="openclaw"
  TARGET_HOME="$OPENCLAW_HOME"
else
  # No existing install — ask
  echo "No existing Hermes or OpenClaw installation found."
  echo "Which platform are you restoring to?"
  select PLATFORM in "hermes" "openclaw"; do
    [[ -n "$PLATFORM" ]] && break
  done
  TARGET_PLATFORM="$PLATFORM"
  [[ "$PLATFORM" == "hermes" ]] && TARGET_HOME="$HERMES_HOME" || TARGET_HOME="$OPENCLAW_HOME"
  mkdir -p "$TARGET_HOME"
fi

echo "Target: ${TARGET_PLATFORM} (${TARGET_HOME})"
echo ""

# ── Safety Confirmation ──────────────────────────────────────────────────────
if ! $DRY_RUN && ! $FORCE; then
  echo -e "${RED}⚠️  WARNING: This will OVERWRITE your current ${TARGET_PLATFORM} installation!${NC}"
  echo "   Backup: $(basename $1)"
  echo "   Target: ${TARGET_HOME}"
  echo ""
  echo -n "Type 'yes' to confirm: "
  read -r CONFIRM
  [[ "$CONFIRM" != "yes" ]] && { echo "Aborted."; exit 0; }
  echo ""
fi

# ── Pre-Restore Safety Backup ────────────────────────────────────────────────
if ! $DRY_RUN; then
  AUTO_BACKUP="/tmp/hermes-pre-restore-$(date +%Y%m%d_%H%M%S).tar.gz"
  warn "Creating safety backup of current state..."
  tar -czf "$AUTO_BACKUP" -C "$HOME" ".${TARGET_PLATFORM}" 2>/dev/null || true
  chmod 600 "$AUTO_BACKUP"
  info "Safety backup: $AUTO_BACKUP"
  echo ""
fi

# ── Restore Functions ────────────────────────────────────────────────────────

restore_item() {
  local src="$1"
  local dst="$2"
  local name="$3"
  
  if [[ -e "$src" ]]; then
    if $DRY_RUN; then
      dry "Restore: $name"
    else
      mkdir -p "$(dirname $dst)"
      rsync -a "$src" "$dst"
      info "Restored: $name"
    fi
  fi
}

# ── Execute Restore ───────────────────────────────────────────────────────────

# Stop gateway if running
if [[ "$TARGET_PLATFORM" == "openclaw" ]] && ! $DRY_RUN; then
  warn "Stopping OpenClaw gateway..."
  pkill -f "openclaw gateway" 2>/dev/null || true
  sleep 2
fi

# Platform-specific restores
if [[ "$TARGET_PLATFORM" == "hermes" ]]; then
  # Hermes-specific files
  [[ -d "${BACKUP_DIR}/config" ]] && restore_item "${BACKUP_DIR}/config/config.yaml" "${TARGET_HOME}/config.yaml" "config.yaml"
  [[ -f "${BACKUP_DIR}/config/.env" ]] && restore_item "${BACKUP_DIR}/config/.env" "${TARGET_HOME}/.env" ".env"
  [[ -d "${BACKUP_DIR}/identity" ]] && restore_item "${BACKUP_DIR}/identity/SOUL.md" "${TARGET_HOME}/SOUL.md" "SOUL.md"
  [[ -d "${BACKUP_DIR}/memories" ]] && restore_item "${BACKUP_DIR}/memories/" "${TARGET_HOME}/memories" "memories"
  [[ -d "${BACKUP_DIR}/sessions" ]] && restore_item "${BACKUP_DIR}/sessions/" "${TARGET_HOME}/sessions" "sessions"
  [[ -d "${BACKUP_DIR}/skills" ]] && restore_item "${BACKUP_DIR}/skills/" "${TARGET_HOME}/skills" "skills"
  [[ -f "${BACKUP_DIR}/state.db" ]] && restore_item "${BACKUP_DIR}/state.db" "${TARGET_HOME}/state.db" "state.db"
  [[ -f "${BACKUP_DIR}/auth.json" ]] && restore_item "${BACKUP_DIR}/auth.json" "${TARGET_HOME}/auth.json" "auth.json"
else
  # OpenClaw-specific files
  [[ -d "${BACKUP_DIR}/config" ]] && restore_item "${BACKUP_DIR}/config/openclaw.json" "${TARGET_HOME}/openclaw.json" "openclaw.json"
  [[ -d "${BACKUP_DIR}/credentials" ]] && restore_item "${BACKUP_DIR}/credentials/" "${TARGET_HOME}/credentials" "credentials"
  [[ -d "${BACKUP_DIR}/channels" ]] && restore_item "${BACKUP_DIR}/channels/" "${TARGET_HOME}/" "channel state"
  [[ -d "${BACKUP_DIR}/agents" ]] && restore_item "${BACKUP_DIR}/agents/" "${TARGET_HOME}/agents" "agents"
  [[ -d "${BACKUP_DIR}/skills-system" ]] && restore_item "${BACKUP_DIR}/skills-system/" "${TARGET_HOME}/skills" "system skills"
  [[ -d "${BACKUP_DIR}/cron" ]] && restore_item "${BACKUP_DIR}/cron/" "${TARGET_HOME}/cron" "cron"
  [[ -d "${BACKUP_DIR}/scripts" ]] && restore_item "${BACKUP_DIR}/scripts/" "${TARGET_HOME}/" "scripts"
fi

# Common workspace
[[ -d "${BACKUP_DIR}/workspace" ]] && restore_item "${BACKUP_DIR}/workspace/" "${HOME}/.openclaw/workspace" "workspace"

# ── Completion ─────────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if $DRY_RUN; then
  echo -e "${CYAN}Dry run complete — no changes made${NC}"
  echo "Run without --dry-run to apply restore"
else
  info "Restore complete!"
  echo ""
  echo "Next steps:"
  if [[ "$TARGET_PLATFORM" == "openclaw" ]]; then
    echo "  1. Run: openclaw gateway start"
    echo "  2. Channels should reconnect automatically"
    echo "  3. If Telegram is silent, send /start to your bot"
  else
    echo "  1. Restart your Hermes Agent"
    echo "  2. Verify configuration loaded correctly"
  fi
  echo ""
  echo "Safety backup saved at:"
  echo "  $AUTO_BACKUP"
  echo "  (Remove after confirming restore works)"
fi

echo ""
