# Products Browse Skill — API Reference

Complete API documentation for the semantic product search endpoints.

## Table of Contents

- [Endpoints](#endpoints)
  - [`GET /api/v1/products/search`](#get-apiv1productssearch)
  - [`POST /api/v1/products/search/bulk`](#post-apiv1productssearchbulk)
- [Response Schemas](#response-schemas)
  - [`SearchResponse`](#searchresponse)
  - [`SearchMetadata`](#searchmetadata)
  - [`SearchResult`](#searchresult)
  - [`ProductAttributes`](#productattributes)
  - [`BatchSearchResponse`](#batchsearchresponse)
- [Request Schemas](#request-schemas)
  - [`SearchRequest`](#searchrequest)
  - [`QueryModel`](#querymodel)
  - [`SearchFilters`](#searchfilters)
  - [`PaginationModel`](#paginationmodel)
  - [`SortingModel`](#sortingmodel)
- [Error Responses](#error-responses)
- [Rate Limits](#rate-limits)

---

## Endpoints

### `GET /api/v1/products/search`

Search for products using semantic vector search. Queries are converted to embeddings and matched against product vectors in Qdrant.

**Base URL:** `https://pbs-search-api-fp45p.ondigitalocean.app/api/v1/products/search`

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | `string` | **Yes** | — | Natural language search text (max 500 characters) |
| `minPrice` | `number` | No | — | Minimum price filter |
| `maxPrice` | `number` | No | — | Maximum price filter |
| `page` | `integer` | No | `1` | Page number (1-based) |
| `pageSize` | `integer` | No | `20` | Results per page (max 100) |
| `titleOnly` | `boolean` | No | `false` | Search only product titles |
| `descriptionOnly` | `boolean` | No | `false` | Search only product descriptions |
| `sortBy` | `string` | No | `relevance` | Sort field: `relevance`, `price`, `date` |
| `sortOrder` | `string` | No | `desc` | Sort order: `asc`, `desc` |

#### Example Request

```
GET https://pbs-search-api-fp45p.ondigitalocean.app/api/v1/products/search?query=wireless+bluetooth+headphones&minPrice=50&maxPrice=200&page=1&pageSize=10
```

#### Success Response

**Status:** `200 OK`

**Body:** `SearchResponse`

```json
{
  "metadata": {
    "totalResults": 142,
    "page": 1,
    "pageSize": 10,
    "totalPages": 15,
    "searchTimeMs": 23,
    "cacheHit": false,
    "embeddingUsed": "qwen3-embedding-8b"
  },
  "results": [
    {
      "id": "abc123",
      "programName": "ExampleShop",
      "title": "Wireless Bluetooth Headphones",
      "description": "High-quality noise-canceling wireless headphones...",
      "price": 149.99,
      "currency": "PLN",
      "url": "https://example.com/product/123",
      "relevanceScore": 0.87,
      "imageUrls": [
        "https://example.com/img/headphones-1.jpg"
      ],
      "attributes": {
        "brand": "AudioTech",
        "category": "Electronics > Audio > Headphones"
      },
      "lastModified": "2026-04-20T10:30:00Z"
    }
  ]
}
```

#### Error Responses

| Status | Condition | Body |
|--------|-----------|------|
| `400 Bad Request` | `query` is empty or missing | `{"error": "Query text is required"}` |
| `400 Bad Request` | `query` exceeds 500 characters | `{"error": "Query text exceeds maximum length of 500 characters"}` |
| `500 Internal Server Error` | Unexpected server error | `{"error": "An error occurred while processing your search request"}` |

---

### `POST /api/v1/products/search/bulk`

Perform batch search for multiple queries in a single request. Returns combined and grouped results.

**Base URL:** `https://pbs-search-api-fp45p.ondigitalocean.app/api/v1/products/search/bulk`

**Content-Type:** `application/json`

#### Request Body

An array of `SearchRequest` objects (max 50 queries per request).

```json
[
  {
    "query": {
      "text": "running shoes",
      "title_only": false,
      "description_only": false
    },
    "filters": {
      "minPrice": 100,
      "maxPrice": 500
    },
    "pagination": {
      "page": 1,
      "pageSize": 10
    },
    "sorting": {
      "field": "relevance",
      "order": "desc"
    }
  },
  {
    "query": {
      "text": "basketball shoes",
      "title_only": true
    },
    "pagination": {
      "page": 1,
      "pageSize": 5
    }
  }
]
```

#### Success Response

**Status:** `200 OK`

**Body:** `BatchSearchResponse`

```json
{
  "results": [
    {
      "id": "def456",
      "programName": "SportShop",
      "title": "Running Shoes Pro",
      "description": "Professional running shoes...",
      "price": 349.00,
      "currency": "PLN",
      "url": "https://example.com/shoes/456",
      "relevanceScore": 0.92,
      "imageUrls": [],
      "attributes": {
        "brand": "RunFast",
        "category": "Sports > Footwear > Running"
      },
      "lastModified": "2026-04-18T08:00:00Z"
    }
  ],
  "groupedResults": {
    "running shoes": [
      { "id": "def456", "title": "Running Shoes Pro", "relevanceScore": 0.92 }
    ],
    "basketball shoes": [
      { "id": "ghi789", "title": "Basketball Shoes Elite", "relevanceScore": 0.85 }
    ]
  },
  "totalTimeMs": 145,
  "queriesProcessed": 2
}
```

#### Error Responses

| Status | Condition | Body |
|--------|-----------|------|
| `400 Bad Request` | Request body is empty or null | `{"error": "At least one search request is required"}` |
| `400 Bad Request` | More than 50 queries in the batch | `{"error": "Maximum of 50 queries allowed per batch request"}` |
| `400 Bad Request` | Query text is empty at index N | `{"error": "Query text is required for request at index N"}` |
| `400 Bad Request` | Query text exceeds 500 chars at index N | `{"error": "Query text at index N exceeds maximum length of 500 characters"}` |
| `500 Internal Server Error` | Unexpected server error | `{"error": "An error occurred while processing your bulk search request"}` |

---

## Response Schemas

### `SearchResponse`

Top-level response object for a single search query.

| Field | Type | Description |
|-------|------|-------------|
| `metadata` | `SearchMetadata` | Search metadata including pagination and performance info |
| `results` | `SearchResult[]` | List of matching products |

### `SearchMetadata`

Pagination and performance metadata.

| Field | Type | Description |
|-------|------|-------------|
| `totalResults` | `integer` | Total number of matching results across all pages |
| `page` | `integer` | Current page number (1-based) |
| `pageSize` | `integer` | Number of results per page |
| `totalPages` | `integer` | Total number of pages available |
| `searchTimeMs` | `integer` | Search execution time in milliseconds |
| `cacheHit` | `boolean` | Whether the query embedding was served from cache |
| `embeddingUsed` | `string` | Name of the embedding model used (e.g., `"qwen3-embedding-8b"`) |

### `SearchResult`

Individual product match.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Unique product identifier |
| `programName` | `string` | Name of the program/merchant |
| `title` | `string` | Product title |
| `description` | `string` | Product description |
| `price` | `number` | Product price |
| `currency` | `string` | Currency code (e.g., `"PLN"`, `"USD"`) |
| `url` | `string` | Product affiliate URL |
| `relevanceScore` | `number` | Semantic relevance score from 0.0 to 1.0 (higher = better match) |
| `imageUrls` | `string[]` | List of product image URLs |
| `attributes` | `ProductAttributes` | Additional product attributes |
| `lastModified` | `string` | ISO 8601 timestamp of last modification (nullable) |

### `ProductAttributes`

Extracted product metadata.

| Field | Type | Description |
|-------|------|-------------|
| `brand` | `string` | Product brand (nullable) |
| `category` | `string` | Product category path (nullable) |

### `BatchSearchResponse`

Response for bulk search requests.

| Field | Type | Description |
|-------|------|-------------|
| `results` | `SearchResult[]` | Flat list of all results from all queries |
| `groupedResults` | `object` | Dictionary mapping query text to its `SearchResult[]` |
| `totalTimeMs` | `integer` | Total execution time for all queries in milliseconds |
| `queriesProcessed` | `integer` | Number of queries processed in the batch |

---

## Request Schemas

### `SearchRequest`

Used as the request body for bulk search. For single search via GET, parameters are passed as query string arguments.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | `QueryModel` | **Yes** | Search query configuration |
| `filters` | `SearchFilters` | No | Optional price and category filters |
| `pagination` | `PaginationModel` | No | Pagination settings (defaults: page=1, pageSize=20) |
| `sorting` | `SortingModel` | No | Sorting preferences (defaults: field=relevance, order=desc) |

### `QueryModel`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `text` | `string` | **Yes** | — | Search text (max 500 characters) |
| `title_only` | `boolean` | No | `false` | Restrict search to product titles only |
| `description_only` | `boolean` | No | `false` | Restrict search to product descriptions only |

### `SearchFilters`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `minPrice` | `number` | No | Minimum price filter |
| `maxPrice` | `number` | No | Maximum price filter |
| `brand` | `string` | No | Brand filter (exact match) |
| `category` | `string` | No | Category filter (exact match) |

### `PaginationModel`

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `page` | `integer` | No | `1` | Must be >= 1 |
| `pageSize` | `integer` | No | `20` | Must be >= 1 and <= 100 |

### `SortingModel`

| Field | Type | Required | Default | Allowed Values |
|-------|------|----------|---------|----------------|
| `field` | `string` | No | `relevance` | `relevance`, `price`, `date` |
| `order` | `string` | No | `desc` | `asc`, `desc` |

---

## Error Responses

All error responses use a consistent format:

```json
{
  "error": "Human-readable error message"
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| `200 OK` | Request succeeded |
| `302 Found` | Redirect (used by `/go` endpoint) |
| `400 Bad Request` | Invalid input: missing or malformed parameters |
| `500 Internal Server Error` | Unexpected server-side error |

---

## Rate Limits

- **Single search:** No explicit rate limit
- **Bulk search:** Maximum 50 queries per request
- **Query length:** Maximum 500 characters per query text

---

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