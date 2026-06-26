#!/usr/bin/env bash
set -euo pipefail

# bootstrap_deps.sh - install the published clawfetch CLI locally for this skill
#
# This script is intentionally minimal and reviewable. It only installs the
# public "clawfetch" npm package into the skill directory. It does NOT:
# - clone any git repositories
# - install arbitrary extra packages beyond clawfetch and its declared deps
# - modify global npm/node state
#
# Expected environment:
# - node / npm available on PATH
# - network access to registry.npmjs.org

# Install clawfetch at the version currently published for agents (0.1.3)
echo "[clawfetch-skill] Installing clawfetch@0.1.7 into $(pwd)" >&2
npm install clawfetch@0.1.7

echo "[clawfetch-skill] Done. CLI entrypoint: node_modules/clawfetch/clawfetch.js" >&2
