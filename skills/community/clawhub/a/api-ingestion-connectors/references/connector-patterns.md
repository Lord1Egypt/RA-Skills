# API Connector Design Patterns

This guide provides patterns for building and configuring API connectors for knowledge graph ingestion.

## REST API Connector Patterns

### Basic REST Connector

```yaml
Pattern: Simple HTTP GET request

name: basic_connector
api_type: rest
endpoint: https://api.example.com/data
method: GET
timeout: 30
```

**When to use:**
✓ Public APIs with no authentication
✓ Simple read-only data extraction
✓ Single-page responses

---

### REST with Query Parameters

```yaml
Pattern: API endpoint with query parameters

name: parameterized_connector
api_type: rest
endpoint: https://api.example.com/search
method: GET
params:
  q: "knowledge graph"
  type: "article"
  sort: "date_desc"
```

**When to use:**
✓ Filtered data retrieval
✓ Search and filtering APIs
✓ Dynamic parameter configuration

---

### REST with Request Headers

```yaml
Pattern: Custom headers for API communication

name: header_connector
api_type: rest
endpoint: https://api.example.com/v2/data
method: GET
headers:
  Accept: application/json
  User-Agent: MyConnector/1.0
  X-Custom-Header: custom_value
```

**When to use:**
✓ APIs requiring specific headers
✓ Content negotiation
✓ Custom API protocols

---

### REST with Request Body (POST)

```yaml
Pattern: POST request with JSON body

name: post_connector
api_type: rest
endpoint: https://api.example.com/query
method: POST
headers:
  Content-Type: application/json
body:
  query: "SELECT * FROM users WHERE active = true"
  limit: 100
```

**When to use:**
✓ Complex query submission
✓ Bulk data operations
✓ Custom request bodies

---

## Authentication Patterns

### Bearer Token Authentication

```yaml
Pattern: OAuth 2.0 bearer token

auth:
  type: bearer
  token: ${BEARER_TOKEN}
```

**Implementation:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**When to use:**
✓ OAuth 2.0 token-based APIs
✓ JWT tokens
✓ Modern API authentication

---

### API Key Authentication

```yaml
Pattern: API key in header

auth:
  type: api_key
  header: X-API-Key
  value: ${API_KEY}
```

**Implementation:**
```
X-API-Key: sk-1234567890abcdef
```

**Alternative (Query Parameter):**
```yaml
auth:
  type: api_key
  param: api_key
  value: ${API_KEY}
```

**When to use:**
✓ Simple API key authentication
✓ Public APIs with rate limiting
✓ Legacy APIs

---

### Basic Authentication

```yaml
Pattern: HTTP Basic Authentication

auth:
  type: basic
  username: ${USERNAME}
  password: ${PASSWORD}
```

**Implementation:**
```
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

**When to use:**
✓ Legacy authentication methods
✓ Database REST wrappers
✓ Internal APIs

---

### OAuth 2.0 Client Credentials

```yaml
Pattern: OAuth 2.0 server-to-server flow

auth:
  type: oauth2
  grant_type: client_credentials
  token_endpoint: https://auth.example.com/token
  client_id: ${CLIENT_ID}
  client_secret: ${CLIENT_SECRET}
  scope: api.read
```

**Flow:**
```
1. POST /token with client_id and client_secret
2. Receive access_token and expires_in
3. Use access_token for API requests
4. Refresh token before expiration
```

**When to use:**
✓ Service-to-service authentication
✓ Background jobs and batch processing
✓ Trusted applications

---

### OAuth 2.0 Authorization Code Flow

```yaml
Pattern: OAuth 2.0 user authentication

auth:
  type: oauth2
  grant_type: authorization_code
  authorize_url: https://auth.example.com/authorize
  token_endpoint: https://auth.example.com/token
  client_id: ${CLIENT_ID}
  client_secret: ${CLIENT_SECRET}
  redirect_uri: http://localhost:8080/callback
```

**Flow:**
```
1. Redirect user to authorize_url
2. User grants permission
3. Receive authorization_code
4. Exchange code for access_token
5. Use access_token for API requests
```

**When to use:**
✓ User-facing applications
✓ Multi-user systems
✓ Delegated access

---

## Pagination Patterns

### Offset/Limit Pagination

```yaml
Pattern: Offset-based pagination for APIs

connector:
  pagination:
    type: offset
    param_offset: offset
    param_limit: limit
    page_size: 50
    start_at: 0

Example:
  - GET /api/items?offset=0&limit=50
  - GET /api/items?offset=50&limit=50
  - GET /api/items?offset=100&limit=50
```

**Properties:**
```
offset: Starting position (0-based)
limit: Number of items per page
page_size: Items per request
start_at: First page number
```

**When to use:**
✓ Simple sequential pagination
✓ Database APIs
✓ Legacy REST APIs

---

### Page-Based Pagination

```yaml
Pattern: Page number-based pagination

connector:
  pagination:
    type: page
    param_page: page
    page_size: 30
    start_at: 1

Example:
  - GET /api/users?page=1&per_page=30
  - GET /api/users?page=2&per_page=30
  - GET /api/users?page=3&per_page=30
```

**Properties:**
```
param_page: Query parameter for page number
page_size: Items per page
start_at: First page number (1 or 0)
```

**When to use:**
✓ Public APIs (GitHub, Twitter, etc.)
✓ RESTful APIs with standard pagination
✓ User-friendly pagination

---

### Cursor-Based Pagination

```yaml
Pattern: Opaque cursor for stateless pagination

connector:
  pagination:
    type: cursor
    cursor_param: after
    next_cursor_field: pageInfo.endCursor
    has_next_field: pageInfo.hasNextPage

