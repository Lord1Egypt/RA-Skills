---
name: Endpoint Compliance Check
description: Use this skill to verify that an API endpoint (or route implementation) follows the Endpoint Standard. Run through the checklist for each endpoint under review.
---

# Endpoint Compliance Check

Use this checklist to verify that an endpoint follows the **Endpoint Standard** (see `ENDPOINT_REQUIREMENT.md`). For each endpoint, answer **Yes** / **No** / **N/A** and note any gaps.

---

## 1. Response format

| # | Check | Yes / No / N/A | Notes |
|---|--------|-----------------|--------|
| 1.1 | Response is JSON (unless another format is explicitly requested)? | | |
| 1.2 | Success responses use envelope `{ success, data }` with `success: true`? | | |
| 1.3 | Response does **not** put business data at the root (only inside `data`)? | | |
| 1.4 | HTTP status code is set correctly (2xx for success)? | | |

---

## 2. Error format

| # | Check | Yes / No / N/A | Notes |
|---|--------|-----------------|--------|
| 2.1 | Error responses use envelope `{ success: false, error }`? | | |
| 2.2 | `error` has at least `code` (string) and `message` (string)? | | |
| 2.3 | Optional `details` used for validation/extra context only? | | |
| 2.4 | HTTP status matches the error (4xx client, 5xx server)? | | |

---

## 3. Authentication

| # | Check | Yes / No / N/A | Notes |
|---|--------|-----------------|--------|
| 3.1 | Auth is done via token (e.g. Bearer in `Authorization` header)? | | |
| 3.2 | Credentials (e.g. password) are **not** sent in request body for normal authenticated calls? | | |
| 3.3 | 401 used for missing/invalid token; 403 for valid token but insufficient permission? | | |

---

## 4. Request format

| # | Check | Yes / No / N/A | Notes |
|---|--------|-----------------|--------|
| 4.1 | Request body is JSON with `Content-Type: application/json` where applicable? | | |
| 4.2 | Resource ids in path (e.g. `/items/:id`); filters/sort/pagination in query? | | |
| 4.3 | If paginated, response `data` includes pagination metadata (e.g. total, page, limit)? | | |

---

## 5. Status codes

| # | Check | Yes / No / N/A | Notes |
|---|--------|-----------------|--------|
| 5.1 | 200 for successful GET/PATCH/PUT? | | |
| 5.2 | 201 for successful creation with body? | | |
| 5.3 | 204 for success with no body (e.g. delete)? | | |
| 5.4 | 400/422 for validation/bad request; 401/403 for auth; 404 for not found; 500 for server errors? | | |

---

## 6. Optional (recommended)

| # | Check | Yes / No / N/A | Notes |
|---|--------|-----------------|--------|
| 6.1 | API versioning (e.g. `/api/v1/...`) or equivalent? | | |
| 6.2 | CORS headers set for web clients if needed? | | |
| 6.3 | Rate limiting returns 429 with standard error body? | | |
| 6.4 | Health/readiness endpoint (e.g. GET /health) returns 200 + minimal JSON? | | |

---

## How to use

1. **Per endpoint**: Copy the tables (or reference this file) and fill Yes/No/N/A and notes for the endpoint you are reviewing.
2. **Compliance**: An endpoint is **compliant** if all required items (sections 1–5) are **Yes** or **N/A** where appropriate. Section 6 is recommended but not required for “compliant” status.
3. **Reporting**: List any **No** answers and fix the implementation to match the Endpoint Standard, then re-run the check.

---

## One-line summary

**Endpoint follows the standard if:**  
JSON envelope (`success` + `data` or `error`), correct HTTP status, token-based auth only, consistent error shape (`code`, `message`, optional `details`), and request/response formats as above.
