# redirects module

This module contains `4` endpoints in the `redirects` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/redirects.create` | `redirects-create` | `apiKey` | `json` | body.regex, body.replacement, body.permanent, body.applicationId | - |
| POST | `/redirects.delete` | `redirects-delete` | `apiKey` | `json` | body.redirectId | - |
| GET | `/redirects.one` | `redirects-one` | `apiKey` | `params` | query.redirectId | - |
| POST | `/redirects.update` | `redirects-update` | `apiKey` | `json` | body.redirectId, body.regex, body.replacement, body.permanent | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `redirects-create`

- Method: `POST`
- Path: `/redirects.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.regex` | `required` | `string` | minLength=1 |
| `body.replacement` | `required` | `string` | minLength=1 |
| `body.permanent` | `required` | `boolean` | - |
| `body.applicationId` | `required` | `string` | - |

### `redirects-delete`

- Method: `POST`
- Path: `/redirects.delete`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.redirectId` | `required` | `string` | minLength=1 |

### `redirects-one`

- Method: `GET`
- Path: `/redirects.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `redirectId` | `query` | yes | `string` | minLength=1 |

### `redirects-update`

- Method: `POST`
- Path: `/redirects.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.redirectId` | `required` | `string` | minLength=1 |
| `body.regex` | `required` | `string` | minLength=1 |
| `body.replacement` | `required` | `string` | minLength=1 |
| `body.permanent` | `required` | `boolean` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
