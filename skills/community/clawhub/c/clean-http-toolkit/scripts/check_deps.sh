#!/usr/bin/env bash
set -eu
if ! command -v python3 >/dev/null 2>&1; then
    echo "missing dependency: python3" >&2
    exit 1
fi
python3 --version
echo "All dependencies satisfied."
