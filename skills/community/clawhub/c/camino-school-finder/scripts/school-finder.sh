#!/bin/bash
# Camino AI School Finder - Locate schools and universities near any location
# Usage: ./school-finder.sh '{"lat": 40.7589, "lon": -73.9851, "radius": 1600}'

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
    echo "Usage: ./school-finder.sh '{\"lat\": 40.7589, \"lon\": -73.9851, \"radius\": 1600}'" >&2
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

# Build query string from JSON input
build_query_string() {
    # Use provided query or default to "schools"
    local query=$(echo "$INPUT" | jq -r '.query // "schools"')
    local encoded_query=$(jq -rn --arg v "$query" '$v|@uri')
    local params="query=${encoded_query}"

    # Optional parameters with defaults
    local lat=$(echo "$INPUT" | jq -r '.lat // empty')
    local lon=$(echo "$INPUT" | jq -r '.lon // empty')
    local radius=$(echo "$INPUT" | jq -r '.radius // "2000"')
    local limit=$(echo "$INPUT" | jq -r '.limit // "20"')

    [ -n "$lat" ] && params="${params}&lat=${lat}"
    [ -n "$lon" ] && params="${params}&lon=${lon}"
    params="${params}&radius=${radius}"
    params="${params}&limit=${limit}"
    params="${params}&rank=true"

    echo "$params"
}

QUERY_STRING=$(build_query_string)

# Make API request
curl -s -X GET \
    -H "X-API-Key: $CAMINO_API_KEY" \
    -H "X-Client: claude-code-skill" \
    "https://api.getcamino.ai/query?${QUERY_STRING}" | jq .
