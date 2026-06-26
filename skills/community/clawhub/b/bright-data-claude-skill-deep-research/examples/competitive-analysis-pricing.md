# Example: Competitive Price Comparison

Compare product prices across multiple retailers.

## Goal

Compare iPhone 15 Pro Max prices across major retailers to find the best deal.

## Command

```
/research-brightdata \
  query="iphone 15 pro max 256GB price amazon bestbuy walmart target" \
  mode=standard \
  max_results=15 \
  extract_schema="Extract: retailer name, product name including model and storage, price as number (USD), currency, availability (in stock/out of stock), shipping cost, delivery estimate, any promotions or discounts" \
  output_format=json
```

## Expected Workflow

### Phase 1: Discovery

Search for product pages across retailers:
```
Query: iphone 15 pro max 256GB price
Target retailers: Amazon, Best Buy, Walmart, Target
Expected results: 3-4 pages per retailer
```

### Phase 2: Collection

Batch scrape retailer product pages:
```
URLs collected: 12-15
Batch processing: 10 URLs at a time
Time: ~20 seconds
```

### Phase 3: Extraction

Extract pricing and availability data:
```json
{
  "retailer": "Walmart",
  "product": "Apple iPhone 15 Pro Max 256GB",
  "price": 999.00,
  "currency": "USD",
  "availability": "in_stock",
  "shipping": 0,
  "delivery": "2-3 business days",
  "promotions": "Free shipping, no tax in some states"
}
```

### Phase 4: Analysis

Compare prices and find best deal:
- Calculate total price (including shipping and tax)
- Check availability
- Factor in delivery time
- Identify promotions

### Phase 5: Report

Generate comparison with recommendation.

## Expected Output

```json
{
  "query": "iphone 15 pro max 256GB price comparison",
  "timestamp": "2024-01-22T10:30:00Z",
  "summary": {
    "total_retailers": 4,
    "lowest_price": 999.00,
    "highest_price": 1199.00,
    "average_price": 1089.50,
    "savings_range": "$0 - $200"
  },
  "comparison": [
    {
      "rank": 1,
      "retailer": "Walmart",
      "product": "iPhone 15 Pro Max 256GB",
      "price": 999.00,
      "shipping": 0,
      "total": 999.00,
      "availability": "in_stock",
      "delivery": "2-3 business days",
      "promotions": "Free shipping",
      "notes": "Best price, free shipping"
    },
    {
      "rank": 2,
      "retailer": "Amazon",
      "price": 1049.00,
      "shipping": 0,
      "total": 1049.00,
      "availability": "in_stock",
      "delivery": "Next-day delivery for Prime members",
      "promotions": "None",
      "notes": "Faster delivery available"
    },
    {
      "rank": 3,
      "retailer": "Best Buy",
      "price": 1099.00,
      "shipping": 0,
      "total": 1099.00,
      "availability": "in_stock",
      "delivery": "Same-day pickup available",
      "promotions": "Student discount available",
      "notes": "Good for immediate pickup"
    },
    {
      "rank": 4,
      "retailer": "Target",
      "price": 1199.00,
      "shipping": 0,
      "total": 1199.00,
      "availability": "in_stock",
      "delivery": "2-4 business days",
      "promotions": "RedCard discount 5%",
      "notes": "RedCard brings price to $1139.05"
    }
  ],
  "recommendation": {
    "best_price": "Walmart at $999.00 (save $200 vs MSRP)",
    "fastest_delivery": "Amazon with next-day for Prime members",
    "best_pickup": "Best Buy with same-day pickup",
    "overall_best": "Walmart - best price with free shipping"
  },
  "sources": [
    "https://www.walmart.com/ip/...",
    "https://www.amazon.com/dp/...",
    "https://www.bestbuy.com/site/...",
    "https://www.target.com/p/..."
  ]
}
```

## Variations

### Quick Price Check

```
/research-brightdata \
  query="iphone 15 price" \
  mode=quick \
  max_results=5 \
  output_format=markdown
```

### Multiple Product Comparison

```
/research-brightdata \
  query="Galaxy S24 Ultra vs iPhone 15 Pro Max vs Pixel 8 Pro price comparison" \
  mode=standard \
  extract_schema="Extract: product name, price, screen size, storage, key features" \
  max_results=10
```

### With Trade-in Values

```
/research-brightdata \
  query="iphone 15 pro max trade in value amazon bestbuy" \
  extract_schema="Extract: retailer name, new price, trade-in offer for iPhone 14 Pro Max, final price after trade-in" \
  mode=standard
```

## Tips for This Use Case

1. **Be Specific**: Include exact model and storage capacity
2. **Check Availability**: Stock levels vary by retailer
3. **Consider Total Cost**: Include shipping, tax, and fees
4. **Factor in Timing**: Delivery speed may matter more than small price differences
5. **Look for Promotions**: Student discounts, credit card offers, etc.

## Analysis Considerations

### Price Matching
- Some retailers price match (Best Buy, Target)
- Bring proof of lower price
- Check price match policies before purchasing

### Additional Costs
- Sales tax (varies by location)
- Shipping (usually free for expensive items)
- Accessories (cases, chargers not included)

### Timing
- New product releases may lower prices
- Holiday sales (Black Friday, Cyber Monday)
- Back-to-school promotions

### Trade-in Programs
- Apple Trade In
- Carrier trade-in deals
- Retailer trade-in promotions
