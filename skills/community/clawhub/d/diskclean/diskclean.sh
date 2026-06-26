#!/usr/bin/env bash
set -uo pipefail

# diskclean - AI-assisted disk space scanner and cleaner
DATA_DIR="${HOME}/.openclaw/diskclean"
SCAN_DIR="${DATA_DIR}/scans"
LOG_FILE="${DATA_DIR}/deletion-log.jsonl"
SCAN_ROOT="${HOME}"

mkdir -p "$SCAN_DIR"

# --- Configuration ---
AGE_NODE_MODULES=7
AGE_BUILD_OUTPUT=7
AGE_PYTHON_CACHE=7
AGE_XCODE_DERIVED=7
AGE_PKG_CACHE=14
AGE_GO_CACHE=14
AGE_LOGS=30

NOW_EPOCH=$(date +%s)

# --- Helpers ---

now_iso() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

dir_size_mb() {
  du -sm "$1" 2>/dev/null | cut -f1 || echo 0
}

file_size_mb() {
  local bytes
  bytes=$(stat -f%z "$1" 2>/dev/null || echo 0)
  echo $(( bytes / 1048576 ))
}

days_since_modified() {
  local mod_epoch
  mod_epoch=$(stat -f%m "$1" 2>/dev/null || echo "$NOW_EPOCH")
  echo $(( (NOW_EPOCH - mod_epoch) / 86400 ))
}

# Pure bash JSON escape (handles backslash, quotes, common control chars)
json_str() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\t'/\\t}"
  printf '"%s"' "$s"
}

emit_item() {
  local path="$1" category="$2" size_mb="$3" age_days="$4" tier="$5"
  local display_path="${path/#$HOME/~}"
  printf '{"path":%s,"category":"%s","size_mb":%d,"age_days":%d,"tier":"%s"}\n' \
    "$(json_str "$display_path")" "$category" "$size_mb" "$age_days" "$tier"
}

# --- Scanning Functions ---

scan_node_modules() {
  find "$SCAN_ROOT" -maxdepth 6 -type d -name "node_modules" \
    -not -path "*/node_modules/*/node_modules" \
    -not -path "*/Library/*" \
    -not -path "*/.Trash/*" \
    2>/dev/null | while read -r dir; do
    local parent
    parent="$(dirname "$dir")"
    [[ -f "${parent}/package.json" ]] || continue
    local size age tier
    size=$(dir_size_mb "$dir")
    age=$(days_since_modified "$dir")
    if (( age >= AGE_NODE_MODULES )); then tier="safe"; else tier="suggest"; fi
    emit_item "$dir" "node_modules" "$size" "$age" "$tier"
  done
}

scan_python_cache() {
  find "$SCAN_ROOT" -maxdepth 8 -type d \( -name "__pycache__" -o -name ".pytest_cache" \) \
    -not -path "*/Library/*" -not -path "*/.Trash/*" -not -path "*/node_modules/*" \
    2>/dev/null | while read -r dir; do
    local size age tier
    size=$(dir_size_mb "$dir")
    age=$(days_since_modified "$dir")
    if (( age >= AGE_PYTHON_CACHE )); then tier="safe"; else tier="suggest"; fi
    local cat_name="python_cache"
    [[ "$(basename "$dir")" == ".pytest_cache" ]] && cat_name="pytest_cache"
    emit_item "$dir" "$cat_name" "$size" "$age" "$tier"
  done
}

scan_build_outputs() {
  find "$SCAN_ROOT" -maxdepth 5 -type d \( -name "build" -o -name "dist" -o -name ".next" -o -name ".nuxt" -o -name "target" \) \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    -not -path "*/Library/*" \
    -not -path "*/.Trash/*" \
    2>/dev/null | while read -r dir; do
    local parent
    parent="$(dirname "$dir")"
    [[ -f "${parent}/package.json" ]] || [[ -f "${parent}/Makefile" ]] || \
    [[ -f "${parent}/Cargo.toml" ]] || [[ -f "${parent}/pom.xml" ]] || \
    [[ -f "${parent}/build.gradle" ]] || [[ -f "${parent}/pyproject.toml" ]] || \
    [[ -f "${parent}/go.mod" ]] || continue
    local size age tier
    size=$(dir_size_mb "$dir")
    (( size < 10 )) && continue
    age=$(days_since_modified "$dir")
    if (( age >= AGE_BUILD_OUTPUT )); then tier="safe"; else tier="suggest"; fi
    emit_item "$dir" "build_output" "$size" "$age" "$tier"
  done
}

