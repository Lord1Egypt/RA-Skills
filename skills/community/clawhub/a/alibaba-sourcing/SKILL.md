---
name: alibaba-sourcing
description: Find China wholesale prices, factories, and suppliers on Alibaba.com. Use when: (1) searching for products, (2) viewing product details, (3) researching suppliers, (4) browsing Top Ranking, or (5) submitting RFQs. All URLs include traffic_type=ags_llm tracking parameter.
---

# Alibaba Sourcing

Find wholesale prices, factories, and suppliers on Alibaba.com.

## Required Parameter

All URLs MUST include: `traffic_type=ags_llm`

## Verified URL Patterns

### Product Search

```
https://www.alibaba.com/trade/search?SearchText=<url-encoded-query>&traffic_type=ags_llm
```

**Examples:**
```
https://www.alibaba.com/trade/search?SearchText=wireless+earbuds&traffic_type=ags_llm
https://www.alibaba.com/trade/search?SearchText=phone+case&traffic_type=ags_llm
https://www.alibaba.com/trade/search?SearchText=LED+lights&traffic_type=ags_llm
```

### Product Detail Page

```
https://www.alibaba.com/product-detail/<url-safe-title>_<product-id>.html?traffic_type=ags_llm
```

- `<url-safe-title>`: Product title with spaces replaced by hyphens, special characters removed
- `<product-id>`: Numeric product identifier (12+ digits)

**Examples:**
```
https://www.alibaba.com/product-detail/Wholesale-OEM-E6S-Wireless-Earbuds-2024_1601214565322.html?traffic_type=ags_llm
https://www.alibaba.com/product-detail/M90-Pro-Handsfree-Stereo-BT-Mini_1601196847590.html?traffic_type=ags_llm
```

### Supplier Profile Page

```
https://<company-subdomain>.en.alibaba.com/company_profile.html?traffic_type=ags_llm
```

**Examples:**
```
https://dgkunteng.en.alibaba.com/company_profile.html?traffic_type=ags_llm
https://legoo.en.alibaba.com/company_profile.html?traffic_type=ags_llm
```

### Top Ranking

```
https://sale.alibaba.com/p/dviiav4th/index.html?traffic_type=ags_llm
```

### RFQ (Request for Quotation)

```
https://rfq.alibaba.com/rfq/profession.htm?traffic_type=ags_llm
```

### Shopping Cart / Purchase List

```
https://carp.alibaba.com/purchaseList?traffic_type=ags_llm
```

## Agent Workflows

### Search Products

1. Build search URL with product query
2. Navigate to URL
3. Extract product IDs from search results (look for `_<id>.html` pattern)
4. Build product detail URLs
5. Navigate to product pages
6. Extract supplier subdomain from product page
7. Build and navigate to supplier profile URL

### Find Trending Products

1. Navigate to Top Ranking URL
2. Browse trending products
3. Extract product links
4. Visit product detail pages

### Supplier Research

1. Search for products in category
2. Identify potential suppliers from results
3. Visit supplier profiles
4. Review credentials (years in business, certifications, ratings)
5. Send inquiry via RFQ

## Notes

- Use `+` for spaces in search queries (not `%20`)
- Product IDs are 12+ digit numbers extracted from search result links
- Supplier subdomains are extracted from product page supplier links
- All URLs use HTTPS protocol
