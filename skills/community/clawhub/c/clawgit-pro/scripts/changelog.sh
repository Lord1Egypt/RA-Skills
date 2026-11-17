#!/usr/bin/env bash
# ClawGit Pro — Auto-changelog-generator (unik feature)
set -euo pipefail
REPO="${1:?BRUG: changelog.sh owner/repo [tag1 tag2 | --since dato]}"
shift

echo "# Changelog — $REPO"
echo ""

if [ "${1:-}" = "--since" ]; then
    SINCE="${2:?Angiv dato, f.eks. 2026-01-01}"
    echo "## Siden $SINCE"
    gh api "repos/$REPO/commits?since=${SINCE}T00:00:00Z&per_page=50" \
      --jq '.[] | "- \(.commit.message | split("\n")[0]) (\(.commit.author.name))"' 2>/dev/null
else
    TAG1="${1:?Angiv tag1 tag2 eller --since dato}"
    TAG2="${2:?Angiv tag2}"
    echo "## $TAG1 → $TAG2"
    gh api "repos/$REPO/compare/$TAG1...$TAG2" \
      --jq '.commits[] | "- \(.commit.message | split("\n")[0]) (\(.commit.author.name))"' 2>/dev/null
fi

echo ""
echo "## PR'er"
gh pr list --repo "$REPO" --state merged --limit 20 --json number,title,mergedAt \
  --jq '.[] | "- #\(.number) \(.title) [merged \(.mergedAt[:10])]"' 2>/dev/null || true