scan_go_cache() {
  local cache_dir="${HOME}/go/pkg/mod/cache"
  if [[ -d "$cache_dir" ]]; then
    local size age tier
    size=$(dir_size_mb "$cache_dir")
    age=$(days_since_modified "$cache_dir")
    if (( age >= AGE_GO_CACHE )); then tier="safe"; else tier="suggest"; fi
    emit_item "$cache_dir" "go_cache" "$size" "$age" "$tier"
  fi
  local build_cache
  build_cache="$(go env GOCACHE 2>/dev/null || echo "${HOME}/Library/Caches/go-build")"
  if [[ -d "$build_cache" ]]; then
    local size age tier
    size=$(dir_size_mb "$build_cache")
    age=$(days_since_modified "$build_cache")
    if (( age >= AGE_GO_CACHE )); then tier="safe"; else tier="suggest"; fi
    emit_item "$build_cache" "go_build_cache" "$size" "$age" "$tier"
  fi
}

scan_homebrew_cache() {
  local cache_dir="${HOME}/Library/Caches/Homebrew"
  if [[ -d "$cache_dir" ]]; then
    local size age tier
    size=$(dir_size_mb "$cache_dir")
    age=$(days_since_modified "$cache_dir")
    if (( age >= AGE_PKG_CACHE )); then tier="safe"; else tier="suggest"; fi
    emit_item "$cache_dir" "homebrew_cache" "$size" "$age" "$tier"
  fi
}

scan_npm_yarn_pnpm_cache() {
  local -a dirs=(
    "${HOME}/.npm/_cacache"
    "${HOME}/Library/Caches/Yarn"
    "${HOME}/.local/share/pnpm/store"
    "${HOME}/.pnpm-store"
  )
  for cache_dir in "${dirs[@]}"; do
    if [[ -d "$cache_dir" ]]; then
      local size age tier
      size=$(dir_size_mb "$cache_dir")
      age=$(days_since_modified "$cache_dir")
      if (( age >= AGE_PKG_CACHE )); then tier="safe"; else tier="suggest"; fi
      emit_item "$cache_dir" "npm_yarn_pnpm_cache" "$size" "$age" "$tier"
    fi
  done
}

scan_pip_cache() {
  local cache_dir="${HOME}/Library/Caches/pip"
  if [[ -d "$cache_dir" ]]; then
    local size age tier
    size=$(dir_size_mb "$cache_dir")
    age=$(days_since_modified "$cache_dir")
    if (( age >= AGE_PKG_CACHE )); then tier="safe"; else tier="suggest"; fi
    emit_item "$cache_dir" "pip_cache" "$size" "$age" "$tier"
  fi
}

scan_xcode_derived() {
  local derived_dir="${HOME}/Library/Developer/Xcode/DerivedData"
  if [[ -d "$derived_dir" ]]; then
    local size age tier
    size=$(dir_size_mb "$derived_dir")
    age=$(days_since_modified "$derived_dir")
    if (( age >= AGE_XCODE_DERIVED )); then tier="safe"; else tier="suggest"; fi
    emit_item "$derived_dir" "xcode_derived" "$size" "$age" "$tier"
  fi
}

scan_docker() {
  command -v docker &>/dev/null || return
  # Use docker system df --format for clean parsing
  local reclaimable_mb=0
  while IFS=$'\t' read -r type total active size reclaimable; do
    # Parse reclaimable field (e.g., "1.2GB (50%)" or "500MB")
    local num unit
    num=$(echo "$reclaimable" | grep -oE '[0-9]+\.?[0-9]*' | head -1)
    unit=$(echo "$reclaimable" | grep -oE '[A-Za-z]+' | head -1)
    [[ -z "$num" ]] && continue
    case "$unit" in
      GB|gb) reclaimable_mb=$(( reclaimable_mb + ${num%.*} * 1024 )) ;;
      MB|mb) reclaimable_mb=$(( reclaimable_mb + ${num%.*} )) ;;
    esac
  done < <(docker system df --format "{{.Type}}\t{{.TotalCount}}\t{{.Active}}\t{{.Size}}\t{{.Reclaimable}}" 2>/dev/null || true)
  if (( reclaimable_mb > 0 )); then
    emit_item "docker://system" "docker" "$reclaimable_mb" "0" "suggest"
  fi
}

