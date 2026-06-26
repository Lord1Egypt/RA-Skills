#!/bin/bash
# USDA FoodData Central API - Get Food Details
# Usage: fdc_food.sh <fdcId> [format] [nutrients]

# Configuration
API_BASE="https://api.nal.usda.gov/fdc/v1"

# Check for API key
if [ -z "$FDC_API_KEY" ]; then
    echo "❌ Error: FDC_API_KEY environment variable is not set."
    echo ""
    echo "To get an API key:"
    echo "1. Visit: https://fdc.nal.usda.gov/api-key-signup"
    echo "2. Fill out: First Name, Last Name, Email"
    echo "3. Check your email for the 40-character API key"
    echo "4. Add to ~/.openclaw/openclaw.json:"
    echo '   {"env": {"FDC_API_KEY": "your-api-key-here"}}'
    exit 1
fi

# Parse arguments
FDC_ID="$1"
FORMAT="${2:-full}"
NUTRIENTS="$3"

if [ -z "$FDC_ID" ]; then
    echo "Usage: fdc_food.sh <fdcId> [format] [nutrients]"
    echo "  fdcId: The FDC ID of the food (from search results)"
    echo "  format: 'abridged' or 'full' (default: full)"
    echo "  nutrients: Comma-separated nutrient numbers (optional, max 25)"
    echo ""
    echo "Example: fdc_food.sh 168917"
    echo "Example: fdc_food.sh 168917 full '203,204,205'"
    exit 1
fi

# Build URL with query parameters
URL="${API_BASE}/food/${FDC_ID}?format=${FORMAT}"

# Add nutrients filter if provided
if [ -n "$NUTRIENTS" ]; then
    # Convert comma-separated to multiple query params
    URL="${URL}&nutrients=${NUTRIENTS}"
fi

# Make API request
RESPONSE=$(curl -s -w "\n%{http_code}" \
    -H "X-Api-Key: $FDC_API_KEY" \
    "$URL")

# Separate body and status code
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Check for errors
case "$HTTP_CODE" in
    200)
        # Success - process results
        ;;
    403)
        ERROR_CODE=$(echo "$BODY" | jq -r '.error.code // "UNKNOWN"' 2>/dev/null)
        if [ "$ERROR_CODE" = "API_KEY_MISSING" ]; then
            echo "❌ Error: API key is missing. Please set FDC_API_KEY environment variable."
        elif [ "$ERROR_CODE" = "API_KEY_INVALID" ]; then
            echo "❌ Error: API key is invalid. Please verify your API key."
        else
            echo "❌ Error: Authentication failed (HTTP 403)"
        fi
        exit 1
        ;;
    429)
        echo "❌ Error: Rate limit exceeded. You have made too many requests."
        echo "Please wait 1 hour before trying again."
        exit 1
        ;;
    404)
        echo "❌ Error: Food with FDC ID '$FDC_ID' not found."
        echo "Please check the FDC ID and try again."
        exit 1
        ;;
    400)
        echo "❌ Error: Bad request (HTTP 400)"
        echo "$BODY" | jq -r '.error.message // .message // "Unknown error"' 2>/dev/null
        exit 1
        ;;
    *)
        echo "❌ Error: Unexpected HTTP status code: $HTTP_CODE"
        exit 1
        ;;
esac

# Parse and display results
DESCRIPTION=$(echo "$BODY" | jq -r '.description // "Unknown"')
DATA_TYPE=$(echo "$BODY" | jq -r '.dataType // "Unknown"')
FDC_ID_RESULT=$(echo "$BODY" | jq -r '.fdcId // "Unknown"')
PUBLICATION_DATE=$(echo "$BODY" | jq -r '.publicationDate // "N/A"')

echo "# $DESCRIPTION"
echo ""
echo "**FDC ID:** $FDC_ID_RESULT"
echo "**Data Type:** $DATA_TYPE"
echo "**Publication Date:** $PUBLICATION_DATE"

# Display type-specific identifiers
case "$DATA_TYPE" in
    "Branded")
        BRAND_OWNER=$(echo "$BODY" | jq -r '.brandOwner // "N/A"')
        GTIN_UPC=$(echo "$BODY" | jq -r '.gtinUpc // "N/A"')
        SERVING_SIZE=$(echo "$BODY" | jq -r '.servingSize // "N/A"')
        SERVING_UNIT=$(echo "$BODY" | jq -r '.servingSizeUnit // ""')
        echo "**Brand Owner:** $BRAND_OWNER"
        echo "**GTIN/UPC:** $GTIN_UPC"
        if [ "$SERVING_SIZE" != "N/A" ] && [ "$SERVING_SIZE" != "null" ]; then
            echo "**Serving Size:** $SERVING_SIZE $SERVING_UNIT"
        fi
        ;;
    "Foundation"|"SR Legacy")
        NDB_NUMBER=$(echo "$BODY" | jq -r '.ndbNumber // "N/A"')
        SCIENTIFIC_NAME=$(echo "$BODY" | jq -r '.scientificName // "N/A"')
        echo "**NDB Number:** $NDB_NUMBER"
        if [ "$SCIENTIFIC_NAME" != "N/A" ] && [ "$SCIENTIFIC_NAME" != "null" ]; then
            echo "**Scientific Name:** $SCIENTIFIC_NAME"
        fi
        ;;
    "Survey (FNDDS)")
        FOOD_CODE=$(echo "$BODY" | jq -r '.foodCode // "N/A"')
        echo "**Food Code:** $FOOD_CODE"
        ;;
esac

echo ""

# Display ingredients for branded foods
if [ "$DATA_TYPE" = "Branded" ]; then
    INGREDIENTS=$(echo "$BODY" | jq -r '.ingredients // ""')
    if [ -n "$INGREDIENTS" ] && [ "$INGREDIENTS" != "null" ]; then
        echo "## Ingredients"
        echo "$INGREDIENTS"
        echo ""
    fi
fi

# Display nutritional information
echo "## Nutritional Information"
echo ""

# Check if we have foodNutrients
NUTRIENT_COUNT=$(echo "$BODY" | jq '.foodNutrients | length')

if [ "$NUTRIENT_COUNT" -eq 0 ]; then
    echo "No nutritional data available for this food."
else
    echo "| Nutrient | Amount | Unit |"
    echo "|----------|--------|------|"
    
    # Try different nutrient formats based on data type
    echo "$BODY" | jq -r '.foodNutrients[] | 
        if .nutrient then
            [(.nutrient.name // "Unknown"), (.amount // 0), (.nutrient.unitName // "N/A")]
        elif .name then
            [(.name // "Unknown"), (.amount // 0), (.unitName // "N/A")]
        else
            empty
        end | @tsv' 2>/dev/null | while IFS=$'\t' read -r name amount unit; do
        echo "| $name | $amount | $unit |"
    done | head -50  # Limit output to prevent token overload
    
    if [ "$NUTRIENT_COUNT" -gt 50 ]; then
        echo ""
        echo "*Showing first 50 of $NUTRIENT_COUNT nutrients. Use nutrient filtering to see specific values.*"
    fi
fi

echo ""
echo "---"
echo "To search for more foods, use: ./skills/fdc-api/scripts/fdc_search.sh \"<query>\""
