# registry module

This module contains `7` endpoints in the `registry` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/registry.all` | `registry-all` | `apiKey` | `none` | - | - |
| POST | `/registry.create` | `registry-create` | `apiKey` | `json` | body.registryName, body.username, body.password, body.registryUrl, body.registryType, body.imagePrefix | - |
| GET | `/registry.one` | `registry-one` | `apiKey` | `params` | query.registryId | - |
| POST | `/registry.remove` | `registry-remove` | `apiKey` | `json` | body.registryId | - |
| POST | `/registry.testRegistry` | `registry-testRegistry` | `apiKey` | `json` | body.username, body.password, body.registryUrl, body.registryType | - |
| POST | `/registry.testRegistryById` | `registry-testRegistryById` | `apiKey` | `json` | - | - |
| POST | `/registry.update` | `registry-update` | `apiKey` | `json` | body.registryId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `registry-all`

- Method: `GET`
- Path: `/registry.all`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `registry-create`

- Method: `POST`
- Path: `/registry.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.registryName` | `required` | `string` | minLength=1 |
| `body.username` | `required` | `string` | minLength=1 |
| `body.password` | `required` | `string` | minLength=1 |
| `body.registryUrl` | `required` | `string` | - |
| `body.registryType` | `required` | `enum(cloud)` | - |
| `body.imagePrefix` | `required` | `string | null` | - |
| `body.serverId` | `optional` | `string` | - |

### `registry-one`

- Method: `GET`
- Path: `/registry.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `registryId` | `query` | yes | `string` | minLength=1 |

### `registry-remove`

- Method: `POST`
- Path: `/registry.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.registryId` | `required` | `string` | minLength=1 |

### `registry-testRegistry`

- Method: `POST`
- Path: `/registry.testRegistry`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.registryName` | `optional` | `string` | - |
| `body.username` | `required` | `string` | minLength=1 |
| `body.password` | `required` | `string` | minLength=1 |
| `body.registryUrl` | `required` | `string` | - |
| `body.registryType` | `required` | `enum(cloud)` | - |
| `body.imagePrefix` | `optional` | `string | null` | - |
| `body.serverId` | `optional` | `string` | - |

### `registry-testRegistryById`

- Method: `POST`
- Path: `/registry.testRegistryById`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.registryId` | `optional` | `string` | minLength=1 |
| `body.serverId` | `optional` | `string` | - |

### `registry-update`

- Method: `POST`
- Path: `/registry.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.registryId` | `required` | `string` | minLength=1 |
| `body.registryName` | `optional` | `string` | minLength=1 |
| `body.imagePrefix` | `optional` | `string | null | null` | - |
| `body.username` | `optional` | `string` | minLength=1 |
| `body.password` | `optional` | `string` | minLength=1 |
| `body.registryUrl` | `optional` | `string` | - |
| `body.createdAt` | `optional` | `string` | - |
| `body.registryType` | `optional` | `enum(cloud)` | - |
| `body.organizationId` | `optional` | `string` | minLength=1 |
| `body.serverId` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
