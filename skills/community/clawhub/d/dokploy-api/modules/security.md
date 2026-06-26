# security module

This module contains `4` endpoints in the `security` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/security.create` | `security-create` | `apiKey` | `json` | body.applicationId, body.username, body.password | - |
| POST | `/security.delete` | `security-delete` | `apiKey` | `json` | body.securityId | - |
| GET | `/security.one` | `security-one` | `apiKey` | `params` | query.securityId | - |
| POST | `/security.update` | `security-update` | `apiKey` | `json` | body.securityId, body.username, body.password | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `security-create`

- Method: `POST`
- Path: `/security.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | - |
| `body.username` | `required` | `string` | minLength=1 |
| `body.password` | `required` | `string` | minLength=1 |

### `security-delete`

- Method: `POST`
- Path: `/security.delete`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.securityId` | `required` | `string` | minLength=1 |

### `security-one`

- Method: `GET`
- Path: `/security.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `securityId` | `query` | yes | `string` | minLength=1 |

### `security-update`

- Method: `POST`
- Path: `/security.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.securityId` | `required` | `string` | minLength=1 |
| `body.username` | `required` | `string` | minLength=1 |
| `body.password` | `required` | `string` | minLength=1 |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
