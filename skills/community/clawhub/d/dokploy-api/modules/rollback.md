# rollback module

This module contains `2` endpoints in the `rollback` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/rollback.delete` | `rollback-delete` | `apiKey` | `json` | body.rollbackId | - |
| POST | `/rollback.rollback` | `rollback-rollback` | `apiKey` | `json` | body.rollbackId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `rollback-delete`

- Method: `POST`
- Path: `/rollback.delete`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.rollbackId` | `required` | `string` | minLength=1 |

### `rollback-rollback`

- Method: `POST`
- Path: `/rollback.rollback`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.rollbackId` | `required` | `string` | minLength=1 |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
