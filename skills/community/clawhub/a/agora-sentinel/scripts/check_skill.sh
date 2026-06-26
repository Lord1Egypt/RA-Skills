#!/bin/bash
# Agora Sentinel — Check a single ClawHub skill's trust score
# Usage: bash scripts/check_skill.sh <skill-slug>

SLUG="$1"
API="https://checksafe.dev/api/v1"

if [ -z "$SLUG" ]; then
    echo "Usage: check_skill.sh <skill-slug>"
    echo "Example: check_skill.sh crypto-wallet-helper"
    exit 1
fi

# Fetch badge data
BADGE_DATA=$(curl -sf "${API}/skills/${SLUG}/badge.json" 2>/dev/null)

if [ $? -ne 0 ] || [ -z "$BADGE_DATA" ]; then
    echo "  Skill '${SLUG}' not found in Sentinel database."
    echo "It may be too new or not yet scanned."
    echo "Check manually: ${API}/skills/${SLUG}"
    exit 1
fi

# Parse JSON (using python3 for portability since jq may not be available)
python3 -c "
import json, sys
data = json.loads('''${BADGE_DATA}''')
badge = data.get('message', data.get('badge', 'UNKNOWN')).upper()
score = data.get('trust_score', data.get('score', 0))
tier = data.get('tier', 0)
slug = data.get('slug', '${SLUG}')

# Badge emoji
emojis = {'TRUSTED': '\U0001f7e2', 'CLEAN': '\U0001f535', 'CAUTION': '\U0001f7e1', 'WARNING': '\U0001f7e0', 'DANGER': '\U0001f534'}
emoji = emojis.get(badge, '\u26aa')

print(f'')
print(f'{emoji} Agora Sentinel Report: {slug}')
print(f'   Badge:   {badge}')
print(f'   Score:   {score}/100')
print(f'   Tier:    {tier}/4')
print(f'   Details: https://checksafe.dev/dashboard/{slug}')
print(f'')

if badge == 'DANGER':
    print('\U0001f6ab DANGER: This skill has been flagged as potentially malicious.')
    print('   DO NOT install without reviewing the full report.')
elif badge == 'WARNING':
    print('\u26a0\ufe0f  WARNING: This skill has significant security concerns.')
    print('   Review findings before installing.')
elif badge == 'CAUTION':
    print('\u26a1 CAUTION: Some concerns detected. Review recommended.')
elif badge == 'CLEAN':
    print('\u2705 Clean: No significant issues detected.')
elif badge == 'TRUSTED':
    print('\u2705 Trusted: This skill has a strong safety record.')
" 2>/dev/null

if [ $? -ne 0 ]; then
    # Fallback if python parsing fails — just show raw JSON
    echo "Sentinel result for ${SLUG}:"
    echo "$BADGE_DATA"
fi
