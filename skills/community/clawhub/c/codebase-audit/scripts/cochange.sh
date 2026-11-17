#!/bin/sh
# List file pairs in different folders that change in the same commits.
# Usage: cochange.sh [since="12 months ago"] [min_commits=3] [path=.]
# Output: commits-together  share-of-the-rarer-file  fileA  fileB
# Commits touching more than 30 files (renames, formatting sweeps) are ignored.
# Lockfiles are skipped; set EXCLUDE to an extra regex of paths to skip (e.g. EXCLUDE='^\.claude-status/').
since=${1:-12 months ago}
min=${2:-3}
path=${3:-.}

git log --since="$since" --no-merges --name-only --format='tformat:@@' -- "$path" |
awk -v min="$min" -v extra="${EXCLUDE:-^$}" '
function dir(p) { return (p ~ /\//) ? substr(p, 1, match(p, /\/[^\/]*$/) - 1) : "." }
function flush(   i, j, a, b, t) {
  if (n > 1 && n <= 30)
    for (i = 1; i <= n; i++)
      for (j = i + 1; j <= n; j++) {
        a = f[i]; b = f[j]
        if (a > b) { t = a; a = b; b = t }
        if (dir(a) != dir(b)) pair[a SUBSEP b]++
      }
  n = 0
}
/^@@$/ { flush(); next }
/(^|\/)(package-lock\.json|pnpm-lock\.yaml|yarn\.lock|[^\/]*\.lock|Package\.resolved|go\.sum|Cargo\.lock|poetry\.lock)$/ { next }
NF && $0 !~ extra { f[++n] = $0; touched[$0]++ }
END {
  flush()
  for (p in pair) if (pair[p] >= min) {
    split(p, x, SUBSEP)
    rare = touched[x[1]] < touched[x[2]] ? touched[x[1]] : touched[x[2]]
    printf "%d\t%d%%\t%s\t%s\n", pair[p], int(100 * pair[p] / rare), x[1], x[2]
  }
}' | sort -t "$(printf '\t')" -k1,1nr -k2,2nr | head -50
