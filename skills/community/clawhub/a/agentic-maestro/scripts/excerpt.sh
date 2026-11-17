#!/bin/bash
# Prints a code excerpt for a brief: the first line matching a regex and the next N lines.
# Usage: excerpt.sh <file> <regex> [lines=40]
# Exit: 0 match found, 1 no match, 2 usage or file error.
if [ "$#" -lt 2 ]; then
  echo "excerpt.sh: usage: excerpt.sh <file> <regex> [lines]" >&2
  exit 2
fi
F=$1; P=$2; N=${3:-40}
if [ ! -f "$F" ]; then
  echo "excerpt.sh: no such file: $F" >&2
  exit 2
fi
case "$N" in
  '' | *[!0-9]*)
    echo "excerpt.sh: lines must be a positive integer (got '$N')" >&2
    exit 2
    ;;
esac
# Read the count base 10 ('08' is 8); the value must be >= 1, i.e. match ^[1-9][0-9]*$.
N=$((10#$N))
if [ "$N" -lt 1 ]; then
  echo "excerpt.sh: lines must be a positive integer (got '$N')" >&2
  exit 2
fi

grep -qE -- "$P" "$F" 2>/dev/null
st=$?
if [ "$st" -gt 1 ]; then
  echo "excerpt.sh: grep error in $F for regex '$P'" >&2
  exit 2
fi
if [ "$st" -eq 1 ]; then
  echo "(no match for $P in $F)"
  exit 1
fi

n=$(grep -nE -- "$P" "$F" | head -1 | cut -d: -f1)
echo "--- $F:$n ---"
sed -n "${n},$((n + N - 1))p" "$F"
