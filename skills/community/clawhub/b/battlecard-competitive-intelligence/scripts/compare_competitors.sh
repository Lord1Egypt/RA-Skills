#!/bin/bash
# Compare multiple competitors
# Usage: ./compare_competitors.sh "Company" "Comp1,Comp2,Comp3"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/battlecard.sh"
CO=$(json_escape "$1")
IFS=',' read -ra COMPS <<< "$2"
COMP_JSON=""
for c in "${COMPS[@]}"; do
  ESCAPED=$(json_escape "$c")
  COMP_JSON="${COMP_JSON}${COMP_JSON:+,}$ESCAPED"
done
"$SCRIPT_DIR/battlecard.sh" "compare_competitors" "{\"company\":$CO,\"competitors\":[$COMP_JSON]}"
