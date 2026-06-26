#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/config.env"
DEFAULT_OUT_DIR="$HOME/backups/openclaw-snapshots"
DEFAULT_SOURCE_DIR="$HOME/.openclaw"
DEFAULT_PREFIX="occt7pkbak"
DEFAULT_KEEP=5
PACKAGE_MANIFEST_NAME="manifest.txt"
PACKAGE_CHECKSUM_NAME="SHA256SUMS"
RESTORE_SCRIPT_NAME="restore.sh"

CONFIG_OUT_DIR=""
CONFIG_PREFIX=""
CONFIG_KEEP=""
if [[ -f "$CONFIG_FILE" ]]; then
  while IFS='=' read -r key value; do
    case "$key" in
      OPENCLAW_SNAPSHOT_DIR) CONFIG_OUT_DIR="${value//\$HOME/$HOME}" ;;
      OPENCLAW_SNAPSHOT_PREFIX) CONFIG_PREFIX="$value" ;;
      OPENCLAW_SNAPSHOT_KEEP) CONFIG_KEEP="$value" ;;
    esac
  done < "$CONFIG_FILE"
fi

OUT_DIR="${CONFIG_OUT_DIR:-${OPENCLAW_SNAPSHOT_DIR:-$DEFAULT_OUT_DIR}}"
SOURCE_DIR="${OPENCLAW_SOURCE_DIR:-$DEFAULT_SOURCE_DIR}"
PREFIX="${CONFIG_PREFIX:-${OPENCLAW_SNAPSHOT_PREFIX:-$DEFAULT_PREFIX}}"
KEEP_COUNT="${CONFIG_KEEP:-${OPENCLAW_SNAPSHOT_KEEP:-$DEFAULT_KEEP}}"

usage() {
  cat <<'EOF'
Usage: create_backup.sh [--out-dir DIR] [--source-dir DIR] [--keep N] [--prefix NAME]

Create a self-contained OpenClaw backup bundle.
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

validate_source_tree() {
  local root="$1"
  if find "$root" -type l -print -quit | grep -q .; then
    echo "Source directory contains symbolic links, which are not allowed in backup bundles" >&2
    exit 1
  fi
  if find "$root" \( -type b -o -type c -o -type p -o -type s \) -print -quit | grep -q .; then
    echo "Source directory contains special files, which are not allowed in backup bundles" >&2
    exit 1
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out-dir|--backup-dir)
      require_value "$1" "${2-}"
      OUT_DIR="$2"
      shift 2
      ;;
    --source-dir)
      require_value "$1" "${2-}"
      SOURCE_DIR="$2"
      shift 2
      ;;
    --keep)
      require_value "$1" "${2-}"
      KEEP_COUNT="$2"
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

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Source directory does not exist: $SOURCE_DIR" >&2
  exit 1
fi
validate_source_tree "$SOURCE_DIR"

if ! [[ "$KEEP_COUNT" =~ ^[0-9]+$ ]] || (( KEEP_COUNT < 1 )); then
  echo "--keep must be an integer greater than or equal to 1" >&2
  exit 1
