#!/bin/bash
# agent-deploy v2.1: List all configured agents
HELPER="$(dirname "$0")/deploy_helper.py"
python3 "$HELPER" list
