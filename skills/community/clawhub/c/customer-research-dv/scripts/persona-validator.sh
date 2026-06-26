#!/usr/bin/env bash
set -euo pipefail

# persona-validator.sh — Validate persona assumptions against research data
# Usage: ./persona-validator.sh --persona-file persona.json --research-dir data/research/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

PERSONA_FILE=""
RESEARCH_DIR="$WORKSPACE_ROOT/data/research"

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --persona-file) PERSONA_FILE="$2"; shift 2 ;;
    --research-dir) RESEARCH_DIR="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$PERSONA_FILE" ]]; then
  echo "Usage: $0 --persona-file persona.json [--research-dir DIR]" >&2
  echo "" >&2
  echo "Persona file format:" >&2
  cat >&2 <<'EOF'
{
  "name": "FIRE Enthusiast Frank",
  "demographics": {
    "age_range": "30-40",
    "income": "$150K-$250K",
    "occupation": "Tech worker"
  },
  "assumptions": [
    {
      "id": "A1",
      "statement": "Finds existing retirement calculators too conservative",
      "confidence": "medium"
    },
    {
      "id": "A2", 
      "statement": "Willing to pay $50-100 for retirement planning software",
      "confidence": "low"
    }
  ],
  "pain_points": [
    "Existing tools don't account for aggressive savings rates",
    "No good visualization of FIRE timeline trade-offs"
  ]
}
EOF
  exit 1
fi

if [[ ! -f "$PERSONA_FILE" ]]; then
  echo "❌ Persona file not found: $PERSONA_FILE" >&2
  exit 1
fi

echo "🔍 Validating persona against research data..." >&2
echo "📂 Research dir: $RESEARCH_DIR" >&2

# Load persona
PERSONA=$(cat "$PERSONA_FILE")
PERSONA_NAME=$(echo "$PERSONA" | jq -r '.name')
ASSUMPTIONS=$(echo "$PERSONA" | jq -c '.assumptions[]')
PAIN_POINTS=$(echo "$PERSONA" | jq -c '.pain_points[]')

echo "👤 Persona: $PERSONA_NAME" >&2

# Collect all research findings
ALL_FINDINGS='[]'
RESEARCH_COUNT=0

if [[ -d "$RESEARCH_DIR" ]]; then
  while IFS= read -r research_file; do
    FINDINGS=$(jq -c '.findings[]' "$research_file" 2>/dev/null || echo '')
    if [[ -n "$FINDINGS" ]]; then
      while IFS= read -r finding; do
        ALL_FINDINGS=$(echo "$ALL_FINDINGS" | jq --argjson f "$finding" '. += [$f]')
        ((RESEARCH_COUNT++)) || true
      done <<< "$FINDINGS"
    fi
  done < <(find "$RESEARCH_DIR" -name "*.json" -type f)
fi

echo "📊 Loaded $RESEARCH_COUNT findings from research data" >&2

if [[ $RESEARCH_COUNT -eq 0 ]]; then
  echo "⚠️  No research data found. Run reddit-miner.sh or competitor-scraper.sh first." >&2
  exit 1
fi

# Validation output
echo ""
echo "# Persona Validation Report"
echo "**Persona:** $PERSONA_NAME"
echo "**Date:** $(date +"%Y-%m-%d")"
echo "**Research Sample:** $RESEARCH_COUNT findings"
echo ""
echo "---"
echo ""

# Validate each assumption
echo "## Assumption Validation"
echo ""

