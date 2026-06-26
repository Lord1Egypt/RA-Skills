#!/usr/bin/env bash
set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
BACKUP_DIR="${BACKUP_DIR:-$OPENCLAW_DIR/backups}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERIFY_SCRIPT="$SCRIPT_DIR/verify.sh"

warn() { printf 'WARNING: %s\n' "$*" >&2; }
info() { printf '%s\n' "$*"; }
die() { warn "$*"; exit 1; }

command -v python3 >/dev/null 2>&1 || die "python3 is required"
[ -x "$VERIFY_SCRIPT" ] || die "verify.sh is required and must be executable: $VERIFY_SCRIPT"

mkdir -p "$BACKUP_DIR"

TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/openclaw-weekly-verify.XXXXXX")"
trap 'rm -rf "$TMP_DIR"' EXIT

METRICS_JSON="$TMP_DIR/metrics.json"
PRUNE_JSON="$TMP_DIR/prune.json"
ORPHAN_JSON="$TMP_DIR/orphans.json"
RUNS_TSV="$TMP_DIR/runs.tsv"
PRUNE_LIST="$TMP_DIR/prune.list"

printf '{"total":0,"ok":0,"failed":0,"missing_manifest":0}' > "$METRICS_JSON"
printf '{"deleted_runs":0}' > "$PRUNE_JSON"
printf '{"manifests_without_archives":0,"secrets_without_manifests":0}' > "$ORPHAN_JSON"
: > "$RUNS_TSV"
: > "$PRUNE_LIST"

update_metric() {
  python3 - "$METRICS_JSON" "$1" <<'PY'
import json, sys
path, key = sys.argv[1:3]
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
data[key] = int(data.get(key, 0)) + 1
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f)
PY
}

update_prune() {
  python3 - "$PRUNE_JSON" "$1" <<'PY'
import json, sys
path, key = sys.argv[1:3]
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
data[key] = int(data.get(key, 0)) + 1
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f)
PY
}

update_orphan() {
  python3 - "$ORPHAN_JSON" "$1" <<'PY'
import json, sys
path, key = sys.argv[1:3]
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
data[key] = int(data.get(key, 0)) + 1
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f)
PY
}

find_run_archive() {
  find "$1" -maxdepth 1 -type f \( -name 'openclaw-backup-*.tar.gz' -o -name 'openclaw-snapshot-pre-change-*.tar.gz' \) | sort | head -n 1
}

find_run_secrets() {
  find "$1" -maxdepth 1 -type f -name 'openclaw-secrets-*.tar.gz.age' | sort | head -n 1
}

collect_runs() {
  find "$BACKUP_DIR" -mindepth 1 -maxdepth 1 -type d | while IFS= read -r run_dir; do
    manifest="$run_dir/manifest.json"
    if [ ! -f "$manifest" ]; then
      update_metric missing_manifest
      continue
    fi

    update_metric total
    archive="$(find_run_archive "$run_dir")"
    secrets="$(find_run_secrets "$run_dir")"

    if [ -z "$archive" ]; then
      update_metric failed
      continue
    fi

    if [ -n "$secrets" ]; then
      if bash "$VERIFY_SCRIPT" --manifest "$manifest" --archive "$archive" --secrets "$secrets" >/dev/null 2>&1; then
        update_metric ok
      else
        update_metric failed
      fi
    else
      if bash "$VERIFY_SCRIPT" --manifest "$manifest" --archive "$archive" >/dev/null 2>&1; then
        update_metric ok
      else
        update_metric failed
      fi
    fi

    ts="$(python3 - "$manifest" <<'PY'
import json, sys
from pathlib import Path
try:
    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
except Exception:
    print('')
    raise SystemExit(0)
print(data.get('timestamp', ''))
PY
)"
    if [ -n "$ts" ]; then
      printf '%s\t%s\n' "$ts" "$run_dir" >> "$RUNS_TSV"
    fi
  done
}

collect_runs

python3 - "$RUNS_TSV" "$PRUNE_LIST" <<'PY'
import datetime as dt
import sys
from collections import OrderedDict
from pathlib import Path

runs_file, out_file = sys.argv[1:3]
entries = []
for line in Path(runs_file).read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    ts, run_dir = line.split('\t', 1)
    try:
        when = dt.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        continue
    entries.append((when, run_dir))
entries.sort(reverse=True)

keep = set()
for _, run_dir in entries[:14]:
    keep.add(run_dir)

weekly = OrderedDict()
monthly = OrderedDict()
for when, run_dir in entries:
    iso_year, iso_week, _ = when.isocalendar()
    weekly.setdefault((iso_year, iso_week), run_dir)
    monthly.setdefault((when.year, when.month), run_dir)

for run_dir in list(weekly.values())[:8]:
    keep.add(run_dir)
for run_dir in list(monthly.values())[:6]:
    keep.add(run_dir)

with open(out_file, 'w', encoding='utf-8') as f:
    for _, run_dir in entries:
        if run_dir not in keep:
            f.write(run_dir + '\n')
PY

while IFS= read -r prune_dir; do
  [ -n "$prune_dir" ] || continue
  if [ -d "$prune_dir" ]; then
    rm -rf "$prune_dir"
    update_prune deleted_runs
  fi
done < "$PRUNE_LIST"

find "$BACKUP_DIR" -mindepth 1 -maxdepth 1 -type d | while IFS= read -r run_dir; do
  manifest="$run_dir/manifest.json"
  archive="$(find_run_archive "$run_dir")"

  if [ -f "$manifest" ] && [ -z "$archive" ]; then
    rm -f "$manifest"
    update_orphan manifests_without_archives
  fi

  if [ ! -f "$manifest" ]; then
    find "$run_dir" -maxdepth 1 -type f -name 'openclaw-secrets-*.tar.gz.age' | while IFS= read -r orphan_secret; do
      rm -f "$orphan_secret"
      update_orphan secrets_without_manifests
    done
  fi

done

metrics_line="$(python3 - "$METRICS_JSON" "$PRUNE_JSON" "$ORPHAN_JSON" <<'PY'
import json, sys
m = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
p = json.load(open(sys.argv[2], 'r', encoding='utf-8'))
o = json.load(open(sys.argv[3], 'r', encoding='utf-8'))
status = '✅' if int(m.get('failed', 0)) == 0 and int(m.get('missing_manifest', 0)) == 0 else '⚠️'
print(status)
print(f"Archives: {m.get('total',0)} total | {m.get('ok',0)} OK | {m.get('failed',0)} failed | {m.get('missing_manifest',0)} missing manifest")
print(f"Cleanup: {p.get('deleted_runs',0)} pruned | {o.get('manifests_without_archives',0)} orphan manifests removed | {o.get('secrets_without_manifests',0)} orphan secrets removed")
PY
)"

status_icon="$(printf '%s' "$metrics_line" | sed -n '1p')"
summary_one="$(printf '%s' "$metrics_line" | sed -n '2p')"
summary_two="$(printf '%s' "$metrics_line" | sed -n '3p')"

info "${status_icon} Weekly backup verify"
info "$summary_one"
info "$summary_two"
