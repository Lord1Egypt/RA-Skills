---
name: amazon-paapi
description: "Search Amazon products and get product details using Amazon Product Advertising API (PA-API). Use for product searches, price lookups, and affiliate links."
metadata: {"requires":{"env":["AMAZON_ACCESS_KEY","AMAZON_SECRET_KEY","AMAZON_PARTNER_TAG"]},"emoji":"🛒","always":true}
user-invocable: true
---

# Amazon Product Advertising API Skill

This skill allows you to search for products on Amazon.de and retrieve product information using the Amazon PA-API.

## Tools

### amazon_search
Search for products on Amazon.

**Usage:**
```bash
amazon-search "search keywords" [--category CATEGORY] [--max-results N]
```

**Examples:**
- `amazon-search "wireless headphones"`
- `amazon-search "gaming laptop" --category Electronics --max-results 5`

### amazon_product
Get details for a specific product by ASIN.

**Usage:**
```bash
amazon-product ASIN
```

**Example:**
- `amazon-product B09V3KXJPB`

## Environment Variables Required
- AMAZON_ACCESS_KEY: Your Amazon PA-API Access Key
- AMAZON_SECRET_KEY: Your Amazon PA-API Secret Key  
- AMAZON_PARTNER_TAG: Your Amazon Associates Partner Tag
- AMAZON_HOST: Amazon API host (default: webservices.amazon.de)
- AMAZON_REGION: AWS region (default: eu-west-1)