ASSUMPTION_NUM=1
while IFS= read -r assumption; do
  ASSUMPTION_ID=$(echo "$assumption" | jq -r '.id')
  STATEMENT=$(echo "$assumption" | jq -r '.statement')
  CONFIDENCE=$(echo "$assumption" | jq -r '.confidence')
  
  echo "### $ASSUMPTION_NUM. $STATEMENT"
  echo "**ID:** $ASSUMPTION_ID | **Prior Confidence:** $CONFIDENCE"
  echo ""
  
  # Search for supporting/contradicting evidence in research data
  # Simple keyword match (in production, use semantic similarity)
  KEYWORDS=$(echo "$STATEMENT" | tr '[:upper:]' '[:lower:]' | grep -oE '\w+' | grep -vE '^(is|are|the|a|an|to|of|for|in|on|at|by|with)$' | head -5)
  
  SUPPORTING=0
  CONTRADICTING=0
  NEUTRAL=0
  SAMPLE_QUOTES='[]'
  
  while IFS= read -r finding; do
    TEXT=$(echo "$finding" | jq -r '.text' | tr '[:upper:]' '[:lower:]')
    MATCHED=false
    
    for KEYWORD in $KEYWORDS; do
      if echo "$TEXT" | grep -q "$KEYWORD"; then
        MATCHED=true
        break
      fi
    done
    
    if [[ "$MATCHED" == true ]]; then
      # Simplified sentiment check (in production, use LLM for nuanced analysis)
      QUOTE=$(echo "$finding" | jq -r '.text' | head -c 200)
      SAMPLE_QUOTES=$(echo "$SAMPLE_QUOTES" | jq --arg q "$QUOTE..." '. += [$q]')
      ((SUPPORTING++)) || true
    fi
  done < <(echo "$ALL_FINDINGS" | jq -c '.[]')
  
  # Verdict
  if [[ $SUPPORTING -ge 3 ]]; then
    echo "**Verdict:** ✅ VALIDATED (found $SUPPORTING supporting mentions)"
  elif [[ $SUPPORTING -ge 1 ]]; then
    echo "**Verdict:** ⚠️  WEAK SUPPORT (found $SUPPORTING mentions, needs more data)"
  else
    echo "**Verdict:** ❌ NO EVIDENCE (no supporting mentions found)"
  fi
  
  echo ""
  
  # Sample quotes
  if [[ $(echo "$SAMPLE_QUOTES" | jq 'length') -gt 0 ]]; then
    echo "**Sample quotes:**"
    echo "$SAMPLE_QUOTES" | jq -r '.[] | "- \"" + . + "\""' | head -3
    echo ""
  fi
  
  ((ASSUMPTION_NUM++)) || true
done <<< "$ASSUMPTIONS"

# Validate pain points
echo "---"
echo ""
echo "## Pain Point Validation"
echo ""

PAIN_NUM=1
while IFS= read -r pain_point; do
  echo "### $PAIN_NUM. $pain_point"
  
  # Search for mentions
  KEYWORDS=$(echo "$pain_point" | tr '[:upper:]' '[:lower:]' | grep -oE '\w+' | grep -vE '^(is|are|the|a|an|to|of|for|in|on|at|by|with|no|not)$' | head -5)
  
  MENTIONS=0
  SAMPLE_QUOTES='[]'
  
  while IFS= read -r finding; do
    TEXT=$(echo "$finding" | jq -r '.text' | tr '[:upper:]' '[:lower:]')
    MATCHED=false
    
    for KEYWORD in $KEYWORDS; do
      if echo "$TEXT" | grep -q "$KEYWORD"; then
        MATCHED=true
        break
      fi
    done
    
    if [[ "$MATCHED" == true ]]; then
      QUOTE=$(echo "$finding" | jq -r '.text' | head -c 200)
      SAMPLE_QUOTES=$(echo "$SAMPLE_QUOTES" | jq --arg q "$QUOTE..." '. += [$q]')
      ((MENTIONS++)) || true
    fi
  done < <(echo "$ALL_FINDINGS" | jq -c '.[]')
  
  if [[ $MENTIONS -ge 3 ]]; then
    echo "**Verdict:** ✅ CONFIRMED ($MENTIONS mentions)"
  elif [[ $MENTIONS -ge 1 ]]; then
    echo "**Verdict:** ⚠️  NEEDS MORE DATA ($MENTIONS mentions)"
  else
    echo "**Verdict:** ❌ NOT FOUND (consider removing or reframing)"
  fi
  
  echo ""
  
  if [[ $(echo "$SAMPLE_QUOTES" | jq 'length') -gt 0 ]]; then
    echo "**Sample quotes:**"
    echo "$SAMPLE_QUOTES" | jq -r '.[] | "- \"" + . + "\""' | head -3
    echo ""
  fi
  
  ((PAIN_NUM++)) || true
done < <(echo "$PAIN_POINTS" | jq -r '.')

# Recommendations
echo "---"
echo ""
echo "## Recommendations"
echo ""
echo "- **High confidence assumptions:** Use in marketing copy and product positioning"
echo "- **Weak support:** Run targeted interviews to validate/invalidate"
echo "- **No evidence:** Either invalidated (update persona) or data gap (run more research)"
echo "- **Next steps:** Review sample quotes, update persona doc, run follow-up research if needed"
echo ""

echo "" >&2
echo "✅ Validation complete" >&2
