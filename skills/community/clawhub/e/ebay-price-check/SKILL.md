# eBay Price Check Skill

Check eBay item prices, including sold listings for historical data.

## Usage

### Check current price of an item
```
/eBay price check iPhone 14 Pro Max 256GB
```

### Check sold prices (historical data)
```
/eBay sold prices MacBook Pro 14" M3
```

### Get price history summary
```
/eBay price history Samsung Galaxy S23
```

## Capabilities

- **Search eBay** for items by keyword
- **Get current listing prices** (active listings)
- **Get sold prices** (historical data from sold listings)
- **Price range analysis** (min/max/average)
- **Shipping cost information**
- **Item condition filtering** (new, used, refurbished)

## How it Works

1. Searches eBay using their public search API
2. Parses results to extract prices, titles, shipping costs
3. For sold prices, filters by "Sold Items" category
4. Returns formatted summary with price statistics

## Notes

- Requires internet connection
- eBay may limit search frequency
- Sold data may not be available for all items
- Prices shown are in USD unless specified