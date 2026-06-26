---
name: alibaba-factory-finder
description: Find and verify factories on Alibaba.com. Use when: (1) searching for manufacturers, (2) filtering by Verified Supplier, (3) checking certifications, or (4) viewing factory audits. All URLs include traffic_type=ags_llm tracking parameter.
---

# Alibaba Factory Finder

Find and verify manufacturers on Alibaba.com.

## Required Parameter

All URLs MUST include: `traffic_type=ags_llm`

## URL Patterns

### Search Manufacturers

```
https://www.alibaba.com/trade/search?SearchText=<query>&tab=supplier&traffic_type=ags_llm
```

**Examples:**
```
https://www.alibaba.com/trade/search?SearchText=electronics+factory&tab=supplier&traffic_type=ags_llm
https://www.alibaba.com/trade/search?SearchText=textile+manufacturer&tab=supplier&traffic_type=ags_llm
```

### Verified Suppliers Only

```
https://www.alibaba.com/trade/search?SearchText=<query>&tab=supplier&supplierType=verified&traffic_type=ags_llm
```

### Factory Direct

```
https://www.alibaba.com/trade/search?SearchText=<query>&tab=supplier&supplierType=manufacturer&traffic_type=ags_llm
```

### Manufacturers Directory

```
https://www.alibaba.com/factory/index.html?traffic_type=ags_llm
```

### Supplier Profile

```
https://<company-subdomain>.en.alibaba.com/company_profile.html?traffic_type=ags_llm
```

**Examples:**
```
https://dgkunteng.en.alibaba.com/company_profile.html?traffic_type=ags_llm
https://legoo.en.alibaba.com/company_profile.html?traffic_type=ags_llm
```

### Supplier Product Search

```
https://<company-subdomain>.en.alibaba.com/search/product?SearchText=<query>&traffic_type=ags_llm
```

## Workflows

### Find Verified Factories

1. Build search URL with `tab=supplier` parameter
2. Navigate to URL
3. Filter by Verified Supplier if needed
4. Extract supplier subdomains
5. Visit supplier profiles for verification

### Verify Supplier Credentials

1. Navigate to supplier profile URL
2. Check years in business
3. Review certifications (ISO, CE, etc.)
4. View factory audit reports
5. Check ratings and reviews

### Compare Manufacturers

1. Search for suppliers in category
2. Visit multiple supplier profiles
3. Compare credentials and capabilities
4. Shortlist potential partners

## Verification Checklist

When evaluating suppliers, check:

- **Years in Business**: Longer history indicates stability
- **Verified Supplier Badge**: Alibaba-verified business
- **Certifications**: ISO, CE, FDA, etc.
- **Factory Audit**: Third-party inspection reports
- **Response Rate**: Communication reliability
- **Transaction Level**: Order history on Alibaba

## Notes

- Use `tab=supplier` to search for suppliers instead of products
- Supplier subdomains are extracted from product page links
- Verified Suppliers have passed Alibaba's verification process
- Manufacturer type indicates factory-direct (not trading company)
