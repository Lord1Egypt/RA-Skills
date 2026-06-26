#!/usr/bin/env bash
# trust-check.sh — Quick trust lookup for an AXIS-registered agent
# Usage: ./trust-check.sh <AUID>
# Example: ./trust-check.sh "axis:autonomous.registry:enterprise:f1a9x9deck2ed7m9261n:f1a99dec2ed79261"
#
# No authentication required. Public endpoint.

set -euo pipefail

AUID="${1:?Usage: $0 <AUID>}"
BASE_URL="https://www.axistrust.io/api/trpc"

# URL-encode the JSON input
INPUT=$(python3 -c "import urllib.parse, json; print(urllib.parse.quote(json.dumps({'json':{'auid':'$AUID'}})))")

echo "Looking up agent: $AUID"
echo ""

RESPONSE=$(curl -sf "$BASE_URL/agents.getByAuid?input=$INPUT")

# Parse and display key fields
echo "$RESPONSE" | python3 -c "
import json, sys

data = json.load(sys.stdin)
agent = data['result']['data']['json']
trust = agent.get('trustScore', {})
credit = agent.get('creditScore', {})

print('=== AXIS Trust Profile ===')
print(f'Name:        {agent.get(\"name\", \"Unknown\")}')
print(f'AUID:        {agent.get(\"auid\", \"Unknown\")}')
print(f'Class:       {agent.get(\"agentClass\", \"Unknown\")}')
print(f'Model:       {agent.get(\"foundationModel\", \"Unknown\")}')
print()
print(f'T-Score:     {trust.get(\"tScore\", \"N/A\")} / 1000')
print(f'Trust Tier:  T{trust.get(\"trustTier\", \"?\")}'  )
print(f'C-Score:     {credit.get(\"cScore\", \"N/A\")} / 1000')
print(f'Credit Tier: {credit.get(\"creditTier\", \"N/A\")}')
print()

t_score = trust.get('tScore', 0)
if t_score >= 750:
    print('VERDICT: TRUSTED — Safe to delegate tasks and share data.')
elif t_score >= 500:
    print('VERDICT: VERIFIED — Safe for standard tasks. Verify before sensitive operations.')
elif t_score >= 250:
    print('VERDICT: PROVISIONAL — Low-risk tasks only. Monitor closely.')
else:
    print('VERDICT: UNVERIFIED — Do not delegate. Request manual verification.')
"
