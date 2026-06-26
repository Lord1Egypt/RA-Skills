#!/usr/bin/env bash
# OpenClaw restore — extracts a backup archive into ~/.openclaw
# Supports: macOS, Linux, Windows (Git Bash / WSL)
# Usage: bash restore.sh [--home DIR] [--force] [--verify] <archive.tar.gz[.gpg]>

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
FORCE=false
VERIFY_ONLY=false
ARCHIVE=""

# ── arg parsing ───────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --home|-H)    OPENCLAW_HOME="$2"; shift 2 ;;
    --force|-f)   FORCE=true; shift ;;
    --verify|-v)  VERIFY_ONLY=true; shift ;;
    --help|-h)
      echo "Usage: restore.sh [--home DIR] [--force] [--verify] <archive>"
      exit 0 ;;
    -*)  echo "Unknown option: $1"; exit 1 ;;
    *)   ARCHIVE="$1"; shift ;;
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

set_permissions() {
  # chmod is a no-op on Windows NTFS — skip silently
  [[ "$OS" == "windows" ]] && return 0
  for sensitive_dir in identity credentials secrets; do
    if [[ -d "$OPENCLAW_HOME/$sensitive_dir" ]]; then
      chmod 700 "$OPENCLAW_HOME/$sensitive_dir"
      chmod 600 "$OPENCLAW_HOME/$sensitive_dir/"* 2>/dev/null || true
    fi
  done
  [[ -f "$OPENCLAW_HOME/openclaw.json" ]] && chmod 600 "$OPENCLAW_HOME/openclaw.json"
}

# ── auto-select latest backup if none specified ───────────────────────────────
if [[ -z "$ARCHIVE" ]]; then
  LATEST="$(ls -t "$BACKUP_DIR"/openclaw-backup-*.tar.gz* 2>/dev/null | head -1)"
  if [[ -z "$LATEST" ]]; then
    echo "Error: no archive specified and no backups found in $BACKUP_DIR"
    exit 1
  fi
  echo "No archive specified — using latest: $(basename "$LATEST")"
  ARCHIVE="$LATEST"
fi

# resolve archive path — accept bare filename or full path
if [[ -f "$ARCHIVE" ]]; then
  ARCHIVE_PATH="$ARCHIVE"
elif [[ -f "$BACKUP_DIR/$ARCHIVE" ]]; then
  ARCHIVE_PATH="$BACKUP_DIR/$ARCHIVE"
else
  echo "Error: archive not found: $ARCHIVE"
  echo "Looked in: . and $BACKUP_DIR"
  exit 1
fi

# ── path traversal guard ──────────────────────────────────────────────────────
check_no_traversal() {
  local archive="$1"
  if tar -tzf "$archive" 2>/dev/null | grep -qE '^\.\./|/\.\./'; then
    echo "Error: archive contains path traversal sequences (../) — aborting."
    exit 1
  fi
}

# ── GPG decryption ────────────────────────────────────────────────────────────
WORK_ARCHIVE="$ARCHIVE_PATH"
TEMP_DECRYPTED=""

if [[ "$ARCHIVE_PATH" == *.gpg ]]; then
  if ! command -v gpg &>/dev/null; then
    echo "Error: archive is GPG-encrypted but gpg is not installed."
    exit 1
  fi
  TMPDIR="${TMPDIR:-${TMP:-${TEMP:-/tmp}}}"
  TEMP_DECRYPTED="$(mktemp "${TMPDIR}/openclaw-restore-XXXXXX.tar.gz")"
  echo "Decrypting archive..."
  gpg --output "$TEMP_DECRYPTED" --decrypt "$ARCHIVE_PATH"
  WORK_ARCHIVE="$TEMP_DECRYPTED"
  trap 'rm -f "$TEMP_DECRYPTED"' EXIT
fi

# ── verify mode ───────────────────────────────────────────────────────────────
if $VERIFY_ONLY; then
  echo "Verifying: $ARCHIVE_PATH"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  if gzip -t "$WORK_ARCHIVE" 2>/dev/null; then
    echo "  Integrity : OK"
  else
    echo "  Integrity : FAILED — archive may be corrupt"
    exit 1
  fi
  check_no_traversal "$WORK_ARCHIVE"
  echo "  Traversal : OK (no path escape detected)"
  FILE_COUNT="$(tar -tzf "$WORK_ARCHIVE" | wc -l | tr -d ' ')"
  echo "  Files     : $FILE_COUNT"
  echo ""
  echo "Top-level contents:"
  tar -tzf "$WORK_ARCHIVE" | awk -F'/' 'NF<=2 && $0!~"^\\.$"' | sort -u | head -40 | sed 's/^/  /'
  exit 0
fi

# ── restore ───────────────────────────────────────────────────────────────────
echo "OpenClaw Restore"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  OS      : $OS"
echo "  Archive : $ARCHIVE_PATH"
echo "  Target  : $OPENCLAW_HOME"
echo ""

# integrity check before touching anything
if ! gzip -t "$WORK_ARCHIVE" 2>/dev/null; then
  echo "Error: archive failed integrity check — aborting."
  exit 1
fi
check_no_traversal "$WORK_ARCHIVE"

# confirm if target exists — move it aside with timestamp
if [[ -d "$OPENCLAW_HOME" ]]; then
  if ! $FORCE; then
    echo "Warning: $OPENCLAW_HOME already exists."
    printf "Overwrite? The existing directory will be saved as ~/.openclaw_$(date +%Y-%m-%d_%H%M%S) [y/N] "
    read -r CONFIRM
    if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
      echo "Aborted."
      exit 0
    fi
  fi
  SNAPSHOT="${OPENCLAW_HOME}_$(date +%Y-%m-%d_%H%M%S)"
  echo "Moving existing ~/.openclaw → $SNAPSHOT"
  mv "$OPENCLAW_HOME" "$SNAPSHOT"
fi

# warn if openclaw is running
if is_openclaw_running; then
  echo ""
  echo "Warning: OpenClaw is currently running. Stop it before restoring for a clean state."
  if ! $FORCE; then
    printf "Continue anyway? [y/N] "
    read -r CONFIRM
    [[ "$CONFIRM" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }
  fi
fi

PARENT_DIR="$(dirname "$OPENCLAW_HOME")"
mkdir -p "$PARENT_DIR"

echo "Extracting..."
tar -xzf "$WORK_ARCHIVE" -C "$PARENT_DIR"

echo "Setting permissions..."
set_permissions

# ── summary ───────────────────────────────────────────────────────────────────
FILE_COUNT="$(tar -tzf "$WORK_ARCHIVE" | wc -l | tr -d ' ')"

echo ""
echo "Restore complete"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Restored : $OPENCLAW_HOME"
[[ -n "${SNAPSHOT:-}" ]] && echo "  Previous : $SNAPSHOT"
echo "  Files    : $FILE_COUNT"
echo ""
echo "OpenClaw is ready. Start it with your usual command."
