#!/bin/sh
# Print a numbered outline of a plain text notes file.
set -eu
f="${1:-notes.txt}"
[ -f "$f" ] || { echo "missing notes file: $f" >&2; exit 2; }
awk 'NF { printf "%d. %s\n", ++n, $0 }' "$f"
