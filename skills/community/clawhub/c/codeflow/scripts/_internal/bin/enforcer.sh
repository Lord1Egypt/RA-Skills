#!/bin/bash

set -euo pipefail
umask 077

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$BIN_DIR/../.." && pwd)"
PLUGIN_DIR="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$ROOT_DIR/../extensions/codeflow-enforcer")"
PLUGIN_MANIFEST="$PLUGIN_DIR/openclaw.plugin.json"
PLUGIN_ID="codeflow-enforcer"
INSTALL_CALLBACK_DATA="cfe:install"
OPENCLAW_LAUNCHER_KIND=""
OPENCLAW_LAUNCHER_LABEL=""
OPENCLAW_CMD=()
OPENCLAW_NVM_SCRIPT=""

detect_openclaw_launcher() {
  if [ -n "$OPENCLAW_LAUNCHER_KIND" ]; then
    [ "$OPENCLAW_LAUNCHER_KIND" != "missing" ]
    return
  fi

  if [ -n "${HOME:-}" ]; then
    local nvm_script="$HOME/.nvm/nvm.sh"
    if [ -f "$nvm_script" ] && bash -lc 'source "$1" >/dev/null 2>&1 && command -v openclaw >/dev/null 2>&1' _ "$nvm_script" >/dev/null 2>&1; then
      OPENCLAW_LAUNCHER_KIND="native"
      OPENCLAW_LAUNCHER_LABEL="openclaw"
      OPENCLAW_CMD=()
      OPENCLAW_NVM_SCRIPT="$nvm_script"
      return 0
    fi
  fi

  if command -v openclaw >/dev/null 2>&1; then
    OPENCLAW_LAUNCHER_KIND="native"
    OPENCLAW_LAUNCHER_LABEL="openclaw"
    OPENCLAW_CMD=(openclaw)
    return 0
  fi

  if command -v npx >/dev/null 2>&1; then
    OPENCLAW_LAUNCHER_KIND="npx"
    OPENCLAW_LAUNCHER_LABEL="npx -y openclaw"
    OPENCLAW_CMD=(npx -y openclaw)
    return 0
  fi

  OPENCLAW_LAUNCHER_KIND="missing"
  OPENCLAW_LAUNCHER_LABEL=""
  OPENCLAW_CMD=()
  return 1
}

run_openclaw() {
  detect_openclaw_launcher || {
    echo "Error: openclaw CLI not found in PATH, and no npx fallback is available" >&2
    return 127
  }
  if [ -n "$OPENCLAW_NVM_SCRIPT" ]; then
    bash -lc 'set -e; source "$1" >/dev/null 2>&1; shift; openclaw "$@"' _ "$OPENCLAW_NVM_SCRIPT" "$@"
    return
  fi
  "${OPENCLAW_CMD[@]}" "$@"
}

require_openclaw() {
  if ! detect_openclaw_launcher; then
    echo "Error: openclaw CLI not found in PATH, and no npx fallback is available" >&2
    exit 127
  fi
}

require_bundled_plugin() {
  if [ ! -d "$PLUGIN_DIR" ] || [ ! -f "$PLUGIN_MANIFEST" ]; then
    echo "Error: bundled enforcer plugin not found at $PLUGIN_DIR" >&2
    exit 2
  fi
}

maybe_restart_gateway() {
  local requested="${1:-false}"
  if [ "$requested" = true ]; then
    run_openclaw gateway restart
  else
    echo "Restart required: run '${OPENCLAW_LAUNCHER_LABEL:-openclaw} gateway restart' to load changes."
  fi
}

plugin_list_json() {
  run_openclaw plugins list --json 2>/dev/null || run_openclaw plugins list
}

