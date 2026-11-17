#!/usr/bin/env sh
# Print a stable UTC timestamp and ISO date.
set -eu
printf 'utc=%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
printf 'date=%s\n' "$(date -u '+%Y-%m-%d')"
