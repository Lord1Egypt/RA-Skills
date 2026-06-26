#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/config.env"
DEFAULT_OUT_DIR="$HOME/backups/openclaw-snapshots"
DEFAULT_PREFIX="occt7pkbak"
PACKAGE_MANIFEST_NAME="manifest.txt"
PACKAGE_CHECKSUM_NAME="SHA256SUMS"
RESTORE_SCRIPT_NAME="restore.sh"

CONFIG_OUT_DIR=""
CONFIG_PREFIX=""
if [[ -f "$CONFIG_FILE" ]]; then
  while IFS='=' read -r key value; do
    case "$key" in
      OPENCLAW_SNAPSHOT_DIR) CONFIG_OUT_DIR="${value//\$HOME/$HOME}" ;;
      OPENCLAW_SNAPSHOT_PREFIX) CONFIG_PREFIX="$value" ;;
    esac
  done < "$CONFIG_FILE"
fi

OUT_DIR="${CONFIG_OUT_DIR:-${OPENCLAW_SNAPSHOT_DIR:-$DEFAULT_OUT_DIR}}"
PREFIX="${CONFIG_PREFIX:-${OPENCLAW_SNAPSHOT_PREFIX:-$DEFAULT_PREFIX}}"

usage() {
  cat <<'EOF'
Usage: select_and_restore.sh [--out-dir DIR] [--prefix NAME]
EOF
}

require_value() {
  local option="$1"
  local value="${2-}"
  if [[ -z "$value" ]]; then
    echo "Missing value for $option" >&2
    usage >&2
    exit 1
  fi
}

audit_bundle_archive() {
  local archive_path="$1"
  local expected_prefix="$2"
  mapfile -t entries < <(tar -tvzf "$archive_path")
  if (( ${#entries[@]} == 0 )); then
    echo "Archive is empty: $archive_path" >&2
    exit 1
  fi

  local bundle_root=""
  local line type path rel rest first_component
  for line in "${entries[@]}"; do
    type="${line:0:1}"
    path="$(printf '%s\n' "$line" | awk '{for (i=6; i<=NF; i++) printf (i==6 ? "%s" : " %s"), $i; printf "\n"}')"
    [[ -n "$path" ]] || { echo "Archive contains malformed listing entry" >&2; exit 1; }
    if [[ "$path" == /* ]] || [[ "$path" == *".."* ]]; then
      echo "Archive contains unsafe path: $path" >&2
      exit 1
    fi
    case "$type" in
      d|-)
        ;;
      h)
        echo "Archive contains unsupported hard link entry: $path" >&2
        exit 1
        ;;
      *)
        echo "Archive contains unsupported entry type: $path" >&2
        exit 1
        ;;
    esac
    rel="${path#./}"
    first_component="${rel%%/*}"
    if [[ -z "$bundle_root" ]]; then
      bundle_root="$first_component"
      if [[ ! "$bundle_root" =~ ^${expected_prefix}-[0-9]{8}-[0-9]{6}/?$ && ! "$bundle_root" =~ ^${expected_prefix}-[0-9]{8}-[0-9]{6}$ ]]; then
        echo "Archive root does not match expected bundle naming: $bundle_root" >&2
        exit 1
      fi
    elif [[ "$first_component" != "$bundle_root" ]]; then
      echo "Archive contains multiple top-level roots" >&2
      exit 1
    fi
    if [[ "$rel" == "$bundle_root" || "$rel" == "$bundle_root/" ]]; then
      [[ "$type" == d ]] || { echo "Archive root must be a directory: $path" >&2; exit 1; }
      continue
    fi
    rest="${rel#${bundle_root}/}"
    case "$rest" in
      "$PACKAGE_MANIFEST_NAME"|"$PACKAGE_CHECKSUM_NAME"|"$RESTORE_SCRIPT_NAME")
        [[ "$type" == - ]] || { echo "Bundle metadata entry must be a regular file: $path" >&2; exit 1; }
        ;;
      .openclaw)
        [[ "$type" == d ]] || { echo "Bundled .openclaw root must be a directory: $path" >&2; exit 1; }
        ;;
      .openclaw/*)
        [[ "$type" == d || "$type" == - ]] || { echo "Bundled .openclaw contains unsupported entry type: $path" >&2; exit 1; }
        ;;
      *)
        echo "Archive contains unexpected entry: $path" >&2
        exit 1
        ;;
    esac
  done
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out-dir|--backup-dir)
      require_value "$1" "${2-}"
      OUT_DIR="$2"
      shift 2
      ;;
    --prefix)
      require_value "$1" "${2-}"
      PREFIX="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if ! [[ "$PREFIX" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "--prefix may contain only letters, digits, dot, underscore, and hyphen" >&2
  exit 1
fi

mapfile -t bundles < <(find "$OUT_DIR" -maxdepth 1 -type f -name "${PREFIX}-*.tar.gz" | sort -r)
if (( ${#bundles[@]} == 0 )); then
  echo "No backup bundles found in: $OUT_DIR" >&2
  exit 1
fi

printf 'Available backup bundles in %s\n\n' "$OUT_DIR"
for i in "${!bundles[@]}"; do
  file="${bundles[$i]}"
  mtime="$(date -d "@$(stat -c %Y "$file")" '+%Y-%m-%d %H:%M:%S')"
  size="$(du -h "$file" | cut -f1)"
  printf '%2d) %s  [%s, %s]\n' "$((i + 1))" "$(basename "$file")" "$mtime" "$size"
done

printf '\nChoose bundle number to extract: '
if ! read -r choice; then
  echo "No selection received" >&2
  exit 1
fi
if ! [[ "$choice" =~ ^[0-9]+$ ]]; then
  echo "Choice must be a number" >&2
  exit 1
fi
index=$((choice - 1))
if (( index < 0 || index >= ${#bundles[@]} )); then
  echo "Choice out of range" >&2
  exit 1
fi

selected="${bundles[$index]}"
audit_bundle_archive "$selected" "$PREFIX"
extract_dir="$(mktemp -d /tmp/openclaw-restore-bundle.XXXXXX)"
tar -C "$extract_dir" -xzf "$selected"
bundle_root="$(find "$extract_dir" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
if [[ -z "$bundle_root" || ! -f "$bundle_root/$RESTORE_SCRIPT_NAME" || ! -f "$bundle_root/$PACKAGE_MANIFEST_NAME" || ! -f "$bundle_root/$PACKAGE_CHECKSUM_NAME" ]]; then
  echo "Extracted bundle is incomplete" >&2
  exit 1
fi
if [[ ! -d "$bundle_root/.openclaw" ]]; then
  echo "Extracted bundle is missing .openclaw" >&2
  exit 1
fi
if [[ -L "$bundle_root" ]]; then
  echo "Refusing symbolic-link bundle root: $bundle_root" >&2
  exit 1
fi
if find "$bundle_root/.openclaw" -type l -print -quit | grep -q .; then
  echo "Refusing bundle with symbolic links in .openclaw" >&2
  exit 1
fi
if find "$bundle_root/.openclaw" \( -type b -o -type c -o -type p -o -type s \) -print -quit | grep -q .; then
  echo "Refusing bundle with special files in .openclaw" >&2
  exit 1
fi

printf 'Extracted to: %s\n' "$bundle_root"
printf 'Run this to restore:\n'
printf 'bash %q/%s\n' "$bundle_root" "$RESTORE_SCRIPT_NAME"
