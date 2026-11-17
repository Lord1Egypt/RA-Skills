#!/usr/bin/env bash
set -euo pipefail
NAME="${1:-world}"
if [ -z "$NAME" ]; then NAME="world"; fi
echo "Hello, ${NAME}!"
