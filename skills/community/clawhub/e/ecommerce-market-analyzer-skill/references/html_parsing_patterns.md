# HTML Parsing Patterns for E-commerce Sites

## Product Extraction Strategies

### Strategy 1: JSON-LD Schema
Many e-commerce sites use structured data:

```python
import re
import json

# Extract JSON-LD schema
pattern = r'<script type="application/ld\+json">(.*?)</script>'
matches = re.findall(pattern, html_content, re.DOTALL)

for match in matches:
    try:
        data = json.loads(match)
        if data.get('@type') == 'Product':
            name = data.get('name')
            price = data.get('offers', {}).get('price')
            print(f"{name}: {price}€")
    except:
        continue
```

### Strategy 2: Data Attributes
```python
# Common data attribute patterns
title_pattern = r'data-product-title="([^"]+)"'
price_pattern = r'data-price="([^"]+)"'
sku_pattern = r'data-product-id="([^"]+)"'

titles = re.findall(title_pattern, content)
prices = re.findall(price_pattern, content)
skus = re.findall(sku_pattern, content)
```

### Strategy 3: Class-based Extraction
```python
# Product title classes
title_patterns = [
    r'class="product-title[^"]*">([^<]+)</.*?>',
    r'class="item-title[^"]*">([^<]+)</.*?>',
    r'class="product-name[^"]*">([^<]+)</.*?>',
]

# Price classes
price_patterns = [
    r'class="price[^"]*">([^<]+)</span>',
    r'class="product-price[^"]*">([^<]+)</.*?>',
    r'class="sale-price[^"]*">([^<]+)</.*?>',
]
```

## Platform-Specific Patterns

### REWE.de (Supermarket)
```python
# Product offers
title_pattern = r'data-offer-title="([^"]+)"'
price_pattern = r'<div class="cor-offer-price__tag-price">([^<]+)</div>'

titles = re.findall(title_pattern, content)
prices = re.findall(price_pattern, content)
```

### eBay.de (Marketplace)
```python
# eBay uses GraphQL JSON in HTML
product_pattern = r'"bc-item-detail-title[^>]*>([^<]+)</a>[^}]{0,500}?"scalar":([0-9.]+)'
matches = re.findall(product_pattern, content)

for title, price in matches:
    print(f"{title}: {price}€")
```

### Amazon.de
```python
# Amazon product patterns
title_pattern = r'aria-label="([^"]+\w+[^"]*)"[^>]*data-asin'
price_pattern = r'<span class="a-price-whole">([^<]+)</span>'

# Clean prices
prices = [p.replace(',', '.') for p in prices]
```

### Otto.de (Department Store)
```python
# Otto JSON-based
product_pattern = r'"name":"([^"]+)".*?"price":"([^"]+)"'
matches = re.findall(product_pattern, content)
```

### Zalando/AboutYou (Fashion)
```python
# Fashion sites often use product cards
card_pattern = r'data-product-name="([^"]+)".*?data-price="([^"]+)"'
matches = re.findall(card_pattern, content, re.DOTALL)
```

## Price Normalization

```python
def normalize_price(price_str):
    """Convert various price formats to float"""
    # Remove currency symbols and whitespace
    price_str = price_str.replace('€', '').replace('EUR', '').strip()

    # Handle German format (1.234,56)
    if ',' in price_str and '.' in price_str:
        price_str = price_str.replace('.', '').replace(',', '.')
    # Handle comma as decimal separator
    elif ',' in price_str:
        price_str = price_str.replace(',', '.')

    try:
        return float(price_str)
    except:
        return None
```

## Category Extraction

```python
# Breadcrumb navigation
breadcrumb_pattern = r'<nav[^>]*class="breadcrumb[^"]*"[^>]*>(.*?)</nav>'
category_pattern = r'<a[^>]*>([^<]+)</a>'

breadcrumb = re.search(breadcrumb_pattern, content, re.DOTALL)
if breadcrumb:
    categories = re.findall(category_pattern, breadcrumb.group(1))
```

## Discount/Sale Detection

```python
# Original vs sale price
original_price_pattern = r'<span class="[^"]*original-price[^"]*">([^<]+)</span>'
sale_price_pattern = r'<span class="[^"]*sale-price[^"]*">([^<]+)</span>'
discount_pattern = r'(-\d+%)'

# Badge detection
sale_badge_pattern = r'<span[^>]*class="[^"]*sale[^"]*badge[^"]*">([^<]+)</span>'
```

## Product Specifications

```python
# Table-based specs
spec_pattern = r'<tr>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*</tr>'
specs = re.findall(spec_pattern, content)

# List-based specs
list_spec_pattern = r'<li[^>]*><strong>([^<]+)</strong>:\s*([^<]+)</li>'
```

## Image URLs

```python
# Product images
image_patterns = [
    r'data-src="([^"]+\.jpg[^"]*)"',
    r'src="([^"]+/product/[^"]+\.jpg)"',
    r'<img[^>]*class="product-image[^"]*"[^>]*src="([^"]+)"',
]

for pattern in image_patterns:
    images = re.findall(pattern, content)
    if images:
        break
```

## Fallback Strategy

When specific patterns fail, use keyword matching:

```python
def extract_by_keywords(content, keywords):
    """Extract products mentioning specific keywords"""
    results = []
    for keyword in keywords:
        pattern = f'{keyword}[^<>{{}}]{{0,80}}'
        matches = re.findall(pattern, content, re.IGNORECASE)
        results.extend([m.strip() for m in matches if 10 < len(m) < 100])
    return list(set(results))[:10]

keywords = ['iPhone', 'Samsung', 'PlayStation', 'AirPods', 'Sofa',
            'Tisch', 'Schuhe', 'Jacke', 'Buch', 'Laptop']
```

## Best Practices

1. **Try multiple patterns**: Start with JSON-LD, fall back to data attributes, then class-based
2. **Validate extractions**: Check extracted data for reasonable length and format
3. **Handle encoding**: Use `encoding='utf-8'` when reading HTML files
4. **Remove duplicates**: Use sets or track seen products
5. **Limit results**: Cap at 10-20 products per site to avoid noise
6. **Clean text**: Strip whitespace, remove special characters from titles
