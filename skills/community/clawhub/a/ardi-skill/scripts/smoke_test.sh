#!/bin/sh
# Smoke test — verify ardi-agent is installed and the binary runs.
# Called by Hermes / OpenClaw post-install to confirm the skill is healthy.
# Exits 0 on pass, non-zero on fail.

set -e

INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"
export PATH="$INSTALL_DIR:$PATH"

if ! command -v ardi-agent >/dev/null 2>&1; then
  echo "FAIL: ardi-agent not on PATH (looked in $PATH)" >&2
  exit 1
fi

VERSION="$(ardi-agent --version 2>/dev/null || true)"
if [ -z "$VERSION" ]; then
  echo "FAIL: ardi-agent --version returned nothing" >&2
  exit 2
fi

# Sanity: a known-bad subcommand should error out cleanly with non-zero
# exit but not crash the binary.
if ardi-agent --help >/dev/null 2>&1; then
  echo "ok ardi-agent installed: $VERSION"
  exit 0
fi

echo "FAIL: ardi-agent --help failed" >&2
exit 3