ensure_plugin_allowlisted() {
  local raw merged changed
  raw="$(run_openclaw config get plugins.allow 2>/dev/null || true)"
  merged="$(PLUGIN_ALLOW_RAW="$raw" python3 - "$PLUGIN_ID" <<'PY'
import json
import os
import sys

plugin_id = sys.argv[1]
raw = os.environ.get("PLUGIN_ALLOW_RAW", "").strip()
items = []

if raw and raw not in {"null", "undefined"}:
    try:
        parsed = json.loads(raw)
    except Exception:
        raise SystemExit("Error: plugins.allow must be a JSON array or unset")

    if parsed is None:
        parsed = []

    if not isinstance(parsed, list):
        raise SystemExit("Error: plugins.allow must be a JSON array")

    for item in parsed:
        text = str(item).strip()
        if text and text not in items:
            items.append(text)

changed = plugin_id not in items
if changed:
    items.append(plugin_id)

print(("true" if changed else "false") + "\t" + json.dumps(items, ensure_ascii=False))
PY
)"
  changed="${merged%%	*}"
  merged="${merged#*	}"

  if [ "$changed" = true ]; then
    run_openclaw config set plugins.allow "$merged" --json >/dev/null
  fi
}

current_session_key() {
  if [ -n "${SESSION_KEY_OVERRIDE:-}" ]; then
    printf '%s\n' "$SESSION_KEY_OVERRIDE"
    return
  fi
  printf '%s\n' "${OPENCLAW_SESSION_KEY:-${OPENCLAW_SESSION:-}}"
}

parse_plugin_list_status() {
  local raw="${1:-}"
  local parsed rest

  PLUGIN_INSTALLED=false
  PLUGIN_ENABLED=false
  PLUGIN_LOADED=false
  PLUGIN_HEALTHY=false
  PLUGIN_STATUS=""
  PLUGIN_HOOK_COUNT=""

  if [ -z "$raw" ]; then
    return 0
  fi

  parsed="$(PLUGIN_LIST_INPUT="$raw" python3 - "$PLUGIN_ID" <<'PY'
import json
import os
import re
import sys

plugin_id = sys.argv[1]
raw = os.environ.get("PLUGIN_LIST_INPUT", "")
result = {
    "installed": False,
    "enabled": False,
    "loaded": False,
    "healthy": False,
    "status": "",
    "hook_count": "",
}
text = raw.strip()

def emit() -> None:
    print(
        "\t".join(
            [
                "true" if result["installed"] else "false",
                "true" if result["enabled"] else "false",
                "true" if result["loaded"] else "false",
                "true" if result["healthy"] else "false",
                str(result["status"] or ""),
                "" if result["hook_count"] == "" else str(result["hook_count"]),
            ]
        )
    )

if not text:
    emit()
    raise SystemExit(0)

items = None
try:
    parsed = json.loads(text)
except Exception:
    parsed = None

if isinstance(parsed, dict):
    if isinstance(parsed.get("plugins"), list):
        items = parsed["plugins"]
    else:
        items = [parsed]
elif isinstance(parsed, list):
    items = parsed

if items is not None:
    for item in items:
        if not isinstance(item, dict):
            continue
        candidate = str(item.get("id") or item.get("pluginId") or item.get("name") or "").strip()
        if candidate != plugin_id:
            continue
        result["installed"] = True
        enabled = item.get("enabled")
        result["enabled"] = True if enabled is None else bool(enabled)
        status = str(item.get("status") or "").strip().lower()
        if status:
            result["status"] = status
        hook_count = item.get("hookCount")
        if isinstance(hook_count, int) and not isinstance(hook_count, bool):
            result["hook_count"] = hook_count
        if status in {"loaded", "ready", "active"}:
            result["loaded"] = True
        if result["loaded"] and result["enabled"]:
            result["healthy"] = True
        elif status in {"degraded", "error", "failed", "disabled"} or enabled is False:
            result["healthy"] = False
        else:
            result["healthy"] = result["loaded"] and result["enabled"]
        break

    if result["installed"] and not result["status"]:
        result["status"] = "loaded" if result["loaded"] else "installed"

    emit()
    raise SystemExit(0)

if re.search(rf"\b{re.escape(plugin_id)}\b", text, re.IGNORECASE):
    result["installed"] = True
    status_match = re.search(
        r"\b(loaded|ready|active|degraded|error|failed|disabled|installed)\b",
        text,
        re.IGNORECASE,
    )
    if status_match:
        result["status"] = status_match.group(1).lower()
    if result["status"] in {"loaded", "ready", "active"}:
        result["enabled"] = True
        result["loaded"] = True
        result["healthy"] = True
    elif result["status"] in {"degraded", "error", "failed", "disabled"}:
        result["enabled"] = result["status"] != "disabled"
        result["healthy"] = False
    else:
        result["status"] = result["status"] or "installed"

emit()
PY
)"

  if [ -z "$parsed" ]; then
    return 0
  fi

  PLUGIN_INSTALLED_RAW="${parsed%%	*}"
  rest="${parsed#*	}"
  PLUGIN_ENABLED_RAW="${rest%%	*}"
  rest="${rest#*	}"
  PLUGIN_LOADED_RAW="${rest%%	*}"
  rest="${rest#*	}"
  PLUGIN_HEALTHY_RAW="${rest%%	*}"
  rest="${rest#*	}"
  PLUGIN_STATUS="${rest%%	*}"
  if [ "$PLUGIN_STATUS" != "$rest" ]; then
    PLUGIN_HOOK_COUNT="${rest#*	}"
  fi

  if [ "$PLUGIN_INSTALLED_RAW" = "true" ]; then
    PLUGIN_INSTALLED=true
  fi
  if [ "$PLUGIN_ENABLED_RAW" = "true" ]; then
    PLUGIN_ENABLED=true
  fi
  if [ "$PLUGIN_LOADED_RAW" = "true" ]; then
    PLUGIN_LOADED=true
  fi
  if [ "$PLUGIN_HEALTHY_RAW" = "true" ]; then
    PLUGIN_HEALTHY=true
  fi
}

