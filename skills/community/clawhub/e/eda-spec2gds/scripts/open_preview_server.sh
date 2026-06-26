#!/usr/bin/env bash
set -euo pipefail
PORT="${1:-8765}"
python3 /root/.openclaw/workspace/skills/eda-spec2gds/scripts/serve_multi_project_dashboard.py "$PORT"
