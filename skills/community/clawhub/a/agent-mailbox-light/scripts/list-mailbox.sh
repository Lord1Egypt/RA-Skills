#!/usr/bin/env bash
set -euo pipefail

workspace="${1:-$(pwd)}"
limit="${2:-5}"
inbox="$workspace/.agent-mailbox/inbox"
mkdir -p "$inbox"

find "$inbox" -maxdepth 1 -type f -name '*.md' | sort -r | head -n "$limit"
