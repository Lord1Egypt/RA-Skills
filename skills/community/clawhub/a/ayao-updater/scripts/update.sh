#!/usr/bin/env bash
# openclaw-auto-update/scripts/update.sh
# Automatically updates OpenClaw and installed skills.
# Uses the built-in OpenClaw updater, handles conflicts, respects skiplist,
# and sends notifications.
#
# Usage:
#   ./update.sh [--dry-run] [--config /path/to/config.json]
#
# Config file (JSON): See references/config-schema.md for all options.

set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 required" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${OPENCLAW_UPDATE_CONFIG:-$HOME/.openclaw/workspace/skills/openclaw-auto-update/config.json}"
LOG_FILE="/tmp/openclaw-auto-update.log"
DRY_RUN=false

# ── Parse args ───────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --config=*)
      CONFIG_FILE="${1#--config=}"
      shift
      ;;
    --config)
      CONFIG_FILE="${2:?--config requires a value}"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

# ── Logging ──────────────────────────────────────────────────────────────────
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
log_section() { log ""; log "═══ $* ═══"; }

# ── Load config ──────────────────────────────────────────────────────────────
load_config() {
  python3 - "$CONFIG_FILE" <<'PYEOF'
import json
import os
import sys

default = {
    "skipSkills": [],
    "skipPreRelease": True,
    "restartGateway": True,
    "notify": True,
    "dryRun": False,
    "notifyTarget": None
}
cfg = default.copy()
config_path = os.path.expanduser(sys.argv[1])
if os.path.exists(config_path):
    try:
        with open(config_path) as f:
            user = json.load(f)
        cfg.update(user)
    except Exception as e:
        print(f"WARN: Failed to load config: {e}", file=sys.stderr)
for k, v in cfg.items():
    print(f"{k}={json.dumps(v)}")
PYEOF
}

# Parse config into shell variables
eval "$(load_config | python3 -c "
import json
import shlex
import sys

for line in sys.stdin:
    k, _, v = line.partition('=')
    v = v.strip()
    val = json.loads(v)
    name = f'CONFIG_{k.upper()}'
    if isinstance(val, list):
        items = ' '.join(shlex.quote(str(item)) for item in val)
        print(f'{name}=({items})')
    elif isinstance(val, bool):
        print(f'{name}={\"true\" if val else \"false\"}')
    else:
        rendered = '' if val is None else shlex.quote(str(val))
        print(f'{name}={rendered}')
" 2>/dev/null)"

# CLI --dry-run overrides config
[[ "$DRY_RUN" == "true" ]] && CONFIG_DRYRUN=true

# ── Notify helper ─────────────────────────────────────────────────────────────
notify() {
  local msg="$1"
  [[ "$CONFIG_NOTIFY" != "true" ]] && return 0
  local target="${CONFIG_NOTIFYTARGET:-}"
  if [[ -n "$target" ]]; then
    openclaw message send --target "$target" -m "$msg" 2>/dev/null || true
  else
    openclaw system event --text "$msg" --mode now 2>/dev/null || true
  fi
}

# ── Check if skill is in skiplist ─────────────────────────────────────────────
is_skipped() {
  local skill="$1"
  local skip
  for skip in "${CONFIG_SKIPSKILLS[@]:-}"; do
    [[ -z "$skip" ]] && continue
    [[ "$skill" == "$skip" ]] && return 0
  done
  return 1
}

# ── Detect locally modified skills ───────────────────────────────────────────
is_locally_modified() {
  local skill_dir="$1"
  # If skill dir is inside a git repo with uncommitted changes, skip it
  if git -C "$skill_dir" rev-parse --git-dir &>/dev/null 2>&1; then
    if [[ -n "$(git -C "$skill_dir" status --porcelain 2>/dev/null)" ]]; then
      return 0  # modified
    fi
  fi
  return 1  # not modified
}

