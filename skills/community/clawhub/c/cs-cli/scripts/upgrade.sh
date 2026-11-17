#!/usr/bin/env bash
# camscanner-cli upgrade script — checks for new versions and upgrades CLI + Skill files.
# Run by AI Agent at the start of each session. Safe to run repeatedly.
#
# Usage:
#   bash scripts/upgrade.sh
#   bash scripts/upgrade.sh --rollback
#
# Behavior:
#   - If no update needed: exits silently (exit 0)
#   - If network fails: exits silently (exit 0), does not block usage
#   - If upgrade fails: auto-rollback, then exit 1
#   - If lock conflict: exits silently (exit 0)

set -eu

CDN_BASE="${CAMSCANNER_CLI_CDN:-https://data.camscanner.com/camscanner-cli}"

# ── Locate paths ────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TMP_DIR="$(dirname "$SKILL_DIR")/camscanner-temp"
BACKUP_DIR="$TMP_DIR/backup"
LOCK_DIR="$TMP_DIR/upgrade.lock.d"
CLI_PATH=""
# Patched to "cp" for targets whose shared mounts prohibit file removal.
CLI_REPLACE_METHOD="mv"
# Optional installation directory, patched for targets with a nonstandard PATH.
CLI_INSTALL_DIR=""

# ── Helpers ─────────────────────────────────────────────────────────────────

say()  { printf '  %s\n' "$@"; }
warn() { printf '  [warn] %s\n' "$@" >&2; }
err()  { printf '  [error] %s\n' "$@" >&2; }

detect_os() {
  case "$(uname -s)" in
    Linux*)  echo "linux"  ;;
    Darwin*) echo "darwin" ;;
    MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
    *) echo "" ;;
  esac
}

detect_arch() {
  case "$(uname -m)" in
    x86_64|amd64)  echo "amd64" ;;
    arm64|aarch64) echo "arm64" ;;
    *) echo "" ;;
  esac
}

version_gt() {
  [ -n "$1" ] || return 1
  [ -n "$2" ] || return 0
  [ "$1" = "$2" ] && return 1
  local IFS='.'
  set -- $1 $2
  local major1="${1:-0}" minor1="${2:-0}" patch1="${3:-0}"
  local major2="${4:-0}" minor2="${5:-0}" patch2="${6:-0}"
  if [ "$major1" -gt "$major2" ]; then return 0; fi
  if [ "$major1" -lt "$major2" ]; then return 1; fi
  if [ "$minor1" -gt "$minor2" ]; then return 0; fi
  if [ "$minor1" -lt "$minor2" ]; then return 1; fi
  if [ "$patch1" -gt "$patch2" ]; then return 0; fi
  return 1
}

get_local_version() {
  if [ -n "$CLI_PATH" ]; then
    "$CLI_PATH" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1
  fi
}

get_skill_version() {
  if [ -f "$SKILL_DIR/SKILL.md" ]; then
    grep -oE "^version:[[:space:]]*['\"]?[0-9]+\.[0-9]+\.[0-9]+" "$SKILL_DIR/SKILL.md" \
      | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1
  fi
}

get_remote_version() {
  local ver=""
  if command -v curl >/dev/null 2>&1; then
    ver=$(curl -fsSL --connect-timeout 5 --max-time 10 "$CDN_BASE/latest-version.txt" 2>/dev/null || true)
  elif command -v wget >/dev/null 2>&1; then
    ver=$(wget -qO- --timeout=10 "$CDN_BASE/latest-version.txt" 2>/dev/null || true)
  fi
  printf '%s' "$ver" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1
}

download() {
  local url="$1" dest="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL --connect-timeout 10 --max-time 120 "$url" -o "$dest"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "$dest" --timeout=120 "$url"
  else
    return 1
  fi
}

# ── Lock management ─────────────────────────────────────────────────────────

acquire_lock() {
  mkdir -p "$(dirname "$LOCK_DIR")"
  if ! mkdir "$LOCK_DIR" 2>/dev/null; then
    if [ -f "$LOCK_DIR/pid" ]; then
      local lock_pid
      lock_pid=$(cat "$LOCK_DIR/pid" 2>/dev/null || echo "")
      if [ -n "$lock_pid" ] && kill -0 "$lock_pid" 2>/dev/null; then
        return 1
      fi
      rm -rf "$LOCK_DIR"
      mkdir "$LOCK_DIR" 2>/dev/null || return 1
    else
      return 1
    fi
  fi
  echo $$ > "$LOCK_DIR/pid"
}

release_lock() {
  rm -rf "$LOCK_DIR"
}

# ── Backup & Rollback ───────────────────────────────────────────────────────

