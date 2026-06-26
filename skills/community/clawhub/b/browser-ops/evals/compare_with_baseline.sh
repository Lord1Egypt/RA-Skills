#!/usr/bin/env bash
# browser-ops with-skill vs baseline comparison
# Usage: bash evals/compare_with_baseline.sh
# NOTE: This script is a reference template. The --skill-file flag requires Claude Code Pro.

set -euo pipefail

SKILL_DIR="/tmp/browser-ops"
RESULTS_DIR="$SKILL_DIR/evals/comparison_results"
mkdir -p "$RESULTS_DIR"

QUERIES=(
  "帮我抓取 https://paulgraham.com/worked.html 的正文"
  "获取 HackerNews 今天的热门"
  "查一下招商银行今天的股价"
  "帮我在小红书上搜索旅行攻略"
  "打开 https://example.com 并截图"
)

EXPECTED_TOOLS=(
  "jina|curl|r.jina.ai"
  "opencli|hackernews"
  "opencli|sinajs|akshare|stock"
  "opencli|xiaohongshu"
  "agent-browser|screenshot|playwright"
)

echo "=== browser-ops Comparison Test ==="
echo "Date: $(date)"
echo ""

pass=0
fail=0
total=${#QUERIES[@]}

for i in "${!QUERIES[@]}"; do
  query="${QUERIES[$i]}"
  expected="${EXPECTED_TOOLS[$i]}"
  echo "--- Test $((i+1))/$total ---"
  echo "Query: $query"
  echo "Expected tools: $expected"

  # Run WITH skill (using --skill-file to load SKILL.md)
  echo "  Running with skill..."
  result=$(timeout 30 env CLAUDE_SKILLS_PATH="$SKILL_DIR" claude -p "$query" --allowedTools '' 2>/dev/null || echo "TIMEOUT")

  # Check if expected tool/approach was mentioned
  matched=false
  IFS='|' read -ra patterns <<< "$expected"
  for pat in "${patterns[@]}"; do
    if echo "$result" | grep -qi "$pat"; then
      matched=true
      break
    fi
  done

  if $matched; then
    echo "  PASS: Correct tool selected"
    ((pass++))
  else
    echo "  FAIL: Expected pattern not found"
    echo "  Response preview: $(echo "$result" | head -3)"
    ((fail++))
  fi

  # Save full result
  echo "$result" > "$RESULTS_DIR/test_$((i+1))_with_skill.txt"
  echo ""
done

echo "=== Results ==="
echo "Passed: $pass/$total"
echo "Failed: $fail/$total"
echo "Results saved to: $RESULTS_DIR/"
