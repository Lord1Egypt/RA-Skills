# API Documentation Patterns Reference

## HTTP Status Codes

### Success (2xx)

- **200 OK** - Standard successful response (GET, PUT, PATCH)
- **201 Created** - Resource created successfully (POST)
- **202 Accepted** - Request accepted, processing async
- **204 No Content** - Successful deletion (DELETE)

### Client Errors (4xx)

- **400 Bad Request** - Invalid input data
- **401 Unauthorized** - Missing or invalid authentication
- **403 Forbidden** - Authenticated but lacks permission
- **404 Not Found** - Resource doesn't exist
- **409 Conflict** - Resource conflict (duplicate email)
- **422 Unprocessable Entity** - Validation failed
- **429 Too Many Requests** - Rate limit exceeded

### Server Errors (5xx)

- **500 Internal Server Error** - Unexpected server error
- **502 Bad Gateway** - Upstream service error
- **503 Service Unavailable** - Temporary outage
- **504 Gateway Timeout** - Upstream timeout

## Common Request Parameters

### Path Parameters

```
GET /users/:id          # User identifier
GET /posts/:slug        # Post URL slug
GET /orgs/:org/repos    # Nested resources
```

### Query Parameters

```
GET /users?page=2&limit=20           # Pagination
GET /posts?sort=created_at&order=desc # Sorting
GET /users?filter[role]=admin        # Filtering
GET /posts?fields=id,title           # Field selection
GET /users?include=profile,posts     # Include related
```

### Header Parameters

```
Authorization: Bearer <token>        # Authentication
Content-Type: application/json       # Request format
Accept: application/json             # Response format
X-API-Key: <key>                    # API key auth
If-None-Match: "etag"               # Conditional requests
```

## Request/Response Patterns

### Pagination (Offset-based)

Request:
```
GET /users?page=2&limit=20
```

Response:
```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 156,
    "totalPages": 8
  }
}
```

### Pagination (Cursor-based)

Request:
```
GET /posts?cursor=eyJpZCI6MTIzfQ==&limit=20
```

Response:
```json
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTQ0fQ==",
    "hasMore": true
  }
}
```

### Filtering

```
GET /users?filter[role]=admin&filter[status]=active
GET /posts?tags[]=javascript&tags[]=tutorial
GET /products?price[gte]=100&price[lte]=500
```

### Sorting

```
GET /posts?sort=-createdAt,title  # Descending createdAt, then title asc
GET /users?orderBy=name&order=asc
```

### Field Selection (Sparse Fieldsets)

```
GET /users?fields=id,name,email
```

Response:
```json
{
  "data": [
    {
      "id": "123",
      "name": "John Doe",
      "email": "john@example.com"
    }
  ]
}
```

### Including Relations

```
GET /posts?include=author,comments
```

Response:
```json
{
  "data": {
    "id": "1",
    "title": "My Post",
    "author": { "id": "10", "name": "John" },
    "comments": [...]
  }
}
```

## Error Response Patterns

### Standard Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ],
    "requestId": "req_abc123"
  }
}
```

### Validation Errors

```json
{
  "error": "Validation failed",
  "validationErrors": {
    "email": ["Must be a valid email", "Email already exists"],
    "password": ["Must be at least 8 characters"]
  }
}
```

### Simple Error Format

```json
{
  "error": "User not found"
}
```

## Authentication Patterns

### Bearer Token (JWT)

```
Authorization: Bearer <your-jwt-token>
```

### API Key

```
X-API-Key: YOUR_API_KEY
```

or query parameter:
```
GET /users?api_key=YOUR_API_KEY
```

### Basic Auth

```
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

### OAuth 2.0

```
Authorization: Bearer <access_token>
```

## Rate Limiting

### Response Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1640995200
```

### Rate Limit Error

```json
{
  "error": "Rate limit exceeded",
  "retryAfter": 45,
  "limit": 100,
  "window": 60
}
```

## Versioning Strategies

### URL Versioning

```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

### Header Versioning

```
Accept: application/vnd.myapi.v2+json
```

