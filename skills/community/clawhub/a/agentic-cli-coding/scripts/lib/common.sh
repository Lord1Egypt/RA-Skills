#!/usr/bin/env bash
# common.sh — Shared utilities for oce-* commands.
# Always source paths.sh BEFORE this file in the calling script.

set -euo pipefail

# Colors (stripped if not a tty or NO_COLOR is set)
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  C_RED=$'\033[0;31m'
  C_GREEN=$'\033[0;32m'
  C_YELLOW=$'\033[0;33m'
  C_BLUE=$'\033[0;34m'
  C_DIM=$'\033[2m'
  C_RESET=$'\033[0m'
else
  C_RED="" C_GREEN="" C_YELLOW="" C_BLUE="" C_DIM="" C_RESET=""
fi

# JSON output mode (set by --json flag in calling scripts)
OCE_JSON_MODE="${OCE_JSON_MODE:-0}"
OCE_DRY_RUN="${OCE_DRY_RUN:-0}"

# ---------- Logging ----------
log() {
  local level="$1"; shift
  local msg="$*"
  printf '[%s] [%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$level" "$msg" >> "$OCE_LOG" 2>/dev/null || true
}

# ---------- JSON helpers ----------
json_escape() {
  # Use Node since it's a hard dependency anyway
  node -e 'process.stdout.write(JSON.stringify(process.argv[1]))' -- "$1"
}

# Emit a JSON object. Args are alternating key/value pairs.
# String values are auto-escaped. Numeric/boolean values can be passed
# with the prefix "raw:" (e.g. "raw:42" or "raw:true").
emit_json() {
  local out="{" first=1
  while [ $# -ge 2 ]; do
    local k="$1" v="$2"; shift 2
    [ "$first" = 1 ] && first=0 || out+=","
    out+="\"$k\":"
    if [[ "$v" == raw:* ]]; then
      out+="${v#raw:}"
    else
      out+=$(json_escape "$v")
    fi
  done
  out+="}"
  printf '%s\n' "$out"
}

# ---------- Output ----------
die() {
  local msg="$*"
  log ERROR "$msg"
  if [ "$OCE_JSON_MODE" = "1" ]; then
    emit_json status error message "$msg" >&2
  else
    printf '%sERROR:%s %s\n' "$C_RED" "$C_RESET" "$msg" >&2
  fi
  exit 1
}

success() {
  local msg="$*"
  log SUCCESS "$msg"
  if [ "$OCE_JSON_MODE" = "1" ]; then
    emit_json status success message "$msg"
  else
    printf '%s✓%s %s\n' "$C_GREEN" "$C_RESET" "$msg"
  fi
}

warn() {
  local msg="$*"
  log WARN "$msg"
  if [ "$OCE_JSON_MODE" = "1" ]; then
    emit_json status warning message "$msg" >&2
  else
    printf '%s⚠%s  %s\n' "$C_YELLOW" "$C_RESET" "$msg" >&2
  fi
}

info() {
  [ "$OCE_JSON_MODE" = "1" ] && return 0
  printf '%s%s%s\n' "$C_DIM" "$*" "$C_RESET"
}

# ---------- File guards ----------
require_file() {
  local f="$1"
  [ -f "$f" ] || die "File not found: $f"
  [ -r "$f" ] || die "File not readable: $f"
}

require_writable() {
  local f="$1"
  if [ -e "$f" ]; then
    [ -w "$f" ] || die "File not writable: $f"
  else
    local dir; dir="$(dirname "$f")"
    [ -w "$dir" ] || die "Directory not writable: $dir"
  fi
}

# Refuse binary files and oversized files. Warns about lock files.
preflight_check() {
  local file="$1"
  require_file "$file"

  # Binary detection: look for NUL bytes in the first 8KB. Use Node since
  # bash strings can't reliably hold NULs and `file` may not be installed.
  if node -e "
    const fs=require('fs');
    const buf=Buffer.alloc(8192);
    const fd=fs.openSync(process.argv[1],'r');
    const n=fs.readSync(fd,buf,0,8192,0);
    fs.closeSync(fd);
    process.exit(buf.slice(0,n).includes(0) ? 0 : 1);
  " "$file" 2>/dev/null; then
    die "Refusing to edit binary file: $file"
  fi

  local size
  size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null || wc -c < "$file")
  local max_size="${OCE_MAX_FILE_SIZE:-5242880}"
  if [ "$size" -gt "$max_size" ]; then
    die "File too large ($size bytes > $max_size). Set OCE_MAX_FILE_SIZE to override."
  fi

  if [ -e "${file}.swp" ] || [ -e "${file}.lock" ]; then
    warn "Lock file detected near $file — another process may be editing it"
  fi
}