backup_current() {
  local current_version="$1"
  mkdir -p "$BACKUP_DIR"
  if [ -n "$CLI_PATH" ] && [ -f "$CLI_PATH" ]; then
    cp "$CLI_PATH" "$BACKUP_DIR/camscanner-cli.bak"
  fi
  tar -czf "$BACKUP_DIR/skill-${current_version}.tar.gz" \
    -C "$SKILL_DIR" SKILL.md references/ scripts/ 2>/dev/null || true
  echo "$current_version" > "$BACKUP_DIR/previous-version.txt"
}

rollback() {
  local prev_version="$1"
  warn "Upgrade failed, rolling back to v${prev_version}..."
  if [ -f "$BACKUP_DIR/camscanner-cli.bak" ] && [ -n "$CLI_PATH" ]; then
    cp "$BACKUP_DIR/camscanner-cli.bak" "$CLI_PATH"
    chmod +x "$CLI_PATH"
  fi
  if [ -f "$BACKUP_DIR/skill-${prev_version}.tar.gz" ]; then
    tar -xzf "$BACKUP_DIR/skill-${prev_version}.tar.gz" -C "$SKILL_DIR" 2>/dev/null || true
  fi
  err "Rolled back to v${prev_version}"
}

do_rollback() {
  if [ ! -f "$BACKUP_DIR/previous-version.txt" ]; then
    err "No backup found, cannot rollback."
    exit 1
  fi
  local prev_version
  prev_version=$(cat "$BACKUP_DIR/previous-version.txt")
  rollback "$prev_version"
  say "Rollback to v${prev_version} complete."
  exit 0
}

# ── Cleanup ─────────────────────────────────────────────────────────────────

cleanup() {
  rm -f "$TMP_DIR/camscanner-cli-"* 2>/dev/null
  rm -f "$TMP_DIR/camscanner-skill-"* 2>/dev/null
  rm -f "$TMP_DIR/checksums.txt" 2>/dev/null
  rm -rf "$TMP_DIR/skill" 2>/dev/null
  release_lock
}

# ── Main ────────────────────────────────────────────────────────────────────

