# Backend Specification Template

This section of the Implementation Plan is written exclusively for the BE Developer. It must be self-contained — the BE dev should be able to complete all backend work using only this section, the DB schema spec, and the cross-cutting concerns section.

## ID Convention

All backend items use the prefix `BE-` followed by a sequential number: BE-001, BE-002, etc.

---

## BE-S1: API Endpoint Definitions

For every endpoint the backend must expose:

```
BE-001: [Descriptive Name]
SRS Requirement(s): [SRS-XXX]
Method: GET | POST | PUT | PATCH | DELETE
Path: /api/v1/[resource]/[path]
Auth Required: Yes | No
Required Role(s): [admin, user, etc. — or "any authenticated"]
Rate Limited: [Yes — X requests per Y seconds | No]

Request:
  Headers:
    Authorization: Bearer <token>
    Content-Type: application/json
  URL Params: [id, slug, etc.]
  Query Params:
    - page (integer, optional, default: 1)
    - limit (integer, optional, default: 20, max: 100)
    - sort (string, optional, values: [created_at, name])
    - [other filters]
  Body:
    {
      "field_name": "type — required | optional — description",
      "field_name": "type — required | optional — description"
    }

Response (200/201):
    {
      "field_name": "type — description",
      "field_name": "type — description"
    }

Error Responses:
    400: { "error": { "code": "VALIDATION_ERROR", "message": "...", "details": { "field": "reason" } } }
    401: { "error": { "code": "UNAUTHORIZED", "message": "Authentication required" } }
    403: { "error": { "code": "FORBIDDEN", "message": "Insufficient permissions" } }
    404: { "error": { "code": "NOT_FOUND", "message": "[Resource] not found" } }
    409: { "error": { "code": "CONFLICT", "message": "..." } }
    500: { "error": { "code": "INTERNAL_ERROR", "message": "An unexpected error occurred" } }
```

Not every endpoint will use every error code — include only the ones that apply.

## BE-S2: Business Logic Rules

For each endpoint or feature that involves business logic beyond simple CRUD:

```
Rule: BE-BL-001 — [descriptive name]
Applies to: [BE-XXX endpoint(s)]
SRS Requirement: [SRS-XXX]
Logic:
  1. [step-by-step description of the business rule]
  2. [next step]
  3. [next step]
Edge Cases:
  - [what happens if X]
  - [what happens if Y]
Validation:
  - [field]: [rule — e.g., must be positive integer, must be unique, must reference existing record]
```

## BE-S3: Service / Controller / Model Structure

Define the code organization:

```
Structure:
  controllers/
    [resource]Controller — Handles HTTP request/response for [resource]
  services/
    [resource]Service — Business logic for [resource]
  models/
    [Resource] — Database model/entity for [resource]
  middleware/
    authMiddleware — Validates token, attaches user to request
    validationMiddleware — Runs request validation schemas
    errorHandler — Catches and formats all errors
  utils/
    [utility files as needed]
```

For each service, note its public methods and what they do:

```
[Resource]Service:
  - create(data) → [Resource] — creates a new record, validates [rules]
  - getById(id) → [Resource] | null — retrieves by primary key
  - list(filters, pagination) → { items: [Resource][], total: number }
  - update(id, data) → [Resource] — partial update, validates [rules]
  - delete(id) → void — [soft delete / hard delete], checks [conditions]
```

## BE-S4: Authentication & Permission Implementation

```
Auth Flow:
  1. Login: POST /api/v1/auth/login → validates credentials → returns token
  2. Token Type: [JWT / session / OAuth token]
  3. Token Expiry: [duration]
  4. Refresh: [how token refresh works, if applicable]
  5. Logout: [what happens server-side — blacklist token, destroy session, etc.]

Permission Checks:
  - Middleware extracts user from token
  - Each endpoint specifies required role(s)
  - Middleware rejects with 403 if role insufficient
  - Resource-level permissions: [e.g., users can only edit their own records unless admin]
```

## BE-S5: Data Validation Rules

For each endpoint's request body, define validation:

```
Endpoint: BE-001
Validation:
  - email: required, valid email format, max 255 chars, unique in users table
  - password: required, min 8 chars, must contain uppercase + number
  - name: required, string, max 100 chars, trimmed
  - role: optional, must be one of ["admin", "user", "viewer"], default "user"
```

Note where validation happens (middleware vs. service layer) and how errors are returned (per the cross-cutting error format).

## BE-S6: Integration Points

For each third-party service the backend communicates with:

```
Integration: [service name]
Purpose: [what it's used for]
Endpoint(s): [API URLs or SDK methods]
Auth: [API key, OAuth, etc.]
Data Sent: [what data goes out]
Data Received: [what comes back]
Error Handling: [what happens if the service is down or returns an error]
Fallback: [retry strategy, graceful degradation, etc.]
```

## BE-S7: Security Checklist

This checklist is mandatory for every backend spec. Complete it before submitting the Implementation Plan.

```
[ ] Input Validation: All user inputs are validated and sanitized before processing
[ ] Authentication: All non-public endpoints require valid authentication
[ ] Authorization: Endpoints enforce role-based access; users cannot access other users' data without explicit permission
[ ] Secrets Management: No hardcoded secrets; all sensitive values come from environment variables
[ ] SQL Injection: All database queries use parameterized queries or ORM methods (never string concatenation)
[ ] Rate Limiting: Authentication endpoints (login, register, password reset) have rate limits
[ ] CORS: CORS is configured to allow only known origins
[ ] Headers: Security headers set (X-Content-Type-Options, X-Frame-Options, etc.)
[ ] Error Messages: Error responses never expose stack traces, internal paths, or database details
[ ] Logging: Sensitive data (passwords, tokens, PII) is never written to logs
[ ] Dependencies: No known critical CVEs in production dependencies
[ ] File Uploads: If applicable — file type validation, size limits, malware considerations
```

If an item does not apply, mark it N/A with a reason.

## BE-S8: Acceptance Criteria

For each endpoint or business logic rule, write acceptance criteria:

```
BE-AC-001 (maps to BE-001, SRS-XXX):
  Given: [precondition]
  When: [API call with specific inputs]
  Then: [expected response status and body]

BE-AC-002 (maps to BE-001, SRS-XXX):
  Given: [precondition — e.g., user is not authenticated]
  When: [API call]
  Then: [401 response]
```

Cover: happy path, authentication failure, authorization failure, validation failure, and any business-logic edge cases. QA uses these directly.
