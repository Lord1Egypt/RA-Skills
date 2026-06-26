#!/usr/bin/env bash
# dev-reflect: reflect a local dev source repo's plugin/skill changes into the
# registered Claude Code marketplace clone for local testing BEFORE commit/push.
#
# Usage:
#   dev-reflect.sh --source <repo-path> --marketplace <name> [--enable <plugin>] [--dry-run]
#
#   --source       Local dev source repo (must contain .claude-plugin/marketplace.json)
#   --marketplace  Target clone name under ~/.claude/plugins/marketplaces/<name>/
#   --enable       Optional plugin name to enable as "<plugin>@<marketplace>" in settings.json
#   --dry-run      Print actions without writing
#
# What it does:
#   1. Sync component dirs (skills/ agents/ commands/ hooks/ plugins/) source -> clone
#   2. Upsert source's marketplace.json plugin entries into the clone (by name; clone-only kept)
#   3. chmod +x synced hook scripts
#   4. (optional) enable the plugin in settings.json (with backup)
#   5. Print the 4-step plugin-activation verification + reload reminder
#
# Notes:
#   - Additive sync (rsync --delete only when rsync is present). Removed source files
#     are NOT pruned from the clone unless rsync is available.
#   - Direct clone edits are a TEST shortcut. A later GitHub re-sync overwrites them.
#     Commit/push the source repo to make changes durable.

set -euo pipefail

SOURCE="" MARKETPLACE="" ENABLE="" DRYRUN=0
while [ $# -gt 0 ]; do
  case "$1" in
    --source) SOURCE="$2"; shift 2 ;;
    --marketplace) MARKETPLACE="$2"; shift 2 ;;
    --enable) ENABLE="$2"; shift 2 ;;
    --dry-run) DRYRUN=1; shift ;;
    *) echo "[dev-reflect] unknown arg: $1" >&2; exit 2 ;;
  esac
done

[ -n "$SOURCE" ] || { echo "[dev-reflect] --source required" >&2; exit 2; }
[ -n "$MARKETPLACE" ] || { echo "[dev-reflect] --marketplace required" >&2; exit 2; }

SRC_MP="$SOURCE/.claude-plugin/marketplace.json"
CLONE="$HOME/.claude/plugins/marketplaces/$MARKETPLACE"
CLONE_MP="$CLONE/.claude-plugin/marketplace.json"

[ -f "$SRC_MP" ]   || { echo "[dev-reflect] not a marketplace source (no $SRC_MP)" >&2; exit 1; }
[ -d "$CLONE" ]    || { echo "[dev-reflect] marketplace clone not found: $CLONE" >&2; exit 1; }
[ -f "$CLONE_MP" ] || { echo "[dev-reflect] clone has no marketplace.json: $CLONE_MP" >&2; exit 1; }
command -v jq >/dev/null || { echo "[dev-reflect] jq required" >&2; exit 1; }

run() { if [ "$DRYRUN" = 1 ]; then echo "DRY: $*"; else eval "$*"; fi; }

# 1. Sync component dirs
HAVE_RSYNC=0; command -v rsync >/dev/null && HAVE_RSYNC=1
for dir in skills agents commands hooks plugins; do
  [ -d "$SOURCE/$dir" ] || continue
  if [ "$HAVE_RSYNC" = 1 ]; then
    run "rsync -a --delete \"$SOURCE/$dir/\" \"$CLONE/$dir/\""
  else
    run "mkdir -p \"$CLONE/$dir\""
    run "command cp -r \"$SOURCE/$dir/.\" \"$CLONE/$dir/\""
  fi
  echo "[dev-reflect] synced $dir/"
done

# 2. Upsert source plugin entries into clone marketplace.json (clone-only entries kept)
if [ "$DRYRUN" = 1 ]; then
  echo "DRY: upsert plugins from $SRC_MP into $CLONE_MP"
else
  TMP="$(mktemp)"
  jq --slurpfile s <(jq '.plugins' "$SRC_MP") '
    ($s[0]) as $src
    | ($src | map(.name)) as $names
    | .plugins = ([.plugins[] | select(.name as $n | ($names | index($n) | not))] + $src)
  ' "$CLONE_MP" > "$TMP"
  jq empty "$TMP"
  command cp "$TMP" "$CLONE_MP"; rm -f "$TMP"
  echo "[dev-reflect] marketplace.json plugins upserted"
fi

# 3. chmod +x synced hook scripts
if [ "$DRYRUN" != 1 ]; then
  find "$CLONE/skills" "$CLONE/hooks" "$CLONE/plugins" -type f -name '*.sh' 2>/dev/null \
    -exec chmod +x {} \; || true
fi

# 4. Optional: enable plugin in settings.json
if [ -n "$ENABLE" ]; then
  S="$HOME/.claude/settings.json"
  KEY="$ENABLE@$MARKETPLACE"
  if [ "$DRYRUN" = 1 ]; then
    echo "DRY: enable $KEY in $S (with backup)"
  else
    command cp "$S" "$S.bak-dev-reflect"
    TMP="$(mktemp)"
    jq --arg k "$KEY" '.enabledPlugins[$k] = true' "$S" > "$TMP"
    jq empty "$TMP"
    command cp "$TMP" "$S"; rm -f "$TMP"
    echo "[dev-reflect] enabled $KEY (backup: settings.json.bak-dev-reflect)"
  fi
fi

# 5. Verification report
cat <<EOF

[dev-reflect] Reflected to clone: $CLONE
Plugin activation verification:
  1) marketplace registered ........ $MARKETPLACE (extraKnownMarketplaces)
  2) component files in clone ...... synced above
  3) enabledPlugins ................ $( [ -n "$ENABLE" ] && echo "$ENABLE@$MARKETPLACE=true (this run)" || echo "not changed (pass --enable to set)" )
  4) Skill tool detection .......... NEXT SESSION (plugins load at session start)

=> Restart Claude Code / start a new session, then verify the skill is detected.
   This edits the clone only (test shortcut). Commit/push the source repo to persist.
EOF
