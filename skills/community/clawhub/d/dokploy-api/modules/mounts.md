# mounts module

This module contains `6` endpoints in the `mounts` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/mounts.allNamedByApplicationId` | `mounts-allNamedByApplicationId` | `apiKey` | `params` | query.applicationId | - |
| POST | `/mounts.create` | `mounts-create` | `apiKey` | `json` | body.type, body.mountPath, body.serviceId | - |
| GET | `/mounts.listByServiceId` | `mounts-listByServiceId` | `apiKey` | `params` | query.serviceId, query.serviceType | - |
| GET | `/mounts.one` | `mounts-one` | `apiKey` | `params` | query.mountId | - |
| POST | `/mounts.remove` | `mounts-remove` | `apiKey` | `json` | body.mountId | - |
| POST | `/mounts.update` | `mounts-update` | `apiKey` | `json` | body.mountId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `mounts-allNamedByApplicationId`

- Method: `GET`
- Path: `/mounts.allNamedByApplicationId`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `applicationId` | `query` | yes | `string` | minLength=1 |

### `mounts-create`

- Method: `POST`
- Path: `/mounts.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.type` | `required` | `enum(bind, volume, file)` | - |
| `body.hostPath` | `optional` | `string | null` | - |
| `body.volumeName` | `optional` | `string | null` | - |
| `body.content` | `optional` | `string | null` | - |
| `body.mountPath` | `required` | `string` | minLength=1 |
| `body.serviceType` | `optional` | `enum(application, postgres, mysql, mariadb, mongo, redis, ...)` | - |
| `body.filePath` | `optional` | `string | null` | - |
| `body.serviceId` | `required` | `string` | minLength=1 |

### `mounts-listByServiceId`

- Method: `GET`
- Path: `/mounts.listByServiceId`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serviceId` | `query` | yes | `string` | minLength=1 |
| `serviceType` | `query` | yes | `enum(application, postgres, mysql, mariadb, mongo, redis, ...)` | - |

### `mounts-one`

- Method: `GET`
- Path: `/mounts.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `mountId` | `query` | yes | `string` | minLength=1 |

### `mounts-remove`

- Method: `POST`
- Path: `/mounts.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mountId` | `required` | `string` | - |

### `mounts-update`

- Method: `POST`
- Path: `/mounts.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mountId` | `required` | `string` | minLength=1 |
| `body.type` | `optional` | `enum(bind, volume, file)` | - |
| `body.hostPath` | `optional` | `string | null` | - |
| `body.volumeName` | `optional` | `string | null` | - |
| `body.filePath` | `optional` | `string | null` | - |
| `body.content` | `optional` | `string | null` | - |
| `body.serviceType` | `optional` | `enum(application, postgres, mysql, mariadb, mongo, redis, ...)` | - |
| `body.mountPath` | `optional` | `string` | minLength=1 |
| `body.applicationId` | `optional` | `string | null` | - |
| `body.postgresId` | `optional` | `string | null` | - |
| `body.mariadbId` | `optional` | `string | null` | - |
| `body.mongoId` | `optional` | `string | null` | - |
| `body.mysqlId` | `optional` | `string | null` | - |
| `body.redisId` | `optional` | `string | null` | - |
| `body.composeId` | `optional` | `string | null` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