main() {
  # Handle --rollback flag
  if [ "${1:-}" = "--rollback" ]; then
    do_rollback
  fi

  # Find CLI
  if [ -n "$CLI_INSTALL_DIR" ]; then
    export PATH="$CLI_INSTALL_DIR:$PATH"
  fi
  CLI_PATH="$(command -v camscanner-cli 2>/dev/null || true)"
  if [ -z "$CLI_PATH" ]; then
    exit 0
  fi

  # Get versions
  local cli_version skill_version local_version remote_version
  cli_version="$(get_local_version)"
  if [ -z "$cli_version" ]; then
    exit 0
  fi
  skill_version="$(get_skill_version)"
  if [ -z "$skill_version" ]; then
    warn "Cannot read Skill version from $SKILL_DIR/SKILL.md; using CLI version $cli_version."
  fi

  # Take the lower of CLI and Skill versions
  if [ -n "$skill_version" ] && version_gt "$cli_version" "$skill_version"; then
    local_version="$skill_version"
  else
    local_version="$cli_version"
  fi

  remote_version="$(get_remote_version)"
  if [ -z "$remote_version" ]; then
    exit 0
  fi

  # Compare versions
  if ! version_gt "$remote_version" "$local_version"; then
    exit 0
  fi

  # Acquire lock
  if ! acquire_lock; then
    exit 0
  fi
  trap cleanup EXIT

  say "Update available: v${local_version} → v${remote_version}"

  # Detect platform
  local os_name arch_name
  os_name="$(detect_os)"
  arch_name="$(detect_arch)"
  if [ -z "$os_name" ] || [ -z "$arch_name" ]; then
    err "Unsupported platform"
    exit 0
  fi

  # Prepare temp directory
  mkdir -p "$TMP_DIR"

  # Download CLI binary
  # CLI subpath — patched at build time for each target
  local cli_subpath="clawhub/"

  local bin_suffix bin_url
  if [ "$os_name" = "windows" ]; then
    bin_suffix="camscanner-cli-${os_name}-${arch_name}.exe"
  else
    bin_suffix="camscanner-cli-${os_name}-${arch_name}"
  fi
  bin_url="${CDN_BASE}/releases/v${remote_version}/${cli_subpath}${bin_suffix}"

  say "Downloading CLI binary..."
  if ! download "$bin_url" "$TMP_DIR/$bin_suffix"; then
    warn "Download CLI failed, skipping upgrade."
    exit 0
  fi

  # Download Skill ZIP
  local skill_zip="camscanner-skill-clawhub-v${remote_version}.zip"
  local skill_url="${CDN_BASE}/releases/v${remote_version}/${skill_zip}"

  say "Downloading Skill package..."
  if ! download "$skill_url" "$TMP_DIR/$skill_zip"; then
    warn "Download Skill ZIP failed, skipping upgrade."
    exit 0
  fi

  # Download and verify checksums (mandatory — abort if unavailable)
  local checksums_url="${CDN_BASE}/releases/v${remote_version}/${cli_subpath}checksums.txt"
  if ! download "$checksums_url" "$TMP_DIR/checksums.txt" 2>/dev/null; then
    warn "Cannot download checksums.txt, aborting upgrade for security."
    exit 0
  fi

  local expected_cli
  expected_cli=$(grep "$bin_suffix" "$TMP_DIR/checksums.txt" 2>/dev/null | awk '{print $1}')

  if [ -z "$expected_cli" ]; then
    warn "checksums.txt missing entry for CLI binary, aborting upgrade."
    exit 0
  fi

  local actual_cli
  if command -v shasum >/dev/null 2>&1; then
    actual_cli=$(shasum -a 256 "$TMP_DIR/$bin_suffix" | awk '{print $1}')
  elif command -v sha256sum >/dev/null 2>&1; then
    actual_cli=$(sha256sum "$TMP_DIR/$bin_suffix" | awk '{print $1}')
  else
    warn "No sha256 tool available, aborting upgrade."
    exit 0
  fi
  if [ "$actual_cli" != "$expected_cli" ]; then
    warn "CLI binary checksum mismatch, skipping upgrade."
    exit 0
  fi

  # Verify downloaded CLI binary is executable
  chmod +x "$TMP_DIR/$bin_suffix"
  local downloaded_ver
  downloaded_ver=$("$TMP_DIR/$bin_suffix" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)
  if [ -z "$downloaded_ver" ]; then
    warn "Downloaded CLI binary is not valid, skipping upgrade."
    exit 0
  fi

  # Backup current version
  say "Backing up current version..."
  backup_current "$local_version"

  # Replace CLI binary
  say "Replacing CLI binary..."
  if [ "$CLI_REPLACE_METHOD" = "cp" ]; then
    # Overwrite in place without unlinking the existing binary.
    if cp "$TMP_DIR/$bin_suffix" "$CLI_PATH" && chmod +x "$CLI_PATH"; then
      :
    else
      warn "Failed to replace CLI binary: $CLI_PATH"
      rollback "$local_version"
      exit 1
    fi
  elif [ -w "$CLI_PATH" ]; then
    mv "$TMP_DIR/$bin_suffix" "$CLI_PATH"
    chmod +x "$CLI_PATH"
  else
    if cp "$TMP_DIR/$bin_suffix" "$CLI_PATH" 2>/dev/null; then
      chmod +x "$CLI_PATH"
    else
      warn "Cannot write to $CLI_PATH (permission denied)."
      rollback "$local_version"
      exit 1
    fi
  fi

  # Replace Skill files
  say "Replacing Skill files..."
  mkdir -p "$TMP_DIR/skill"
  if ! unzip -qo "$TMP_DIR/$skill_zip" -d "$TMP_DIR/skill/"; then
    warn "Failed to extract Skill ZIP."
    rollback "$local_version"
    exit 1
  fi

  # Find extracted content root (may have a wrapper directory)
  local skill_src="$TMP_DIR/skill"
  if [ ! -f "$skill_src/SKILL.md" ]; then
    local nested
    nested=$(find "$skill_src" -maxdepth 2 -name "SKILL.md" -type f | head -1)
    if [ -n "$nested" ]; then
      skill_src="$(dirname "$nested")"
    else
      warn "Skill ZIP does not contain SKILL.md."
      rollback "$local_version"
      exit 1
    fi
  fi

  # Replace SKILL.md
  cp -f "$skill_src/SKILL.md" "$SKILL_DIR/SKILL.md"

  # Replace references/
  if [ -d "$skill_src/references" ]; then
    mkdir -p "$SKILL_DIR/references"
    cp -Rf "$skill_src/references/." "$SKILL_DIR/references/"
  fi

  # Replace scripts/ (last, since this script is in it)
  if [ -d "$skill_src/scripts" ]; then
    mkdir -p "$SKILL_DIR/scripts"
    cp -Rf "$skill_src/scripts/." "$SKILL_DIR/scripts/"
  fi

  # Verify upgrade
  local new_ver
  new_ver="$("$CLI_PATH" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)"
  if [ "$new_ver" != "$remote_version" ]; then
    rollback "$local_version"
    exit 1
  fi

  # Clean old skill backups, keep only the latest one
  find "$BACKUP_DIR" -name "skill-*.tar.gz" ! -name "skill-${local_version}.tar.gz" -delete 2>/dev/null || true

  say "Upgrade complete: v${local_version} → v${remote_version}"
}

main "$@"
