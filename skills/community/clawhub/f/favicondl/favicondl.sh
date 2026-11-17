#!/usr/bin/env bash
set -euo pipefail

api_endpoint="https://favicondl.com/api/extract"
domain="${1:-}"
size="${2:-128}"
output="${3:-}"

if [[ -z "$domain" || "$#" -gt 3 ]]; then
  printf 'Usage: %s <domain-or-url> [size] [output]\n' "$0" >&2
  exit 2
fi

if ! [[ "$size" =~ ^[0-9]+$ ]] || (( size < 16 || size > 512 )); then
  printf 'Size must be an integer from 16 to 512.\n' >&2
  exit 2
fi

host="$domain"
host="${host#http://}"
host="${host#https://}"
host="${host%%/*}"
safe_name="$(printf '%s' "$host" | sed 's/^www\.//; s/[^A-Za-z0-9_-]/_/g')"
if [[ -z "$safe_name" ]]; then
  printf 'Invalid domain or URL: %s\n' "$domain" >&2
  exit 2
fi

if [[ -z "$output" ]]; then
  output="${safe_name}_favicon.img"
fi

parent="$(dirname -- "$output")"
if [[ "$parent" != "." ]]; then
  mkdir -p -- "$parent"
fi

printf 'Fetching favicon for %s at %spx...\n' "$domain" "$size"
curl --fail --location --retry 2 --connect-timeout 10 --max-time 30 \
  --get --data-urlencode "url=$domain" --data-urlencode "size=$size" \
  --output "$output" "$api_endpoint"

bytes="$(wc -c < "$output" | tr -d ' ')"
printf 'Saved: %s (%s bytes)\n' "$output" "$bytes"
