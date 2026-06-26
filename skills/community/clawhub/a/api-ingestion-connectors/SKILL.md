---
name: api_ingestion_connectors
title: API Ingestion Connectors
description: Connect to external APIs and ingest data into graph-ready structures for ETL pipelines and knowledge graph construction.
category: data-ingestion
tags:
  - api-integration
  - rest-api
  - graphql
  - data-ingestion
  - etl
  - knowledge-graph
  - authentication
  - pagination
  - data-transformation
  - developer-tools
version: 1.0.0
author: community
license: MIT
metadata:
  {"openclaw":{"emoji":"🌐","homepage":"https://clawhub.com"}}
---

# API Ingestion Connectors

**Ingest data from external APIs into graph-ready formats for knowledge graph construction.**

This skill retrieves data from diverse API sources and prepares it for transformation into **graph-ready structures** such as nodes, relationships, and triples.

## Quick Start

### Use When
- Ingesting data from REST APIs
- Querying GraphQL endpoints
- Integrating external services into data pipelines
- Pulling data from SaaS platforms
- Transforming API responses into graph datasets
- Building real-time knowledge graph updates

### Inputs
- API endpoint URLs
- Authentication credentials
- Request parameters and headers
- Pagination configuration
- Response format specifications
- Transformation mappings

### Outputs
- JSON/CSV datasets
- Graph-ready node/edge structures
- RDF triples
- Connector configurations
- ETL pipeline definitions

## Example

**Input API Configuration:**
```
Endpoint: https://api.example.com/users
Method: GET
Auth: Bearer Token
Pagination: page-based, 30 items per page
```

**Generated Output:**
```json
{
  "nodes": [
    {"id": "user_1", "type": "Person", "name": "Alice", "email": "alice@example.com"},
    {"id": "org_1", "type": "Organization", "name": "Acme Corp"}
  ],
  "edges": [
    {"source": "user_1", "target": "org_1", "relation": "WORKS_AT"}
  ]
}
```

## Supported API Types

### 1. REST APIs
Connect to standard HTTP REST endpoints with flexible authentication and pagination

```text
type: rest
endpoint: https://api.example.com/resource
method: GET|POST|PUT|DELETE
response_format: json|xml|csv
```

### 2. GraphQL APIs
Query GraphQL endpoints with structured query definitions

```graphql
query {
  users {
    id
    name
    email
    organization {
      name
    }
  }
}
```

### 3. OAuth-Protected APIs
Authenticate using OAuth 2.0 flows (authorization code, client credentials)

```text
auth_type: oauth2
client_id: ${CLIENT_ID}
client_secret: ${CLIENT_SECRET}
token_endpoint: https://api.example.com/oauth/token
```

### 4. API Key Authentication
Simple API key-based authentication

```text
auth_type: api_key
key_param: X-API-Key
key_value: ${API_KEY}
```

### 5. Bearer Token Authentication
OAuth 2.0 bearer token authentication

```text
auth_type: bearer
token: ${ACCESS_TOKEN}
```

## Pagination Strategies

### Offset/Limit Pagination
```text
type: offset
param_offset: offset
param_limit: limit
start_at: 0
page_size: 20
```

### Page-Based Pagination
```text
type: page
param_page: page
page_size: 30
start_at: 1
```

### Cursor-Based Pagination
```text
type: cursor
cursor_param: after
next_cursor_field: pageInfo.endCursor
has_next_field: pageInfo.hasNextPage
```

## Execution Steps

1. **Validate Configuration** – Check endpoint, auth, and parameters
2. **Authenticate** – Obtain credentials and tokens
3. **Make Request** – Execute HTTP/GraphQL request
4. **Handle Pagination** – Fetch all pages/results
5. **Parse Response** – Extract and validate response data
6. **Transform Data** – Convert to graph-ready format
7. **Generate Output** – Create nodes, edges, or triples
8. **Feed to Pipeline** – Pass to downstream transformation skills

## Output Formats

### Node-Edge Structure
```json
{
  "nodes": [{"id": "...", "type": "...", "properties": {...}}],
  "edges": [{"source": "...", "target": "...", "type": "...", "properties": {...}}]
}
```

### Graph Triples (RDF)
```turtle
:entity1 :relationType :entity2 .
:entity1 :property "value" .
```

### CSV Export
```csv
node_id,node_type,node_name,property1,property2
```

## Error Handling

The connector should handle:

- **Network Errors** – Retry logic with exponential backoff
- **Authentication Errors** – Token refresh, credential validation
- **Rate Limiting** – Backoff and request throttling
- **Malformed Responses** – Schema validation and error reporting
- **Timeouts** – Connection and read timeout handling

Example retry strategy:
```text
retry:
  max_attempts: 3
  backoff_factor: 2
  initial_delay: 1s
  max_delay: 60s
  retryable_status_codes: [429, 500, 502, 503, 504]
```

## Recommended Libraries

- **HTTP Clients:** requests, httpx, aiohttp
- **GraphQL:** gql, graphene, strawberry
- **OAuth:** authlib, oauthlib
- **Data Validation:** pydantic, jsonschema
- **Data Transformation:** pandas, polars

## Best Practices

✓ Respect API rate limits and terms of service  
✓ Implement exponential backoff for retries  
✓ Validate response schemas before processing  
✓ Handle and log errors appropriately  
✓ Cache results when possible  
✓ Normalize and deduplicate entities  
✓ Secure credentials (use environment variables)  
✓ Monitor API changes and versioning  
✓ Implement request timeout handling  
✓ Document API assumptions and requirements  

## Integration with Downstream Skills

The ingested data feeds into:

- **JSON → Triples Converter** – Transform to RDF
- **CSV → Graph Loader** – Load into graph database
- **Text → Entity/Relation Extractor** – Extract structured knowledge
- **ETL Pipeline Generator** – Orchestrate full workflows
- **Schema Validation** – Validate against graph schema

## References

See [connector-patterns.md](references/connector-patterns.md) for detailed API connector patterns and [example-connectors.md](examples/example-connectors.md) for complete connector examples.

---

**Version:** 1.0.0
