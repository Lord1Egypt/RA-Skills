# API Design Quick Reference

## HTTP Methods at a Glance

| Method | Safe | Idempotent | Request Body | Response Body |
|--------|------|------------|--------------|---------------|
| GET | Yes | Yes | No | Yes |
| POST | No | No | Yes | Yes |
| PUT | No | Yes | Yes | Yes |
| PATCH | No | No | Yes | Yes |
| DELETE | No | Yes | No | No |

## Status Codes Cheat Sheet

### 2xx Success
- **200 OK** - GET, PUT, PATCH success
- **201 Created** - POST success (include Location header)
- **204 No Content** - DELETE success

### 4xx Client Error
- **400 Bad Request** - Malformed request syntax
- **401 Unauthorized** - Missing or invalid authentication
- **403 Forbidden** - Authenticated but not authorized
- **404 Not Found** - Resource doesn't exist
- **409 Conflict** - State conflict (duplicate, version mismatch)
- **422 Unprocessable Entity** - Validation failed
- **429 Too Many Requests** - Rate limited

### 5xx Server Error
- **500 Internal Server Error** - Unexpected error
- **503 Service Unavailable** - Temporarily down

## URL Patterns

```
# Collection
GET    /api/resources          → List all
POST   /api/resources          → Create new

# Item
GET    /api/resources/{id}     → Get one
PUT    /api/resources/{id}     → Replace
PATCH  /api/resources/{id}     → Partial update
DELETE /api/resources/{id}     → Remove

# Nested (max 1 level)
GET    /api/users/{id}/orders  → User's orders

# Actions (when REST doesn't fit)
POST   /api/orders/{id}/cancel → Action on resource
```

## Query Parameters

```
# Pagination
?page=2&page_size=20
?limit=20&cursor=abc123

# Filtering
?status=active
?status=active,pending

# Sorting
?sort=created_at
?sort=-created_at        (descending)
?sort=status,-created_at (multiple)

# Search
?search=keyword
?q=keyword

# Field selection
?fields=id,name,email
```

## Standard Headers

### Request
```
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
Idempotency-Key: <unique-id>
```

### Response
```
Content-Type: application/json
Location: /api/resources/123       (after 201)
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 742
X-RateLimit-Reset: 1640000000
Cache-Control: public, max-age=3600
ETag: "33a64df551"
```

## Error Response Template

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable message",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "value": "not-an-email"
      }
    ],
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

## Pagination Response Template

```json
{
  "items": [...],
  "pagination": {
    "page": 2,
    "page_size": 20,
    "total": 150,
    "pages": 8,
    "has_next": true,
    "has_prev": true
  }
}
```

## GraphQL Quick Reference

### Query
```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    orders(first: 10) {
      edges {
        node {
          id
          total
        }
      }
      pageInfo {
        hasNextPage
      }
    }
  }
}
```

### Mutation
```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    user {
      id
      name
    }
    errors {
      field
      message
    }
  }
}
```

## Common Mistakes to Avoid

| Wrong | Right |
|-------|-------|
| `POST /getUsers` | `GET /users` |
| `GET /createUser` | `POST /users` |
| `POST /users/delete/123` | `DELETE /users/123` |
| `/user/123` | `/users/123` (plural) |
| `/api/users/123/orders/456/items` | Max 2 levels |
| 200 for everything | Correct status codes |
| Different error formats | Consistent structure |
