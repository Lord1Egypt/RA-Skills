#!/bin/bash
# ClawOrchestrate — Secure Broadcast Script
# Dispatches a message to all registered agents across all machines
# Usage: bash dispatch-all.sh "Your message here"

MESSAGE="${1:-Daily standup — report progress and blockers.}"
API_KEY="${CLAWORCHESTRATE_KEY:-changeme}"

# Generate a secure key: openssl rand -hex 32
# Set it: export CLAWORCHESTRATE_KEY="your-key-here"

# PC2 Agents
PC2="100.73.101.62"
PC2_AGENTS=("byondedu-ceo" "agentsocial-ceo")

# PC3 Agents
PC3="100.109.228.58"
PC3_AGENTS=("main" "pleij" "social-strategist")

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "[$TIMESTAMP] Broadcasting: $MESSAGE"
echo ""

for agent in "${PC2_AGENTS[@]}"; do
    echo -n "  PC2 → $agent: "
    result=$(curl -s -X POST "http://$PC2:9876/dispatch" \
        -H 'Content-Type: application/json' \
        -H "Authorization: Bearer $API_KEY" \
        -d "{\"agent\":\"$agent\",\"message\":\"$MESSAGE\"}" 2>&1)
    echo "$result"
done

for agent in "${PC3_AGENTS[@]}"; do
    echo -n "  PC3 → $agent: "
    result=$(curl -s -X POST "http://$PC3:9876/dispatch" \
        -H 'Content-Type: application/json' \
        -H "Authorization: Bearer $API_KEY" \
        -d "{\"agent\":\"$agent\",\"message\":\"$MESSAGE\"}" 2>&1)
    echo "$result"
done

echo ""
echo "Broadcast complete."
