---
name: fdc-api
description: Interact with the USDA FoodData Central (FDC) API to search for foods and retrieve detailed nutritional information. Use when the user asks to look up food nutrition data, search for foods by name, get nutritional details for specific foods, or query the USDA food database. Requires FDC_API_KEY environment variable to be set.
metadata: {"openclaw": {"requires": {"bins": ["curl", "jq"], "env": ["FDC_API_KEY"]}, "primaryEnv": "FDC_API_KEY"}}
---

# USDA FoodData Central API Skill

This skill provides access to the USDA FoodData Central API for searching foods and retrieving detailed nutritional information.

## Important Limitations

**Language:** All food descriptions and search queries must be in **English**. The database does not support searching in other languages.

**Geographic Scope:** This is a **US-focused database**. The "Branded" data type contains primarily US commercial food products. While "Foundation" and "SR Legacy" include generic foods (like "apples, raw" or "chicken, grilled"), brand-specific items will be American brands. European or other international brands will generally not be found.

## Prerequisites

The skill requires a valid FDC API key to function. The key should be available via the `FDC_API_KEY` environment variable.

### Getting an API Key

If `FDC_API_KEY` is not set, guide the user through this onboarding process:

1. **Navigate to:** https://fdc.nal.usda.gov/api-key-signup
2. **Fill out the form with these required fields:**
   - First Name
   - Last Name
   - Email
3. **Submit the form** and check your email for the 40-character API key
4. **Add the key to OpenClaw configuration:**
   - Edit `~/.openclaw/openclaw.json`
   - Add the API key to the environment variables section:
     ```json
     {
       "env": {
         "FDC_API_KEY": "your-40-character-api-key-here"
       }
     }
     ```
   - Save the file and restart OpenClaw or reload the session

## API Usage

All API requests are made to `https://api.nal.usda.gov/fdc/v1` with authentication via the `X-Api-Key` header.

### Rate Limits

- **Standard Limit:** 1,000 requests per hour per IP address
- **DEMO_KEY Limit:** 30 requests per hour (not recommended)
- Rate limit headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`) are included in all responses
- Exceeding limits returns HTTP 429 (blocked for 1 hour)

## Commands

### Search Foods

Search for foods by keyword using `/foods/search` endpoint.

**Usage:**
```bash
./skills/fdc-api/scripts/fdc_search.sh "search query" [pageSize] [dataType]
```

**Parameters:**
- `search query` (required): Keywords to search for (e.g., "cheddar cheese")
- `pageSize` (optional): Number of results to return (1-200, default: 10)
- `dataType` (optional): Filter by data type - "Branded", "Foundation", "Survey (FNDDS)", "SR Legacy"

**Example:**
```bash
./skills/fdc-api/scripts/fdc_search.sh "apple" 5
./skills/fdc-api/scripts/fdc_search.sh "milk" 10 "Foundation"
```

**Response Format:**
Returns a formatted table with:
- FDC ID (use this to get full details)
- Description
- Data Type
- Brand Owner (if applicable)

### Get Food Details

Retrieve detailed nutritional information for a specific food by FDC ID.

**Usage:**
```bash
./skills/fdc-api/scripts/fdc_food.sh <fdcId> [format] [nutrients]
```

**Parameters:**
- `fdcId` (required): The FDC ID of the food (from search results)
- `format` (optional): "abridged" or "full" (default: "full")
- `nutrients` (optional): Comma-separated list of up to 25 nutrient numbers to filter (e.g., "203,204,205")

**Example:**
```bash
./skills/fdc-api/scripts/fdc_food.sh 168917
./skills/fdc-api/scripts/fdc_food.sh 168917 full "203,204,205"
```

**Response Format:**
Returns formatted output with:
- Food description and basic info
- Data type and identifiers
- Nutritional information (formatted as a table)
- Ingredients (for branded foods)
- Serving size information (when available)

## Error Handling

Common error codes and their meanings:
- **403 API_KEY_MISSING**: No API key provided → Trigger onboarding flow
- **403 API_KEY_INVALID**: Invalid API key → Ask user to verify key
- **429 OVER_RATE_LIMIT**: Rate limit exceeded → Wait 1 hour before retrying
- **404 NOT_FOUND**: Food ID not found → Check FDC ID is correct

## Workflow Examples

### Example 1: Find nutritional info for a food

1. Search for the food: `./skills/fdc-api/scripts/fdc_search.sh "banana" 5`
2. Note the FDC ID from results (e.g., 173944)
3. Get full details: `./skills/fdc-api/scripts/fdc_food.sh 173944`

### Example 2: Compare multiple foods

1. Search for first food and get details
2. Search for second food and get details
3. Compare nutritional information side-by-side

## Nutrient Number Reference

Common nutrient numbers for filtering:
- 203: Protein
- 204: Total lipid (fat)
- 205: Carbohydrate, by difference
- 208: Energy (kcal)
- 269: Sugars, total including NLEA
- 291: Fiber, total dietary
- 301: Calcium
- 303: Iron
- 304: Magnesium
- 305: Phosphorus
- 306: Potassium
- 307: Sodium
- 401: Vitamin C

To filter by specific nutrients, pass them as comma-separated values:
```bash
./skills/fdc-api/scripts/fdc_food.sh 168917 full "208,203,204,205"
```

## Notes

- The API returns deeply nested JSON; this skill processes it into readable markdown tables
- For branded foods, brand owner and GTIN/UPC codes are included
- Foundation and SR Legacy foods include NDB numbers
- Survey foods include food codes and portion data
