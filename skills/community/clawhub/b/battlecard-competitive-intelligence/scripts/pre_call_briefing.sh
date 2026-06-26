#!/bin/bash
# Generate a pre-call briefing
# Usage: ./pre_call_briefing.sh "Competitor" [context]
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/battlecard.sh"
COMP=$(json_escape "$1")
if [ -n "$2" ]; then
  CTX=$(json_escape "$2")
  "$SCRIPT_DIR/battlecard.sh" "generate_pre_call_briefing" "{\"competitor\":$COMP,\"context\":$CTX}"
else
  "$SCRIPT_DIR/battlecard.sh" "generate_pre_call_briefing" "{\"competitor\":$COMP}"
fi
