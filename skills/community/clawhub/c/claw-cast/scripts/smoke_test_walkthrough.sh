#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/require_obs_mcp.sh"

HOLD_SECONDS="${1:-7}"

mc() { mcporter call "$1" >/dev/null; }

ORDER=("Intro" "Main Live" "Work Mode" "Presentation Mode" "Feature Demo" "Metrics" "Chat Interaction" "BRB Screen" "Outro")

mc 'obs.set_current_scene(scene_name: "Intro")'
mc 'obs.start_recording()'
for s in "${ORDER[@]}"; do
  mc "obs.set_current_scene(scene_name: \"$s\")"
  sleep "$HOLD_SECONDS"
done

OUT=$(mcporter call 'obs.stop_recording()')
echo "$OUT"
