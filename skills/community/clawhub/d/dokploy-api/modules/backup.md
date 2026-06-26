# backup module

This module contains `11` endpoints in the `backup` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/backup.create` | `backup-create` | `apiKey` | `json` | body.schedule, body.prefix, body.destinationId, body.database, body.databaseType | - |
| GET | `/backup.listBackupFiles` | `backup-listBackupFiles` | `apiKey` | `params` | query.destinationId, query.search | - |
| POST | `/backup.manualBackupCompose` | `backup-manualBackupCompose` | `apiKey` | `json` | body.backupId | - |
| POST | `/backup.manualBackupMariadb` | `backup-manualBackupMariadb` | `apiKey` | `json` | body.backupId | - |
| POST | `/backup.manualBackupMongo` | `backup-manualBackupMongo` | `apiKey` | `json` | body.backupId | - |
| POST | `/backup.manualBackupMySql` | `backup-manualBackupMySql` | `apiKey` | `json` | body.backupId | - |
| POST | `/backup.manualBackupPostgres` | `backup-manualBackupPostgres` | `apiKey` | `json` | body.backupId | - |
| POST | `/backup.manualBackupWebServer` | `backup-manualBackupWebServer` | `apiKey` | `json` | body.backupId | - |
| GET | `/backup.one` | `backup-one` | `apiKey` | `params` | query.backupId | - |
| POST | `/backup.remove` | `backup-remove` | `apiKey` | `json` | body.backupId | - |
| POST | `/backup.update` | `backup-update` | `apiKey` | `json` | body.schedule, body.enabled, body.prefix, body.backupId, body.destinationId, body.database, body.keepLatestCount, body.serviceName, body.metadata, body.databaseType | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `backup-create`

- Method: `POST`
- Path: `/backup.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.schedule` | `required` | `string` | - |
| `body.enabled` | `optional` | `boolean | null` | - |
| `body.prefix` | `required` | `string` | minLength=1 |
| `body.destinationId` | `required` | `string` | - |
| `body.keepLatestCount` | `optional` | `number | null` | - |
| `body.database` | `required` | `string` | minLength=1 |
| `body.mariadbId` | `optional` | `string | null` | - |
| `body.mysqlId` | `optional` | `string | null` | - |
| `body.postgresId` | `optional` | `string | null` | - |
| `body.mongoId` | `optional` | `string | null` | - |
| `body.databaseType` | `required` | `enum(postgres, mariadb, mysql, mongo, web-server)` | - |
| `body.userId` | `optional` | `string | null` | - |
| `body.backupType` | `optional` | `enum(database, compose)` | - |
| `body.composeId` | `optional` | `string | null` | - |
| `body.serviceName` | `optional` | `string | null` | - |
| `body.metadata` | `optional` | `any | null` | - |

### `backup-listBackupFiles`

- Method: `GET`
- Path: `/backup.listBackupFiles`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `destinationId` | `query` | yes | `string` | - |
| `search` | `query` | yes | `string` | - |
| `serverId` | `query` | no | `string` | - |

### `backup-manualBackupCompose`

- Method: `POST`
- Path: `/backup.manualBackupCompose`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.backupId` | `required` | `string` | minLength=1 |

### `backup-manualBackupMariadb`

- Method: `POST`
- Path: `/backup.manualBackupMariadb`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.backupId` | `required` | `string` | minLength=1 |

### `backup-manualBackupMongo`

- Method: `POST`
- Path: `/backup.manualBackupMongo`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.backupId` | `required` | `string` | minLength=1 |

### `backup-manualBackupMySql`

- Method: `POST`
- Path: `/backup.manualBackupMySql`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.backupId` | `required` | `string` | minLength=1 |

### `backup-manualBackupPostgres`

- Method: `POST`
- Path: `/backup.manualBackupPostgres`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.backupId` | `required` | `string` | minLength=1 |

### `backup-manualBackupWebServer`

- Method: `POST`
- Path: `/backup.manualBackupWebServer`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.backupId` | `required` | `string` | minLength=1 |

### `backup-one`

- Method: `GET`
- Path: `/backup.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `backupId` | `query` | yes | `string` | minLength=1 |

### `backup-remove`

- Method: `POST`
- Path: `/backup.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.backupId` | `required` | `string` | - |

### `backup-update`

- Method: `POST`
- Path: `/backup.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.schedule` | `required` | `string` | - |
| `body.enabled` | `required` | `boolean | null` | - |
| `body.prefix` | `required` | `string` | minLength=1 |
| `body.backupId` | `required` | `string` | - |
| `body.destinationId` | `required` | `string` | - |
| `body.database` | `required` | `string` | minLength=1 |
| `body.keepLatestCount` | `required` | `number | null` | - |
| `body.serviceName` | `required` | `string | null` | - |
| `body.metadata` | `required` | `any | null` | - |
| `body.databaseType` | `required` | `enum(postgres, mariadb, mysql, mongo, web-server)` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
