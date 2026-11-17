#!/usr/bin/env bash
# ClawGit Pro — Issue-triage (unik feature)
set -euo pipefail
REPO="${1:?BRUG: triage.sh owner/repo}"

echo "🐛 Issue-triage: $REPO"
echo "=================================="

echo ""
echo "🔥 GAMLE issues (>30 dage) — bør gennemgås:"
gh issue list --repo "$REPO" --state open --limit 50 --json number,title,createdAt \
  --jq '.[] | select((now - (.createdAt | fromdateiso8601)) > 2592000) | "  #\(.number) [\(.createdAt[:10])] \(.title[:70])"' 2>/dev/null || echo "  (ingen)"

echo ""
echo "🏷️ Issues efter label:"
gh issue list --repo "$REPO" --state open --limit 100 --json labels,title \
  --jq '.[] | .labels[].name' 2>/dev/null | sort | uniq -c | sort -rn | head -10 || echo "  (ingen labels)"

echo ""
echo "👤 Top-issue-skabere (åbne):"
gh issue list --repo "$REPO" --state open --limit 100 --json author,title \
  --jq '.[] | .author.login' 2>/dev/null | sort | uniq -c | sort -rn | head -5 || echo "  (ingen)"

echo ""
echo "💡 Forslag: fokuser på issues uden kommentarer/assignee — de er ofte glemt:"
gh issue list --repo "$REPO" --state open --limit 50 --json number,title,comments \
  --jq '.[] | select(.comments == 0) | "  #\(.number) (0 kommentarer) \(.title[:70])"' 2>/dev/null | head -10 || true
