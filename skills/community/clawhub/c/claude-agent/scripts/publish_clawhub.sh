#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

DEFAULT_VERSION="$(sed -n 's/^## \[\([^]]*\)\].*/\1/p' CHANGELOG.md | head -1)"
VERSION="${1:-${CLAWHUB_VERSION:-$DEFAULT_VERSION}}"
CHANGELOG_TEXT="${CHANGELOG_TEXT:-Security hardening, ClawHub packaging, bilingual docs, and privacy-by-default notifications.}"
TAGS="${CLAWHUB_TAGS:-latest,openclaw,claude-code,developer-tools,automation,security}"

if [ -z "$VERSION" ]; then
    echo "Failed to resolve version from CHANGELOG.md" >&2
    exit 1
fi

pnpm dlx clawhub publish . \
    --slug claude-agent \
    --name "Claude Agent" \
    --version "$VERSION" \
    --changelog "$CHANGELOG_TEXT" \
    --tags "$TAGS"