collect_status() {
  PLUGIN_BUNDLED=false
  OPENCLAW_CLI=false
  PLUGIN_DETECTED=false
  PLUGIN_INSTALLED=false
  PLUGIN_ENABLED=false
  PLUGIN_LOADED=false
  PLUGIN_HEALTHY=false
  PLUGIN_STATUS=""
  PLUGIN_HOOK_COUNT=""
  PLUGIN_STATE="unknown"
  CAN_INSTALL=false
  PLUGIN_LIST_RAW=""
  SESSION_KEY_RESOLVED="$(current_session_key)"
  GUARD_ACTIVE=false
  GUARD_MATCHED=false
  GUARD_STATE="unavailable"
  GUARD_BINDING=""
  GUARD_RAW=""
  RECOMMEND_ACTION="none"
  RECOMMEND_MESSAGE=""
  RECOMMEND_BUTTON_TEXT=""
  RECOMMEND_CALLBACK_DATA=""

  if [ -d "$PLUGIN_DIR" ] && [ -f "$PLUGIN_MANIFEST" ]; then
    PLUGIN_BUNDLED=true
  fi

  if detect_openclaw_launcher; then
    OPENCLAW_CLI=true
  fi

  if [ "$OPENCLAW_CLI" = true ]; then
    PLUGIN_LIST_RAW="$(plugin_list_json 2>/dev/null || true)"
    parse_plugin_list_status "$PLUGIN_LIST_RAW"
    if [ "$PLUGIN_INSTALLED" = true ]; then
      PLUGIN_DETECTED=true
    fi
  fi

  if [ "$PLUGIN_BUNDLED" = true ] && [ "$OPENCLAW_CLI" = true ]; then
    CAN_INSTALL=true
  fi

  if [ -n "$SESSION_KEY_RESOLVED" ]; then
    GUARD_RAW="$(bash "$ROOT_DIR/codeflow" guard current -P auto --session-key "$SESSION_KEY_RESOLVED" 2>/dev/null || true)"
    if [ -n "$GUARD_RAW" ]; then
      GUARD_PARSED="$(printf '%s' "$GUARD_RAW" | python3 -c '
import json
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    raise SystemExit(1)

active = bool(data.get("active"))
matched = bool(data.get("matched"))
state = "active" if active else "inactive" if matched else "unbound"
binding = str(data.get("bindingKey") or "")
print(("true" if active else "false") + "\t" + ("true" if matched else "false") + "\t" + state + "\t" + binding)
' 2>/dev/null || true)"
      if [ -n "$GUARD_PARSED" ]; then
        GUARD_ACTIVE_RAW="${GUARD_PARSED%%	*}"
        REST_GUARD="${GUARD_PARSED#*	}"
        GUARD_MATCHED_RAW="${REST_GUARD%%	*}"
        REST_GUARD="${REST_GUARD#*	}"
        GUARD_STATE="${REST_GUARD%%	*}"
        if [ "$GUARD_STATE" != "$REST_GUARD" ]; then
          GUARD_BINDING="${REST_GUARD#*	}"
        fi
        if [ "$GUARD_ACTIVE_RAW" = "true" ]; then
          GUARD_ACTIVE=true
        fi
        if [ "$GUARD_MATCHED_RAW" = "true" ]; then
          GUARD_MATCHED=true
        fi
      fi
    fi
  fi

  if [ "$PLUGIN_BUNDLED" != true ]; then
    PLUGIN_STATE="missing-bundle"
  elif [ "$OPENCLAW_CLI" != true ]; then
    PLUGIN_STATE="cli-unavailable"
  elif [ "$PLUGIN_INSTALLED" != true ]; then
    PLUGIN_STATE="not-installed"
  elif [ "$PLUGIN_HEALTHY" = true ]; then
    PLUGIN_STATE="loaded"
  elif [ -n "$PLUGIN_STATUS" ] && [ "$PLUGIN_STATUS" != "installed" ]; then
    PLUGIN_STATE="degraded"
  else
    PLUGIN_STATE="restart-pending"
  fi

  if [ "$PLUGIN_STATE" = "loaded" ]; then
    RECOMMEND_ACTION="none"
    RECOMMEND_MESSAGE="Codeflow soft mode remains active because /codeflow is owned by the skill. The bundled enforcer plugin is installed and loaded on this host, so hard tool blocking is available when the guard is active."
  elif [ "$PLUGIN_STATE" = "restart-pending" ]; then
    RECOMMEND_ACTION="restart"
    RECOMMEND_MESSAGE="Codeflow soft mode remains active. The bundled enforcer plugin is installed on this host, but OpenClaw has not loaded it yet. Restart the gateway to make hard tool blocking effective."
  elif [ "$PLUGIN_STATE" = "degraded" ]; then
    RECOMMEND_ACTION="restart"
    RECOMMEND_MESSAGE="Codeflow soft mode remains active. The bundled enforcer plugin is installed, but OpenClaw is not reporting it as healthy yet."
    if [ -n "$PLUGIN_STATUS" ]; then
      RECOMMEND_MESSAGE="$RECOMMEND_MESSAGE Current plugin status: $PLUGIN_STATUS."
    fi
  elif [ "$OPENCLAW_CLI" = true ] && [ "$OPENCLAW_LAUNCHER_KIND" = "npx" ]; then
    RECOMMEND_ACTION="install"
    RECOMMEND_MESSAGE="Codeflow soft mode remains active. A global openclaw binary is not on PATH, but npx can run the bundled installer, so hard enforcement can still be installed from chat."
    RECOMMEND_BUTTON_TEXT="Install Enforcer"
    RECOMMEND_CALLBACK_DATA="$INSTALL_CALLBACK_DATA"
  elif [ "$PLUGIN_STATE" = "missing-bundle" ]; then
    RECOMMEND_ACTION="manual"
    RECOMMEND_MESSAGE="Codeflow soft mode remains active. This skill install is incomplete because the bundled enforcer plugin directory is missing."
  elif [ "$PLUGIN_STATE" = "cli-unavailable" ]; then
    RECOMMEND_ACTION="manual"
    RECOMMEND_MESSAGE="Codeflow soft mode remains active. openclaw CLI is not available on this host, so the bundled enforcer plugin cannot be installed from chat."
  else
    RECOMMEND_ACTION="install"
    RECOMMEND_MESSAGE="Codeflow soft mode remains active. Hard thread-scoped enforcement is unavailable because the bundled codeflow-enforcer plugin is not installed on this host."
    RECOMMEND_BUTTON_TEXT="Install Enforcer"
    RECOMMEND_CALLBACK_DATA="$INSTALL_CALLBACK_DATA"
  fi
}

