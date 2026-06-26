#!/usr/bin/env bash
# sync.sh — generate GEMINI.md from AGENTS.md
#
# AGENTS.md is the canonical Gestalt protocol.
# CLAUDE.md is a one-line @AGENTS.md import (no sync needed).
# GEMINI.md needs the full content because Gemini CLI doesn't read AGENTS.md.
#
# Run this after editing AGENTS.md.
# Usage: bash sync.sh

set -euo pipefail

# Strip the "# Gestalt" heading (line 1) and its following blank line (line 2)
BODY=$(tail -n +3 AGENTS.md)

cat > GEMINI.md << 'HEADER'
# Gestalt

<!-- Gemini CLI reads GEMINI.md automatically. This file mirrors AGENTS.md.
     Gemini CLI does not read AGENTS.md natively, so this copy is required.
     Edit AGENTS.md; run sync.sh to update this file. -->

HEADER
printf '%s\n' "$BODY" >> GEMINI.md

echo "Synced GEMINI.md from AGENTS.md"
