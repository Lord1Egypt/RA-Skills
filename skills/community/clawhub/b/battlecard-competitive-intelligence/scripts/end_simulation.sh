#!/bin/bash
# End simulation and get debrief
# Usage: ./end_simulation.sh "simulation_id"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/battlecard.sh"
SID=$(json_escape "$1")
"$SCRIPT_DIR/battlecard.sh" "end_simulation" "{\"simulation_id\":$SID}"
