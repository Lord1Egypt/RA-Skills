#!/usr/bin/env bash
set -euo pipefail

PROFILES_DIR="$HOME/.clawgrid-profiles"
CLAWGRID_LINK="$HOME/.clawgrid"
SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
IS_MACOS=false
[ "$(uname -s)" = "Darwin" ] && IS_MACOS=true
LAUNCHD_LABEL="ai.clawgrid.heartbeat"

_active_profile() {
  if [ -L "$CLAWGRID_LINK" ]; then
    basename "$(readlink "$CLAWGRID_LINK")"
  else
    echo ""
  fi
}

_read_api_base() {
  local cfg="$1/config.json"
  [ -f "$cfg" ] && python3 -c "import json; print(json.load(open('$cfg'))['api_base'])" 2>/dev/null || echo "?"
}

_stop_crons() {
  local ctl="$SKILL_DIR/scripts/heartbeat-ctl.sh"
  if [ -f "$ctl" ]; then
    bash "$ctl" stop --quiet >/dev/null 2>&1 || true
  else
    if $IS_MACOS; then
      launchctl bootout "gui/$(id -u)/$LAUNCHD_LABEL" 2>/dev/null || true
    else
      (crontab -l 2>/dev/null | grep -v 'clawgrid-heartbeat') | crontab - 2>/dev/null || true
    fi
  fi
}

_start_crons() {
  local ctl="$SKILL_DIR/scripts/heartbeat-ctl.sh"
  if [ -f "$ctl" ]; then
    bash "$ctl" start || true
  elif [ -f "$SKILL_DIR/scripts/setup-crons.sh" ]; then
    bash "$SKILL_DIR/scripts/setup-crons.sh"
  else
    echo "[WARN] heartbeat-ctl.sh / setup-crons.sh not found, skipping cron setup"
  fi
}

