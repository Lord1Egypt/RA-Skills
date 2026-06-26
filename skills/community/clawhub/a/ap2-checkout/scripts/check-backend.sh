#!/usr/bin/env bash
# Verify AP2 openclaw mock backend ports (no mcporter required).
set -eu

if [ -z "${AP2_HOME:-}" ]; then
  echo "ERROR: set AP2_HOME to your AP2 repository root." >&2
  exit 1
fi

UNIFIED="$AP2_HOME/code/samples/python/scenarios/a2a/unified"
if [ ! -f "$UNIFIED/openclaw/start_ap2_backend.sh" ]; then
  echo "ERROR: AP2_HOME invalid — missing $UNIFIED/openclaw/start_ap2_backend.sh" >&2
  exit 1
fi

missing=0
for port in 8091 8092 8093 8094 8100 8101 8102 8103; do
  if lsof -ti tcp:"$port" >/dev/null 2>&1; then
    echo "OK  port $port"
  else
    echo "FAIL port $port"
    missing=1
  fi
done

if [ "$missing" = "1" ]; then
  echo "Start backend: cd $UNIFIED && ./openclaw/start_ap2_backend.sh" >&2
  exit 1
fi

echo "AP2 mock backend looks up."
