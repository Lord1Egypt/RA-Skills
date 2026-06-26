#!/usr/bin/env bash
set -euo pipefail

workspace="${1:-$(pwd)}"
root="$workspace/.agent-mailbox"
mkdir -p "$root/inbox" "$root/archive"

cat <<EOF
Initialized mailbox:
  $root

Subdirectories:
  $root/inbox
  $root/archive
EOF
