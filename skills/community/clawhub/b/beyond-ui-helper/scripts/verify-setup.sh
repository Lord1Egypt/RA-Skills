#!/usr/bin/env bash
set -euo pipefail

log() {
  echo "[beyond-ui-helper] $*"
}

log "Running npm install to ensure dependencies are present"
npm install

log "Running lint"
npm run lint

log "Running tests"
npm test

log "Building library and docs"
npm run build

log "Optionally run Storybook build"
npm run build-storybook

log "Verification complete"