Example:
  - GET /api/items?after=
  - GET /api/items?after=Y3Vyc29yOnYyOpHOA1MDAA==
  - GET /api/items?after=Y3Vyc29yOnYyOpHOBEBFAA==
```

**Properties:**
```
cursor_param: Query parameter for cursor
next_cursor_field: Path to next cursor in response
has_next_field: Path to hasNextPage flag
```

**When to use:**
✓ GraphQL APIs
✓ Large datasets
✓ Real-time data streams

---

### Link-Based Pagination

```yaml
Pattern: Using rel="next" links in response

connector:
  pagination:
    type: link
    next_link_field: _links.next.href

Example Response:
{
  "_links": {
    "next": {"href": "/api/items?page=2"}
  },
  "items": [...]
}
```

**When to use:**
✓ HATEOAS APIs
✓ Hypermedia-driven APIs
✓ APIs with dynamic pagination

---

## GraphQL Connector Patterns

### Simple GraphQL Query

```yaml
Pattern: Basic GraphQL query

api_type: graphql
endpoint: https://api.example.com/graphql
auth:
  type: bearer
  token: ${TOKEN}

query:
  query: |
    query {
      users {
        id
        name
        email
      }
    }
```

**When to use:**
✓ Simple data retrieval
✓ No pagination required
✓ Single query execution

---

### GraphQL with Variables

```yaml
Pattern: Parameterized GraphQL query

api_type: graphql
endpoint: https://api.example.com/graphql

query:
  query: |
    query GetUser($id: ID!) {
      user(id: $id) {
        id
        name
        email
        posts {
          id
          title
        }
      }
    }
  variables:
    id: "${USER_ID}"
```

**When to use:**
✓ Dynamic parameter values
✓ Filtered queries
✓ Parameterized operations

---

### GraphQL with Pagination

```yaml
Pattern: GraphQL pagination with cursor

api_type: graphql
endpoint: https://api.example.com/graphql

query:
  query: |
    query($after: String) {
      users(first: 20, after: $after) {
        edges {
          node {
            id
            name
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  variables:
    after: "${CURSOR}"
```

**When to use:**
✓ Large result sets
✓ Cursor-based pagination
✓ Memory-efficient fetching

---

### GraphQL Batch Query

```yaml
Pattern: Multiple GraphQL queries in one request

api_type: graphql
endpoint: https://api.example.com/graphql

query:
  query: |
    query {
      users {
        id
        name
      }
      posts {
        id
        title
        author {
          id
        }
      }
      comments {
        id
        text
      }
    }
```

**When to use:**
✓ Fetching multiple entities
✓ Reducing request count
✓ Related data retrieval

---

## Error Handling Patterns

### Retry with Exponential Backoff

```yaml
Pattern: Automatic retry on failure

retry:
  enabled: true
  max_attempts: 3
  initial_delay: 1
  backoff_factor: 2
  max_delay: 60
  retryable_status_codes: [429, 500, 502, 503, 504]

Logic:
  Attempt 1: immediate
  Attempt 2: wait 1s (2^0 * 1)
  Attempt 3: wait 2s (2^1 * 1)
  Attempt 4: wait 4s (2^2 * 1)
  Max: 60s
```

**When to use:**
✓ Rate-limited APIs
✓ Unreliable networks
✓ Transient failures

---

### Rate Limit Handling

```yaml
Pattern: Respect API rate limits

rate_limiting:
  enabled: true
  requests_per_second: 10
  check_headers: true
  header_remaining: X-RateLimit-Remaining
  header_reset: X-RateLimit-Reset

Logic:
  1. Check rate limit headers
  2. Sleep if approaching limit
  3. Respect reset time
```

**When to use:**
✓ APIs with strict rate limits
✓ Shared API quotas
✓ Large-scale data extraction

---

### Response Validation

```yaml
Pattern: Validate response schema

validation:
  enabled: true
  schema:
    type: object
    required: [id, name]
    properties:
      id:
        type: string
      name:
        type: string
  on_error: log_and_continue
```

**When to use:**
✓ Unreliable APIs
✓ Data quality assurance
✓ Error detection

---

## Data Transformation Patterns

### Simple Field Mapping

```yaml
Pattern: Map API fields to graph properties

mapping:
  node_type: user
  fields:
    api_id: graph_id
    full_name: name
    email_address: email
    created_timestamp: created_at
```

**When to use:**
✓ Direct field mapping
✓ Field naming differences
✓ Simple transformations

---

### Nested Object Flattening

```yaml
Pattern: Flatten nested API responses

mapping:
  nodes:
    - type: person
      id_field: user.id
      properties:
        name: user.profile.full_name
        email: user.contact.email
        company: user.profile.company.name
```

**When to use:**
✓ Nested API responses
✓ Complex object structures
✓ Path-based extraction

---

### Entity Deduplication

```yaml
Pattern: Remove duplicate entities during ingestion

deduplication:
  enabled: true
  key_fields: [id, email]
  strategy: keep_first
```

**When to use:**
✓ Pagination-heavy APIs
✓ Overlapping result sets
✓ Data consistency

---

## Best Practices

✓ **Validate configuration before execution** – Check endpoints, auth, parameters  
✓ **Implement proper error handling** – Log errors, apply retries, notify on failures  
✓ **Respect API rate limits** – Check headers, implement backoff  
✓ **Validate response data** – Schema validation, type checking  
✓ **Cache results when possible** – Reduce API calls, improve performance  
✓ **Monitor API changes** – Track versioning, API deprecations  
✓ **Secure credentials** – Use environment variables, key management services  
✓ **Document assumptions** – API version, expected fields, edge cases  
✓ **Test with real data** – Validate transformations end-to-end  
✓ **Log meaningful information** – Request/response metadata, timing, errors  

---

See [example-connectors.md](../examples/example-connectors.md) for complete connector implementation examples.


