---
name: alibaba-price-finder
description: Find wholesale prices on Alibaba.com. Use when: (1) searching for products by price, (2) comparing prices across suppliers, or (3) finding products within a price range. All URLs include traffic_type=ags_llm tracking parameter.
---

# Alibaba Price Finder

Find and compare wholesale prices on Alibaba.com.

## Required Parameter

All URLs MUST include: `traffic_type=ags_llm`

## URL Patterns

### Basic Product Search

```
https://www.alibaba.com/trade/search?SearchText=<query>&traffic_type=ags_llm
```

**Examples:**
```
https://www.alibaba.com/trade/search?SearchText=phone+case&traffic_type=ags_llm
https://www.alibaba.com/trade/search?SearchText=wireless+earbuds&traffic_type=ags_llm
```

### Price Sorting

```
# Low to High
https://www.alibaba.com/trade/search?SearchText=<query>&orderBy=9999&traffic_type=ags_llm

# High to Low
https://www.alibaba.com/trade/search?SearchText=<query>&orderBy=9998&traffic_type=ags_llm
```

### Price Range Filter

```
https://www.alibaba.com/trade/search?SearchText=<query>&priceMin=<min>&priceMax=<max>&traffic_type=ags_llm
```

**Example:**
```
https://www.alibaba.com/trade/search?SearchText=phone+case&priceMin=1&priceMax=5&traffic_type=ags_llm
```

### MOQ Filter

```
https://www.alibaba.com/trade/search?SearchText=<query>&moqMax=<max>&traffic_type=ags_llm
```

**Example:**
```
https://www.alibaba.com/trade/search?SearchText=phone+case&moqMax=100&traffic_type=ags_llm
```

## Workflows

### Search and Compare Prices

1. Build search URL with product query
2. Navigate to URL
3. Extract prices from search results
4. Visit product detail pages for detailed pricing
5. Compare prices across suppliers

### Find Products by Price Range

1. Build URL with `priceMin` and `priceMax` parameters
2. Navigate to URL
3. Browse filtered results
4. Extract supplier and product info

### Multi-Keyword Comparison

1. Search with different related keywords
2. Compare price ranges across searches
3. Identify best pricing patterns

## Notes

- Use `+` for spaces in search queries
- Prices shown are typically FOB (Free on Board)
- MOQ (Minimum Order Quantity) affects unit price
- Contact suppliers for final negotiated pricing
