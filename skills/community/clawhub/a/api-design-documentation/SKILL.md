---
name: "API Design & Documentation Generator"
description: "AI-powered API design and documentation assistant — generate RESTful/OpenAPI specs, write comprehensive API docs (guides, tutorials, reference), create mock servers, validate API designs, and produce SDK code snippets. Supports OpenAPI 3.0/3.1, AsyncAPI, GraphQL SDL, and major languages. Built for backend developers, API product managers, DevOps engineers, and technical writers who need to design, document, and ship APIs faster. Keywords: API documentation, OpenAPI spec, REST API design, API reference, developer portal, API guide, Swagger, AsyncAPI, GraphQL schema, API validation, mock server, SDK generation, API设计, 接口文档, OpenAPI, Swagger文档."
version: "1.0.0"
---

# API Design & Documentation Generator

## Overview

Stop wrestling with API documentation. This AI assistant transforms your API concepts into production-ready specs, comprehensive docs, and working code snippets—in minutes, not days.

## Triggers

- 中文触发词：`API文档`、`接口文档`、`生成OpenAPI`、`API设计`、`Swagger文档`、`接口规范`、`API教程`、`GraphQL文档`
- English triggers: `API documentation`, `OpenAPI spec`, `REST API design`, `Swagger docs`, `API reference`, `generate API docs`, `API guide`, `mock server`

## Features

### 1. API Design Intelligence
- Generate OpenAPI 3.0/3.1 specs from descriptions or existing code
- Validate API designs against best practices (REST maturity, naming conventions)
- Suggest improvements for security, performance, and developer experience
- Convert between OpenAPI, AsyncAPI, and GraphQL SDL

