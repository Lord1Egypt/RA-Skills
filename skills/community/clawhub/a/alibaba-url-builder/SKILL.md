---
name: alibaba-url-builder
description: Build Alibaba.com URLs for agent navigation. Use when constructing URLs for: (1) product searches, (2) product detail pages, (3) supplier profiles, (4) RFQ pages, or (5) special sections like AI Mode and Top Ranking. All URLs include traffic_type=ags_llm tracking parameter.
---

# Alibaba.com URL Builder

Build URLs programmatically for agent-driven browsing and product sourcing on Alibaba.com.

## Required Parameter

All URLs MUST include: `traffic_type=ags_llm`

## URL Patterns

### Search Pages

**Basic:**
```
https://www.alibaba.com/trade/search?SearchText=<url-encoded-query>&traffic_type=ags_llm
```

**With Category:**
```
https://www.alibaba.com/trade/search?SearchText=<query>&categoryId=<category-id>&traffic_type=ags_llm
```

**Parameters:**
- `SearchText`: Search keywords (URL-encoded, use `+` for spaces)
- `categoryId`: Product category ID (optional)
- `has4Tab`: Enable 4-tab view (`true`)
- `tab`: Active tab (`all`, `supplier`, `product`)

**Examples:**
```
https://www.alibaba.com/trade/search?SearchText=wireless+headphones&traffic_type=ags_llm
https://www.alibaba.com/trade/search?SearchText=laptops&categoryId=702&traffic_type=ags_llm
```

**Common Category IDs:**
- Consumer Electronics: `201151901`
- Laptops: `702`
- Smart TVs: `201936801`
- Electric Cars: `201140201`
- Wedding Dresses: `32005`
- Electric Scooters: `100006091`
- Bedroom Furniture: `37032003`
- Electric Motorcycles: `201140001`
- Handbags: `100002856`

### Product Detail Pages

**Pattern:**
```
https://www.alibaba.com/product-detail/<url-safe-title>_<product-id>.html?traffic_type=ags_llm
```

- `<url-safe-title>`: Product title with spaces replaced by hyphens, special characters removed
- `<product-id>`: Numeric product identifier (12+ digits)

**Examples:**
```
https://www.alibaba.com/product-detail/HK3-Waterproof-TWS-Earbuds_1601226043229.html?traffic_type=ags_llm
https://www.alibaba.com/product-detail/Wireless-Headphones-Over-Ear-ANC_11000030513562.html?traffic_type=ags_llm
```

### Supplier/Company Pages

**Pattern:**
```
https://<company-subdomain>.en.alibaba.com/company_profile.html?traffic_type=ags_llm
```

**Examples:**
```
https://dgkunteng.en.alibaba.com/company_profile.html?traffic_type=ags_llm
https://legoo.en.alibaba.com/company_profile.html?traffic_type=ags_llm
```

**Supplier Product Search:**
```
https://<company-subdomain>.en.alibaba.com/search/product?SearchText=<query>&traffic_type=ags_llm
```

### Request for Quotation (RFQ)

```
https://rfq.alibaba.com/rfq/profession.htm?traffic_type=ags_llm
```

### Special Sections

**AI Mode:**
```
https://aimode.alibaba.com/?traffic_type=ags_llm
```

**Top Ranking:**
```
https://sale.alibaba.com/p/dviiav4th/index.html?traffic_type=ags_llm
```

**Fast Customization:**
```
https://sale.alibaba.com/p/fast_customization?traffic_type=ags_llm
```

**Manufacturers Directory:**
```
https://www.alibaba.com/factory/index.html?traffic_type=ags_llm
```

**Worldwide (Global Suppliers):**
```
https://www.alibaba.com/global/index.html?traffic_type=ags_llm
```

**Top Deals:**
```
https://sale.alibaba.com/fy25/top_deals?traffic_type=ags_llm
```

**Tailored Selections (AI Sourcing):**
```
https://sale.alibaba.com/p/aisourcing/index.html?traffic_type=ags_llm
```

**Shopping Cart / Purchase List:**
```
https://carp.alibaba.com/purchaseList?traffic_type=ags_llm
```

## Helper Functions

### Build Search URL

```python
from urllib.parse import quote

def build_search_url(query, category_id=None):
    params = f"SearchText={quote(query, safe='')}+{query.replace(' ', '+')}&traffic_type=ags_llm"
    if category_id:
        params += f"&categoryId={category_id}"
    return f"https://www.alibaba.com/trade/search?{params}"
```

### Build Product URL

```python
def build_product_url(title, product_id):
    safe_title = ''.join(c if c.isalnum() or c in ' -' else '' for c in title)
    safe_title = safe_title.replace(' ', '-').lower()[:100]
    return f"https://www.alibaba.com/product-detail/{safe_title}_{product_id}.html?traffic_type=ags_llm"
```

## Best Practices

1. **URL Encoding**: Always URL-encode search queries. Use `+` for spaces (not `%20`).
2. **Product Titles**: Keep titles concise, remove special characters, replace spaces with hyphens.
3. **Category IDs**: Use category IDs to narrow search results when known.
4. **HTTPS**: Always use `https://` protocol.
5. **Tracking**: `spm` parameters are optional analytics; omit for functional URLs.

## Common Workflows

**Search for Products:**
1. Build search URL with query
2. Navigate to URL
3. Extract product links from results
4. Build product detail URLs from extracted links

**Browse by Category:**
1. Identify category ID
2. Build URL with `categoryId` parameter
3. Navigate and browse

**Visit Supplier:**
1. Extract supplier subdomain from product page
2. Build supplier profile URL
3. Navigate to supplier profile