emit_status_json() {
  collect_status
  export CODEFLOW_ENFORCER_PLUGIN_ID="$PLUGIN_ID"
  export CODEFLOW_ENFORCER_PLUGIN_DIR="$PLUGIN_DIR"
  export CODEFLOW_ENFORCER_PLUGIN_MANIFEST="$PLUGIN_MANIFEST"
  export CODEFLOW_ENFORCER_PLUGIN_BUNDLED="$PLUGIN_BUNDLED"
  export CODEFLOW_ENFORCER_OPENCLAW_CLI="$OPENCLAW_CLI"
  export CODEFLOW_ENFORCER_OPENCLAW_LAUNCHER="$OPENCLAW_LAUNCHER_LABEL"
  export CODEFLOW_ENFORCER_OPENCLAW_LAUNCHER_KIND="$OPENCLAW_LAUNCHER_KIND"
  export CODEFLOW_ENFORCER_PLUGIN_DETECTED="$PLUGIN_DETECTED"
  export CODEFLOW_ENFORCER_PLUGIN_INSTALLED="$PLUGIN_INSTALLED"
  export CODEFLOW_ENFORCER_PLUGIN_ENABLED="$PLUGIN_ENABLED"
  export CODEFLOW_ENFORCER_PLUGIN_LOADED="$PLUGIN_LOADED"
  export CODEFLOW_ENFORCER_PLUGIN_HEALTHY="$PLUGIN_HEALTHY"
  export CODEFLOW_ENFORCER_PLUGIN_STATUS="$PLUGIN_STATUS"
  export CODEFLOW_ENFORCER_PLUGIN_HOOK_COUNT="$PLUGIN_HOOK_COUNT"
  export CODEFLOW_ENFORCER_PLUGIN_STATE="$PLUGIN_STATE"
  export CODEFLOW_ENFORCER_CAN_INSTALL="$CAN_INSTALL"
  export CODEFLOW_ENFORCER_SESSION_KEY="$SESSION_KEY_RESOLVED"
  export CODEFLOW_ENFORCER_GUARD_ACTIVE="$GUARD_ACTIVE"
  export CODEFLOW_ENFORCER_GUARD_MATCHED="$GUARD_MATCHED"
  export CODEFLOW_ENFORCER_GUARD_STATE="$GUARD_STATE"
  export CODEFLOW_ENFORCER_GUARD_BINDING="$GUARD_BINDING"
  export CODEFLOW_ENFORCER_INSTALL_COMMAND="bash $ROOT_DIR/codeflow enforcer install --restart"
  export CODEFLOW_ENFORCER_RESTART_COMMAND="${OPENCLAW_LAUNCHER_LABEL:-openclaw} gateway restart"
  export CODEFLOW_ENFORCER_RECOMMEND_ACTION="$RECOMMEND_ACTION"
  export CODEFLOW_ENFORCER_RECOMMEND_MESSAGE="$RECOMMEND_MESSAGE"
  export CODEFLOW_ENFORCER_RECOMMEND_BUTTON_TEXT="$RECOMMEND_BUTTON_TEXT"
  export CODEFLOW_ENFORCER_RECOMMEND_CALLBACK_DATA="$RECOMMEND_CALLBACK_DATA"
  python3 - <<'PY'
import json
import os

def b(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() == "true"

hook_count_raw = os.environ.get("CODEFLOW_ENFORCER_PLUGIN_HOOK_COUNT", "").strip()
hook_count = None
if hook_count_raw:
    try:
        hook_count = int(hook_count_raw)
    except Exception:
        hook_count = hook_count_raw

button_text = os.environ.get("CODEFLOW_ENFORCER_RECOMMEND_BUTTON_TEXT", "").strip()
callback_data = os.environ.get("CODEFLOW_ENFORCER_RECOMMEND_CALLBACK_DATA", "").strip()
buttons = [[{"text": button_text, "callback_data": callback_data}]] if button_text and callback_data else []

payload = {
    "ok": True,
    "pluginId": os.environ.get("CODEFLOW_ENFORCER_PLUGIN_ID", ""),
    "pluginDir": os.environ.get("CODEFLOW_ENFORCER_PLUGIN_DIR", ""),
    "pluginManifest": os.environ.get("CODEFLOW_ENFORCER_PLUGIN_MANIFEST", ""),
    "pluginBundled": b("CODEFLOW_ENFORCER_PLUGIN_BUNDLED"),
    "openclawCli": b("CODEFLOW_ENFORCER_OPENCLAW_CLI"),
    "openclawLauncher": os.environ.get("CODEFLOW_ENFORCER_OPENCLAW_LAUNCHER", ""),
    "openclawLauncherKind": os.environ.get("CODEFLOW_ENFORCER_OPENCLAW_LAUNCHER_KIND", ""),
    "pluginDetected": b("CODEFLOW_ENFORCER_PLUGIN_DETECTED"),
    "plugin": {
        "state": os.environ.get("CODEFLOW_ENFORCER_PLUGIN_STATE", ""),
        "installed": b("CODEFLOW_ENFORCER_PLUGIN_INSTALLED"),
        "enabled": b("CODEFLOW_ENFORCER_PLUGIN_ENABLED"),
        "loaded": b("CODEFLOW_ENFORCER_PLUGIN_LOADED"),
        "healthy": b("CODEFLOW_ENFORCER_PLUGIN_HEALTHY"),
        "status": os.environ.get("CODEFLOW_ENFORCER_PLUGIN_STATUS", ""),
        "hookCount": hook_count,
    },
    "canInstall": b("CODEFLOW_ENFORCER_CAN_INSTALL"),
    "sessionKey": os.environ.get("CODEFLOW_ENFORCER_SESSION_KEY", ""),
    "installCommand": os.environ.get("CODEFLOW_ENFORCER_INSTALL_COMMAND", ""),
    "restartCommand": os.environ.get("CODEFLOW_ENFORCER_RESTART_COMMAND", ""),
    "guard": {
        "active": b("CODEFLOW_ENFORCER_GUARD_ACTIVE"),
        "matched": b("CODEFLOW_ENFORCER_GUARD_MATCHED"),
        "state": os.environ.get("CODEFLOW_ENFORCER_GUARD_STATE", ""),
        "bindingKey": os.environ.get("CODEFLOW_ENFORCER_GUARD_BINDING", ""),
    },
    "recommendation": {
        "action": os.environ.get("CODEFLOW_ENFORCER_RECOMMEND_ACTION", ""),
        "message": os.environ.get("CODEFLOW_ENFORCER_RECOMMEND_MESSAGE", ""),
        "buttonText": button_text,
        "callbackData": callback_data,
        "buttons": buttons,
    },
}
print(json.dumps(payload, ensure_ascii=False))
PY
}

show_status() {
  collect_status
  echo "== plugin =="
  if [ "$OPENCLAW_CLI" = true ]; then
    if [ -n "$PLUGIN_LIST_RAW" ]; then
      printf '%s\n' "$PLUGIN_LIST_RAW"
    else
      echo "(no plugin list output)"
    fi
  else
    echo "openclaw CLI not found in PATH"
  fi
  echo
  echo "== summary =="
  echo "skill_bundle: $( [ "$PLUGIN_BUNDLED" = true ] && echo ok || echo missing )"
  if [ "$OPENCLAW_CLI" = true ]; then
    echo "openclaw_cli: ok (${OPENCLAW_LAUNCHER_LABEL})"
  else
    echo "openclaw_cli: missing"
  fi
  echo "host_plugin: $PLUGIN_STATE"
  if [ -n "$PLUGIN_STATUS" ]; then
    echo "plugin_status: $PLUGIN_STATUS"
  fi
  if [ -n "$PLUGIN_HOOK_COUNT" ]; then
    echo "plugin_hook_count: $PLUGIN_HOOK_COUNT"
  fi
  echo
  echo "== guard =="
  if [ -n "$SESSION_KEY_RESOLVED" ]; then
    if [ -n "$GUARD_BINDING" ]; then
      echo "$GUARD_STATE ($GUARD_BINDING)"
    else
      echo "$GUARD_STATE"
    fi
  else
    echo "Set OPENCLAW_SESSION_KEY (or OPENCLAW_SESSION), or pass --session-key, to inspect the current thread binding."
  fi
  echo
  echo "== recommendation =="
  printf '%s\n' "$RECOMMEND_MESSAGE"
  if [ "$RECOMMEND_ACTION" = "install" ]; then
    echo "Install: bash $ROOT_DIR/codeflow enforcer install --restart"
  elif [ "$RECOMMEND_ACTION" = "restart" ]; then
    echo "Restart: ${OPENCLAW_LAUNCHER_LABEL:-openclaw} gateway restart"
  fi
}

ACTION="${1:-}"
case "$ACTION" in
  -h|--help|help)
    ACTION="help"
    shift || true
    ;;
  *)
    shift || true
    ;;
