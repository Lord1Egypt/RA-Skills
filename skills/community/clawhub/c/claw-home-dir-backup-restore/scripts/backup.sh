#!/usr/bin/env bash
# OpenClaw backup — creates a portable .tar.gz of the full ~/.openclaw directory
# Supports: macOS, Linux, Windows (Git Bash / WSL)
# Usage: bash backup.sh [--output DIR] [--encrypt RECIPIENT] [--list] [--help]

set -euo pipefail

# ── OS detection ──────────────────────────────────────────────────────────────
case "$(uname -s 2>/dev/null)" in
  Darwin)               OS="macos" ;;
  Linux)                OS="linux" ;;
  MINGW*|MSYS*|CYGWIN*) OS="windows" ;;
  *)                    OS="unknown" ;;
esac

# ── defaults ──────────────────────────────────────────────────────────────────
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/openclaw-backups}"
GPG_RECIPIENT="${BACKUP_GPG_RECIPIENT:-}"
ENCRYPT=false
LIST=false

# ── arg parsing ───────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --output|-o)   BACKUP_DIR="$2"; shift 2 ;;
    --encrypt|-e)  ENCRYPT=true; GPG_RECIPIENT="$2"; shift 2 ;;
    --list|-l)     LIST=true; shift ;;
    --help|-h)
      echo "Usage: backup.sh [--output DIR] [--encrypt RECIPIENT] [--list]"
      exit 0 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# ── cross-platform helpers ────────────────────────────────────────────────────
is_openclaw_running() {
  if command -v pgrep &>/dev/null; then
    pgrep -f "openclaw" &>/dev/null
  elif [[ "$OS" == "windows" ]]; then
    tasklist 2>/dev/null | grep -qi "openclaw.exe"
  else
    false
  fi
}

file_size() {
  local file="$1"
  du -sh "$file" 2>/dev/null | cut -f1
}

gpg_install_hint() {
  case "$OS" in
    macos)   echo "  Install: brew install gnupg" ;;
    linux)   echo "  Install: sudo apt install gnupg  OR  sudo dnf install gnupg2" ;;
    windows) echo "  Install: winget install GnuPG.GnuPG  OR include via Git for Windows" ;;
    *)       echo "  Install gpg from https://gnupg.org/download/" ;;
  esac
}

# ── list mode ─────────────────────────────────────────────────────────────────
if $LIST; then
  if [[ ! -d "$BACKUP_DIR" ]] || [[ -z "$(ls -A "$BACKUP_DIR" 2>/dev/null)" ]]; then
    echo "No backups found in $BACKUP_DIR"
    exit 0
  fi
  echo "OpenClaw backups in $BACKUP_DIR"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  for f in "$BACKUP_DIR"/openclaw-backup-*.tar.gz*; do
    [[ -f "$f" ]] || continue
    echo "  $(basename "$f")  [$(file_size "$f")]"
  done
  exit 0
fi

# ── pre-flight checks ─────────────────────────────────────────────────────────
if [[ ! -d "$OPENCLAW_HOME" ]]; then
  echo "Error: OpenClaw home not found at $OPENCLAW_HOME"
  echo "Set OPENCLAW_HOME if your installation is elsewhere."
  exit 1
fi

if $ENCRYPT && [[ -z "$GPG_RECIPIENT" ]]; then
  echo "Error: --encrypt requires a GPG recipient (email or key ID)"
  exit 1
fi

if $ENCRYPT && ! command -v gpg &>/dev/null; then
  echo "Error: gpg is not installed."
  gpg_install_hint
  exit 1
fi

if is_openclaw_running; then
  echo "Warning: OpenClaw appears to be running. SQLite databases may be in WAL state."
  echo "         For a clean backup, stop OpenClaw first. Continuing anyway..."
  echo ""
fi

# ── build archive ─────────────────────────────────────────────────────────────
mkdir -p "$BACKUP_DIR"

TIMESTAMP="$(date +%Y-%m-%d_%H%M%S)"
ARCHIVE_NAME="openclaw-backup-${TIMESTAMP}.tar.gz"
ARCHIVE_PATH="${BACKUP_DIR}/${ARCHIVE_NAME}"

echo "OpenClaw Backup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  OS      : $OS"
echo "  Source  : $OPENCLAW_HOME"
echo "  Output  : $ARCHIVE_PATH"
$ENCRYPT && echo "  Encrypt : $GPG_RECIPIENT"
echo ""

tar -czf "$ARCHIVE_PATH" \
  -C "$(dirname "$OPENCLAW_HOME")" \
  "$(basename "$OPENCLAW_HOME")"

# ── optional GPG encryption ───────────────────────────────────────────────────
if $ENCRYPT; then
  gpg --output "${ARCHIVE_PATH}.gpg" \
      --encrypt \
      --recipient "$GPG_RECIPIENT" \
      "$ARCHIVE_PATH"
  rm "$ARCHIVE_PATH"
  ARCHIVE_PATH="${ARCHIVE_PATH}.gpg"
  ARCHIVE_NAME="${ARCHIVE_NAME}.gpg"
fi

# ── summary ───────────────────────────────────────────────────────────────────
SIZE="$(file_size "$ARCHIVE_PATH")"
if $ENCRYPT; then
  FILE_COUNT="N/A (encrypted)"
else
  FILE_COUNT="$(tar -tzf "$ARCHIVE_PATH" 2>/dev/null | wc -l | tr -d ' ')"
fi

echo "Backup complete"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Archive : $ARCHIVE_PATH"
echo "  Size    : $SIZE"
echo "  Files   : $FILE_COUNT"
echo ""
echo "To restore on any machine:"
echo "  bash restore.sh $ARCHIVE_NAME"
