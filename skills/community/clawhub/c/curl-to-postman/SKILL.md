---
name: curl-to-postman
description: Convert curl commands to Postman Collection v2.1 importable JSON
---

# curl-to-postman

Convert curl commands into Postman-importable JSON with a single paste.

## Usage

Paste a curl command and receive a formatted Postman Collection v2.1 JSON that you can import directly into Postman via the Import button.

## What it converts

| curl flag | Postman field |
|-----------|---------------|
| `-X METHOD` / `--request METHOD` | request method (default: GET) |
| `-H "Key: Value"` / `--header "Key: Value"` | request headers |
| `-d "body"` / `--data "body"` / `--data-raw "body"` | request body |
| `--user user:pass` / `-u user:pass` | Basic Auth header |
| `-H "Authorization: Bearer token"` | Bearer token (preserved as-is) |
| URL query string `?key=value` | url.query[] |

## Supported options

- **SSL**: `-k` / `--insecure` → `checkDisableSSLValidation: true`
- **Redirects**: `-L` / `--location` → follow redirects
- **Auth**: `--user` / `-u` → Basic Auth; Bearer token via `-H` takes priority

## Output structure

```json
{
  "info": {
    "name": "Converted from curl",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "POST /endpoint",
      "request": {
        "method": "POST",
        "header": [{ "key": "Content-Type", "value": "application/json" }],
        "url": {
          "raw": "https://api.example.com/users",
          "protocol": "https",
          "host": ["api", "example", "com"],
          "path": ["users"],
          "query": []
        },
        "body": { "mode": "raw", "raw": "{\"name\":\"John\"}" }
      }
    }
  ]
}
```

## Example

**Input:**
```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ***" \
  -d '{"name":"John","email":"john@example.com"}'
```

**Output:** Postman Collection v2.1 JSON ready to import.

## Notes

- If no `Content-Type` is set but a body is present, defaults to `application/json`
- URL query parameters are automatically parsed into the `query` array
- Output is pretty-printed and can be pasted directly into Postman's Import dialog