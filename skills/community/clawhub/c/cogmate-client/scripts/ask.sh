#!/bin/bash
# Ask a question to Cogmate
# Usage: ./ask.sh <cogmate_url> <token> "question"

COGMATE_URL="${1%/}"
TOKEN="$2"
QUESTION="$3"

if [ -z "$COGMATE_URL" ] || [ -z "$TOKEN" ] || [ -z "$QUESTION" ]; then
    echo "Usage: $0 <cogmate_url> <token> \"question\""
    echo "Example: $0 http://example.com:8000 tok_xxx \"What do you know about AI?\""
    exit 1
fi

curl -s -X POST "${COGMATE_URL}/api/ask?token=${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"question\": \"${QUESTION}\"}" | \
    python3 -c "import sys,json; r=json.load(sys.stdin); print(r.get('answer','No answer'))"
