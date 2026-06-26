#!/bin/bash
# Start a sales simulation
# Usage: ./start_simulation.sh "Company" "Competitor" [difficulty]
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/battlecard.sh"
CO=$(json_escape "$1")
COMP=$(json_escape "$2")
DIFF=$(json_escape "${3:-easy}")
"$SCRIPT_DIR/battlecard.sh" "start_simulation" "{\"company\":$CO,\"competitor\":$COMP,\"difficulty\":$DIFF}"
