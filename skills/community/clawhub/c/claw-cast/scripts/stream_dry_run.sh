#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/require_obs_mcp.sh"

SECONDS_ON_AIR="${1:-15}"
START_SCENE="${2:-Intro}"
MAIN_SCENE="${3:-Main Live}"

CURRENT=$(mcporter call 'obs.list_scenes()' | python3 -c 'import sys,json; print(json.load(sys.stdin)["current_scene"])')

mcporter call "obs.set_current_scene(scene_name: \"$START_SCENE\")" >/dev/null || true
mcporter call 'obs.start_streaming()' >/dev/null
sleep 3
mcporter call "obs.set_current_scene(scene_name: \"$MAIN_SCENE\")" >/dev/null || true
sleep "$SECONDS_ON_AIR"
mcporter call 'obs.stop_streaming()' >/dev/null
mcporter call "obs.set_current_scene(scene_name: \"$CURRENT\")" >/dev/null || true

echo "Dry-run stream complete (${SECONDS_ON_AIR}s). Restored scene: $CURRENT"