# ---------- Backups ----------
# Encode an absolute path into a single safe filename
_encode_path() {
  local p; p="$(cd -P "$(dirname "$1")" 2>/dev/null && pwd)/$(basename "$1")"
  printf '%s' "${p//\//__}"
}

create_backup() {
  local file="$1"
  require_file "$file"
  local hash ts encoded backup_path
  hash=$(sha256sum "$file" | cut -c1-12)
  ts=$(date +%Y%m%d-%H%M%S)
  encoded=$(_encode_path "$file")
  backup_path="$OCE_BACKUP_DIR/${encoded}.${ts}.${hash}.bak"
  cp -p "$file" "$backup_path"
  printf '%s\n' "$backup_path"
}

# List backups for a file, newest first
list_backups() {
  local file="$1"
  local encoded; encoded=$(_encode_path "$file")
  ls -t "$OCE_BACKUP_DIR"/"${encoded}".*.bak 2>/dev/null || true
}

# ---------- Language detection ----------
detect_language() {
  local file="$1"
  local base; base="$(basename "$file")"
  local ext="${base##*.}"
  # Lowercase
  ext="${ext,,}"
  case "$ext" in
    js|mjs|cjs)        echo "javascript" ;;
    ts)                echo "typescript" ;;
    tsx)               echo "tsx" ;;
    jsx)               echo "jsx" ;;
    vue)               echo "vue" ;;
    svelte)            echo "svelte" ;;
    py|pyi)            echo "python" ;;
    rb)                echo "ruby" ;;
    go)                echo "go" ;;
    rs)                echo "rust" ;;
    java)              echo "java" ;;
    kt|kts)            echo "kotlin" ;;
    swift)             echo "swift" ;;
    c|h)               echo "c" ;;
    cpp|cc|cxx|hpp|hh) echo "cpp" ;;
    cs)                echo "csharp" ;;
    sh|bash)           echo "bash" ;;
    zsh)               echo "zsh" ;;
    php)               echo "php" ;;
    json)              echo "json" ;;
    jsonc|json5)       echo "jsonc" ;;
    yaml|yml)          echo "yaml" ;;
    toml)              echo "toml" ;;
    xml)               echo "xml" ;;
    html|htm)          echo "html" ;;
    css)               echo "css" ;;
    scss|sass)         echo "scss" ;;
    less)              echo "less" ;;
    md|markdown|mdx)   echo "markdown" ;;
    sql)               echo "sql" ;;
    dockerfile)        echo "dockerfile" ;;
    *)
      # Filename-based fallback
      case "$base" in
        Dockerfile*|dockerfile*) echo "dockerfile" ;;
        Makefile|makefile|GNUmakefile) echo "makefile" ;;
        *.config.*) echo "javascript" ;;
        *) echo "unknown" ;;
      esac
      ;;
  esac
}

count_lines() {
  awk 'END{print NR}' "$1"
}

# Parse common flags from an arg list.
# Mutates the global OCE_JSON_MODE / OCE_DRY_RUN; returns the remaining
# args in a global array OCE_ARGS.
parse_global_flags() {
  OCE_ARGS=()
  while [ $# -gt 0 ]; do
    case "$1" in
      --json)    OCE_JSON_MODE=1; shift ;;
      --dry-run) OCE_DRY_RUN=1; shift ;;
      --no-color) C_RED="" C_GREEN="" C_YELLOW="" C_BLUE="" C_DIM="" C_RESET=""; shift ;;
      *) OCE_ARGS+=("$1"); shift ;;
    esac
  done
}