# ── Enumerate installed skills ────────────────────────────────────────────────
list_installed_skills() {
  local listed=false

  while IFS= read -r line; do
    if [[ "$line" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
      echo "$line"
      listed=true
      continue
    fi

    if [[ "$line" =~ ^([a-z0-9][a-z0-9-]*)[[:space:]]+ ]]; then
      echo "${BASH_REMATCH[1]}"
      listed=true
    fi
  done < <(clawhub list 2>/dev/null || true)

  if [[ "$listed" == "true" ]]; then
    return 0
  fi

  local workspace_skills_dir="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}/skills"
  if [[ -d "$workspace_skills_dir" ]]; then
    find "$workspace_skills_dir" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; 2>/dev/null | sort -u
  fi
}

# ── Parse version from clawhub inspect output ────────────────────────────────
parse_inspect_version() {
  python3 -c '
import json
import re
import sys

text = sys.stdin.read().strip()
version_re = re.compile(r"\b\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?\b")

def find_version(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() == "version":
                match = version_re.search(str(item))
                if match:
                    return match.group(0)
            nested = find_version(item)
            if nested:
                return nested
        return None
    if isinstance(value, list):
        for item in value:
            nested = find_version(item)
            if nested:
                return nested
        return None
    match = version_re.search(str(value))
    return match.group(0) if match else None

if text:
    try:
        parsed = json.loads(text)
    except Exception:
        parsed = None

    if parsed is not None:
        version = find_version(parsed)
        if version:
            print(version)
            sys.exit(0)

    for line in text.splitlines():
        if "version" not in line.lower():
            continue
        match = version_re.search(line)
        if match:
            print(match.group(0))
            sys.exit(0)

    match = version_re.search(text)
    if match:
        print(match.group(0))
'
}

# ── Main ──────────────────────────────────────────────────────────────────────
main() {
  log_section "OpenClaw Auto Update"
  [[ "$CONFIG_DRYRUN" == "true" ]] && log "⚠️  DRY RUN MODE — no changes will be made"

  local openclaw_version_before
  openclaw_version_before=$(openclaw --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "unknown")
  log "Current OpenClaw version: $openclaw_version_before"

  # ── Update OpenClaw ───────────────────────────────────────────────────────
  log_section "Updating OpenClaw"
  local new_version="$openclaw_version_before"

  if [[ "$CONFIG_DRYRUN" == "true" ]]; then
    log "[DRY RUN] Would run: openclaw update --dry-run --yes --no-restart"
  else
    local install_output=""
    install_output=$(openclaw update --yes --no-restart 2>&1) || true
    log "$install_output"

    new_version=$(openclaw --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "unknown")
    # openclaw update returns non-zero even when already up to date — check version instead
    if [[ "$new_version" != "$openclaw_version_before" ]]; then
      log "✅ OpenClaw updated: $openclaw_version_before → $new_version"
    elif echo "$install_output" | grep -qiE "error|failed|ERR" && ! echo "$install_output" | grep -qiE "already up.to.date|no update|latest"; then
      log "❌ openclaw update failed (see output above)"
      update_ok=false
    else
      log "✅ OpenClaw already up to date ($new_version)"
    fi
  fi

  # ── Update Skills ─────────────────────────────────────────────────────────
  log_section "Updating Skills"
  local skills_updated=0
  local skills_skipped=0
  local skills_failed=0
  local skills_modified=0
  local skill_summary=""

  if [[ "$CONFIG_DRYRUN" == "true" ]]; then
    log "[DRY RUN] Would run: clawhub update --all"
    log "[DRY RUN] Installed clawhub does not support --dry-run for update; skipping skill preview."
    skill_summary="[Dry run — clawhub update preview not supported]"
  else
    local all_slugs=()
    local workspace_skills_dir="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}/skills"
    while IFS= read -r slug; do
      [[ -n "$slug" ]] && all_slugs+=("$slug")
    done < <(list_installed_skills)

    if [[ ${#all_slugs[@]} -eq 0 ]]; then
      log "All skills already up to date (or no skills found)"
    fi

    for slug in "${all_slugs[@]}"; do
      local skill_dir="$workspace_skills_dir/$slug"

      # Skiplist check
      if is_skipped "$slug"; then
        log "⏭️  Skipping $slug (in skiplist)"
        ((skills_skipped++)) || true
        skill_summary+="⏭️ $slug (skipped)\n"
        continue
      fi

      # Pre-release check
      if [[ "$CONFIG_SKIPPRERELEASE" == "true" ]]; then
        local inspect_output latest
        if ! inspect_output=$(clawhub inspect "$slug" 2>&1); then
          log "⚠️  Skipping $slug (clawhub inspect failed)"
          [[ -n "$inspect_output" ]] && log "$inspect_output"
          ((skills_skipped++)) || true
          skill_summary+="⏭️ $slug (inspect failed)\n"
          continue
        fi

        latest=$(printf '%s\n' "$inspect_output" | parse_inspect_version || true)
        if [[ -z "$latest" ]]; then
          log "⚠️  Could not parse version for $slug from clawhub inspect output; proceeding with update"
        elif [[ "$latest" == *-* ]]; then
          log "⏭️  Skipping $slug (pre-release: $latest)"
          ((skills_skipped++)) || true
          skill_summary+="⏭️ $slug (pre-release)\n"
          continue
        fi
      fi

      if [[ -d "$skill_dir" ]] && is_locally_modified "$skill_dir"; then
        log "Skipping $slug — local modifications detected"
        ((skills_modified++)) || true
        skill_summary+="⚠️ $slug (local modifications detected)\n"
        continue
      fi

      log "🔄 Updating $slug..."
      if clawhub update "$slug" --no-input 2>&1 | tee -a "$LOG_FILE"; then
        log "✅ $slug updated"
        ((skills_updated++)) || true
        skill_summary+="✅ $slug\n"
      else
        log "❌ $slug update failed"
        ((skills_failed++)) || true
        skill_summary+="❌ $slug (failed)\n"
      fi
    done
  fi

  # ── Restart Gateway ───────────────────────────────────────────────────────
  if [[ "$CONFIG_RESTARTGATEWAY" == "true" ]] && [[ "$CONFIG_DRYRUN" != "true" ]]; then
    # Only restart if openclaw was actually updated
    if [[ "$new_version" != "$openclaw_version_before" ]]; then
      log_section "Restarting Gateway"
      log "Restarting OpenClaw gateway..."
      openclaw gateway restart 2>&1 | tee -a "$LOG_FILE" || log "⚠️  Gateway restart failed (may need manual restart)"
      sleep 3
      log "✅ Gateway restarted"
    else
      log "Gateway restart skipped (no version change)"
    fi
  fi

  # ── Summary ───────────────────────────────────────────────────────────────
  log_section "Summary"
  local summary_msg

  if [[ "$CONFIG_DRYRUN" == "true" ]]; then
    summary_msg="🔍 [Dry Run] OpenClaw auto-update preview complete"
  else
    summary_msg="✅ OpenClaw auto-update complete"
    [[ "$new_version" != "$openclaw_version_before" ]] && \
      summary_msg+=" | OpenClaw: $openclaw_version_before → $new_version"
    summary_msg+=" | Skills: ✅${skills_updated} ⏭️${skills_skipped} ❌${skills_failed}"
    [[ $skills_modified -gt 0 ]] && summary_msg+=" ⚠️${skills_modified} modified"
  fi

  log "$summary_msg"

  # Send notification
  if [[ $skills_failed -gt 0 ]]; then
    notify "⚠️ OpenClaw auto-update: $skills_failed skill(s) failed to update. Check log: $LOG_FILE"
  else
    notify "$summary_msg"
  fi
}

main "$@"
