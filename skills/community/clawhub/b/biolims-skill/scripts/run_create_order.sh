#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JSON=$(cat "$SCRIPT_DIR/../../../temp_order.json" | tr -d '\n\r' | sed 's/  */ /g')
bash "$SCRIPT_DIR/biolims.sh" create-order "$JSON"
