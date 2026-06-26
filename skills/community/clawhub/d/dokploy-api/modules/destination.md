# destination module

This module contains `6` endpoints in the `destination` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/destination.all` | `destination-all` | `apiKey` | `none` | - | - |
| POST | `/destination.create` | `destination-create` | `apiKey` | `json` | body.name, body.provider, body.accessKey, body.bucket, body.region, body.endpoint, body.secretAccessKey | - |
| GET | `/destination.one` | `destination-one` | `apiKey` | `params` | query.destinationId | - |
| POST | `/destination.remove` | `destination-remove` | `apiKey` | `json` | body.destinationId | - |
| POST | `/destination.testConnection` | `destination-testConnection` | `apiKey` | `json` | body.name, body.provider, body.accessKey, body.bucket, body.region, body.endpoint, body.secretAccessKey | - |
| POST | `/destination.update` | `destination-update` | `apiKey` | `json` | body.name, body.accessKey, body.bucket, body.region, body.endpoint, body.secretAccessKey, body.destinationId, body.provider | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `destination-all`

- Method: `GET`
- Path: `/destination.all`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `destination-create`

- Method: `POST`
- Path: `/destination.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.provider` | `required` | `string | null` | - |
| `body.accessKey` | `required` | `string` | - |
| `body.bucket` | `required` | `string` | - |
| `body.region` | `required` | `string` | - |
| `body.endpoint` | `required` | `string` | - |
| `body.secretAccessKey` | `required` | `string` | - |
| `body.serverId` | `optional` | `string` | - |

### `destination-one`

- Method: `GET`
- Path: `/destination.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `destinationId` | `query` | yes | `string` | minLength=1 |

### `destination-remove`

- Method: `POST`
- Path: `/destination.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.destinationId` | `required` | `string` | - |

### `destination-testConnection`

- Method: `POST`
- Path: `/destination.testConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.provider` | `required` | `string | null` | - |
| `body.accessKey` | `required` | `string` | - |
| `body.bucket` | `required` | `string` | - |
| `body.region` | `required` | `string` | - |
| `body.endpoint` | `required` | `string` | - |
| `body.secretAccessKey` | `required` | `string` | - |
| `body.serverId` | `optional` | `string` | - |

### `destination-update`

- Method: `POST`
- Path: `/destination.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.accessKey` | `required` | `string` | - |
| `body.bucket` | `required` | `string` | - |
| `body.region` | `required` | `string` | - |
| `body.endpoint` | `required` | `string` | - |
| `body.secretAccessKey` | `required` | `string` | - |
| `body.destinationId` | `required` | `string` | - |
| `body.provider` | `required` | `string | null` | - |
| `body.serverId` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
