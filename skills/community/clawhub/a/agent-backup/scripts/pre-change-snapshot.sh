#!/usr/bin/env bash
set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
BACKUP_DIR="${BACKUP_DIR:-$OPENCLAW_DIR/backups}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_SCRIPT="$SCRIPT_DIR/backup.sh"

warn() { printf 'WARNING: %s\n' "$*" >&2; }
info() { printf '%s\n' "$*"; }
die() { warn "$*"; exit 1; }

[ -x "$BACKUP_SCRIPT" ] || die "backup.sh is required and must be executable: $BACKUP_SCRIPT"
command -v python3 >/dev/null 2>&1 || die "python3 is required"
mkdir -p "$BACKUP_DIR"

TMP_OUTPUT="$(mktemp "${TMPDIR:-/tmp}/openclaw-snapshot.XXXXXX")"
STAGE_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/openclaw-snapshot-stage.XXXXXX")"
trap 'rm -f "$TMP_OUTPUT"; rm -rf "$STAGE_ROOT"' EXIT

bash "$BACKUP_SCRIPT" --no-secrets --output-dir "$STAGE_ROOT" >"$TMP_OUTPUT"

STAGED_RUN_DIR="$(sed -n 's/^Created manifest: //p' "$TMP_OUTPUT" | tail -n 1 | xargs dirname)"
MANIFEST_PATH="$(sed -n 's/^Created manifest: //p' "$TMP_OUTPUT" | tail -n 1)"
OP_ARCHIVE="$(sed -n 's/^Created operational archive: //p' "$TMP_OUTPUT" | tail -n 1)"

[ -n "$STAGED_RUN_DIR" ] || die "Could not determine backup run directory"
[ -f "$MANIFEST_PATH" ] || die "Manifest missing after snapshot creation"
[ -f "$OP_ARCHIVE" ] || die "Operational archive missing after snapshot creation"

TIMESTAMP="$(date +%Y-%m-%d_%H%M%S)"
RUN_DIR="$BACKUP_DIR/pre-change-$TIMESTAMP"
mkdir -p "$RUN_DIR"
SNAPSHOT_NAME="openclaw-snapshot-pre-change-$TIMESTAMP.tar.gz"
SNAPSHOT_PATH="$RUN_DIR/$SNAPSHOT_NAME"
mv "$OP_ARCHIVE" "$SNAPSHOT_PATH"

FINAL_MANIFEST="$RUN_DIR/manifest.json"
python3 - "$MANIFEST_PATH" "$FINAL_MANIFEST" "$SNAPSHOT_NAME" <<'PY'
import json, sys
from pathlib import Path
source_manifest, final_manifest, snapshot_name = sys.argv[1:4]
data = json.loads(Path(source_manifest).read_text(encoding='utf-8'))
if 'archives' in data and 'operational' in data['archives']:
    data['archives']['operational']['file'] = snapshot_name
Path(final_manifest).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')
PY

python3 - "$BACKUP_DIR" <<'PY'
from pathlib import Path
import shutil, sys
root = Path(sys.argv[1])
snapshots = []
for run_dir in root.iterdir():
    if not run_dir.is_dir():
        continue
    for archive in run_dir.glob('openclaw-snapshot-pre-change-*.tar.gz'):
        snapshots.append((archive.stat().st_mtime, run_dir, archive))
snapshots.sort(reverse=True)
for _, run_dir, archive in snapshots[5:]:
    shutil.rmtree(run_dir, ignore_errors=True)
PY

info "Snapshot ready ✅"
info "Path: $SNAPSHOT_PATH"
info "Rollback ref: $RUN_DIR"
