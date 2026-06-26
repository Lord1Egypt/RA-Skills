#!/usr/bin/env bash
# openclaw-tab-title — apply/remove the Control UI per-agent tab-title patch.
# Mirrors PR openclaw/openclaw#80944 as a local zero-build override.
#
# Usage:
#   bash apply.sh                   # apply (idempotent)
#   bash apply.sh --uninstall       # restore from .bak
#   bash apply.sh --target <path>   # explicit Control UI index.html
#
# Env:
#   OPENCLAW_CONTROL_UI_INDEX  override target path

set -euo pipefail

MARKER="openclaw-tab-title local patch"

# ----- patch payload (kept self-contained inside this script) -----
read -r -d '' PATCH_SNIPPET <<'PATCH_EOF' || true
    <script>
      // openclaw-tab-title local patch — mirrors PR openclaw/openclaw#80944
      // Sets document.title to "<assistantName|assistantAgentId> · OpenClaw"
      // so multi-agent operators can disambiguate Control UI browser tabs.
      (function () {
        var STATIC = "OpenClaw Control";
        var lastTitle = "";
        function compute() {
          var el = document.querySelector("openclaw-app");
          if (!el) return STATIC;
          var name =
            (typeof el.assistantName === "string" && el.assistantName.trim()) ||
            (typeof el.assistantAgentId === "string" && el.assistantAgentId.trim()) ||
            "";
          return name ? name + " \u00B7 OpenClaw" : STATIC;
        }
        function tick() {
          var next = compute();
          if (next !== lastTitle) {
            document.title = next;
            lastTitle = next;
          }
        }
        setInterval(tick, 200);
        tick();
      })();
    </script>
PATCH_EOF

# ----- arg parse -----
mode="apply"
target=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --uninstall|--remove) mode="uninstall"; shift ;;
    --target) target="${2:-}"; shift 2 ;;
    -h|--help)
      sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

# ----- target resolution -----
resolve_target() {
  if [[ -n "${OPENCLAW_CONTROL_UI_INDEX:-}" ]]; then
    echo "$OPENCLAW_CONTROL_UI_INDEX"; return
  fi
  if [[ -n "$target" ]]; then echo "$target"; return; fi

  local candidate
  if command -v npm >/dev/null 2>&1; then
    candidate="$(npm root -g 2>/dev/null)/openclaw/dist/control-ui/index.html"
    if [[ -f "$candidate" ]]; then echo "$candidate"; return; fi
  fi

  # nvm fallback (newest node version wins)
  local nvm_root="$HOME/.nvm/versions/node"
  if [[ -d "$nvm_root" ]]; then
    candidate="$(ls -1d "$nvm_root"/v*/lib/node_modules/openclaw/dist/control-ui/index.html 2>/dev/null | sort -V | tail -n 1)"
    if [[ -n "$candidate" && -f "$candidate" ]]; then echo "$candidate"; return; fi
  fi

  echo ""
}

INDEX_FILE="$(resolve_target)"
if [[ -z "$INDEX_FILE" || ! -f "$INDEX_FILE" ]]; then
  cat >&2 <<EOF
ERROR: could not locate Control UI index.html.
Tried: \$OPENCLAW_CONTROL_UI_INDEX, --target, \$(npm root -g)/openclaw/dist/control-ui/index.html,
       ~/.nvm/versions/node/*/lib/node_modules/openclaw/dist/control-ui/index.html
Pass --target /path/to/openclaw/dist/control-ui/index.html
EOF
  exit 1
fi

BAK_FILE="${INDEX_FILE}.bak"

# ----- uninstall -----
if [[ "$mode" == "uninstall" ]]; then
  if [[ -f "$BAK_FILE" ]]; then
    cp "$BAK_FILE" "$INDEX_FILE"
    echo "Restored $INDEX_FILE from $BAK_FILE"
    echo "(.bak kept; remove manually if you want.)"
  elif grep -q "$MARKER" "$INDEX_FILE"; then
    # No backup but patch present — strip it inline.
    awk -v marker="$MARKER" '
      BEGIN { skip=0 }
      /<script>/ { buf=$0; in_script=1; next }
      in_script {
        buf=buf"\n"$0
        if (index($0, marker)) { has_marker=1 }
        if ($0 ~ /<\/script>/) {
          if (!has_marker) print buf
          buf=""; in_script=0; has_marker=0
        }
        next
      }
      { print }
    ' "$INDEX_FILE" > "${INDEX_FILE}.tmp" && mv "${INDEX_FILE}.tmp" "$INDEX_FILE"
    echo "Stripped patch in-place from $INDEX_FILE (no .bak found)."
  else
    echo "Nothing to do: no .bak and no patch marker in $INDEX_FILE."
  fi
  echo "Reload Control UI in your browser to see the static title again."
  exit 0
fi

# ----- apply -----
if grep -q "$MARKER" "$INDEX_FILE"; then
  echo "Already patched: $INDEX_FILE"
  echo "(Marker '$MARKER' present — skipping.)"
  exit 0
fi

if [[ ! -f "$BAK_FILE" ]]; then
  cp "$INDEX_FILE" "$BAK_FILE"
  echo "Backed up original -> $BAK_FILE"
else
  echo "Backup already exists at $BAK_FILE (kept as the pristine rollback point)."
fi

# Inject snippet right before </body>. Use a file to dodge sed escaping hell.
TMP_SNIPPET="$(mktemp)"
trap 'rm -f "$TMP_SNIPPET"' EXIT
printf '%s\n' "$PATCH_SNIPPET" > "$TMP_SNIPPET"

# Portable insert-before-marker using awk.
awk -v snippet_file="$TMP_SNIPPET" '
  BEGIN {
    while ((getline line < snippet_file) > 0) {
      snippet = snippet (snippet ? "\n" : "") line
    }
    close(snippet_file)
  }
  /<\/body>/ && !done {
    print snippet
    done = 1
  }
  { print }
' "$INDEX_FILE" > "${INDEX_FILE}.tmp" && mv "${INDEX_FILE}.tmp" "$INDEX_FILE"

if grep -q "$MARKER" "$INDEX_FILE"; then
  echo "Injected patch -> $INDEX_FILE"
  echo "Reload Control UI in your browser; tab title should now follow the active agent."
else
  echo "ERROR: injection failed — restoring backup." >&2
  cp "$BAK_FILE" "$INDEX_FILE"
  exit 1
fi