fi
if ! [[ "$PREFIX" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "--prefix may contain only letters, digits, dot, underscore, and hyphen" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BUNDLE_NAME="${PREFIX}-${TIMESTAMP}"
ARCHIVE_BASENAME="${BUNDLE_NAME}.tar.gz"
ARCHIVE_PATH="$OUT_DIR/$ARCHIVE_BASENAME"
SOURCE_NAME="$(basename "$SOURCE_DIR")"
STAGING_DIR="$(mktemp -d)"
BUNDLE_DIR="$STAGING_DIR/$BUNDLE_NAME"
TMP_ARCHIVE="${ARCHIVE_PATH}.tmp"
cleanup() {
  rm -rf "$STAGING_DIR"
  rm -f "$TMP_ARCHIVE"
}
trap cleanup EXIT

mkdir -p "$BUNDLE_DIR/$SOURCE_NAME"
cp -a "$SOURCE_DIR/." "$BUNDLE_DIR/$SOURCE_NAME/"

cat > "$BUNDLE_DIR/$PACKAGE_MANIFEST_NAME" <<EOF
format=openclaw-backup-bundle-v1
bundle_name=$BUNDLE_NAME
prefix=$PREFIX
source_basename=$SOURCE_NAME
created_at=$TIMESTAMP
EOF

cat > "$BUNDLE_DIR/$RESTORE_SCRIPT_NAME" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

PACKAGE_MANIFEST_NAME="manifest.txt"
PACKAGE_CHECKSUM_NAME="SHA256SUMS"
RESTORE_SCRIPT_NAME="restore.sh"
DEFAULT_TARGET_DIR="$HOME/.openclaw"
FORCE=0
NO_BACKUP=0
TARGET_DIR="${OPENCLAW_RESTORE_TARGET:-$DEFAULT_TARGET_DIR}"

usage() {
  cat <<'USAGE'
Usage: bash restore.sh [--target-dir DIR] [--force] [--no-backup]
USAGE
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

is_dangerous_target() {
  local path="$1"
  case "$path" in
    ""|/|.|..)
      return 0
      ;;
  esac
  local resolved
  resolved="$(realpath -m "$path")"
  local home_dir
  home_dir="$(realpath -m "$HOME")"
  case "$resolved" in
    /|"$home_dir")
      return 0
      ;;
  esac
  return 1
}

safe_create_checksum() {
  local archive_path="$1"
  local checksum_path="$2"
  local digest
  digest="$(sha256sum "$archive_path" | awk '{print $1}')"
  printf '%s  %s\n' "$digest" "$(basename "$archive_path")" > "$checksum_path"
}

require_physical_directory() {
  local dir="$1"
  if [[ ! -d "$dir" ]]; then
    return 1
  fi
  if [[ -L "$dir" ]]; then
    echo "Refusing symbolic-link directory: $dir" >&2
    exit 1
  fi
}

validate_bundle_layout() {
  local root="$1"
  local expected_source="$2"
  mapfile -t top_entries < <(find "$root" -mindepth 1 -maxdepth 1 -printf '%P\n' | LC_ALL=C sort)
  mapfile -t expected < <(printf '%s\n' "$PACKAGE_CHECKSUM_NAME" "$PACKAGE_MANIFEST_NAME" "$RESTORE_SCRIPT_NAME" "$expected_source" | LC_ALL=C sort)
  if (( ${#top_entries[@]} != ${#expected[@]} )); then
    echo "Unexpected bundle layout at: $root" >&2
    exit 1
  fi
  local i
  for i in "${!expected[@]}"; do
    if [[ "${top_entries[$i]}" != "${expected[$i]}" ]]; then
      echo "Unexpected bundle entry: ${top_entries[$i]}" >&2
      exit 1
    fi
  done
  if [[ ! -d "$root/$expected_source" ]]; then
    echo "Bundled source directory missing: $expected_source" >&2
    exit 1
  fi
  if find "$root/$expected_source" -type l -print -quit | grep -q .; then
    echo "Bundled source directory contains symbolic links, refusing restore" >&2
    exit 1
  fi
  if find "$root/$expected_source" \( -type b -o -type c -o -type p -o -type s \) -print -quit | grep -q .; then
    echo "Bundled source directory contains special files, refusing restore" >&2
    exit 1
  fi
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-dir)
      require_value "$1" "${2-}"
      TARGET_DIR="$2"
      shift 2
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --no-backup)
      NO_BACKUP=1
      shift
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

if [[ ! -f "$SCRIPT_DIR/$PACKAGE_MANIFEST_NAME" ]]; then
  echo "Manifest file not found: $SCRIPT_DIR/$PACKAGE_MANIFEST_NAME" >&2
  exit 1
fi
if [[ ! -f "$SCRIPT_DIR/$PACKAGE_CHECKSUM_NAME" ]]; then
  echo "Checksum file not found: $SCRIPT_DIR/$PACKAGE_CHECKSUM_NAME" >&2
  exit 1
fi
if [[ ! -f "$SCRIPT_DIR/$RESTORE_SCRIPT_NAME" ]]; then
  echo "Restore script not found in bundle" >&2
  exit 1
fi

manifest_format="$(awk -F= '$1=="format" {print $2}' "$SCRIPT_DIR/$PACKAGE_MANIFEST_NAME" | tail -n 1)"
manifest_bundle_name="$(awk -F= '$1=="bundle_name" {print $2}' "$SCRIPT_DIR/$PACKAGE_MANIFEST_NAME" | tail -n 1)"
manifest_prefix="$(awk -F= '$1=="prefix" {print $2}' "$SCRIPT_DIR/$PACKAGE_MANIFEST_NAME" | tail -n 1)"
manifest_source_basename="$(awk -F= '$1=="source_basename" {print $2}' "$SCRIPT_DIR/$PACKAGE_MANIFEST_NAME" | tail -n 1)"
manifest_created_at="$(awk -F= '$1=="created_at" {print $2}' "$SCRIPT_DIR/$PACKAGE_MANIFEST_NAME" | tail -n 1)"

if [[ "$manifest_format" != "openclaw-backup-bundle-v1" ]]; then
  echo "Unsupported bundle format: ${manifest_format:-missing}" >&2
  exit 1
fi
if [[ -z "$manifest_bundle_name" || "$manifest_bundle_name" != "$(basename "$SCRIPT_DIR")" ]]; then
  echo "Bundle name mismatch in manifest" >&2
  exit 1
fi
if [[ -z "$manifest_prefix" || ! "$manifest_prefix" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "Invalid prefix in manifest" >&2
  exit 1
fi
if [[ -z "$manifest_source_basename" ]]; then
  echo "Missing source_basename in manifest" >&2
  exit 1
fi
if [[ -z "$manifest_created_at" || ! "$manifest_created_at" =~ ^[0-9]{8}-[0-9]{6}$ ]]; then
  echo "Invalid created_at in manifest" >&2
  exit 1
fi

validate_bundle_layout "$SCRIPT_DIR" "$manifest_source_basename"

if is_dangerous_target "$TARGET_DIR"; then
  echo "Refusing dangerous target directory: $TARGET_DIR" >&2
  exit 1
fi

PARENT_DIR="$(dirname "$TARGET_DIR")"
TARGET_NAME="$(basename "$TARGET_DIR")"
if [[ "$TARGET_NAME" != "$manifest_source_basename" ]]; then
  echo "Target basename mismatch: target=$TARGET_NAME bundle=$manifest_source_basename" >&2
  exit 1
fi

if [[ -e "$PARENT_DIR" ]]; then
  require_physical_directory "$PARENT_DIR"
else
  if (( FORCE == 0 )); then
    echo "Target parent directory does not exist: $PARENT_DIR" >&2
    echo "Use --force to create the parent path first" >&2
    exit 1
  fi
  mkdir -p "$PARENT_DIR"
  require_physical_directory "$PARENT_DIR"
fi

if [[ -e "$TARGET_DIR" && -L "$TARGET_DIR" ]]; then
  echo "Refusing symbolic-link target directory: $TARGET_DIR" >&2
  exit 1
fi

if grep -Evq '^[0-9a-f]{64}  [^[:space:]].*$' "$SCRIPT_DIR/$PACKAGE_CHECKSUM_NAME"; then
  echo "Checksum file contains malformed entries" >&2
  exit 1
fi
(cd "$SCRIPT_DIR" && sha256sum -c "$PACKAGE_CHECKSUM_NAME")

TIMESTAMP="$(date +%Y%m%d-%H%M%S)-$$"
ROLLBACK_DIR="${PARENT_DIR}/.${TARGET_NAME}.rollback.${TIMESTAMP}"
RESTORE_SOURCE_DIR="$SCRIPT_DIR/$manifest_source_basename"
RESTORE_TARGET_PATH="${PARENT_DIR}/$TARGET_NAME"
restore_failure_cleanup() {
  if [[ -d "$ROLLBACK_DIR" ]]; then
    rm -rf "$RESTORE_TARGET_PATH"
    mv "$ROLLBACK_DIR" "$RESTORE_TARGET_PATH"
  fi
}
trap restore_failure_cleanup EXIT

if [[ -e "$RESTORE_TARGET_PATH" ]]; then
  if [[ ! -d "$RESTORE_TARGET_PATH" ]]; then
    echo "Target exists but is not a directory: $RESTORE_TARGET_PATH" >&2
    exit 1
  fi
  if (( NO_BACKUP == 0 )) && [[ -n "$(find "$RESTORE_TARGET_PATH" -mindepth 1 -maxdepth 1 2>/dev/null)" ]]; then
    BACKUP_PATH="${PARENT_DIR}/pre-restore-backup-${TIMESTAMP}.tar.gz"
    tar -C "$PARENT_DIR" -czf "$BACKUP_PATH" "$TARGET_NAME"
    safe_create_checksum "$BACKUP_PATH" "${BACKUP_PATH}.sha256"
    printf 'Created pre-restore backup: %s\n' "$BACKUP_PATH"
  fi
  mv "$RESTORE_TARGET_PATH" "$ROLLBACK_DIR"
fi

cp -a "$RESTORE_SOURCE_DIR" "$RESTORE_TARGET_PATH"
if [[ -d "$ROLLBACK_DIR" ]]; then
  rm -rf "$ROLLBACK_DIR"
fi

trap - EXIT
printf 'Restore complete: %s\n' "$RESTORE_TARGET_PATH"
EOF
chmod +x "$BUNDLE_DIR/$RESTORE_SCRIPT_NAME"

(
  cd "$BUNDLE_DIR"
  find "$SOURCE_NAME" -type f -print0 | sort -z | xargs -0 sha256sum > "$PACKAGE_CHECKSUM_NAME"
  sha256sum "$RESTORE_SCRIPT_NAME" "$PACKAGE_MANIFEST_NAME" >> "$PACKAGE_CHECKSUM_NAME"
)

tar -C "$STAGING_DIR" -czf "$TMP_ARCHIVE" "$BUNDLE_NAME"
mv "$TMP_ARCHIVE" "$ARCHIVE_PATH"

mapfile -t archives < <(find "$OUT_DIR" -maxdepth 1 -type f -name "${PREFIX}-*.tar.gz" -printf '%f\n' | sort -r)
if (( ${#archives[@]} > KEEP_COUNT )); then
  for old_archive in "${archives[@]:KEEP_COUNT}"; do
    rm -f "$OUT_DIR/$old_archive"
  done
fi

trap - EXIT
cleanup
printf 'Created backup bundle: %s\n' "$ARCHIVE_PATH"
printf 'Bundle root: %s\n' "$BUNDLE_NAME"
printf 'Retention count: %s\n' "$KEEP_COUNT"
