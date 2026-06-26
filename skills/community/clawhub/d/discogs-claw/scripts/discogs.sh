#!/bin/bash

# Openclaw Skill: Discogs Price Search
# Based on Anthropic agent skill standard

# Check if DISCOGS_TOKEN is set
if [ -z "$DISCOGS_TOKEN" ]; then
    echo '{"error": "DISCOGS_TOKEN environment variable is not set. Please set it to use this skill."}'
    exit 1
fi

# Read input from stdin
read -r INPUT_JSON

# Extract query from JSON input
QUERY=$(echo "$INPUT_JSON" | jq -r '.query // empty')

if [ -z "$QUERY" ]; then
    echo '{"error": "Query parameter is missing in input JSON. Please provide a query string."}'
    exit 1
fi

# URL encode the query using jq
ENCODED_QUERY=$(echo "$QUERY" | jq -R -r @uri)

# Step 1: Search for the release
# We search specifically for Vinyl format releases
SEARCH_URL="https://api.discogs.com/database/search?q=${ENCODED_QUERY}&type=release&format=Vinyl"

# Perform search with User-Agent and Authorization headers
SEARCH_RESULT=$(curl -s -H "User-Agent: OpenclawSkill/1.0" -H "Authorization: Discogs token=${DISCOGS_TOKEN}" "$SEARCH_URL")

# Extract the first release ID and details
RELEASE_ID=$(echo "$SEARCH_RESULT" | jq -r '.results[0].id // empty')
RELEASE_TITLE=$(echo "$SEARCH_RESULT" | jq -r '.results[0].title // "Unknown Title"')
RELEASE_YEAR=$(echo "$SEARCH_RESULT" | jq -r '.results[0].year // "Unknown Year"')

if [ -z "$RELEASE_ID" ]; then
    echo "{\"error\": \"No vinyl release found for query: '$QUERY'. Please try a more specific search term.\"}"
    exit 0
fi

# Step 2: Get Price Suggestions
# This endpoint provides suggested prices based on condition
PRICE_URL="https://api.discogs.com/marketplace/price_suggestions/${RELEASE_ID}"
PRICE_RESULT=$(curl -s -H "User-Agent: OpenclawSkill/1.0" -H "Authorization: Discogs token=${DISCOGS_TOKEN}" "$PRICE_URL")

# Step 3: Get Release Statistics
# This endpoint provides number of items for sale and lowest price
STATS_URL="https://api.discogs.com/releases/${RELEASE_ID}/stats"
STATS_RESULT=$(curl -s -H "User-Agent: OpenclawSkill/1.0" -H "Authorization: Discogs token=${DISCOGS_TOKEN}" "$STATS_URL")

# Extract Stats
NUM_FOR_SALE=$(echo "$STATS_RESULT" | jq -r '.num_for_sale // 0')
LOWEST_PRICE=$(echo "$STATS_RESULT" | jq -r '.lowest_price.value // "N/A"')
LOWEST_CURRENCY=$(echo "$STATS_RESULT" | jq -r '.lowest_price.currency // "USD"')

# Ensure defaults if jq fails
NUM_FOR_SALE=${NUM_FOR_SALE:-0}
LOWEST_PRICE=${LOWEST_PRICE:-N/A}
LOWEST_CURRENCY=${LOWEST_CURRENCY:-USD}

# Extract Prices mapping conditions to Low, Median, High
# Low -> Good (G) or Good Plus (G+)
# Median -> Very Good Plus (VG+)
# High -> Mint (M) or Near Mint (NM or M-)

LOW=$(echo "$PRICE_RESULT" | jq -r '."Good (G)".value // ."Good Plus (G+)".value // "N/A"')
MEDIAN=$(echo "$PRICE_RESULT" | jq -r '."Very Good Plus (VG+)".value // ."Very Good (VG)".value // "N/A"')
HIGH=$(echo "$PRICE_RESULT" | jq -r '."Mint (M)".value // ."Near Mint (NM or M-)".value // "N/A"')
CURRENCY=$(echo "$PRICE_RESULT" | jq -r '."Very Good Plus (VG+)".currency // "USD"')

# Construct JSON Output
# Using jq -n to create JSON object safely
jq -n \
    --arg title "$RELEASE_TITLE" \
    --arg low "$LOW" \
    --arg median "$MEDIAN" \
    --arg high "$HIGH" \
    --arg currency "$CURRENCY" \
    --arg num_for_sale "$NUM_FOR_SALE" \
    --arg lowest_price "$LOWEST_PRICE" \
    --arg lowest_currency "$LOWEST_CURRENCY" \
    '{
        title: $title,
        prices: {
            low: ($low|tostring + " " + $currency),
            median: ($median|tostring + " " + $currency),
            high: ($high|tostring + " " + $currency)
        },
        marketplace: {
            num_for_sale: ($num_for_sale|tonumber),
            lowest_price: ($lowest_price|tostring + " " + $lowest_currency)
        }
    }'

