#!/bin/bash
set -euo pipefail
PROJECT_DIR="/Users/ShiXin/Documents/Workspace/github-project/agent-orchestrator"
cd "$PROJECT_DIR"
exec node packages/ao/bin/ao.js "$@"
