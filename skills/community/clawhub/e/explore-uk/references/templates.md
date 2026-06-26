# Parameter Collection & Output Templates

## Parameter Collection SOP

### Step 1: Extract from user query

Scan user message for:
- Origin city/name
- Destination city/name
- Date or date range
- Budget/price preference
- Cabin class preference

### Step 2: Missing parameters

If origin or destination is missing, ask (max 2 questions):
1. "Where are you departing from?"
2. "Where would you like to go?"

### Step 3: Map to CLI

| User says | Map to |
|-----------|--------|
| "cheapest" / "最便宜" | --sort-type 3 |
| "fastest" / "最快" | --sort-type 4 |
| "direct" / "直飞" | --journey-type 1 |
| "business class" / "商务舱" | --seat-class-name business |
| "under 1000" / "1000以内" | --max-price 1000 |

## Output Template

```markdown
## Flight Search Results

| # | Airline | Route | Departure | Duration | Price | |
|---|---------|-------|-----------|----------|-------|-|
| 1 | {airlineName} | {origin} -> {destination} | {depTime} | {duration} | Y{price} | [Book]({{detailUrl}}) |

Powered by flyai - Real-time pricing, click to book
```

## Notes

- Always include [Book](detailUrl) links
- Format prices in CNY (Y)
- Include at least 3 results when available
