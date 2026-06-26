#!/bin/bash
# Search facts in Cogmate
# Usage: ./search.sh <cogmate_url> <token> "search term"

COGMATE_URL="${1%/}"
TOKEN="$2"
SEARCH="$3"

if [ -z "$COGMATE_URL" ] || [ -z "$TOKEN" ]; then
    echo "Usage: $0 <cogmate_url> <token> [search_term]"
    echo "Example: $0 http://example.com:8000 tok_xxx \"AI\""
    exit 1
fi

PARAMS="token=${TOKEN}"
[ -n "$SEARCH" ] && PARAMS="${PARAMS}&search=${SEARCH}"

curl -s "${COGMATE_URL}/api/visual/facts?${PARAMS}" | \
    python3 -c "
import sys, json
data = json.load(sys.stdin)
facts = data.get('facts', [])
if not facts:
    print('No facts found.')
else:
    for f in facts[:10]:
        print(f\"- [{f.get('layer','?')}] {f.get('summary','')}\")
"
