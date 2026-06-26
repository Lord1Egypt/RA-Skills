# Example: Etsy NBA Merchandise Research

Complete workflow for researching NBA merchandise on Etsy.

## Goal

Research NBA merchandise on Etsy to understand:
- Product variety and pricing
- Popular sellers and ratings
- Price ranges by category
- Customer satisfaction levels

## Command

```
/research-brightdata \
  query="site:etsy.com nba merchandise jerseys shirts" \
  mode=standard \
  max_results=20 \
  extract_schema="Extract: product name, price as number, currency, rating (0-5), number of reviews, seller name, product category, availability status" \
  output_format=report
```

## Expected Workflow

### Phase 1: Discovery

Search engine finds Etsy pages:
```
Query: site:etsy.com nba merchandise jerseys shirts
Engine: google
Results: ~20 Etsy product and category pages
```

### Phase 2: Collection

Batch scrape up to 10 URLs concurrently:
```
URLs collected: 20
Batch 1: 10 URLs scraped in parallel
Batch 2: 10 URLs scraped in parallel
Time: ~30 seconds total
```

### Phase 3: Extraction

Extract structured data from each page:
```json
{
  "product_name": "NBA Vintage Basketball Jersey",
  "price": 45.99,
  "currency": "USD",
  "rating": 4.7,
  "review_count": 234,
  "seller": "RetroSports",
  "category": "Jerseys",
  "availability": "in_stock"
}
```

### Phase 4: Analysis

Analyze extracted data:
- Price range: $15 - $120
- Average rating: 4.6/5
- Top categories: Jerseys (40%), T-shirts (30%), Accessories (20%), Other (10%)
- Top 5 sellers by rating and volume

### Phase 5: Report

Generate comprehensive report with findings and recommendations.

## Expected Output

```markdown
# Research Report: NBA Merchandise on Etsy

## Executive Summary

Analyzed 20 NBA merchandise listings on Etsy. Prices range from $15 to $120 with an average of $52. Customer satisfaction is high (4.6/5 average rating). Jerseys are the most popular category (40% of listings), followed by t-shirts (30%).

## Key Findings

### Pricing Analysis
- **Price Range**: $15 - $120
- **Average Price**: $52
- **Median Price**: $48
- **Best Value**: "Custom NBA T-Shirt" at $22 with 4.8/5 rating

### Top Categories
1. **Jerseys** (40% of listings)
   - Price range: $45 - $120
   - Average rating: 4.5/5

2. **T-Shirts** (30% of listings)
   - Price range: $15 - $45
   - Average rating: 4.7/5

3. **Accessories** (20% of listings)
   - Price range: $18 - $65
   - Average rating: 4.6/5

### Top Sellers by Rating
1. RetroSports - 4.8/5 (234 reviews)
2. HoopsFanatic - 4.7/5 (189 reviews)
3. CourtSideGear - 4.7/5 (156 reviews)
4. BasketballBasics - 4.6/5 (98 reviews)
5. TeamSpiritShop - 4.5/5 (87 reviews)

### Recommendations
- **Best Value**: Custom t-shirts under $25 with high ratings
- **Premium Market**: Jerseys priced $80+ have fewer sales but higher margins
- **Opportunity**: Limited accessory selection, room for growth

## Methodology
- Sources: Google search with site:etsy.com filter
- URLs Analyzed: 20
- Data Points Extracted: 140 (7 per listing)
- Confidence: High

## Sources
[Complete list of 20 Etsy URLs analyzed]
```

## Variations

### Quick Overview

```
/research-brightdata \
  query="site:etsy.com nba" \
  mode=quick \
  max_results=5
```

### Deep Analysis with Browser Automation

```
/research-brightdata \
  query="site:etsy.com nba jerseys" \
  mode=deep \
  max_results=30 \
  output_format=report
```

### Price Comparison Only

```
/research-brightdata \
  query="site:etsy.com nba jersey price" \
  extract_schema="Extract: product name, price, seller name" \
  output_format=json
```

## Tips for This Use Case

1. **Use Site Filter**: `site:etsy.com` ensures only Etsy results
2. **Specific Categories**: Add specific terms (jerseys, shirts, hats) for focused results
3. **Standard Mode**: Best balance of speed and depth for e-commerce
4. **Custom Extraction**: Specify exactly which fields to extract

## Common Issues

**Issue**: Some Etsy pages require JavaScript
**Solution**: Use `mode=deep` for browser automation

**Issue**: Duplicate listings from same seller
**Solution**: Report should include deduplication

**Issue**: Variations (sizes, colors) listed separately
**Solution**: Group by base product in analysis

**Issue**: Token limit exceeded when batch scraping
**Solution**: 
- Reduce batch size to 1-2 URLs at a time
- Use `scrape_as_markdown` for individual URLs
- Process URLs sequentially instead of in parallel
- If output is saved, use `Read` with `offset` and `limit` to read in chunks
