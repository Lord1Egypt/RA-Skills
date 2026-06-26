#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/require_obs_mcp.sh"

# Optional comma-separated input names via env:
# export OBS_AUDIO_INPUTS="Mic/Aux,Desktop Audio"
INPUTS_CSV="${OBS_AUDIO_INPUTS:-}"
MIC_MUL="${MIC_MUL:-0.85}"
DESKTOP_MUL="${DESKTOP_MUL:-0.55}"

if [[ -z "$INPUTS_CSV" ]]; then
  echo "No OBS_AUDIO_INPUTS provided; skipping explicit input tuning."
  echo "Tip: export OBS_AUDIO_INPUTS='Mic/Aux,Desktop Audio'"
  exit 0
fi

IFS=',' read -r -a INPUTS <<< "$INPUTS_CSV"
for i in "${!INPUTS[@]}"; do
  name="$(echo "${INPUTS[$i]}" | xargs)"
  [[ -z "$name" ]] && continue
  target_mul="$MIC_MUL"
  [[ "$i" -gt 0 ]] && target_mul="$DESKTOP_MUL"
  mcporter call "obs.set_input_volume(input_name: \"$name\", volume_mul: $target_mul)" >/dev/null || true
  if mcporter call "obs.get_input_mute(input_name: \"$name\")" | grep -q '"is_muted": true'; then
    mcporter call "obs.toggle_input_mute(input_name: \"$name\")" >/dev/null || true
  fi
  echo "Tuned input '$name' to volume_mul=${target_mul}"
done