esac
RESTART=false
JSON=false
SESSION_KEY_OVERRIDE=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --restart)
      RESTART=true
      shift
      ;;
    --json)
      JSON=true
      shift
      ;;
    --session-key)
      [ "$#" -lt 2 ] && { echo "Error: --session-key requires a value" >&2; exit 2; }
      SESSION_KEY_OVERRIDE="$2"
      shift 2
      ;;
    -h|--help|help)
      ACTION="help"
      shift
      ;;
    *)
      echo "Error: unknown argument '$1'" >&2
      exit 2
      ;;
  esac
done

case "$ACTION" in
  install)
    require_openclaw
    require_bundled_plugin
    ensure_plugin_allowlisted
    run_openclaw plugins install -l "$PLUGIN_DIR"
    maybe_restart_gateway "$RESTART"
    ;;
  update)
    require_openclaw
    require_bundled_plugin
    ensure_plugin_allowlisted
    run_openclaw plugins uninstall "$PLUGIN_ID" --keep-files >/dev/null 2>&1 || true
    run_openclaw plugins install -l "$PLUGIN_DIR"
    maybe_restart_gateway "$RESTART"
    ;;
  uninstall)
    require_openclaw
    run_openclaw plugins uninstall "$PLUGIN_ID" --keep-files
    maybe_restart_gateway "$RESTART"
    ;;
  status)
    if [ "$JSON" = true ]; then
      emit_status_json
    else
      show_status
    fi
    ;;
  ""|help)
    cat <<EOF
Usage:
  codeflow enforcer install [--restart]
  codeflow enforcer update [--restart]
  codeflow enforcer uninstall [--restart]
  codeflow enforcer status [--json] [--session-key <openclaw_session_key>]

Plugin path:
  $PLUGIN_DIR
EOF
    ;;
  *)
    echo "Error: unknown enforcer action '$ACTION'" >&2
    exit 2
    ;;
esac
