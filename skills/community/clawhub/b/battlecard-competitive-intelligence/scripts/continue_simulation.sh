#!/bin/bash
# Continue an active simulation
# Usage: ./continue_simulation.sh "simulation_id" "your message"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/battlecard.sh"
SID=$(json_escape "$1")
MSG=$(json_escape "$2")
"$SCRIPT_DIR/battlecard.sh" "continue_simulation" "{\"simulation_id\":$SID,\"message\":$MSG}"
