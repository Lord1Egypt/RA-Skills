#!/usr/bin/env bash
set -euo pipefail

PACKAGE_MANAGER="npm"
VERBOSE=false

usage() {
  cat <<'EOF'
Install @beyondcorp/beyond-ui and required peer dependencies.

Usage:
  install-beyond-ui.sh [--pm npm|pnpm|yarn] [--verbose]

Options:
  --pm       Package manager to use (default: npm)
  --verbose  Print commands before running them
EOF
}

log() {
  echo "[beyond-ui-helper] $*"
}

run() {
  if $VERBOSE; then
    log "> $*"
  fi
  eval "$@"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pm)
      PACKAGE_MANAGER="$2"
      shift 2
      ;;
    --verbose)
      VERBOSE=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

case "$PACKAGE_MANAGER" in
  npm)
    INSTALL_CMD="npm install"
    ;;
  pnpm)
    INSTALL_CMD="pnpm add"
    ;;
  yarn)
    INSTALL_CMD="yarn add"
    ;;
  *)
    echo "Unsupported package manager: $PACKAGE_MANAGER" >&2
    exit 1
    ;;
end

log "Installing @beyondcorp/beyond-ui with $PACKAGE_MANAGER"
run "$INSTALL_CMD @beyondcorp/beyond-ui"

log "Ensuring peer dependencies are available"
run "$INSTALL_CMD react react-dom"

if [[ "$PACKAGE_MANAGER" == "npm" ]]; then
  # tailwindcss is optional; installing as a dev dependency when using npm
  log "Optionally installing tailwindcss (skip if not needed)"
  run "npm install -D tailwindcss"
else
  log "Optionally install tailwindcss using your package manager if theming overrides are required"
fi

log "Installation complete. Remember to import '@beyondcorp/beyond-ui/dist/styles.css' in your entry file."
