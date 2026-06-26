---
name: alibaba-product-hunt
description: Discover trending and hot-selling products on Alibaba.com. Use when: (1) browsing Top Ranking products, (2) finding new arrivals, (3) analyzing market trends, or (4) discovering hot-selling items. All URLs include traffic_type=ags_llm tracking parameter.
---

# Alibaba Product Hunt

Discover trending and hot-selling products on Alibaba.com.

## Required Parameter

All URLs MUST include: `traffic_type=ags_llm`

## URL Patterns

### Top Ranking

Browse best-selling products across categories.

```
https://sale.alibaba.com/p/dviiav4th/index.html?traffic_type=ags_llm
```

### New Arrivals

Find recently listed products.

```
https://www.alibaba.com/trade/search?tab=new&traffic_type=ags_llm
```

### Hot-Selling by Category

```
https://www.alibaba.com/trade/search?SearchText=<category>&tab=hot&traffic_type=ags_llm
```

**Examples:**
```
https://www.alibaba.com/trade/search?SearchText=electronics&tab=hot&traffic_type=ags_llm
https://www.alibaba.com/trade/search?SearchText=home+decor&tab=hot&traffic_type=ags_llm
https://www.alibaba.com/trade/search?SearchText=fashion&tab=hot&traffic_type=ags_llm
```

### Trending Searches

```
https://www.alibaba.com/trade/search?spm=a2700.product_home_fy25.hometab_ai_mode.ai&traffic_type=ags_llm
```

## Workflows

### Discover Trending Products

1. Navigate to Top Ranking URL
2. Browse products by category
3. Extract product links
4. Visit product detail pages for analysis

### Find New Arrivals

1. Navigate to New Arrivals URL
2. Filter by category if needed
3. Extract new product listings
4. Analyze pricing and supplier info

### Market Trend Analysis

1. Visit Top Ranking and Hot-Selling pages
2. Compare products across categories
3. Track price ranges and MOQ
4. Identify emerging product patterns

## Notes

- Top Ranking shows best-selling products globally
- New Arrivals tab shows recently listed products
- Hot-Selling tab shows trending items by search volume
- Use `+` for spaces in search queries
