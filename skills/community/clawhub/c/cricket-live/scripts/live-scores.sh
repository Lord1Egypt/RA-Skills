#!/usr/bin/env bash
# Live cricket scores — all currently live matches
set -uo pipefail
source "$(dirname "$0")/helpers.sh"

response=$(api_call "currentMatches" "live-matches" 120)
rc=$?

if [[ $rc -eq 2 ]]; then
    echo "$response"
    exit 1
fi

if [[ $rc -ne 0 ]]; then
    echo "$response"
    exit 1
fi

matches=$(echo "$response" | jq -r '.data // []')
count=$(echo "$matches" | jq 'length')

if [[ "$count" -eq 0 ]] || [[ "$matches" == "[]" ]]; then
    echo "🏏 No live matches right now"
    echo ""
    echo "Check upcoming matches: bash scripts/upcoming-matches.sh"
    exit 0
fi

echo "🔴 *LIVE CRICKET SCORES*"
echo "━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "$matches" | jq -c '.[]' | while read -r match; do
    name=$(echo "$match" | jq -r '.name // "Unknown"')
    status=$(echo "$match" | jq -r '.status // "In Progress"')
    match_type=$(echo "$match" | jq -r '.matchType // ""' | tr '[:lower:]' '[:upper:]')
    venue=$(echo "$match" | jq -r '.venue // ""')
    id=$(echo "$match" | jq -r '.id // ""')
    
    # Teams and scores
    teams=$(echo "$match" | jq -r '.teams // []')
    t1=$(echo "$teams" | jq -r '.[0] // ""')
    t2=$(echo "$teams" | jq -r '.[1] // ""')
    
    score=$(echo "$match" | jq -r '.score // []')
    
    e1=$(team_emoji "$t1")
    e2=$(team_emoji "$t2")
    
    echo "🏏 *${t1} vs ${t2}*"
    [[ -n "$match_type" ]] && echo "   📋 $match_type"
    
    # Display scores
    echo "$score" | jq -c '.[]' 2>/dev/null | while read -r s; do
        inning=$(echo "$s" | jq -r '.inning // ""')
        runs=$(echo "$s" | jq -r '.r // 0')
        wickets=$(echo "$s" | jq -r '.w // 0')
        overs=$(echo "$s" | jq -r '.o // 0')
        echo "   📊 ${inning}: ${runs}/${wickets} (${overs} ov)"
    done
    
    echo "   $(format_status "$status")"
    [[ -n "$venue" ]] && echo "   📍 $venue"
    [[ -n "$id" ]] && echo "   🔗 ID: $id"
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Details: bash scripts/match-details.sh <match-id>"
