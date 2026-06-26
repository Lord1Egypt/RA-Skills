# Ecommerce Assistant

AI-powered e-commerce research tool for Amazon and Shopify.

## Features

- 🔍 **Amazon Product Search** - Find products with profit analysis
- 🏪 **Shopify Store Analysis** - Research competitor stores
- 📊 **Price Tracking** - Monitor price changes and get alerts
- 💰 **Profit Calculator** - Estimate margins and opportunity scores

## Installation

```bash
clawhub install ecommerce-assistant
```

## Quick Start

### Amazon Product Research
```bash
# Search products with filters
python3 scripts/amazon_search.py "wireless headphones" --min-price 20 --max-price 100 --min-rating 4.0

# Output includes:
# - Product details (ASIN, title, price, rating)
# - Estimated profit margins
# - Opportunity scores (demand + quality + margin)
```

### Shopify Competitor Analysis
```bash
# Analyze any Shopify store
python3 scripts/shopify_analyzer.py https://store-name.myshopify.com

# Get insights:
# - Total products and inventory
# - Price range and averages
# - Category distribution
# - Sample products
```

### Price Monitoring
```bash
# Add product to watchlist
python3 scripts/price_tracker.py --add B08HMWZBXC --target-price 50 --name "Product Name"

# Check all tracked products
python3 scripts/price_tracker.py --check

# Generate weekly report
python3 scripts/price_tracker.py --report weekly
```

## Use Cases

1. **Dropshipping Research** - Find profitable products with high margins
2. **Competitor Intelligence** - Analyze successful Shopify stores
3. **Price Arbitrage** - Track price drops and buying opportunities
4. **Market Analysis** - Understand category trends and pricing strategies

## Example Output

```
🔍 Amazon Search Results: 'yoga mat'
====================================================================================================
ASIN            Title                                    Price      Rating   Margin%    Score 
----------------------------------------------------------------------------------------------------
B08HMWZBXE      Premium Yoga Mat - Extra Thick...        $89.99     4.8      60.0%      5.3   
B08HMWZBXD      Eco-Friendly Yoga Mat...                 $74.99     4.6      60.0%      5.1   
====================================================================================================
Found 5 products | Opportunity Score = (Demand + Quality + Margin) / 3
```

## Data Sources

- Amazon Product Data (via public APIs)
- Shopify Storefront API (public endpoints)
- Price history tracking (local storage)

## Roadmap

- [ ] eBay integration
- [ ] Walmart marketplace support
- [ ] Real-time price alerts via email/webhook
- [ ] CSV bulk import/export
- [ ] Advanced filtering and sorting

## License

MIT

## Support

For issues and feature requests, please use the ClawHub issue tracker.
