#!/bin/bash
# Context Slimmer - Measure always-loaded context files
# Usage: bash measure.sh [--audit] [--workspace /path/to/workspace]

WORKSPACE="${2:-$(pwd)}"
AUDIT=false
[[ "$1" == "--audit" ]] && AUDIT=true

FILES="AGENTS.md TOOLS.md USER.md MEMORY.md HEARTBEAT.md SOUL.md IDENTITY.md"
TOTAL_BYTES=0
TOTAL_TOKENS=0

echo "📏 Context File Sizes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "%-20s %8s %8s %6s\n" "File" "Bytes" "~Tokens" "Lines"
echo "───────────────────────────────────────"

for f in $FILES; do
  filepath="$WORKSPACE/$f"
  if [ -f "$filepath" ]; then
    bytes=$(wc -c < "$filepath" | tr -d ' ')
    lines=$(wc -l < "$filepath" | tr -d ' ')
    tokens=$((bytes / 4))
    TOTAL_BYTES=$((TOTAL_BYTES + bytes))
    TOTAL_TOKENS=$((TOTAL_TOKENS + tokens))
    
    # Flag if over target
    flag=""
    case "$f" in
      AGENTS.md)     [[ $tokens -gt 500 ]] && flag=" ⚠️" ;;
      TOOLS.md)      [[ $tokens -gt 500 ]] && flag=" ⚠️" ;;
      USER.md)       [[ $tokens -gt 700 ]] && flag=" ⚠️" ;;
      MEMORY.md)     [[ $tokens -gt 400 ]] && flag=" ⚠️" ;;
      HEARTBEAT.md)  [[ $tokens -gt 400 ]] && flag=" ⚠️" ;;
      SOUL.md)       [[ $tokens -gt 250 ]] && flag=" ⚠️" ;;
      IDENTITY.md)   [[ $tokens -gt 50 ]]  && flag=" ⚠️" ;;
    esac
    
    printf "%-20s %8d %8d %6d%s\n" "$f" "$bytes" "$tokens" "$lines" "$flag"
  else
    printf "%-20s %8s %8s %6s\n" "$f" "MISSING" "-" "-"
  fi
done

echo "───────────────────────────────────────"
printf "%-20s %8d %8d\n" "TOTAL" "$TOTAL_BYTES" "$TOTAL_TOKENS"
echo ""
echo "Target: < 2,800 tokens"
if [ $TOTAL_TOKENS -le 2800 ]; then
  echo "✅ Within target"
else
  echo "⚠️  Over target by $((TOTAL_TOKENS - 2800)) tokens"
fi

if $AUDIT; then
  echo ""
  echo "📋 Audit Checklist"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  for f in $FILES; do
    filepath="$WORKSPACE/$f"
    if [ -f "$filepath" ]; then
      echo ""
      echo "--- $f ---"
      
      # Check for duplicate content across files
      echo "Potential duplicates:"
      for other in $FILES; do
        [[ "$f" == "$other" ]] && continue
        otherpath="$WORKSPACE/$other"
        [ -f "$otherpath" ] || continue
        # Find shared non-trivial lines (>20 chars)
        common=$(comm -12 <(grep -oE '.{20,}' "$filepath" 2>/dev/null | sort -u) <(grep -oE '.{20,}' "$otherpath" 2>/dev/null | sort -u) | head -3)
        [[ -n "$common" ]] && echo "  ↔ $other: $(echo "$common" | wc -l | tr -d ' ') shared phrases"
      done
      
      # Check for verbose patterns
      bullets=$(grep -c "^- " "$filepath" 2>/dev/null)
      bullets=${bullets:-0}
      [[ $bullets -gt 15 ]] && echo "  📝 $bullets bullet points — consider compressing"
      
      headers=$(grep -c "^##" "$filepath" 2>/dev/null)
      headers=${headers:-0}
      [[ $headers -gt 8 ]] && echo "  📝 $headers sections — consider consolidating"
    fi
  done
fi
