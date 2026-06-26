#!/usr/bin/env sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

python3 -m pytest -q tests
python3 scripts/extract_isbn.py --self-check
python3 scripts/resolve_metadata.py --self-check
python3 scripts/upsert_obsidian_note.py --self-check
python3 scripts/ingest_photo.py --self-check
python3 scripts/migrate_goodreads_csv.py --self-check
python3 scripts/generate_dashboard.py --self-check

sh scripts/security_scan_no_pii.sh

echo "CI checks passed"
