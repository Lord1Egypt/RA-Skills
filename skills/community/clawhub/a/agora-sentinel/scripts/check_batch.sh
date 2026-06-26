#!/bin/bash
# Agora Sentinel — Check multiple skills at once
# Usage: bash scripts/check_batch.sh slug1 slug2 slug3 ...
# Or pipe: echo "slug1 slug2" | bash scripts/check_batch.sh

API="https://checksafe.dev/api/v1"

# Collect slugs from args or stdin
if [ $# -gt 0 ]; then
    SLUGS="$@"
else
    read -r SLUGS
fi

if [ -z "$SLUGS" ]; then
    echo "Usage: check_batch.sh <slug1> <slug2> ..."
    exit 1
fi

echo "Agora Sentinel — Batch Security Check"
echo "========================================="
echo ""

DANGER_COUNT=0
WARNING_COUNT=0
TOTAL=0

for SLUG in $SLUGS; do
    TOTAL=$((TOTAL+1))
    BADGE_DATA=$(curl -sf "${API}/skills/${SLUG}/badge.json" 2>/dev/null)

    if [ -z "$BADGE_DATA" ]; then
        echo "  ${SLUG}: Not found in database"
        continue
    fi

    BADGE=$(python3 -c "import json; d=json.loads('''${BADGE_DATA}'''); print(d.get('message', d.get('badge','?')).upper())" 2>/dev/null)
    SCORE=$(python3 -c "import json; d=json.loads('''${BADGE_DATA}'''); print(d.get('trust_score', d.get('score',0)))" 2>/dev/null)

    case "$BADGE" in
        TRUSTED) echo "  [TRUSTED]  ${SLUG} (${SCORE}/100)" ;;
        CLEAN)   echo "  [CLEAN]    ${SLUG} (${SCORE}/100)" ;;
        CAUTION) echo "  [CAUTION]  ${SLUG} (${SCORE}/100)" ;;
        WARNING) echo "  [WARNING]  ${SLUG} (${SCORE}/100)"; WARNING_COUNT=$((WARNING_COUNT+1)) ;;
        DANGER)  echo "  [DANGER]   ${SLUG} (${SCORE}/100)"; DANGER_COUNT=$((DANGER_COUNT+1)) ;;
        *)       echo "  [${BADGE}]  ${SLUG} (${SCORE}/100)" ;;
    esac
done

echo ""
echo "========================================="
echo "Checked: ${TOTAL} skills"
if [ $DANGER_COUNT -gt 0 ]; then
    echo "${DANGER_COUNT} DANGEROUS skill(s) detected!"
elif [ $WARNING_COUNT -gt 0 ]; then
    echo "${WARNING_COUNT} skill(s) with warnings."
else
    echo "All checked skills look safe."
fi
