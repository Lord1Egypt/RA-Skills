# Example Patterns

Generate request examples from `Casdoor RESTful API` using placeholders instead of invented tenant values.

## Base URL

- Use `https://<casdoor-host>` as the default base URL placeholder.
- Replace `<casdoor-host>` only when the user provides a real Casdoor deployment URL.

## Parameter Mapping

- Path parameters stay in the URL path.
- Query parameters go in the query string and should only include values the user actually supplied.
- Body parameters should be serialized as JSON unless the Swagger operation states another content type.
- Header values such as bearer tokens should use placeholders like `<access-token>` when not provided.

## curl Pattern

```bash
curl -X GET 'https://<casdoor-host>/<path-or-query>' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer <access-token>'
```

## JavaScript Pattern

```javascript
const response = await fetch('https://<casdoor-host>/<path-or-query>', {
  method: 'GET',
  headers: {
    'Accept': 'application/json',
    'Authorization': 'Bearer <access-token>',
  },
});
```

## Python Pattern

```python
import requests

response = requests.get(
    'https://<casdoor-host>/<path-or-query>',
    headers={
        'Accept': 'application/json',
        'Authorization': 'Bearer <access-token>',
    },
)
```

## Output Rules

- Always explain which parameter values are placeholders.
- When a user asks for JS or Python examples, mirror the same endpoint and parameters as the curl example.
- If authentication requirements are unclear, say what is known from Swagger and what must be confirmed in the user’s Casdoor deployment.
