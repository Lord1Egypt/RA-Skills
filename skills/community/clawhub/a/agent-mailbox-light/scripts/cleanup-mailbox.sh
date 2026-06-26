#!/usr/bin/env bash
set -euo pipefail

workspace="${1:-$(pwd)}"
days="${2:-7}"
archive="$workspace/.agent-mailbox/archive"
mkdir -p "$archive"

find "$archive" -maxdepth 1 -type f -name '*.md' -mtime +"$days" -delete
