#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="clawgrid-connector"
SKILLS_BASE="$HOME/.openclaw/workspace/skills"
SKILL_DIR="$SKILLS_BASE/$SKILL_NAME"

# Source shared env if available (not available on first install)
if [ -f "$SKILL_DIR/scripts/_clawgrid_env.sh" ]; then
  source "$SKILL_DIR/scripts/_clawgrid_env.sh"
else
  CONFIG="$SKILL_DIR/config.json"
fi

# --- Parse arguments ---
API_BASE=""
FORCE=false
QUIET=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --api-base) API_BASE="$2"; shift 2 ;;
    --force)    FORCE=true; shift ;;
    --quiet)    QUIET=true; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# Determine API_BASE: arg > config.json > error
if [ -z "$API_BASE" ] && [ -f "$CONFIG" ]; then
  API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])" 2>/dev/null || echo "")
fi

if [ -z "$API_BASE" ]; then
  echo "[ERROR] No API base URL. Use --api-base URL or ensure config.json exists." >&2
  exit 1
fi

API_BASE="${API_BASE%/}"

# --- Fetch manifest ---
MANIFEST_RAW=$(curl -s "$API_BASE/skills" --max-time 15 2>/dev/null || echo "{}")
MANIFEST=$(echo "$MANIFEST_RAW" | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d))" 2>/dev/null || echo "{}")

if [ "$MANIFEST" = "{}" ]; then
  echo "[ERROR] Failed to fetch skill manifest from $API_BASE/skills" >&2
  exit 1
fi

# --- Install / update clawgrid-connector ---
python3 -c "
import json, sys, re, os, subprocess

manifest = json.loads(sys.argv[1])
api_base = sys.argv[2]
skill_name = sys.argv[3]
skills_base = sys.argv[4]
force = sys.argv[5] == 'true'
quiet = sys.argv[6] == 'true'

info = manifest.get(skill_name)
if not info:
    print(f'[ERROR] {skill_name} not found in manifest')
    sys.exit(1)

remote_ver = info.get('version', '')
files = info.get('files', [])
if not remote_ver or not files:
    print(f'[ERROR] Invalid manifest entry for {skill_name}')
    sys.exit(1)

skill_dir = os.path.join(skills_base, skill_name)
skill_md = os.path.join(skill_dir, 'SKILL.md')

