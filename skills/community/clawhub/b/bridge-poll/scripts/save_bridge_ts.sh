#!/bin/bash
# Save the latest bridge poll timestamp.
#
# MUST pass the 'ts' field (float seconds) from the message JSON.
# Do NOT pass the 'id' field (ms integer) — see gotchas.md for why.
#
# Usage: save_bridge_ts.sh <ts_value>
# Example: save_bridge_ts.sh 1773222005.54582
#
# Also accepts ms integers for backward compat (auto-divides by 1000).
# Override cursor file location with BRIDGE_TS_FILE env var.

TS="$1"
if [ -z "$TS" ]; then
    echo "Usage: save_bridge_ts.sh <timestamp>"
    exit 1
fi

TS_FILE="${BRIDGE_TS_FILE:-/tmp/acp_bridge_last_ts}"

# Normalize: if ts > 9999999999, treat as milliseconds and convert
FIXED=$(python3 -c "
from decimal import Decimal
ts = Decimal('$TS')
if ts > 9999999999:
    ts = ts / 1000
print(str(ts))
")

echo "$FIXED" > "$TS_FILE"
echo "Saved ts: $FIXED → $TS_FILE"
