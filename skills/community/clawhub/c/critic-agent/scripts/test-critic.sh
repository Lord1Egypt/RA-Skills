#!/bin/bash
# Critic Agent Test Scenario
# Demonstrates spawning a critic to review a sample task output

set -e

echo "🧪 Critic Agent Pattern - Test Scenario"
echo "========================================"
echo ""

# Check prerequisites
if ! command -v openclaw &> /dev/null; then
  echo "❌ openclaw CLI not found. Please install OpenClaw."
  exit 1
fi

if ! command -v jq &> /dev/null; then
  echo "❌ jq is required. Install with: apt install jq (or brew install jq)"
  exit 1
fi

# Test configuration
TASK="Write a Python function that checks if a string is a palindrome. Ignore spaces and case."
OUTPUT="def is_palindrome(s):\n    s = s.lower().replace(' ', '')\n    return s == s[::-1]"
CONTEXT='{"requirements": ["handle edge cases like empty string", "include docstring", "handle non-string inputs"]}'

echo "📋 Task:"
echo "$TASK"
echo ""
echo "📝 Agent Output:"
echo "$OUTPUT"
echo ""
echo "📦 Context:"
echo "$CONTEXT"
echo ""

# Build critic prompt
PROMPT_TEMPLATE="$(cat /home/weq/.openclaw/workspace/skills/critic-agent/scripts/critic-system-prompt.txt)"
FULL_PROMPT=$(echo "$PROMPT_TEMPLATE" \
  | sed "s/{{TASK}}/$TASK/g" \
  | sed "s/{{OUTPUT}}/$OUTPUT/g" \
  | sed "s/{{CONTEXT}}/$CONTEXT/g")

echo "🤖 Spawning Critic Agent..."
echo ""

# Run critic agent (using --local for deterministic test)
CRITIQUE_JSON=$(echo "$FULL_PROMPT" | openclaw agent --local --json -m "$FULL_PROMPT" 2>/dev/null)

# Check if we got valid JSON
if ! echo "$CRITIQUE_JSON" | jq . > /dev/null 2>&1; then
  echo "⚠️  Critic did not return valid JSON. This may be due to missing API keys or model configuration."
  echo "Raw output: $CRITIQUE_JSON"
  echo ""
  echo "To run this test successfully:"
  echo "1. Ensure your LLM provider API key is configured (e.g., OPENROUTER_API_KEY)"
  echo "2. Or adjust the test to use a different model"
  exit 1
fi

echo "✅ Critic response received:"
echo "$CRITIQUE_JSON" | jq .
echo ""

# Extract score
SCORE=$(echo "$CRITIQUE_JSON" | jq -r '.score')
VERDICT=$(echo "$CRITIQUE_JSON" | jq -r '.overall')
SUGGESTIONS=$(echo "$CRITIQUE_JSON" | jq -r '.suggestions[]')

echo "📊 Results"
echo "---------"
echo "Score: $SCORE"
echo "Verdict: $VERDICT"
echo ""
echo "Suggestions:"
echo "$SUGGESTIONS" | sed 's/^/  • /'
echo ""

# Compute final score using helper
echo "$CRITIQUE_JSON" | node /home/weq/.openclaw/workspace/skills/critic-agent/scripts/compute-score.js > /dev/null 2>&1 || true

# Determine pass/fail
if (( $(echo "$SCORE >= 70" | bc -l 2>/dev/null || echo "$SCORE >= 70" | awk '{print ($1 >= 70)}') )); then
  echo "✅ PASS - Output meets quality threshold"
  exit 0
else
  echo "❌ FAIL - Output needs revision"
  exit 1
fi