local_ver = ''
if os.path.exists(skill_md):
    try:
        text = open(skill_md).read()[:500]
        m = re.search(r'^version:\s*(.+)$', text, re.MULTILINE)
        if m:
            local_ver = m.group(1).strip().strip('\"' + \"'\")
    except Exception:
        pass

if local_ver == remote_ver and not force:
    if not quiet:
        print(f'UP_TO_DATE: {skill_name} v{remote_ver}')
    sys.exit(0)

action = 'UPDATE' if local_ver else 'INSTALL'
print(f'{action}: {skill_name} {local_ver or \"(new)\"} -> {remote_ver}')

other_files = [f for f in files if f != 'SKILL.md']
skill_md_file = 'SKILL.md' if 'SKILL.md' in files else None

failed = 0
for f in other_files:
    target = os.path.join(skill_dir, f)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    url = f'{api_base}/skills/{skill_name}/{f}'
    tmp = target + '.tmp'
    r = subprocess.run(
        ['curl', '-sfL', url, '-o', tmp, '--max-time', '15'],
        capture_output=True,
    )
    if r.returncode != 0 or not os.path.isfile(tmp) or os.path.getsize(tmp) < 10:
        print(f'  WARN: failed to download {f} (HTTP error or empty)')
        if os.path.isfile(tmp):
            os.remove(tmp)
        failed += 1
    else:
        os.replace(tmp, target)
        if not quiet:
            print(f'  ok: {f}')

if failed > 0 and skill_md_file:
    print(f'  SKIP: SKILL.md (held back — {failed} file(s) failed, will retry next heartbeat)')
elif skill_md_file:
    target = os.path.join(skill_dir, skill_md_file)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    url = f'{api_base}/skills/{skill_name}/{skill_md_file}'
    tmp = target + '.tmp'
    r = subprocess.run(
        ['curl', '-sfL', url, '-o', tmp, '--max-time', '15'],
        capture_output=True,
    )
    if r.returncode != 0 or not os.path.isfile(tmp) or os.path.getsize(tmp) < 10:
        print(f'  WARN: failed to download SKILL.md (HTTP error or empty)')
        if os.path.isfile(tmp):
            os.remove(tmp)
        failed += 1
    else:
        os.replace(tmp, target)
        if not quiet:
            print(f'  ok: SKILL.md')

scripts_dir = os.path.join(skill_dir, 'scripts')
if os.path.isdir(scripts_dir):
    for fname in os.listdir(scripts_dir):
        if fname.endswith('.sh'):
            os.chmod(os.path.join(scripts_dir, fname), 0o755)

if action == 'UPDATE' and failed == 0:
    flag_path = os.path.join(skill_dir, '.skill_updated')
    with open(flag_path, 'w') as fh:
        json.dump({'skill': skill_name, 'from': local_ver, 'to': remote_ver}, fh)

if failed > 0:
    print(f'DONE with {failed} download warnings (will retry on next heartbeat)')
else:
    print(f'DONE: {skill_name} v{remote_ver}')
" "$MANIFEST" "$API_BASE" "$SKILL_NAME" "$SKILLS_BASE" "$FORCE" "$QUIET"

# --- Post-install: migrate behavioral settings to server & clean config.json ---
# Re-source env to pick up config migration from the (potentially new) version.
if [ -f "$SKILL_DIR/scripts/_clawgrid_env.sh" ]; then
  source "$SKILL_DIR/scripts/_clawgrid_env.sh"
fi

if [ -f "$CONFIG" ]; then
  python3 - "$CONFIG" "$API_BASE" <<'PYEOF'
import json, sys, os
from pathlib import Path

config_path, api_base = sys.argv[1], sys.argv[2]
try:
    cfg = json.load(open(config_path))
except Exception:
    sys.exit(0)

api_key = cfg.get("api_key", "")
LEGACY_KEYS = {"auto_claim", "allow_types", "min_budget", "max_daily",
               "heartbeat_interval_minutes", "heartbeat_interval_seconds",
               "poll_interval_seconds", "notifier_cron_expression"}
legacy = {k: v for k, v in cfg.items() if k in LEGACY_KEYS}

if not legacy:
    sys.exit(0)

# Upload legacy settings to server as claim-stage compound rules (v3 format)
if api_key:
    import subprocess
    compound = {"action": "accept"}
    has_auto = bool(legacy.get("auto_claim"))
    # Legacy allow_types were task_type strings; server rules expect tag slugs in has_tags — edit in Settings if needed
    if "allow_types" in legacy and legacy["allow_types"]:
        compound["has_tags"] = legacy["allow_types"] if isinstance(legacy["allow_types"], list) else [legacy["allow_types"]]
    if "min_budget" in legacy:
        compound["min_budget"] = float(legacy["min_budget"])

    rules_list = [compound] if compound else []
    if rules_list or has_auto:
        payload = json.dumps({"claim": {"enabled": has_auto, "rules": rules_list}})
        r = subprocess.run(
            ["curl", "-s", "-X", "PUT",
             f"{api_base}/api/lobster/me/automation",
             "-H", f"Authorization: Bearer {api_key}",
             "-H", "Content-Type: application/json",
             "-d", payload, "--max-time", "10"],
            capture_output=True, text=True,
        )
        if r.returncode == 0 and '"status":"ok"' in r.stdout:
            print("[install] Migrated automation settings to server (claim stage)")
        else:
            backup = Path(config_path).parent / "state" / "legacy_config_backup.json"
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_text(json.dumps(legacy, indent=2))
            print(f"[install] Server upload failed — backup saved to {backup}")

# Clean config.json: keep only core fields
clean = {k: v for k, v in cfg.items()
         if k not in LEGACY_KEYS and not k.startswith("_")}
with open(config_path, "w") as f:
    json.dump(clean, f, indent=2)
print("[install] Cleaned config.json — behavioral settings removed")
PYEOF
fi

# --- Clean up deprecated local preferences directory ---
PREFS_DIR="$HOME/.clawgrid/preferences"
if [ -d "$PREFS_DIR" ]; then
  echo "[install] Removing deprecated local preferences directory: $PREFS_DIR"
  rm -rf "$PREFS_DIR"
fi

# --- Post-install: configure exec approval for automated sessions ---
SETUP_EXEC_APPROVAL="$SKILL_DIR/scripts/setup-exec-approval.sh"
if [ -x "$SETUP_EXEC_APPROVAL" ]; then
  bash "$SETUP_EXEC_APPROVAL" --quiet 2>/dev/null || true
fi

SETUP_CRONS="$SKILL_DIR/scripts/setup-crons.sh"
if [ -f "$CONFIG" ] && [ -x "$SETUP_CRONS" ]; then
  _hb_missing=true
  if [ "$(uname -s)" = "Darwin" ]; then
    _hb_plist="$HOME/Library/LaunchAgents/ai.clawgrid.heartbeat.plist"
    if [ -f "$_hb_plist" ]; then
      _hb_missing=false
      launchctl list 2>/dev/null | grep -q 'ai.clawgrid.heartbeat' || \
        launchctl load "$_hb_plist" 2>/dev/null || true
    fi
  else
    crontab -l 2>/dev/null | grep -q 'clawgrid-heartbeat' && _hb_missing=false
  fi
  if [ "$_hb_missing" = "true" ]; then
    bash "$SETUP_CRONS" || true
  fi
fi
