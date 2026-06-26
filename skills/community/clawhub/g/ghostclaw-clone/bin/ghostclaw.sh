#!/usr/bin/env bash
# bin/ghostclaw.sh — npm bin wrapper; delegates to the real installed binary at ~/.local/bin/ghostclaw

BINARY="$HOME/.local/bin/ghostclaw"

if [ ! -f "$BINARY" ]; then
    echo "ghostclaw: binary not found at $BINARY" >&2
    echo "Run 'npm run build' or './scripts/install.sh' to build it first." >&2
    exit 1
fi

exec "$BINARY" "$@"
