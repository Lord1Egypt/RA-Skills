#!/usr/bin/env bash
# Recent results — completed matches from last 3 days
set -uo pipefail
source "$(dirname "$0")/helpers.sh"

response=$(api_call "matches" "recent-results" 1800 "offset=0")
rc=$?

if [[ $rc -ne 0 ]]; then
    echo "$response"
    exit 1
fi

# Filter for completed matches
matches=$(echo "$response" | jq '[.data // [] | .[] | select(.matchEnded == true or .matchEnded == "true")]')
count=$(echo "$matches" | jq 'length')

if [[ "$count" -eq 0 ]]; then
    echo "✅ No recent completed matches found"
    exit 0
fi

echo "✅ *RECENT RESULTS*"
echo "━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "$matches" | jq -c '.[]' | head -15 | while read -r match; do
    name=$(echo "$match" | jq -r '.name // "Unknown"')
    status=$(echo "$match" | jq -r '.status // ""')
    match_type=$(echo "$match" | jq -r '.matchType // ""' | tr '[:lower:]' '[:upper:]')
    venue=$(echo "$match" | jq -r '.venue // ""')
    date_str=$(echo "$match" | jq -r '.date // ""')
    
    # Scores
    score_lines=""
    while read -r s; do
        [[ -z "$s" ]] && continue
        inning=$(echo "$s" | jq -r '.inning // ""')
        runs=$(echo "$s" | jq -r '.r // 0')
        wickets=$(echo "$s" | jq -r '.w // 0')
        overs=$(echo "$s" | jq -r '.o // 0')
        score_lines="${score_lines}   📊 ${inning}: ${runs}/${wickets} (${overs} ov)\n"
    done < <(echo "$match" | jq -c '.score // [] | .[]' 2>/dev/null)
    
    echo "🏏 *${name}*"
    [[ -n "$match_type" ]] && echo "   📋 $match_type"
    [[ -n "$date_str" ]] && echo "   📅 $(to_ist "$date_str")"
    [[ -n "$score_lines" ]] && echo -e "$score_lines"
    echo "   $(format_status "$status")"
    [[ -n "$venue" ]] && echo "   📍 $venue"
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━"
