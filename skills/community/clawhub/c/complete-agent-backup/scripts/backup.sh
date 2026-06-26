#!/usr/bin/env bash
# hermes-backup: Create a full or incremental backup of Hermes Agent or OpenClaw
# Usage: backup.sh [--full|--incremental] [--encrypt] [--cloud-upload] [--tag TAG]

set -euo pipefail

# ── Parse Arguments ──────────────────────────────────────────────────────────
BACKUP_TYPE="full"
ENCRYPT=false
CLOUD_UPLOAD=false
TAG=""
QUIET=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --full) BACKUP_TYPE="full" ;;
    --incremental) BACKUP_TYPE="incremental" ;;
    --encrypt) ENCRYPT=true ;;
    --cloud-upload) CLOUD_UPLOAD=true ;;
    --tag) TAG="$2"; shift ;;
    --quiet) QUIET=true ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
  shift
done

# ── Colors ───────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { [[ "$QUIET" == false ]] && echo -e "${GREEN}[✓]${NC} $*"; }
warn()  { [[ "$QUIET" == false ]] && echo -e "${YELLOW}[!]${NC} $*"; }
error() { echo -e "${RED}[✗]${NC} $*"; exit 1; }

# ── Detect Platform ──────────────────────────────────────────────────────────
HERMES_HOME="${HOME}/.hermes"
OPENCLAW_HOME="${HOME}/.openclaw"
PLATFORM=""

if [[ -d "$HERMES_HOME" && -d "$OPENCLAW_HOME" ]]; then
  # Both exist, check which has more recent activity
  HERMES_MTIME=$(find "$HERMES_HOME" -type f -mtime -7 2>/dev/null | wc -l)
  OPENCLAW_MTIME=$(find "$OPENCLAW_HOME" -type f -mtime -7 2>/dev/null | wc -l)
  if [[ $HERMES_MTIME -ge $OPENCLAW_MTIME ]]; then
    PLATFORM="hermes"
    PLATFORM_HOME="$HERMES_HOME"
  else
    PLATFORM="openclaw"
    PLATFORM_HOME="$OPENCLAW_HOME"
  fi
elif [[ -d "$HERMES_HOME" ]]; then
  PLATFORM="hermes"
  PLATFORM_HOME="$HERMES_HOME"
elif [[ -d "$OPENCLAW_HOME" ]]; then
  PLATFORM="openclaw"
  PLATFORM_HOME="$OPENCLAW_HOME"
else
  error "Neither Hermes (~/.hermes) nor OpenClaw (~/.openclaw) found"
fi

# ── Load Config ───────────────────────────────────────────────────────────────
CONFIG_FILE="${HOME}/.hermes-backup/config.yaml"
if [[ -f "$CONFIG_FILE" ]]; then
  BACKUP_DIR=$(grep "location:" "$CONFIG_FILE" | head -1 | cut -d':' -f2- | xargs | sed "s|~|$HOME|")
  KEEP_COUNT=$(grep "keep_count:" "$CONFIG_FILE" | head -1 | cut -d':' -f2 | xargs)
else
  BACKUP_DIR="${HOME}/backups/hermes"
  KEEP_COUNT=10
fi
BACKUP_DIR="${BACKUP_DIR/#\~/$HOME}"

# ── Setup ─────────────────────────────────────────────────────────────────────
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
TAG_SUFFIX=""
[[ -n "$TAG" ]] && TAG_SUFFIX="_${TAG}"

# Get agent name if available
AGENT_NAME="unknown"
if [[ "$PLATFORM" == "hermes" ]]; then
  [[ -f "${PLATFORM_HOME}/SOUL.md" ]] && AGENT_NAME=$(grep -m1 "^#" "${PLATFORM_HOME}/SOUL.md" 2>/dev/null | sed 's/^# *//' | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | cut -c1-20)
else
  [[ -f "${PLATFORM_HOME}/workspace/IDENTITY.md" ]] && AGENT_NAME=$(grep -m1 "\\*\\*Name:" "${PLATFORM_HOME}/workspace/IDENTITY.md" 2>/dev/null | sed 's/.*\\*\\*Name:\\*\\* *//' | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | cut -c1-20)
fi

BACKUP_NAME="hermes-backup_${PLATFORM}_${AGENT_NAME}${TAG_SUFFIX}_${TIMESTAMP}"
WORK_DIR="/tmp/${BACKUP_NAME}"
ARCHIVE="${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"

mkdir -p "$BACKUP_DIR" "$WORK_DIR"

# ── Header ────────────────────────────────────────────────────────────────────
[[ "$QUIET" == false ]] && echo ""
[[ "$QUIET" == false ]] && echo "🦞 Hermes Backup — ${TIMESTAMP}"
[[ "$QUIET" == false ]] && echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
[[ "$QUIET" == false ]] && echo "Platform: ${PLATFORM}"
[[ "$QUIET" == false ]] && echo "Type: ${BACKUP_TYPE}"
[[ "$QUIET" == false ]] && echo ""

