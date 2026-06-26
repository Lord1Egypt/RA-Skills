#!/bin/bash
# Get a competitive battle card
# Usage: ./get_battle_card.sh "Company Name" "Competitor Name"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/battlecard.sh"
CO=$(json_escape "$1")
COMP=$(json_escape "$2")
"$SCRIPT_DIR/battlecard.sh" "get_battle_card" "{\"company\":$CO,\"competitor\":$COMP}"
