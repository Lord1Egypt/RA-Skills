#!/bin/sh
set -eu

if command -v freefm >/dev/null 2>&1; then
  exec "$(command -v freefm)" sync --quiet
fi

if [ -x "$HOME/.local/bin/freefm" ]; then
  exec "$HOME/.local/bin/freefm" sync --quiet
fi

echo "freefm_not_found: install FreeFM before enabling this job" >&2
exit 127
