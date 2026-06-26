# volumeBackups module

This module contains `6` endpoints in the `volumeBackups` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/volumeBackups.create` | `volumeBackups-create` | `apiKey` | `json` | body.name, body.volumeName, body.prefix, body.cronExpression, body.destinationId | - |
| POST | `/volumeBackups.delete` | `volumeBackups-delete` | `apiKey` | `json` | body.volumeBackupId | - |
| GET | `/volumeBackups.list` | `volumeBackups-list` | `apiKey` | `params` | query.id, query.volumeBackupType | - |
| GET | `/volumeBackups.one` | `volumeBackups-one` | `apiKey` | `params` | query.volumeBackupId | - |
| POST | `/volumeBackups.runManually` | `volumeBackups-runManually` | `apiKey` | `json` | body.volumeBackupId | - |
| POST | `/volumeBackups.update` | `volumeBackups-update` | `apiKey` | `json` | body.name, body.volumeName, body.prefix, body.cronExpression, body.destinationId, body.volumeBackupId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `volumeBackups-create`

- Method: `POST`
- Path: `/volumeBackups.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | - |
| `body.volumeName` | `required` | `string` | - |
| `body.prefix` | `required` | `string` | - |
| `body.serviceType` | `optional` | `enum(application, postgres, mysql, mariadb, mongo, redis, ...)` | - |
| `body.appName` | `optional` | `string` | - |
| `body.serviceName` | `optional` | `string | null` | - |
| `body.turnOff` | `optional` | `boolean` | - |
| `body.cronExpression` | `required` | `string` | - |
| `body.keepLatestCount` | `optional` | `number | null` | - |
| `body.enabled` | `optional` | `boolean | null` | - |
| `body.applicationId` | `optional` | `string | null` | - |
| `body.postgresId` | `optional` | `string | null` | - |
| `body.mariadbId` | `optional` | `string | null` | - |
| `body.mongoId` | `optional` | `string | null` | - |
| `body.mysqlId` | `optional` | `string | null` | - |
| `body.redisId` | `optional` | `string | null` | - |
| `body.composeId` | `optional` | `string | null` | - |
| `body.createdAt` | `optional` | `string` | - |
| `body.destinationId` | `required` | `string` | - |

### `volumeBackups-delete`

- Method: `POST`
- Path: `/volumeBackups.delete`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.volumeBackupId` | `required` | `string` | minLength=1 |

### `volumeBackups-list`

- Method: `GET`
- Path: `/volumeBackups.list`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `id` | `query` | yes | `string` | minLength=1 |
| `volumeBackupType` | `query` | yes | `enum(application, postgres, mysql, mariadb, mongo, redis, ...)` | - |

### `volumeBackups-one`

- Method: `GET`
- Path: `/volumeBackups.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `volumeBackupId` | `query` | yes | `string` | minLength=1 |

### `volumeBackups-runManually`

- Method: `POST`
- Path: `/volumeBackups.runManually`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.volumeBackupId` | `required` | `string` | minLength=1 |

### `volumeBackups-update`

- Method: `POST`
- Path: `/volumeBackups.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | - |
| `body.volumeName` | `required` | `string` | - |
| `body.prefix` | `required` | `string` | - |
| `body.serviceType` | `optional` | `enum(application, postgres, mysql, mariadb, mongo, redis, ...)` | - |
| `body.appName` | `optional` | `string` | - |
| `body.serviceName` | `optional` | `string | null` | - |
| `body.turnOff` | `optional` | `boolean` | - |
| `body.cronExpression` | `required` | `string` | - |
| `body.keepLatestCount` | `optional` | `number | null` | - |
| `body.enabled` | `optional` | `boolean | null` | - |
| `body.applicationId` | `optional` | `string | null` | - |
| `body.postgresId` | `optional` | `string | null` | - |
| `body.mariadbId` | `optional` | `string | null` | - |
| `body.mongoId` | `optional` | `string | null` | - |
| `body.mysqlId` | `optional` | `string | null` | - |
| `body.redisId` | `optional` | `string | null` | - |
| `body.composeId` | `optional` | `string | null` | - |
| `body.createdAt` | `optional` | `string` | - |
| `body.destinationId` | `required` | `string` | - |
| `body.volumeBackupId` | `required` | `string` | minLength=1 |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
