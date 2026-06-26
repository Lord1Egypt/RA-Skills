#!/bin/bash
# Camino AI Search API - Flexible Place Lookup
# Usage: ./places.sh '{"query": "Eiffel Tower"}' or ./places.sh '{"city": "Paris", "country": "France"}'
#
# /search is POST but reads its parameters from the URL query string
# (FastAPI Query()), not from a JSON body. We translate the JSON input
# to URL-encoded query params.

set -e

# Check dependencies
for cmd in jq curl; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "Error: '$cmd' is required but not installed" >&2
        exit 1
    fi
done

# Check if input is provided
if [ -z "$1" ]; then
    echo "Error: JSON input required" >&2
    echo "Usage: ./places.sh '{\"query\": \"Eiffel Tower\"}'" >&2
    echo "   or: ./places.sh '{\"street\": \"123 Main St\", \"city\": \"New York\"}'" >&2
    exit 1
fi

INPUT="$1"

# Validate JSON
if ! echo "$INPUT" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON input" >&2
    exit 1
fi

# Check for API key
if [ -z "$CAMINO_API_KEY" ]; then
    echo "Error: CAMINO_API_KEY environment variable not set" >&2
    echo "Get your API key at https://app.getcamino.ai" >&2
    exit 1
fi

# Check for at least one search parameter
QUERY=$(echo "$INPUT" | jq -r '.query // empty')
AMENITY=$(echo "$INPUT" | jq -r '.amenity // empty')
STREET=$(echo "$INPUT" | jq -r '.street // empty')
CITY=$(echo "$INPUT" | jq -r '.city // empty')
COUNTY=$(echo "$INPUT" | jq -r '.county // empty')
STATE=$(echo "$INPUT" | jq -r '.state // empty')
COUNTRY=$(echo "$INPUT" | jq -r '.country // empty')
POSTALCODE=$(echo "$INPUT" | jq -r '.postalcode // empty')

if [ -z "$QUERY" ] && [ -z "$AMENITY" ] && [ -z "$STREET" ] && [ -z "$CITY" ] && \
   [ -z "$COUNTY" ] && [ -z "$STATE" ] && [ -z "$COUNTRY" ] && [ -z "$POSTALCODE" ]; then
    echo "Error: At least one of 'query' or address components is required" >&2
    exit 1
fi

# Build URL-encoded query string from JSON input
append_string_param() {
    local name="$1"
    local value="$2"
    if [ -n "$value" ]; then
        local encoded=$(jq -rn --arg v "$value" '$v|@uri')
        params="${params}&${name}=${encoded}"
    fi
}

append_raw_param() {
    local name="$1"
    local value="$2"
    if [ -n "$value" ]; then
        params="${params}&${name}=${value}"
    fi
}

params=""
append_string_param query "$QUERY"
append_string_param amenity "$AMENITY"
append_string_param street "$STREET"
append_string_param city "$CITY"
append_string_param county "$COUNTY"
append_string_param state "$STATE"
append_string_param country "$COUNTRY"
append_string_param postalcode "$POSTALCODE"

append_raw_param limit "$(echo "$INPUT" | jq -r '.limit // empty')"
append_raw_param include_photos "$(echo "$INPUT" | jq -r '.include_photos // empty')"
append_raw_param photo_radius "$(echo "$INPUT" | jq -r '.photo_radius // empty')"
append_raw_param mode "$(echo "$INPUT" | jq -r '.mode // empty')"

QUERY_STRING="${params:1}"

# Make API request — POST with URL query params (no body)
curl -s -X POST \
    -H "X-API-Key: $CAMINO_API_KEY" \
    -H "X-Client: claude-code-skill" \
    "https://api.getcamino.ai/search?${QUERY_STRING}" | jq .
