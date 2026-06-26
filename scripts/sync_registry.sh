#!/bin/bash
# Copy the canonical registry.json into the Python and npm package data dirs.
# Run before building/publishing the ra-skills packages. The copies are
# git-ignored — registry.json lives once at the repo root.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/registry.json"
[ -f "$SRC" ] || { echo "registry.json not found at $SRC"; exit 1; }

mkdir -p "$ROOT/python/ra_skills/_data" "$ROOT/js/data"
cp "$SRC" "$ROOT/python/ra_skills/_data/registry.json"
cp "$SRC" "$ROOT/js/data/registry.json"
echo "synced registry.json ($(du -h "$SRC" | cut -f1)) -> python + js packages"
