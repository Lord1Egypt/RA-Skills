# API Connector Examples

Complete connector examples for different API types and scenarios.

## Example 1: REST API with Bearer Token Authentication

### Scenario: GitHub Users API

**Configuration:**
```yaml
name: github_users_connector
api_type: rest
endpoint: https://api.github.com/users
method: GET
auth:
  type: bearer
  token: ${GITHUB_TOKEN}
pagination:
  type: page
  param: page
  page_size: 30
  start_at: 1
```

### Request Format

```bash
GET https://api.github.com/users?page=1&per_page=30
Authorization: Bearer ghp_xxxxxxxxxxxxxxxxxxxx
```

### Response Sample

```json
[
  {
    "login": "torvalds",
    "id": 1024454,
    "avatar_url": "https://avatars.githubusercontent.com/u/1024454",
    "type": "User",
    "company": "Linux",
    "location": "Portland, OR"
  },
  {
    "login": "gvanrossum",
    "id": 6500,
    "avatar_url": "https://avatars.githubusercontent.com/u/6500",
    "type": "User",
    "company": "Dropbox",
    "location": "San Francisco, CA"
  }
]
```

### Data Transformation to Graph

```json
{
  "nodes": [
    {
      "id": "github_torvalds",
      "type": "Person",
      "properties": {
        "login": "torvalds",
        "github_id": 1024454,
        "avatar_url": "https://avatars.githubusercontent.com/u/1024454",
        "user_type": "User",
        "company": "Linux",
        "location": "Portland, OR"
      }
    },
    {
      "id": "org_linux",
      "type": "Organization",
      "properties": {
        "name": "Linux"
      }
    }
  ],
  "edges": [
    {
      "source": "github_torvalds",
      "target": "org_linux",
      "type": "WORKS_AT"
    }
  ]
}
```

---

## Example 2: GraphQL API with API Key Authentication

### Scenario: Shopify GraphQL Admin API

**Configuration:**
```yaml
name: shopify_products_connector
api_type: graphql
endpoint: https://{shop}.myshopify.com/admin/api/2024-01/graphql.json
auth:
  type: api_key
  header: X-Shopify-Access-Token
  value: ${SHOPIFY_ACCESS_TOKEN}
```

### GraphQL Query

```graphql
query {
  products(first: 20) {
    edges {
      node {
        id
        title
        handle
        vendor
        description
        priceRange {
          minVariantPrice {
            amount
            currencyCode
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Response Sample

```json
{
  "data": {
    "products": {
      "edges": [
        {
          "node": {
            "id": "gid://shopify/Product/123456789",
            "title": "Summer T-Shirt",
            "handle": "summer-t-shirt",
            "vendor": "Acme Corp",
            "description": "High quality cotton T-shirt",
            "priceRange": {
              "minVariantPrice": {
                "amount": "29.99",
                "currencyCode": "USD"
              }
            }
          }
        }
      ],
      "pageInfo": {
        "hasNextPage": true,
        "endCursor": "eyJkaXJlY3Rpb24iOiJuZXh0IiwibGFzdElkIjoxMjM0NTY3ODksImxhc3RWYWx1ZSI6IlN1bW1lciBULVNoaXJ0In0"
      }
    }
  }
}
```

### Data Transformation to Graph

```json
{
  "nodes": [
    {
      "id": "shopify_product_123456789",
      "type": "Product",
      "properties": {
        "title": "Summer T-Shirt",
        "handle": "summer-t-shirt",
        "description": "High quality cotton T-shirt",
        "price": 29.99,
        "currency": "USD"
      }
    },
    {
      "id": "shopify_vendor_acme",
      "type": "Vendor",
      "properties": {
        "name": "Acme Corp"
      }
    }
  ],
  "edges": [
    {
      "source": "shopify_product_123456789",
      "target": "shopify_vendor_acme",
      "type": "SOLD_BY"
    }
  ]
}
```

---

## Example 3: REST API with OAuth 2.0 Client Credentials

### Scenario: Twitter/X API v2

**Configuration:**
```yaml
name: twitter_tweets_connector
api_type: rest
endpoint: https://api.twitter.com/2/tweets/search/recent
method: GET
auth:
  type: oauth2
  grant_type: client_credentials
  token_endpoint: https://api.twitter.com/2/oauth2/token
  client_id: ${TWITTER_CLIENT_ID}
  client_secret: ${TWITTER_CLIENT_SECRET}
headers:
  Accept: application/json
pagination:
  type: cursor
  param: pagination_token
  next_cursor_field: meta.next_token
  has_next_field: meta.result_count
