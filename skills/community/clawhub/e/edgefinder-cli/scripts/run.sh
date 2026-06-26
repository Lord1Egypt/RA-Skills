#!/bin/sh
set -eu

if command -v edgefinder >/dev/null 2>&1; then
  exec edgefinder "$@"
fi

if command -v npx >/dev/null 2>&1; then
  exec npx -y @edgefinder/cli "$@"
fi

echo "Error: neither 'edgefinder' nor 'npx' is available on PATH." >&2
exit 1