cmd_list() {
  if [ ! -d "$PROFILES_DIR" ]; then
    echo "No profiles yet. Use 'save <name>' to create one."
    exit 0
  fi
  local active
  active=$(_active_profile)
  for dir in "$PROFILES_DIR"/*/; do
    [ ! -d "$dir" ] && continue
    local name base marker
    name=$(basename "$dir")
    base=$(_read_api_base "$dir")
    marker="  "
    [ "$name" = "$active" ] && marker="* "
    printf "%s%-12s %s\n" "$marker" "$name" "$base"
  done
}

cmd_current() {
  if [ ! -L "$CLAWGRID_LINK" ]; then
    if [ -d "$CLAWGRID_LINK" ]; then
      local base
      base=$(_read_api_base "$CLAWGRID_LINK")
      echo "(unmanaged) -> $base"
      echo "Run 'save <name>' to convert to a managed profile."
    else
      echo "No active profile. Run 'save <name>' or 'init <name>'."
    fi
    exit 0
  fi
  local active base
  active=$(_active_profile)
  base=$(_read_api_base "$CLAWGRID_LINK")
  echo "$active -> $base"
}

cmd_save() {
  local name="${1:?Usage: clawgrid-env save <name>}"
  local target="$PROFILES_DIR/$name"
  mkdir -p "$PROFILES_DIR"

  if [ -L "$CLAWGRID_LINK" ]; then
    local current_target
    current_target=$(readlink "$CLAWGRID_LINK")
    if [ -d "$current_target" ]; then
      cp -r "$current_target" "$target"
      echo "Copied current profile to '$name'"
    else
      echo "[ERROR] Symlink target $current_target does not exist" >&2
      exit 1
    fi
  elif [ -d "$CLAWGRID_LINK" ]; then
    mv "$CLAWGRID_LINK" "$target"
    ln -s "$target" "$CLAWGRID_LINK"
    echo "Migrated ~/.clawgrid -> profile '$name' (symlink created)"
  else
    echo "[ERROR] ~/.clawgrid does not exist. Register on an environment first." >&2
    exit 1
  fi

  local base
  base=$(_read_api_base "$target")
  echo "Saved: $name -> $base"
}

cmd_switch() {
  local name="${1:?Usage: clawgrid-env switch <name>}"
  local target="$PROFILES_DIR/$name"

  if [ ! -d "$target" ]; then
    echo "[ERROR] Profile '$name' not found. Available:" >&2
    cmd_list >&2
    exit 1
  fi
  if [ ! -f "$target/config.json" ]; then
    echo "[ERROR] Profile '$name' has no config.json" >&2
    exit 1
  fi

  local active
  active=$(_active_profile)
  if [ "$name" = "$active" ]; then
    echo "Already on '$name'. Nothing to do."
    exit 0
  fi

  _stop_crons

  if [ -L "$CLAWGRID_LINK" ]; then
    rm "$CLAWGRID_LINK"
  elif [ -d "$CLAWGRID_LINK" ]; then
    echo "[INFO] ~/.clawgrid is a real directory (from fresh onboarding?)."
    echo "       Moving it to profile 'unsaved' before switching."
    mkdir -p "$PROFILES_DIR"
    mv "$CLAWGRID_LINK" "$PROFILES_DIR/unsaved"
  fi

  ln -s "$target" "$CLAWGRID_LINK"

  _start_crons

  local base
  base=$(_read_api_base "$target")
  echo ""
  echo "Switched to: $name -> $base"
}

cmd_init() {
  local name="${1:?Usage: clawgrid-env init <name> --api-base <url> --api-key <key>}"
  shift
  local api_base="" api_key=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --api-base) api_base="$2"; shift 2 ;;
      --api-key)  api_key="$2";  shift 2 ;;
      *) echo "[ERROR] Unknown option: $1" >&2; exit 1 ;;
    esac
  done
  if [ -z "$api_base" ] || [ -z "$api_key" ]; then
    echo "[ERROR] Both --api-base and --api-key are required" >&2
    exit 1
  fi

  local target="$PROFILES_DIR/$name"
  mkdir -p "$target"/{state,cache,logs,pending_artifacts}
  cat > "$target/config.json" << EOF
{
  "api_base": "$api_base",
  "api_key": "$api_key",
  "heartbeat_interval_minutes": 1
}
EOF
  echo "Created profile: $name -> $api_base"
  echo "Switch to it with: clawgrid-env switch $name"
}

cmd_reset() {
  local wipe_profile=false
  [ "${1:-}" = "--wipe" ] && wipe_profile=true

  _stop_crons

  local active=""
  if [ -L "$CLAWGRID_LINK" ]; then
    active=$(_active_profile)
    rm "$CLAWGRID_LINK"
    echo "Removed symlink ~/.clawgrid (was -> $active)"
  elif [ -d "$CLAWGRID_LINK" ]; then
    echo "[WARN] ~/.clawgrid is a real directory (not managed)."
    echo "       Deleting it as a plain reset."
    rm -rf "$CLAWGRID_LINK"
  else
    echo "Nothing to reset (no ~/.clawgrid)."
  fi

  if [ -d "$SKILL_DIR" ]; then
    rm -rf "$SKILL_DIR"
    echo "Removed clawgrid-connector skill dir"
  fi

  if $wipe_profile && [ -n "$active" ] && [ -d "$PROFILES_DIR/$active" ]; then
    rm -rf "$PROFILES_DIR/$active"
    echo "Wiped profile data for '$active'"
  fi

  echo ""
  echo "Reset complete. Node is in clean state for fresh onboarding."
  if [ -d "$PROFILES_DIR" ]; then
    local remaining
    remaining=$(ls -1 "$PROFILES_DIR" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$remaining" -gt 0 ]; then
      echo "Other profiles preserved ($remaining available). Use 'switch <name>' after re-onboarding."
    fi
  fi
}

cmd_help() {
  cat << 'EOF'
clawgrid-env — Manage multiple ClawGrid environment profiles

Commands:
  list              Show all profiles (* = active)
  current           Show active profile and its API base
  save <name>       Save current ~/.clawgrid as a named profile
  switch <name>     Switch to a profile (repoints symlink + restarts crons)
  init <name> --api-base <url> --api-key <key>
                    Create a new profile from scratch
  reset [--wipe]    Clean slate for re-onboarding (removes symlink + connector)
                    --wipe also deletes current profile data
  help              Show this help

Onboarding test workflow:
  1. clawgrid-env switch staging       # point to staging
  2. clawgrid-env reset                # clean slate, other profiles kept
  3. (run open-register on staging)    # fresh onboarding
  4. clawgrid-env save staging         # save new registration
  5. clawgrid-env switch prod          # back to prod when done

Examples:
  clawgrid-env save prod
  clawgrid-env switch staging
  clawgrid-env reset
  clawgrid-env init dev --api-base https://dev.zwalker.me --api-key lf_xxx
EOF
}

case "${1:-help}" in
  list)    cmd_list ;;
  current) cmd_current ;;
  save)    cmd_save "${2:-}" ;;
  switch)  cmd_switch "${2:-}" ;;
  init)    shift; cmd_init "$@" ;;
  reset)   cmd_reset "${2:-}" ;;
  help|--help|-h) cmd_help ;;
  *) echo "[ERROR] Unknown command: $1" >&2; cmd_help >&2; exit 1 ;;
esac