# ── Backup Functions ──────────────────────────────────────────────────────────

backup_hermes() {
  info "Backing up Hermes Agent..."
  
  # Config
  if [[ -f "${PLATFORM_HOME}/config.yaml" ]]; then
    mkdir -p "${WORK_DIR}/config"
    cp "${PLATFORM_HOME}/config.yaml" "${WORK_DIR}/config/"
    info "  config.yaml"
  fi
  
  # Environment (secrets)
  if [[ -f "${PLATFORM_HOME}/.env" ]]; then
    cp "${PLATFORM_HOME}/.env" "${WORK_DIR}/config/"
    info "  .env (secrets)"
  fi
  
  # Identity
  if [[ -f "${PLATFORM_HOME}/SOUL.md" ]]; then
    mkdir -p "${WORK_DIR}/identity"
    cp "${PLATFORM_HOME}/SOUL.md" "${WORK_DIR}/identity/"
    info "  SOUL.md"
  fi
  
  # Memories
  if [[ -d "${PLATFORM_HOME}/memories" ]]; then
    mkdir -p "${WORK_DIR}/memories"
    rsync -a "${PLATFORM_HOME}/memories/" "${WORK_DIR}/memories/"
    COUNT=$(find "${WORK_DIR}/memories" -type f | wc -l)
    info "  memories (${COUNT} files)"
  fi
  
  # Sessions
  if [[ -d "${PLATFORM_HOME}/sessions" ]]; then
    mkdir -p "${WORK_DIR}/sessions"
    rsync -a --exclude='*.lock' "${PLATFORM_HOME}/sessions/" "${WORK_DIR}/sessions/"
    COUNT=$(find "${WORK_DIR}/sessions" -name "*.jsonl" | wc -l)
    info "  sessions (${COUNT} conversations)"
  fi
  
  # Skills
  if [[ -d "${PLATFORM_HOME}/skills" ]]; then
    mkdir -p "${WORK_DIR}/skills"
    rsync -a --exclude='node_modules' --exclude='.git' "${PLATFORM_HOME}/skills/" "${WORK_DIR}/skills/"
    COUNT=$(find "${WORK_DIR}/skills" -name "SKILL.md" | wc -l)
    info "  skills (${COUNT} installed)"
  fi
  
  # State database
  if [[ -f "${PLATFORM_HOME}/state.db" ]]; then
    cp "${PLATFORM_HOME}/state.db" "${WORK_DIR}/"
    SIZE=$(du -h "${PLATFORM_HOME}/state.db" | cut -f1)
    info "  state.db (${SIZE})"
  fi
  
  # Auth
  if [[ -f "${PLATFORM_HOME}/auth.json" ]]; then
    cp "${PLATFORM_HOME}/auth.json" "${WORK_DIR}/"
    info "  auth.json"
  fi
}

backup_openclaw() {
  info "Backing up OpenClaw..."
  
  # Gateway config (contains tokens)
  if [[ -f "${PLATFORM_HOME}/openclaw.json" ]]; then
    mkdir -p "${WORK_DIR}/config"
    cp "${PLATFORM_HOME}/openclaw.json" "${WORK_DIR}/config/"
    info "  openclaw.json (tokens)"
  fi
  
  # Credentials
  if [[ -d "${PLATFORM_HOME}/credentials" ]]; then
    mkdir -p "${WORK_DIR}/credentials"
    rsync -a "${PLATFORM_HOME}/credentials/" "${WORK_DIR}/credentials/"
    info "  credentials"
  fi
  
  # Channel state
  for channel in telegram discord whatsapp signal; do
    if [[ -d "${PLATFORM_HOME}/${channel}" ]]; then
      mkdir -p "${WORK_DIR}/channels/${channel}"
      rsync -a "${PLATFORM_HOME}/${channel}/" "${WORK_DIR}/channels/${channel}/"
      info "  channel: ${channel}"
    fi
  done
  
  # Agents
  if [[ -d "${PLATFORM_HOME}/agents" ]]; then
    mkdir -p "${WORK_DIR}/agents"
    rsync -a --exclude='*.lock' "${PLATFORM_HOME}/agents/" "${WORK_DIR}/agents/"
    SESSIONS=$(find "${WORK_DIR}/agents" -name "*.jsonl" | wc -l)
    info "  agents (${SESSIONS} sessions)"
  fi
  
  # System skills
  if [[ -d "${PLATFORM_HOME}/skills" ]]; then
    mkdir -p "${WORK_DIR}/skills-system"
    rsync -a "${PLATFORM_HOME}/skills/" "${WORK_DIR}/skills-system/"
    COUNT=$(find "${WORK_DIR}/skills-system" -name "SKILL.md" | wc -l)
    info "  system skills (${COUNT})"
  fi
  
  # Cron
  if [[ -d "${PLATFORM_HOME}/cron" ]]; then
    mkdir -p "${WORK_DIR}/cron"
    rsync -a "${PLATFORM_HOME}/cron/" "${WORK_DIR}/cron/"
    info "  cron jobs"
  fi
  
  # Guardian scripts
  mkdir -p "${WORK_DIR}/scripts"
  for script in guardian.sh gw-watchdog.sh start-gateway.sh; do
    [[ -f "${PLATFORM_HOME}/${script}" ]] && cp "${PLATFORM_HOME}/${script}" "${WORK_DIR}/scripts/"
  done
  [[ -d "${WORK_DIR}/scripts" && -n "$(ls -A ${WORK_DIR}/scripts)" ]] && info "  guardian scripts"
}

