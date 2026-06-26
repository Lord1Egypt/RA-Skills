#!/usr/bin/env bash
set -euo pipefail

TOKEN_FILE="${GRIZZLY_TOKEN_FILE:-$HOME/.config/grizzly/token}"
TAG="${RESEARCH_TAG:-待整理}"

if [ "${1:-}" = "list" ]; then
    grizzly open-tag --name "$TAG" --enable-callback --json --token-file "$TOKEN_FILE"
else
    echo "Usage: $0 list"
    exit 1
fi
