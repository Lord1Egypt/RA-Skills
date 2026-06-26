#!/usr/bin/env bash
# hermes-backup-config: Interactive configuration wizard
# Usage: config.sh

set -euo pipefail

# ── Colors ───────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
info() { echo -e "${GREEN}✓${NC} $*"; }
warn() { echo -e "${YELLOW}!${NC} $*"; }
ask() { echo -e "${CYAN}?${NC} $*"; }

echo ""
echo "🦞 Hermes Backup — Configuration Wizard"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

CONFIG_DIR="${HOME}/.hermes-backup"
CONFIG_FILE="${CONFIG_DIR}/config.yaml"
mkdir -p "$CONFIG_DIR"

# ── Detect Platform ──────────────────────────────────────────────────────────
HERMES_HOME="${HOME}/.hermes"
OPENCLAW_HOME="${HOME}/.openclaw"

if [[ -d "$HERMES_HOME" && -d "$OPENCLAW_HOME" ]]; then
  echo "Both Hermes and OpenClaw detected."
  ask "Which platform is primary?"
  select PLATFORM in "hermes" "openclaw" "auto-detect"; do
    [[ -n "$PLATFORM" ]] && break
  done
  [[ "$PLATFORM" == "auto-detect" ]] && PLATFORM="auto"
elif [[ -d "$HERMES_HOME" ]]; then
  PLATFORM="hermes"
  info "Hermes Agent detected"
elif [[ -d "$OPENCLAW_HOME" ]]; then
  PLATFORM="openclaw"
  info "OpenClaw detected"
else
  warn "No existing installation found"
  ask "Which platform will you use?"
  select PLATFORM in "hermes" "openclaw"; do
    [[ -n "$PLATFORM" ]] && break
  done
fi

echo ""

# ── Backup Location ──────────────────────────────────────────────────────────
ask "Where should backups be stored?"
echo "  1) ~/backups/hermes (default)"
echo "  2) ~/Documents/backups"
echo "  3) /var/backups/hermes (requires sudo)"
echo "  4) Custom path"
read -r LOCATION_CHOICE

case "$LOCATION_CHOICE" in
  2) BACKUP_DIR="${HOME}/Documents/backups" ;;
  3) BACKUP_DIR="/var/backups/hermes" ;;
  4) 
    ask "Enter custom path:"
    read -r BACKUP_DIR
    ;;
  *) BACKUP_DIR="${HOME}/backups/hermes" ;;
esac

mkdir -p "$BACKUP_DIR"
info "Backups will be saved to: $BACKUP_DIR"
echo ""

# ── Backup Type ──────────────────────────────────────────────────────────────
ask "Backup type?"
echo "  1) Full (complete backup every time) [default]"
echo "  2) Incremental (faster, only changes since last full)"
read -r TYPE_CHOICE

case "$TYPE_CHOICE" in
  2) 
    BACKUP_TYPE="incremental"
    warn "Incremental requires periodic full backups"
    ;;
  *) BACKUP_TYPE="full" ;;
esac

info "Backup type: $BACKUP_TYPE"
echo ""

# ── Encryption ────────────────────────────────────────────────────────────────
ask "Enable encryption? (password-protected backups)"
echo "  1) No [default]"
echo "  2) Yes — require password for all backups"
read -r ENCRYPT_CHOICE

if [[ "$ENCRYPT_CHOICE" == "2" ]]; then
  ENCRYPT="true"
  warn "⚠️  IMPORTANT: If you lose the password, backups are UNRECOVERABLE!"
  warn "Store the password in a password manager (1Password, Bitwarden, etc.)"
  info "Encryption enabled"
else
  ENCRYPT="false"
  info "Encryption disabled"
fi

echo ""

# ── Retention ─────────────────────────────────────────────────────────────────
ask "Retention policy — how many backups to keep?"
echo "  1) Last 10 backups [default]"
echo "  2) Last 30 days"
echo "  3) Last 5 backups (save space)"
echo "  4) Keep all (manual cleanup)"
read -r RETENTION_CHOICE

case "$RETENTION_CHOICE" in
  2) 
    RETENTION_STRATEGY="days"
    RETENTION_VALUE=30
    ;;
  3) 
    RETENTION_STRATEGY="count"
    RETENTION_VALUE=5
    ;;
  4) 
    RETENTION_STRATEGY="all"
    RETENTION_VALUE=9999
    ;;
  *) 
    RETENTION_STRATEGY="count"
    RETENTION_VALUE=10
    ;;
esac

info "Retention: $RETENTION_STRATEGY (value: $RETENTION_VALUE)"
echo ""

# ── Cloud Storage (Optional) ──────────────────────────────────────────────────
ask "Set up cloud storage for automatic uploads?"
echo "  1) No [default]"
echo "  2) Yes — I'll configure it now"
read -r CLOUD_CHOICE

if [[ "$CLOUD_CHOICE" == "2" ]]; then
  CLOUD_ENABLED="true"
  warn "Cloud setup wizard not yet implemented in v1.0"
  warn "You can run: hermes-backup cloud setup later"
else
  CLOUD_ENABLED="false"
  info "Cloud storage disabled"
fi

echo ""

# ── Write Config ─────────────────────────────────────────────────────────────
cat > "$CONFIG_FILE" <<EOF
# Hermes Backup Configuration
# Generated: $(date)

platform: ${PLATFORM}

backup:
  location: ${BACKUP_DIR}
  type: ${BACKUP_TYPE}
  compression: gzip
  encryption: ${ENCRYPT}

retention:
  strategy: ${RETENTION_STRATEGY}
  keep_count: ${RETENTION_VALUE}
  keep_days: 30
  max_size_gb: 10

incremental:
  enabled: $([[ "$BACKUP_TYPE" == "incremental" ]] && echo "true" || echo "false")
  base_backup: null

cloud:
  enabled: ${CLOUD_ENABLED}
  provider: null

integrity:
  verify_after_backup: true
  checksum_algorithm: sha256
EOF

chmod 600 "$CONFIG_FILE"

# ── Summary ───────────────────────────────────────────────────────────────────
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
info "Configuration saved to: $CONFIG_FILE"
echo ""
echo "Settings:"
echo "  Platform: $PLATFORM"
echo "  Location: $BACKUP_DIR"
echo "  Type: $BACKUP_TYPE"
echo "  Encryption: $ENCRYPT"
echo "  Retention: $RETENTION_STRATEGY ($RETENTION_VALUE)"
echo "  Cloud: $CLOUD_ENABLED"
echo ""
echo "You can now run:"
echo "  hermes-backup create        # Create your first backup"
echo "  hermes-backup list          # View all backups"
echo "  hermes-backup restore       # Restore from backup"
echo ""
