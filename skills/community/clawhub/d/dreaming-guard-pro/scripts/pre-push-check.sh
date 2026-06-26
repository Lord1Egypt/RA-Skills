#!/bin/bash
# Pre-push脱敏检查
echo "🔍 Checking for sensitive data..."
PATTERNS="sk-\|apiKey\|clientSecret\|openid\|Bearer \|ck-\|AIzaSy"
HITS=$(grep -rnE "$PATTERNS" --include="*.js" --include="*.md" --include="*.json" src/ 2>/dev/null)
if [ -n "$HITS" ]; then
  echo "❌ Sensitive data found!"
  echo "$HITS"
  exit 1
fi
echo "✅ No sensitive data found. Safe to push."