scan_downloads() {
  local downloads_dir="${HOME}/Downloads"
  [[ -d "$downloads_dir" ]] || return
  # Large files >100MB
  find "$downloads_dir" -maxdepth 2 -type f -size +100M 2>/dev/null | while read -r f; do
    local size age
    size=$(file_size_mb "$f")
    age=$(days_since_modified "$f")
    emit_item "$f" "large_download" "$size" "$age" "suggest"
  done
  # Installers/archives >10MB
  find "$downloads_dir" -maxdepth 2 -type f \( -name "*.dmg" -o -name "*.pkg" -o -name "*.zip" -o -name "*.tar.gz" -o -name "*.iso" \) 2>/dev/null | while read -r f; do
    local size age
    size=$(file_size_mb "$f")
    (( size < 10 )) && continue
    age=$(days_since_modified "$f")
    emit_item "$f" "installer_archive" "$size" "$age" "suggest"
  done
}

scan_logs_temp() {
  local logs_dir="${HOME}/Library/Logs"
  if [[ -d "$logs_dir" ]]; then
    local size
    size=$(dir_size_mb "$logs_dir")
    if (( size >= 50 )); then
      emit_item "$logs_dir" "logs" "$size" "999" "safe"
    fi
  fi
  local crash_dir="${HOME}/Library/Logs/DiagnosticReports"
  if [[ -d "$crash_dir" ]]; then
    local size
    size=$(dir_size_mb "$crash_dir")
    if (( size >= 10 )); then
      emit_item "$crash_dir" "crash_reports" "$size" "999" "safe"
    fi
  fi
  local tmp_user="/private/tmp/claude-$(id -u)"
  if [[ -d "$tmp_user" ]]; then
    local size
    size=$(dir_size_mb "$tmp_user")
    if (( size >= 50 )); then
      emit_item "$tmp_user" "tmp_files" "$size" "0" "suggest"
    fi
  fi
}

scan_ds_store() {
  local count
  count=$(find "$SCAN_ROOT" -maxdepth 6 -name ".DS_Store" -not -path "*/Library/*" 2>/dev/null | wc -l | tr -d ' ')
  if (( count > 0 )); then
    emit_item "${SCAN_ROOT}/**/.DS_Store" "ds_store" "0" "0" "safe"
  fi
}

scan_trash() {
  local trash_dir="${HOME}/.Trash"
  if [[ -d "$trash_dir" ]]; then
    local size
    size=$(dir_size_mb "$trash_dir")
    if (( size >= 10 )); then
      emit_item "$trash_dir" "trash" "$size" "0" "suggest"
    fi
  fi
}

scan_python_venvs() {
  find "$SCAN_ROOT" -maxdepth 5 -type d \( -name ".venv" -o -name "venv" \) \
    -not -path "*/Library/*" -not -path "*/.Trash/*" -not -path "*/node_modules/*" \
    2>/dev/null | while read -r dir; do
    [[ -f "${dir}/bin/python" ]] || [[ -f "${dir}/bin/python3" ]] || continue
    local size age
    size=$(dir_size_mb "$dir")
    (( size < 50 )) && continue
    age=$(days_since_modified "$dir")
    emit_item "$dir" "python_venv" "$size" "$age" "suggest"
  done
}

# --- Subcommands ---

cmd_scan() {
  local scan_file="${SCAN_DIR}/scan-$(date +%Y%m%d-%H%M%S).json"
  local items_file
  items_file=$(mktemp)

  echo "Scanning ${SCAN_ROOT}..." >&2

  {
    scan_node_modules
    scan_python_cache
    scan_python_venvs
    scan_build_outputs
    scan_go_cache
    scan_homebrew_cache
    scan_npm_yarn_pnpm_cache
    scan_pip_cache
    scan_xcode_derived
    scan_docker
    scan_downloads
    scan_logs_temp
    scan_ds_store
    scan_trash
  } > "$items_file"

  # Use single python3 call to compute totals and build JSON
  python3 -c "
import json, sys

items = []
for line in open('${items_file}'):
    line = line.strip()
    if line:
        items.append(json.loads(line))

safe_mb = sum(i['size_mb'] for i in items if i['tier'] == 'safe')
suggest_mb = sum(i['size_mb'] for i in items if i['tier'] == 'suggest')
total_mb = safe_mb + suggest_mb

# Sort by size descending
items.sort(key=lambda x: x['size_mb'], reverse=True)

report = {
    'scan_date': '$(now_iso)',
    'scan_root': '${SCAN_ROOT}',
    'total_reclaimable_mb': total_mb,
    'safe_tier_mb': safe_mb,
    'suggest_tier_mb': suggest_mb,
    'items': items
}

print(json.dumps(report, indent=2))
" > "$scan_file"

  rm -f "$items_file"
  cp "$scan_file" "${DATA_DIR}/latest-scan.json"
  cat "$scan_file"
  echo "Scan saved to: ${scan_file}" >&2
}