### 2. Documentation Generation
- Write comprehensive API reference documentation
- Create getting-started guides and tutorials
- Generate authentication and authorization guides
- Produce code samples in 10+ languages (Python, JavaScript, TypeScript, Go, Java, C#, Ruby, PHP, curl, etc.)
- Create Postman collections and Insomnia specifications

### 3. Mock Server Setup
- Generate mock server code from OpenAPI specs
- Support for static and dynamic mocking
- Create sample request/response pairs
- Set up delay rules for realistic testing

### 4. API Quality Assurance
- Validate OpenAPI/AsyncAPI syntax
- Check for common anti-patterns
- Ensure backward compatibility
- Generate changelog drafts for API updates

## Workflow

### API Documentation Workflow

```
1. INPUT: API description or existing code
   ↓
2. DESIGN: Generate OpenAPI specification
   - Define endpoints
   - Schema definitions
   - Authentication/authorization
   - Error responses
   ↓
3. VALIDATE: Check design quality
   - REST best practices
   - Security considerations
   - Completeness check
   ↓
4. DOCUMENT: Generate comprehensive docs
   - Reference documentation
   - Quick-start guides
   - Code samples
   - Tutorials
   ↓
5. TEST: Create mock server + test cases
```

### Quick API Spec Generation Workflow

```
Step 1: Describe your API
├── What does it do?
├── Who uses it?
└── What data does it manage?

Step 2: Define endpoints
├── Resources (nouns, not verbs)
├── CRUD operations
└── Query parameters

Step 3: Specify data models
├── Request/response schemas
├── Validation rules
└── Error formats

Step 4: Add security
├── Authentication method
├── Authorization scopes
└── Rate limiting

Step 5: Generate artifacts
├── OpenAPI spec (YAML/JSON)
├── Documentation
└── Code samples
```

## Input Examples

### Example 1: API Description to OpenAPI

**Input:**
```
Design a REST API for a task management system.
- Users can create, read, update, delete tasks
- Tasks have: title, description, due_date, priority, status, tags
- Support pagination for listing tasks
- Require JWT authentication
```

**Expected Output (OpenAPI 3.0):**
```yaml
openapi: 3.0.3
info:
  title: Task Management API
  version: 1.0.0
  description: API for managing tasks with full CRUD operations

paths:
  /tasks:
    get:
      summary: List all tasks
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: List of tasks
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Task'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
    post:
      summary: Create a new task
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [title]
              properties:
                title:
                  type: string
                description:
                  type: string
                due_date:
                  type: string
                  format: date
                priority:
                  type: string
                  enum: [low, medium, high]
      responses:
        '201':
          description: Task created

  /tasks/{id}:
    get:
      summary: Get a task by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Task details
        '404':
          description: Task not found

components:
  schemas:
    Task:
      type: object
      properties:
        id:
          type: string
        title:
          type: string
        description:
          type: string
        due_date:
          type: string
          format: date
        priority:
          type: string
        status:
          type: string
        tags:
          type: array
          items:
            type: string
    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Example 2: Generate Documentation from OpenAPI

**Input:** OpenAPI spec (above YAML)

**Expected Output Sections:**
```markdown
# Task Management API Documentation

## Getting Started

### Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your_token>
```

### Base URL
```
Production: https://api.tasks.example.com/v1
```

## Endpoints

### List Tasks
Retrieves a paginated list of all tasks.

**Request**
```bash
curl -X GET "https://api.tasks.example.com/v1/tasks?page=1&limit=20" \
  -H "Authorization: Bearer <token>"
```

**Response**
```json
{
  "data": [
    {
      "id": "task_123",
      "title": "Complete API docs",
      "priority": "high",
      "status": "pending"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45
  }
}
```

## Code Samples

### Python
```python
import requests

response = requests.get(
    "https://api.tasks.example.com/v1/tasks",
    headers={"Authorization": "Bearer <token>"}
)
tasks = response.json()
```

### JavaScript
```javascript
const response = await fetch(
  'https://api.tasks.example.com/v1/tasks',
  {
    headers: { 'Authorization': 'Bearer <token>' }
  }
);
const { data: tasks } = await response.json();
```
```

### Example 3: Code Sample Generation

**Input:** OpenAPI endpoint definition + language (Python)

**Output:** Complete, runnable code snippet with error handling

## Output Templates

### Template: API Reference Page
```markdown
# {Endpoint Name}

{Method} {Path}

## Description
{What this endpoint does}

## Authentication
{Authentication requirements}

## Request}

### Path Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| ... | ... | ... | ... |

### Query Parameters
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| ... | ... | ... | ... | ... |

### Request Body
```json
{Request body schema}
```

## Response

### 200 OK
```json
{Response schema}
```

### 400 Bad Request
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Description of the error",
    "details": [...]
  }
}
```

## Examples

### Request
```bash
curl -X {METHOD} {URL} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{body}'
```

### Response
```json
{response example}
```
```

## Best Practices

### For API Design
1. **Use nouns for resources:** `/users` not `/getUsers`
2. **Plural naming:** `/tasks` not `/task`
3. **Nest related resources:** `/users/{id}/tasks`
4. **Version from day one:** `/v1`, `/v2`
5. **Use appropriate HTTP methods:** GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove)
6. **Return proper status codes:** 200, 201, 400, 401, 403, 404, 500

### For Documentation
1. **Start with getting started:** Don't assume users know your API
2. **Provide runnable examples:** Copy-paste ready code beats prose
3. **Document errors clearly:** Users will hit them
4. **Keep it updated:** Outdated docs are worse than no docs
5. **Include changelog:** Help users track changes

### For Security
1. **Never log sensitive data:** Tokens, passwords, PII
2. **Use HTTPS only:** No exceptions
3. **Implement rate limiting:** Protect your infrastructure
4. **Validate all input:** Never trust client data

## Supported Standards

| Standard | Support Level |
|----------|---------------|
| OpenAPI 3.0 | Full |
| OpenAPI 3.1 | Full |
| AsyncAPI 2.0 | Full |
| GraphQL SDL | Full |
| RAML | Read/Convert |
| Swagger 2.0 | Read/Convert |

## Supported Languages for Code Generation

- Python (requests, httpx)
- JavaScript (fetch, axios)
- TypeScript
- Go (net/http, gorilla)
- Java (HttpClient, OkHttp)
- C# (.NET HttpClient)
- Ruby (Net::HTTP)
- PHP (cURL)
- curl
- Kotlin

## Version History

- **1.0.0** (2026-05-15): Initial release
  - OpenAPI 3.0/3.1 generation
  - Multi-language code samples
  - Documentation generation
  - Basic validation
