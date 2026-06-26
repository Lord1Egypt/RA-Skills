# gitProvider module

This module contains `2` endpoints in the `gitProvider` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/gitProvider.getAll` | `gitProvider-getAll` | `apiKey` | `none` | - | - |
| POST | `/gitProvider.remove` | `gitProvider-remove` | `apiKey` | `json` | body.gitProviderId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `gitProvider-getAll`

- Method: `GET`
- Path: `/gitProvider.getAll`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `gitProvider-remove`

- Method: `POST`
- Path: `/gitProvider.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.gitProviderId` | `required` | `string` | minLength=1 |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
