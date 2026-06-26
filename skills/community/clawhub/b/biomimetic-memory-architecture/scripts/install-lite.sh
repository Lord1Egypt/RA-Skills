#!/bin/bash
# BMA — minimal non-destructive installer
# Run from OpenClaw workspace root: bash skills/biomimetic-memory-architecture/scripts/install.sh
set -euo pipefail
WORKSPACE="${CLAWD_WORKSPACE:-$(pwd)}"
cd "$WORKSPACE"
mkdir -p memory/projects memory/runbooks memory/contacts memory/workflows memory/archive memory/lesson-imprint memory-archive/reports
python3 skills/biomimetic-memory-architecture/scripts/lesson_imprint.py init
python3 skills/biomimetic-memory-architecture/scripts/lesson_imprint.py promote >/dev/null || true
[ -f .bma-version ] || echo "0.1.7" > .bma-version
echo "BMA installed/verified base directories and Lesson-Imprint store."
echo "Next: configure memory-wiki and cron jobs according to references/installation.md."
