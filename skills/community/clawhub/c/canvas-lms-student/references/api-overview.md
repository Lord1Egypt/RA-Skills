# Canvas LMS API Overview

## Base URL Format

```
https://<institution-domain>/api/v1/
```

Examples:
- `https://canvas.instructure.com/api/v1/`
- `https://canvas.university.edu/api/v1/`

## Authentication

All requests require an `Authorization` header:

```bash
curl -H "Authorization: Bearer <TOKEN>" \
  "https://canvas.instructure.com/api/v1/courses"
```

## Key Response Headers

- `Link`: Pagination links (next, prev, first, last)
- `X-Rate-Limit-Remaining`: API rate limit status

## Pagination

Default: 10 items per page  
Maximum: 100 items per page (`?per_page=100`)

Use `Link` header URLs for pagination - don't construct manually.

## Common HTTP Methods

| Method | Usage |
|--------|-------|
| GET | Retrieve data (all student operations) |
| POST | Create resources (not used in read-only skill) |
| PUT | Update resources (not used) |
| DELETE | Remove resources (not used) |

## Error Codes

| Code | Meaning |
|------|---------|
| 401 | Invalid/expired token |
| 403 | Insufficient permissions |
| 404 | Resource not found |
| 429 | Rate limit exceeded |

## Official Python SDK

```bash
pip install canvasapi
```

Basic usage:
```python
from canvasapi import Canvas

canvas = Canvas("https://canvas.university.edu", "your_token")
user = canvas.get_current_user()
print(user.name)
```

This skill uses `canvasapi` for clean, object-oriented API access.
