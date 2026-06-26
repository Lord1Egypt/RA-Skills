# environment module

This module contains `7` endpoints in the `environment` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/environment.byProjectId` | `environment-byProjectId` | `apiKey` | `params` | query.projectId | - |
| POST | `/environment.create` | `environment-create` | `apiKey` | `json` | body.name, body.projectId | - |
| POST | `/environment.duplicate` | `environment-duplicate` | `apiKey` | `json` | body.environmentId, body.name | - |
| GET | `/environment.one` | `environment-one` | `apiKey` | `params` | query.environmentId | - |
| POST | `/environment.remove` | `environment-remove` | `apiKey` | `json` | body.environmentId | - |
| GET | `/environment.search` | `environment-search` | `apiKey` | `params` | - | - |
| POST | `/environment.update` | `environment-update` | `apiKey` | `json` | body.environmentId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `environment-byProjectId`

- Method: `GET`
- Path: `/environment.byProjectId`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `projectId` | `query` | yes | `string` | - |

### `environment-create`

- Method: `POST`
- Path: `/environment.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.description` | `optional` | `string` | - |
| `body.projectId` | `required` | `string` | minLength=1 |

### `environment-duplicate`

- Method: `POST`
- Path: `/environment.duplicate`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.environmentId` | `required` | `string` | minLength=1 |
| `body.name` | `required` | `string` | minLength=1 |
| `body.description` | `optional` | `string` | - |

### `environment-one`

- Method: `GET`
- Path: `/environment.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `environmentId` | `query` | yes | `string` | minLength=1 |

### `environment-remove`

- Method: `POST`
- Path: `/environment.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.environmentId` | `required` | `string` | minLength=1 |

### `environment-search`

- Method: `GET`
- Path: `/environment.search`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `q` | `query` | no | `string` | - |
| `name` | `query` | no | `string` | - |
| `description` | `query` | no | `string` | - |
| `projectId` | `query` | no | `string` | - |
| `limit` | `query` | no | `number` | minimum=1; maximum=100; default=20 |
| `offset` | `query` | no | `number` | minimum=0; default=0 |

### `environment-update`

- Method: `POST`
- Path: `/environment.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.environmentId` | `required` | `string` | minLength=1 |
| `body.name` | `optional` | `string` | minLength=1 |
| `body.description` | `optional` | `string` | - |
| `body.projectId` | `optional` | `string` | - |
| `body.env` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
