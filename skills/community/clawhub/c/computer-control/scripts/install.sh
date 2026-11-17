#!/bin/bash
# Install tarsx (computer-control backend) for the computer-control skill.
set -e
SRC="$(cd "$(dirname "$0")/tarsx" && pwd)"
BIN_DIR="${HOME}/.local/bin"
mkdir -p "$BIN_DIR"
# node_modules for MCP server use is optional; the CLI itself is dependency-free.
mkdir -p "$HOME/.tarsx"
cp "$SRC/cli.mjs" "$HOME/.tarsx/cli.mjs"
cp "$SRC/core.mjs" "$HOME/.tarsx/core.mjs"
cat > "$BIN_DIR/tarsx" <<'WRAPPER'
#!/usr/bin/env node
import path from 'node:path';
const file = path.join(process.env.HOME, '.tarsx', 'cli.mjs');
await import(file);
WRAPPER
chmod +x "$BIN_DIR/tarsx"
echo "tarsx installed -> $BIN_DIR/tarsx"
# Build the TarsX.app helper: gives macOS Accessibility/Screen Recording a real
# .app to attach to (bare launchd binaries never get the permission prompt).
bash "$(cd "$(dirname "$0")" && pwd)/make-app.sh" || echo "warning: TarsX.app build failed; actions will need manual permission grants"
tarsx info || true
