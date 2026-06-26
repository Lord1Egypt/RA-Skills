#!/bin/bash
# Get objection handlers for a competitor
# Usage: ./get_objection_handlers.sh "Competitor" [context]
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/battlecard.sh"
COMP=$(json_escape "$1")
if [ -n "$2" ]; then
  CTX=$(json_escape "$2")
  "$SCRIPT_DIR/battlecard.sh" "get_objection_handlers" "{\"competitor\":$COMP,\"context\":$CTX}"
else
  "$SCRIPT_DIR/battlecard.sh" "get_objection_handlers" "{\"competitor\":$COMP}"
fi