### Query Parameter

```
GET /users?version=2
```

## Bulk Operations

### Batch Create

```
POST /users/batch
{
  "users": [
    { "name": "John", "email": "john@example.com" },
    { "name": "Jane", "email": "jane@example.com" }
  ]
}
```

Response:
```json
{
  "created": 2,
  "results": [
    { "id": "1", "status": "created" },
    { "id": "2", "status": "created" }
  ]
}
```

### Bulk Update

```
PATCH /users/bulk
{
  "ids": ["1", "2", "3"],
  "updates": {
    "status": "active"
  }
}
```

### Batch Delete

```
DELETE /users/batch
{
  "ids": ["1", "2", "3"]
}
```

## Partial Updates

### PATCH with JSON Patch

```
PATCH /users/123
Content-Type: application/json-patch+json

[
  { "op": "replace", "path": "/name", "value": "New Name" },
  { "op": "add", "path": "/tags/-", "value": "admin" }
]
```

### PATCH with Merge

```
PATCH /users/123
{
  "name": "New Name"
}
```

## File Upload

### Multipart Form Data

```
POST /users/123/avatar
Content-Type: multipart/form-data

--boundary
Content-Disposition: form-data; name="file"; filename="avatar.jpg"
Content-Type: image/jpeg

<file-data>
--boundary--
```

### Base64 Encoded

```
POST /users/123/avatar
{
  "file": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "filename": "avatar.jpg"
}
```

## Webhooks Documentation

### Webhook Payload

```json
{
  "event": "user.created",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "id": "123",
    "email": "user@example.com"
  }
}
```

### Signature Verification

```
X-Webhook-Signature: sha256=abc123...
```

Verify:
```javascript
const signature = hmac('sha256', SECRET, payload);
if (signature !== header['x-webhook-signature']) {
  throw new Error('Invalid signature');
}
```

## OpenAPI Schema Examples

### Parameter Schema

```yaml
parameters:
  - name: userId
    in: path
    required: true
    schema:
      type: string
      format: uuid
    description: Unique user identifier

  - name: page
    in: query
    required: false
    schema:
      type: integer
      minimum: 1
      default: 1
    description: Page number for pagination

  - name: Authorization
    in: header
    required: true
    schema:
      type: string
    description: Bearer token for authentication
```

### Request Body Schema

```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        required:
          - email
          - password
        properties:
          email:
            type: string
            format: email
            example: user@example.com
          password:
            type: string
            format: password
            minLength: 8
            example: SecurePass123
          rememberMe:
            type: boolean
            default: false
```

### Response Schema

```yaml
responses:
  '200':
    description: Successful response
    content:
      application/json:
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/components/schemas/User'
            pagination:
              $ref: '#/components/schemas/Pagination'
```

### Component Schemas

```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        createdAt:
          type: string
          format: date-time

    Error:
      type: object
      properties:
        error:
          type: string
        code:
          type: string
        details:
          type: object
```

## Documentation Best Practices

### Clear Descriptions

✅ Good:
```
"Retrieves a paginated list of active users, sorted by creation date"
```

❌ Bad:
```
"Gets users"
```

### Realistic Examples

✅ Good:
```json
{
  "email": "sarah.connor@example.com",
  "name": "Sarah Connor",
  "role": "admin"
}
```

❌ Bad:
```json
{
  "email": "string",
  "name": "string",
  "role": "string"
}
```

### Complete Error Documentation

Document ALL possible errors:
- 400 with validation details
- 401 for auth failures
- 403 for permission issues
- 404 for not found
- 429 for rate limiting
- 500 for server errors

### Security Documentation

Always document:
- Authentication method
- Required scopes/permissions
- Rate limits
- HTTPS requirement
- CORS policy

## Summary

Good API documentation includes:
- ✅ Clear endpoint descriptions
- ✅ Complete parameter documentation
- ✅ Realistic request/response examples
- ✅ All possible error responses
- ✅ Authentication requirements
- ✅ Rate limiting information
- ✅ Code examples in multiple languages
- ✅ Interactive API explorer
