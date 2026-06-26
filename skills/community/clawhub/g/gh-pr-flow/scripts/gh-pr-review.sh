#!/usr/bin/env bash
# gh-pr-review.sh — Review pending PRs: status, checks, requested reviewers
# Usage: gh-pr-review.sh [--mine] [--repo owner/repo]

set -euo pipefail

SHOW_MINE=false
REPO=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mine) SHOW_MINE=true; shift ;;
    --repo) REPO="$2"; shift 2 ;;
    --help)
      echo "Usage: $0 [--mine] [--repo owner/repo]"
      exit 0
      ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

GH_ARGS=()
[ -n "$REPO" ] && GH_ARGS+=(--repo "$REPO")

echo "=== Pending PRs ==="
if $SHOW_MINE; then
  echo "--- PRs I Created ---"
  gh pr list "${GH_ARGS[@]}" --author "@me" --state open \
    --json number,title,headRefName,baseRefName,reviewDecision \
    --jq '.[] | "#" + (.number|tostring) + " | " + .title + " | " + .baseRefName + " ← " + .headRefName + " | reviews: " + (.reviewDecision // "—")'
  echo ""
  echo "--- PRs Requesting My Review ---"
  gh pr list "${GH_ARGS[@]}" --search "review-requested:@me" --state open \
    --json number,title,author,headRefName,baseRefName,reviewDecision \
    --jq '.[] | "#" + (.number|tostring) + " by @" + .author.login + " | " + .title + " | " + .baseRefName + " ← " + .headRefName + " | reviews: " + (.reviewDecision // "—")'
else
  gh pr list "${GH_ARGS[@]}" --state open --limit 30 \
    --json number,title,author,headRefName,baseRefName,reviewDecision,createdAt \
    --jq 'group_by(.author.login) | .[] | "Author: @" + (.[0].author.login) + "\n" + (map("#" + (.number|tostring) + " | " + .title + " | " + .baseRefName + " ← " + .headRefName + " | reviews: " + (.reviewDecision // "—")) | join("\n")) + "\n"'
fi

echo ""
echo "=== CI Status (last 5 PRs) ==="
gh pr list "${GH_ARGS[@]}" --state open --limit 5 \
  --json number,title,statusCheckRollup \
  --jq '.[] | "PR #" + (.number|tostring) + ": " + .title + "\n" + ((.statusCheckRollup // []) | map("  " + .context + " → " + .state) | join("\n")) + "\n"'
