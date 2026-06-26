#!/bin/bash
# hash-snippet.sh — Compute SHA-256 hash of text input
set -euo pipefail

TEXT="${1:?Usage: $0 <text>}"

echo -n "$TEXT" | shasum -a 256 | cut -d' ' -f1
