#!/usr/bin/env bash
# ClawGit Pro — Repo-sundhedsrapport (unik feature)
set -euo pipefail
REPO="${1:?BRUG: repo_health.sh owner/repo}"

echo "🐙 Sundhedsrapport: $REPO"
echo "=================================="

# Basis-info
INFO=$(gh api "repos/$REPO" --jq '{stars: .stargazers_count, forks: .forks_count, open_issues: .open_issues_count, pushed: .pushed_at, created: .created_at, desc: .description}' 2>/dev/null || echo "{}")
STARS=$(echo "$INFO" | jq -r '.stars // "?"')
FORKS=$(echo "$INFO" | jq -r '.forks // "?"')
ISSUES=$(echo "$INFO" | jq -r '.open_issues // "?"')
PUSHED=$(echo "$INFO" | jq -r '.pushed // "?"')
echo "⭐ Stars: $STARS · 🍴 Forks: $FORKS · 🐛 Åbne issues: $ISSUES"
echo "📅 Sidst push: ${PUSHED:-?}"

# PR-alder (ældste åbne PR)
echo ""
echo "⏳ Ældste åbne PR'er:"
gh pr list --repo "$REPO" --state open --limit 5 --json number,title,createdAt --jq '.[] | "  #\(.number) [\(.createdAt[:10])] \(.title[:70])"' 2>/dev/null || echo "  (ingen eller ingen adgang)"

# Issue-alder
echo ""
echo "🐛 Ældste åbne issues:"
gh issue list --repo "$REPO" --state open --limit 5 --json number,title,createdAt --jq '.[] | "  #\(.number) [\(.createdAt[:10])] \(.title[:70])"' 2>/dev/null || echo "  (ingen eller ingen adgang)"

# CI-status (sidste run)
echo ""
echo "🔧 Sidste workflow-runs:"
gh run list --repo "$REPO" --limit 3 --json name,status,conclusion,createdAt --jq '.[] | "  \(.conclusion // .status) — \(.name[:50])"' 2>/dev/null || echo "  (ingen)"
