#!/usr/bin/env bash
# Convert a file URL to markdown or pdf via EnConvert, printing the result's presigned_url.
#
# Usage:   scripts/convert.sh <markdown|pdf> <file-url>
# Auth:    reads ENCONVERT_API_KEY (private sk_ key) from the environment.
#
# Flow (matches the skill's contract):
#   1. GET the source URL bytes  -> NO api key (third-party host)
#   2. POST them as multipart `file` -> WITH api key
#   3. print presigned_url        -> fetch it later with NO api key
set -euo pipefail

mode="${1:-}"; src="${2:-}"
[ -n "$mode" ] && [ -n "$src" ] || { echo "usage: convert.sh <markdown|pdf> <file-url>" >&2; exit 2; }
[ -n "${ENCONVERT_API_KEY:-}" ] || { echo "ENCONVERT_API_KEY is not set" >&2; exit 2; }

case "$mode" in
  markdown) endpoint="anything-to-markdown" ;;
  pdf)      endpoint="anything-to-pdf" ;;
  *) echo "mode must be 'markdown' or 'pdf'" >&2; exit 2 ;;
esac

# Keep the source filename: the API detects the input format from its extension, so a
# bare mktemp name comes back as 400 Invalid file format '.lJzoMq6Akq'.
name="$(basename "${src%%\?*}")"
case "$name" in *.*) ;; *) name="file.html" ;; esac

dir="$(mktemp -d)"; trap 'rm -rf "$dir"' EXIT
# 1. download source with NO api key
curl -fsSL "$src" -o "$dir/$name"
# 2. multipart POST with the api key (curl sets the multipart Content-Type itself)
# no -f: on a 4xx the API's body names the problem (e.g. which extensions it accepts),
# and step 3 surfaces it instead of curl exiting with a bare code
resp="$(curl -sS -X POST "https://api.enconvert.com/v1/convert/$endpoint" \
  -H "X-API-Key: $ENCONVERT_API_KEY" \
  -F "file=@$dir/$name")"
# 3. surface the presigned_url (fetch it separately, without the key)
# `|| true`: no match is the error path below, not a reason for set -e to kill the script
url="$(echo "$resp" | grep -o '"presigned_url":"[^"]*"' | head -n1 | cut -d'"' -f4 || true)"
[ -n "$url" ] || { echo "no presigned_url in response: $resp" >&2; exit 1; }
echo "$url"
