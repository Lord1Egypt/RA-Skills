#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/require_obs_mcp.sh"

IP="${1:-$(hostname -I | awk '{print $1}')}"
PORT="${OVERLAY_PORT:-8787}"
BASE_PATH="${OVERLAY_BASE_PATH:-/assets/overlays}"
BASE="http://$IP:$PORT$BASE_PATH"

mc() { mcporter call "$1" >/dev/null; }

SAFE_SCENE="Scene"
mc "obs.set_current_scene(scene_name: \"$SAFE_SCENE\")" || true

# Remove known baseline scenes if present
for s in "Intro" "Main Live" "Work Mode" "Presentation Mode" "Feature Demo" "Metrics" "Chat Interaction" "BRB Screen" "Outro"; do
  mc "obs.remove_scene(scene_name: \"$s\")" || true
done

# Create baseline scenes
for s in "Intro" "Main Live" "Work Mode" "Presentation Mode" "Feature Demo" "Metrics" "Chat Interaction" "BRB Screen" "Outro"; do
  mc "obs.create_scene(scene_name: \"$s\")"
done

# Attach default skill-bundled overlays
mc "obs.create_browser_source(scene_name: \"Intro\", source_name: \"Intro Overlay\", url: \"$BASE/intro.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Main Live\", source_name: \"Live Dashboard\", url: \"$BASE/live-dashboard.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Work Mode\", source_name: \"Work Status Overlay\", url: \"$BASE/work_status.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Presentation Mode\", source_name: \"Presentation Overlay\", url: \"$BASE/presentation.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Feature Demo\", source_name: \"Feature Demo Overlay\", url: \"$BASE/control-panel.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Metrics\", source_name: \"Metrics Overlay\", url: \"$BASE/analytics.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Chat Interaction\", source_name: \"Chat Overlay\", url: \"$BASE/chat.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"BRB Screen\", source_name: \"BRB Overlay\", url: \"$BASE/brb.html?v=1\", width: 1920, height: 1080)"
mc "obs.create_browser_source(scene_name: \"Outro\", source_name: \"Outro Overlay\", url: \"$BASE/outro.html?v=1\", width: 1920, height: 1080)"

mc 'obs.set_current_scene(scene_name: "Intro")'
echo "Rebuilt baseline scene pack using $BASE"
