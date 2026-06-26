---
name: api-documentation-generator
description: Generate comprehensive API documentation from code — extract endpoints, parameters, response schemas, and examples from Express, FastAPI, Django, Rails, and more.
metadata:
  tags: ["api", "documentation", "openapi", "swagger", "developer-experience"]
---

# API Documentation Generator

Generate comprehensive API documentation by analyzing source code. Extracts endpoints, parameters, request/response schemas, authentication requirements, and generates examples. Works with Express, FastAPI, Django REST Framework, Rails, Spring Boot, and other frameworks.

## Usage

```
"Generate API docs from my Express app"
"Create API reference documentation"
"Document all endpoints in this project"
"Generate OpenAPI spec from my code"
```

## How It Works

### 1. Framework Detection

```bash
# Detect framework from dependencies
cat package.json 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin).get('dependencies',{})
for fw in ['express','fastify','koa','hapi','nestjs','next']:
    if fw in str(d): print(f'Node: {fw}')
" 2>/dev/null

cat requirements.txt setup.py pyproject.toml 2>/dev/null | grep -i "fastapi\|django\|flask\|starlette"
```

### 2. Endpoint Extraction

Scan source code for route definitions:

**Express/Node:**
```bash
grep -rn "router\.\(get\|post\|put\|patch\|delete\|all\)\|app\.\(get\|post\|put\|patch\|delete\)" src/ routes/
```

**FastAPI/Python:**
```bash
grep -rn "@app\.\(get\|post\|put\|patch\|delete\)\|@router\.\(get\|post\|put\|patch\|delete\)" src/ app/
```

**Django REST Framework:**
```bash
grep -rn "class.*ViewSet\|class.*APIView\|path(" */views.py */urls.py
```

For each endpoint, extract:
- HTTP method and path
- URL parameters and query parameters
- Request body schema (from TypeScript types, Pydantic models, serializers)
- Response format and status codes
- Authentication requirements
- Middleware chain
- Rate limiting rules

### 3. Schema Extraction

Analyze types/models for request/response schemas:

- TypeScript interfaces and types
- Pydantic models with field validators
- Django serializers with field definitions
- Joi/Zod validation schemas
- JSON Schema definitions

### 4. Example Generation

Generate realistic request/response examples:

- Valid request with all required fields
- Response with realistic data
- Error response examples (400, 401, 403, 404, 500)
- Curl command for quick testing
- SDK examples in popular languages

### 5. Documentation Output

Generate in multiple formats:

**Markdown API Reference:**
```markdown
## POST /api/users

Create a new user account.

**Authentication:** Bearer token required
**Rate limit:** 10 requests/minute

### Request Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | yes | Valid email address |
| name | string | yes | Full name (2-100 chars) |
| role | enum | no | "user" or "admin" (default: "user") |

### Response (201 Created)
```json
{
  "id": "usr_abc123",
  "email": "user@example.com",
  "name": "Jane Smith",
  "role": "user",
  "createdAt": "2026-04-30T10:00:00Z"
}
```

### Errors
- `400` — Invalid email format or missing required field
- `409` — Email already registered
- `429` — Rate limit exceeded
```

**OpenAPI 3.1 spec** — machine-readable for Swagger UI, Redoc, Postman

### 6. Completeness Check

Verify documentation quality:
- All endpoints documented
- All parameters described
- Response schemas match actual responses
- Authentication documented
- Error codes listed
- Examples present and valid

## Output

```
## API Documentation Generated

**Framework:** Express.js + TypeScript
**Endpoints found:** 23
**Documentation completeness:** 87%

### Generated Files
- docs/api-reference.md (full markdown reference)
- docs/openapi.yaml (OpenAPI 3.1 spec)
- docs/examples/ (curl examples per endpoint)

### Coverage
| Category | Endpoints | Documented | Missing |
|----------|-----------|------------|---------|
| Auth | 4 | 4 (100%) | — |
| Users | 6 | 5 (83%) | PATCH /users/:id |
| Orders | 8 | 7 (88%) | webhook handler |
| Admin | 5 | 5 (100%) | — |

### Undocumented
- PATCH /api/users/:id — has route but no type annotations
- POST /api/webhooks/stripe — raw req.body, no schema
```