# ── Common Backup (Workspace) ─────────────────────────────────────────────────
backup_workspace() {
  WORKSPACE="${HOME}/.openclaw/workspace"
  if [[ -d "$WORKSPACE" ]]; then
    info "Backing up workspace..."
    mkdir -p "${WORK_DIR}/workspace"
    rsync -a \
      --exclude='node_modules/' \
      --exclude='.git/' \
      --exclude='*.tar.gz' \
      --exclude='*.zip' \
      --exclude='*.mp4' \
      --exclude='*.mp3' \
      --exclude='*.png' \
      --exclude='*.jpg' \
      --exclude='*.jpeg' \
      --exclude='*.gif' \
      --exclude='*.webp' \
      "$WORKSPACE/" "${WORK_DIR}/workspace/"
    SIZE=$(du -sh "${WORK_DIR}/workspace" | cut -f1)
    info "  workspace (${SIZE})"
  fi
}

# ── Execute Backup ────────────────────────────────────────────────────────────
if [[ "$PLATFORM" == "hermes" ]]; then
  backup_hermes
else
  backup_openclaw
fi
backup_workspace

# ── Create Manifest ───────────────────────────────────────────────────────────
cat > "${WORK_DIR}/MANIFEST.json" <<EOF
{
  "backup_name": "${BACKUP_NAME}",
  "platform": "${PLATFORM}",
  "agent_name": "${AGENT_NAME}",
  "timestamp": "${TIMESTAMP}",
  "type": "${BACKUP_TYPE}",
  "hostname": "$(hostname)",
  "version": "1.0.0",
  "encrypted": ${ENCRYPT},
  "created_by": "hermes-backup v1.0.0"
}
EOF

# ── Package ───────────────────────────────────────────────────────────────────
[[ "$QUIET" == false ]] && echo ""
info "Creating archive..."
tar -czf "$ARCHIVE" -C "/tmp" "$BACKUP_NAME"
rm -rf "$WORK_DIR"

# ── Encrypt if requested ──────────────────────────────────────────────────────
if [[ "$ENCRYPT" == true ]]; then
  [[ "$QUIET" == false ]] && echo ""
  warn "Encryption enabled — you MUST remember this password!"
  openssl enc -aes-256-cbc -salt -pbkdf2 -in "$ARCHIVE" -out "${ARCHIVE}.enc"
  rm "$ARCHIVE"
  ARCHIVE="${ARCHIVE}.enc"
  info "Encrypted: ${ARCHIVE}"
fi

# ── Set Permissions ────────────────────────────────────────────────────────────
chmod 600 "$ARCHIVE"

# ── Show Results ───────────────────────────────────────────────────────────────
ARCHIVE_SIZE=$(du -sh "$ARCHIVE" | cut -f1)
[[ "$QUIET" == false ]] && echo ""
[[ "$QUIET" == false ]] && echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
info "Backup complete: ${BACKUP_NAME}"
info "Location: ${ARCHIVE}"
info "Size: ${ARCHIVE_SIZE}"
warn "Archive contains credentials — keep secure!"

# ── Cloud Upload ───────────────────────────────────────────────────────────────
if [[ "$CLOUD_UPLOAD" == true ]]; then
  if [[ -f "${HOME}/.hermes-backup/cloud-config.sh" ]]; then
    [[ "$QUIET" == false ]] && echo ""
    info "Uploading to cloud..."
    bash "${HOME}/.hermes-backup/cloud-upload.sh" "$ARCHIVE"
  else
    warn "Cloud not configured — run: hermes-backup cloud setup"
  fi
fi

# ── Prune Old Backups ─────────────────────────────────────────────────────────
[[ "$QUIET" == false ]] && echo ""
BACKUP_COUNT=$(ls -t "${BACKUP_DIR}"/hermes-backup_*.tar.gz* 2>/dev/null | wc -l)
if [[ "$BACKUP_COUNT" -gt "$KEEP_COUNT" ]]; then
  info "Pruning old backups (keeping last ${KEEP_COUNT})..."
  ls -t "${BACKUP_DIR}"/hermes-backup_*.tar.gz* | tail -n +$((KEEP_COUNT + 1)) | xargs rm -f
  info "  Removed $((BACKUP_COUNT - KEEP_COUNT)) old backup(s)"
fi

[[ "$QUIET" == false ]] && echo ""
[[ "$QUIET" == false ]] && echo "✅ Done!"
[[ "$QUIET" == false ]] && echo ""

# Return archive path for scripts that need it
echo "$ARCHIVE"
