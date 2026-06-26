#!/bin/bash
# Check GitHub repos for failed CI runs and report new failures.
#
# Usage: ./check-ci-failures.sh [--repos "repo1 repo2"] [--owner "GitHubUser"]
#
# Requires: gh CLI (authenticated)
# Output: "OK" if no failures, "FAILURES\n❌ repo: details" if failures found.
# Tracks last check time in a state file to only report NEW failures.

OWNER="${GITHUB_OWNER:-$(gh api user -q .login 2>/dev/null)}"
STATE_FILE="${CI_STATE_FILE:-$HOME/.openclaw/workspace/memory/ci-check-state.json}"

# Auto-discover repos if not provided
if [ -n "$1" ] && [ "$1" = "--repos" ]; then
  REPOS="$2"
elif [ -n "$CI_REPOS" ]; then
  REPOS="$CI_REPOS"
else
  # Auto-discover: all repos with GitHub Actions
  REPOS=$(gh repo list "$OWNER" --limit 50 --json name,hasWiki \
    -q '.[].name' 2>/dev/null | tr '\n' ' ')
fi

# Initialize state file if missing
if [ ! -f "$STATE_FILE" ]; then
  mkdir -p "$(dirname "$STATE_FILE")"
  echo '{"lastCheck":"2026-01-01T00:00:00Z"}' > "$STATE_FILE"
fi

LAST_CHECK=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['lastCheck'])" 2>/dev/null || echo "2026-01-01T00:00:00Z")
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
FAILURES=""
CHECKED=0

for REPO in $REPOS; do
  CHECKED=$((CHECKED + 1))
  
  # Get failed runs since last check
  FAILED=$(gh run list --repo "$OWNER/$REPO" --status failure --json databaseId,createdAt \
    -q "[.[] | select(.createdAt > \"$LAST_CHECK\")] | length" 2>/dev/null)
  
  if [ "$FAILED" != "" ] && [ "$FAILED" != "0" ]; then
    DETAIL=$(gh run list --repo "$OWNER/$REPO" --status failure --limit 1 --json name,headBranch,url \
      -q '.[0] | "\(.name) on \(.headBranch)"' 2>/dev/null)
    URL=$(gh run list --repo "$OWNER/$REPO" --status failure --limit 1 --json url -q '.[0].url' 2>/dev/null)
    FAILURES="$FAILURES\n❌ $REPO: $DETAIL ($FAILED new) $URL"
  fi
done

# Update last check time
python3 -c "import json; json.dump({'lastCheck':'$NOW'}, open('$STATE_FILE','w'))" 2>/dev/null

if [ -n "$FAILURES" ]; then
  echo -e "FAILURES ($CHECKED repos checked)$FAILURES"
else
  echo "OK"
fi
