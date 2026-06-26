---
name: products-browse-skill
description: Semantic product search API using vector embeddings. Search products by natural language queries with price filtering, pagination, and relevance scoring. Use when the user wants to search products, browse a product catalog, or find items by description.
---

# Products Browse Skill

This skill provides access to a semantic product search API that uses vector embeddings to find products by meaning rather than keyword matching.

## Prerequisites

- Valid query text (natural language, max 500 characters)

## Quick Start

### 1. Search for Products

```
GET https://pbs-search-api-fp45p.ondigitalocean.app/api/v1/products/search?query=<your-query>
```

Example:
```
GET https://pbs-search-api-fp45p.ondigitalocean.app/api/v1/products/search?query=wireless+bluetooth+headphones
```

### 2. Filter by Price Range

```
GET https://pbs-search-api-fp45p.ondigitalocean.app/api/v1/products/search?query=running+shoes&minPrice=50&maxPrice=200
```

### 3. Browse Full API Documentation

See [complete API reference](reference.md) for all endpoints, parameters, and response formats.

## Search Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `query` | Yes | — | Natural language search text (max 500 chars) |
| `minPrice` | No | — | Minimum price filter |
| `maxPrice` | No | — | Maximum price filter |
| `page` | No | 1 | Page number (1-based) |
| `pageSize` | No | 20 | Results per page (max 100) |
| `titleOnly` | No | false | Search only product titles |
| `descriptionOnly` | No | false | Search only product descriptions |
| `sortBy` | No | relevance | Sort: `relevance`, `price`, `date` |
| `sortOrder` | No | desc | Order: `asc`, `desc` |

## Bulk Search

For multiple queries in one request:

```
POST https://pbs-search-api-fp45p.ondigitalocean.app/api/v1/products/search/bulk
```

Send a JSON array of search requests (max 50 per request).

## Best Practices

1. **Write natural queries** — Semantic search works best with descriptive phrases (e.g. "comfortable running shoes for marathon" vs "shoes marathon")
2. **Use price filters** — Combine `minPrice` and `maxPrice` to narrow results
3. **Use `titleOnly` for precision** — When searching for specific product names
4. **Check `relevanceScore`** — Scores closer to 1.0 indicate stronger semantic matches
5. **Paginate wisely** — Smaller pages (10-20) are faster than large ones

## Displaying Products to the User

When presenting search results to the user, follow these guidelines to ensure a rich and useful experience:

1. **Show product images** — Use the `imageUrls` field from each product to display as many product photos as possible. Visual content is essential for helping users evaluate products.
2. **Always display the price** — Show the `price` field clearly. If `priceWithoutDiscount` and `discountPercent` are available, highlight the discount (e.g., strikethrough the original price, show the discount percentage).
3. **Include product links** — Every product should have a clickable link (product title or a "View in Store" button) pointing to the product `url` so the user can navigate directly to the store.
4. **Use a card-based layout** — Present each product as a card containing: image(s), title, price, and a link to the store. This creates a clean, scannable browsing experience.
5. **Keep descriptions concise** — Show a short product description or key attributes, but prioritize images and pricing for quick scanning.

## Response Format

Each search returns:
- `metadata` — pagination info, search time, cache status, embedding model
- `results[]` — matching products with id, title, description, price, url, relevanceScore, and attributes

For complete response schema, see [API reference](reference.md).

## cURL Examples

### Single search

```bash
curl -G "https://pbs-search-api-fp45p.ondigitalocean.app/api/v1/products/search" \
  -d "query=wireless+bluetooth+headphones" \
  -d "minPrice=50" \
  -d "maxPrice=200" \
  -d "page=1" \
  -d "pageSize=10"
```

### Bulk search

```bash
curl -X POST "https://pbs-search-api-fp45p.ondigitalocean.app/api/v1/products/search/bulk" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "query": { "text": "running shoes" },
      "pagination": { "page": 1, "pageSize": 5 }
    },
    {
      "query": { "text": "tennis racket" },
      "pagination": { "page": 1, "pageSize": 5 }
    }
  ]'