```

### Request Format

```bash
GET https://api.twitter.com/2/tweets/search/recent?query=knowledge%20graph&max_results=100
Authorization: Bearer {access_token}
Accept: application/json
```

### Response Sample

```json
{
  "data": [
    {
      "id": "1234567890",
      "text": "Knowledge graphs are amazing for semantic search",
      "author_id": "987654321",
      "created_at": "2024-04-09T12:30:00.000Z",
      "public_metrics": {
        "retweet_count": 42,
        "reply_count": 8,
        "like_count": 156
      }
    }
  ],
  "includes": {
    "users": [
      {
        "id": "987654321",
        "name": "Alice Data",
        "username": "alicedata",
        "verified": true
      }
    ]
  },
  "meta": {
    "result_count": 100,
    "newest_id": "1234567890",
    "oldest_id": "1234567800",
    "next_token": "b26v89c19zqg8o3fpza4xwsm9v3465yw5ocdlrj8h39x6"
  }
}
```

### Data Transformation to Graph

```json
{
  "nodes": [
    {
      "id": "twitter_user_987654321",
      "type": "Person",
      "properties": {
        "name": "Alice Data",
        "username": "alicedata",
        "verified": true
      }
    },
    {
      "id": "twitter_tweet_1234567890",
      "type": "Tweet",
      "properties": {
        "text": "Knowledge graphs are amazing for semantic search",
        "created_at": "2024-04-09T12:30:00.000Z",
        "retweet_count": 42,
        "like_count": 156
      }
    }
  ],
  "edges": [
    {
      "source": "twitter_user_987654321",
      "target": "twitter_tweet_1234567890",
      "type": "POSTED"
    }
  ]
}
```

---

## Example 4: REST API with Offset Pagination and Basic Auth

### Scenario: PostgreSQL REST Wrapper

**Configuration:**
```yaml
name: postgres_users_connector
api_type: rest
endpoint: https://db.example.com/api/users
method: GET
auth:
  type: basic
  username: ${DB_USER}
  password: ${DB_PASSWORD}
pagination:
  type: offset
  param_offset: offset
  param_limit: limit
  page_size: 50
  start_at: 0
timeout: 30
retry:
  max_attempts: 3
  backoff_factor: 2
```

### Request Format

```bash
GET https://db.example.com/api/users?offset=0&limit=50
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

### Response Sample

```json
{
  "data": [
    {
      "user_id": "U001",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@company.com",
      "department_id": "DEPT_ENG",
      "hire_date": "2020-01-15"
    },
    {
      "user_id": "U002",
      "first_name": "Jane",
      "last_name": "Smith",
      "email": "jane.smith@company.com",
      "department_id": "DEPT_MKT",
      "hire_date": "2021-06-01"
    }
  ],
  "total_count": 250,
  "page_info": {
    "offset": 0,
    "limit": 50,
    "has_more": true
  }
}
```

### Data Transformation to Graph

```json
{
  "nodes": [
    {
      "id": "employee_U001",
      "type": "Employee",
      "properties": {
        "user_id": "U001",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@company.com",
        "hire_date": "2020-01-15"
      }
    },
    {
      "id": "dept_eng",
      "type": "Department",
      "properties": {
        "department_id": "DEPT_ENG",
        "name": "Engineering"
      }
    }
  ],
  "edges": [
    {
      "source": "employee_U001",
      "target": "dept_eng",
      "type": "WORKS_IN"
    }
  ]
}
```

---

## Example 5: GraphQL API with Cursor Pagination

### Scenario: GitHub GraphQL API

**Configuration:**
```yaml
name: github_repos_connector
api_type: graphql
endpoint: https://api.github.com/graphql
auth:
  type: bearer
  token: ${GITHUB_TOKEN}
pagination:
  type: cursor
  cursor_param: after
  next_cursor_field: pageInfo.endCursor
  has_next_field: pageInfo.hasNextPage
```

### GraphQL Query

```graphql
query($after: String) {
  search(first: 100, query: "stars:>1000 language:python", type: REPOSITORY, after: $after) {
    repositoryCount
    edges {
      node {
        ... on Repository {
          name
          owner {
            login
          }
          description
          stargazerCount
          forkCount
          primaryLanguage {
            name
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Response Sample

```json
{
  "data": {
    "search": {
      "repositoryCount": 5000,
      "edges": [
        {
          "node": {
            "name": "tensorflow",
            "owner": {
              "login": "tensorflow"
            },
            "description": "An Open Source Machine Learning Framework",
            "stargazerCount": 185000,
            "forkCount": 74000,
            "primaryLanguage": {
              "name": "C++"
            }
          }
        }
      ],
      "pageInfo": {
        "hasNextPage": true,
        "endCursor": "Y3Vyc29yOnYyOpHOA1MDAA=="
      }
    }
  }
}
```

### Data Transformation to Graph

```json
{
  "nodes": [
    {
      "id": "github_repo_tensorflow",
      "type": "Repository",
      "properties": {
        "name": "tensorflow",
        "description": "An Open Source Machine Learning Framework",
        "stars": 185000,
        "forks": 74000,
        "primary_language": "C++"
      }
    },
    {
      "id": "github_user_tensorflow",
      "type": "Organization",
      "properties": {
        "login": "tensorflow"
      }
    }
  ],
  "edges": [
    {
      "source": "github_user_tensorflow",
      "target": "github_repo_tensorflow",
      "type": "OWNS"
    }
  ]
}
```

---

## API Connector Comparison Table

| Connector | API Type | Auth Type | Pagination | Response Format | Use Case |
|-----------|----------|-----------|-----------|-----------------|----------|
| GitHub Users | REST | Bearer | Page | JSON | User/org profiles |
| Shopify Products | GraphQL | API Key | Cursor | JSON | E-commerce catalog |
| Twitter Tweets | REST | OAuth2 | Cursor | JSON | Social media analysis |
| PostgreSQL REST | REST | Basic | Offset | JSON | Database sync |
| GitHub Repos | GraphQL | Bearer | Cursor | JSON | Repository search |

---

## Error Handling Examples

### Rate Limiting (429)
```
Retry-After: 3600
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1712686800

Action: Wait 1 hour, apply exponential backoff
```

### Authentication Error (401)
```
WWW-Authenticate: Bearer realm="GitHub API v3"
error: invalid_token

Action: Refresh token or re-authenticate
```

### Server Error (503)
```
Retry-After: 120

Action: Exponential backoff, maximum 3 retries
```

---

See [connector-patterns.md](../references/connector-patterns.md) for detailed API connector design patterns.


