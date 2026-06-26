#!/usr/bin/env bash
set -euo pipefail

# Fleet PR Agent — Multi-repo PR triage
# Usage: triage.sh owner/repo1 [owner/repo2 ...] [--output file.md]

STALE_DAYS="${FLEET_PR_STALE_DAYS:-5}"
CI_WEIGHT="${FLEET_PR_CI_WEIGHT:-3}"
MAX_PRS="${FLEET_PR_MAX_PRS:-50}"
OUTPUT_FILE=""
REPOS=()

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --output) OUTPUT_FILE="$2"; shift 2 ;;
    *) REPOS+=("$1"); shift ;;
  esac
done

if [[ ${#REPOS[@]} -eq 0 ]]; then
  echo "Usage: triage.sh owner/repo1 [owner/repo2 ...] [--output file.md]"
  exit 1
fi

# Check gh auth
if ! gh auth status &>/dev/null; then
  echo "Error: gh CLI not authenticated. Run 'gh auth login' first."
  exit 1
fi

TODAY=$(date -u +%Y-%m-%d)
STALE_CUTOFF=$(date -u -d "${STALE_DAYS} days ago" +%Y-%m-%d 2>/dev/null || date -u -v-${STALE_DAYS}d +%Y-%m-%d 2>/dev/null || echo "")

report="## PR Triage Report — ${TODAY}\n\n"

p0=()
p1=()
p2=()
p3=()
total=0

for REPO in "${REPOS[@]}"; do
  # Fetch open PRs as JSON
  prs_json=$(gh pr list --repo "$REPO" --state open --limit "$MAX_PRS" --json number,title,url,createdAt,updatedAt,isDraft,reviewDecision,statusCheckRollup,labels,reviewRequests 2>/dev/null || echo "[]")

  count=$(echo "$prs_json" | jq 'length')
  total=$((total + count))

  for i in $(seq 0 $((count - 1))); do
    pr=$(echo "$prs_json" | jq ".[$i]")
    number=$(echo "$pr" | jq -r '.number')
    title=$(echo "$pr" | jq -r '.title')
    url=$(echo "$pr" | jq -r '.url')
    created=$(echo "$pr" | jq -r '.createdAt' | cut -d'T' -f1)
    updated=$(echo "$pr" | jq -r '.updatedAt' | cut -d'T' -f1)
    is_draft=$(echo "$pr" | jq -r '.isDraft')
    review_decision=$(echo "$pr" | jq -r '.reviewDecision // "NONE"')

    # Check CI status
    ci_state=$(echo "$pr" | jq -r '
      if (.statusCheckRollup | length) == 0 then "UNKNOWN"
      elif [.statusCheckRollup[] | select(.conclusion == "FAILURE")] | length > 0 then "FAILURE"
      elif [.statusCheckRollup[] | select(.conclusion == "SUCCESS")] | length == (.statusCheckRollup | length) then "SUCCESS"
      else "PENDING"
      end
    ')

    # Calculate age in days (approximate)
    created_epoch=$(date -d "$created" +%s 2>/dev/null || date -jf "%Y-%m-%d" "$created" +%s 2>/dev/null || echo 0)
    today_epoch=$(date -u +%s)
    age_days=$(( (today_epoch - created_epoch) / 86400 ))

    entry="- [#${number} ${title}](${url}) — age: ${age_days}d, CI: ${ci_state}, review: ${review_decision}"

    # Classify
    if [[ "$ci_state" == "FAILURE" && $age_days -ge 3 ]]; then
      p0+=("$entry")
    elif [[ "$review_decision" == "APPROVED" ]] || [[ "$age_days" -ge 2 && "$review_decision" == "REVIEW_REQUIRED" ]]; then
      p1+=("$entry")
    elif [[ $age_days -ge $STALE_DAYS && "$is_draft" != "true" ]]; then
      p2+=("$entry")
    else
      p3+=("$entry")
    fi
  done
done

# Build report
needs_attention=$(( ${#p0[@]} + ${#p1[@]} ))

if [[ ${#p0[@]} -gt 0 ]]; then
  report+="### P0 — Critical (${#p0[@]})\n"
  for e in "${p0[@]}"; do report+="${e}\n"; done
  report+="\n"
fi

if [[ ${#p1[@]} -gt 0 ]]; then
  report+="### P1 — High (${#p1[@]})\n"
  for e in "${p1[@]}"; do report+="${e}\n"; done
  report+="\n"
fi

if [[ ${#p2[@]} -gt 0 ]]; then
  report+="### P2 — Medium (${#p2[@]})\n"
  for e in "${p2[@]}"; do report+="${e}\n"; done
  report+="\n"
fi

if [[ ${#p3[@]} -gt 0 ]]; then
  report+="### P3 — Low (${#p3[@]})\n"
  for e in "${p3[@]}"; do report+="${e}\n"; done
  report+="\n"
fi

report+="### Summary\n"
report+="- Total open PRs: ${total}\n"
report+="- Needing attention: ${needs_attention}\n"
report+="- Repos scanned: ${#REPOS[@]}\n"

if [[ -n "$OUTPUT_FILE" ]]; then
  echo -e "$report" > "$OUTPUT_FILE"
  echo "Report written to $OUTPUT_FILE"
else
  echo -e "$report"
fi