cmd_clean() {
  local dry_run=true
  for arg in "$@"; do
    case "$arg" in
      --confirm) dry_run=false ;;
      --dry) dry_run=true ;;
    esac
  done

  local scan_file="${DATA_DIR}/latest-scan.json"
  if [[ ! -f "$scan_file" ]]; then
    echo "No scan found. Run 'diskclean scan' first." >&2
    exit 1
  fi

  python3 -c "
import json, os, shutil, sys
from datetime import datetime, timezone

dry_run = $( [[ "$dry_run" == "true" ]] && echo "True" || echo "False" )
home = os.path.expanduser('~')
log_file = '${LOG_FILE}'

with open('${scan_file}') as f:
    data = json.load(f)

safe_items = [i for i in data['items'] if i['tier'] == 'safe']
safe_items.sort(key=lambda x: x['size_mb'], reverse=True)

freed_mb = 0
deleted = 0

for item in safe_items:
    path = item['path'].replace('~', home, 1)

    # Skip special entries
    if '**/' in path or path.startswith('docker://'):
        continue

    # GUARDRAIL: Must be under HOME
    if not path.startswith(home):
        print(f'GUARDRAIL: Skipping {path} (not under HOME)', file=sys.stderr)
        continue

    # GUARDRAIL: Never delete .git
    if '/.git' in path:
        print(f'GUARDRAIL: Skipping {path} (git directory)', file=sys.stderr)
        continue

    if dry_run:
        print(f'[DRY RUN] Would delete: {path} ({item[\"size_mb\"]}MB, {item[\"category\"]})', file=sys.stderr)
    else:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.isfile(path):
                os.remove(path)
            else:
                print(f'Skipped (not found): {path}', file=sys.stderr)
                continue
            print(f'Deleted: {path} ({item[\"size_mb\"]}MB)', file=sys.stderr)
            with open(log_file, 'a') as lf:
                lf.write(json.dumps({
                    'date': datetime.now(timezone.utc).isoformat(),
                    'path': item['path'],
                    'category': item['category'],
                    'size_mb': item['size_mb']
                }) + '\n')
        except Exception as e:
            print(f'Error deleting {path}: {e}', file=sys.stderr)
            continue

    freed_mb += item['size_mb']
    deleted += 1

action = 'dry_run' if dry_run else 'cleaned'
print(json.dumps({'action': action, 'freed_mb': freed_mb, 'item_count': deleted}))
"
}

cmd_report() {
  local scan_file="${DATA_DIR}/latest-scan.json"
  if [[ ! -f "$scan_file" ]]; then
    echo "No scan found. Run 'diskclean scan' first." >&2
    exit 1
  fi
  cat "$scan_file"
}

cmd_history() {
  python3 -c "
import json, os, glob

scans = []
for f in sorted(glob.glob('${SCAN_DIR}/scan-*.json')):
    with open(f) as fh:
        d = json.load(fh)
        scans.append({
            'date': d['scan_date'],
            'total_mb': d['total_reclaimable_mb'],
            'safe_mb': d['safe_tier_mb'],
            'suggest_mb': d['suggest_tier_mb']
        })

log_file = '${LOG_FILE}'
total_freed = 0
if os.path.exists(log_file):
    with open(log_file) as f:
        for line in f:
            if line.strip():
                total_freed += json.loads(line)['size_mb']

print(json.dumps({'scans': scans, 'total_freed_mb': total_freed}, indent=2))
"
}

# --- Main ---
case "${1:-help}" in
  scan)    cmd_scan ;;
  clean)   shift; cmd_clean "$@" ;;
  report)  cmd_report ;;
  history) cmd_history ;;
  help|*)
    cat >&2 <<'USAGE'
diskclean - AI-assisted disk space scanner and cleaner

Usage:
  diskclean scan              Full scan, outputs JSON report
  diskclean clean --dry       Preview safe-tier deletions (default)
  diskclean clean --confirm   Actually delete safe-tier items
  diskclean report            Show last scan results
  diskclean history           Show scan history and total freed
USAGE
    ;;
esac
