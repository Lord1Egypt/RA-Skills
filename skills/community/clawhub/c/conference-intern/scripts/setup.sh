#!/usr/bin/env bash
# Conference Intern — Interactive Setup
# Usage: bash scripts/setup.sh <conference-name>
#
# This script prepares the conference directory and prints the setup prompt
# for the agent to follow interactively with the user.

set -euo pipefail
source "$(dirname "$0")/common.sh"

CONFERENCE_NAME="${1:-}"
if [ -z "$CONFERENCE_NAME" ]; then
  log_error "Usage: bash scripts/setup.sh <conference-name>"
  log_error "Example: bash scripts/setup.sh ethdenver-2026"
  exit 1
fi

# Slugify the conference name
CONFERENCE_ID=$(echo "$CONFERENCE_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')

CONF_DIR=$(init_conf_dir "$CONFERENCE_ID")
log_info "Conference directory: $CONF_DIR"

# Check if config already exists
if [ -f "$CONF_DIR/config.json" ]; then
  log_warn "Config already exists at $CONF_DIR/config.json"
  log_warn "Re-running setup will overwrite it."
fi

# Output the setup prompt for the agent
echo "---"
echo "CONFERENCE_ID=$CONFERENCE_ID"
echo "CONF_DIR=$CONF_DIR"
echo "---"
echo ""
read_template "setup-prompt.md"
