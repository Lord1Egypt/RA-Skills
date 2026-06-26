# mysql module

This module contains `14` endpoints in the `mysql` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/mysql.changeStatus` | `mysql-changeStatus` | `apiKey` | `json` | body.mysqlId, body.applicationStatus | - |
| POST | `/mysql.create` | `mysql-create` | `apiKey` | `json` | body.name, body.environmentId, body.databaseName, body.databaseUser, body.databasePassword | - |
| POST | `/mysql.deploy` | `mysql-deploy` | `apiKey` | `json` | body.mysqlId | - |
| POST | `/mysql.move` | `mysql-move` | `apiKey` | `json` | body.mysqlId, body.targetEnvironmentId | - |
| GET | `/mysql.one` | `mysql-one` | `apiKey` | `params` | query.mysqlId | - |
| POST | `/mysql.rebuild` | `mysql-rebuild` | `apiKey` | `json` | body.mysqlId | - |
| POST | `/mysql.reload` | `mysql-reload` | `apiKey` | `json` | body.mysqlId, body.appName | - |
| POST | `/mysql.remove` | `mysql-remove` | `apiKey` | `json` | body.mysqlId | - |
| POST | `/mysql.saveEnvironment` | `mysql-saveEnvironment` | `apiKey` | `json` | body.mysqlId, body.env | - |
| POST | `/mysql.saveExternalPort` | `mysql-saveExternalPort` | `apiKey` | `json` | body.mysqlId, body.externalPort | - |
| GET | `/mysql.search` | `mysql-search` | `apiKey` | `params` | - | - |
| POST | `/mysql.start` | `mysql-start` | `apiKey` | `json` | body.mysqlId | - |
| POST | `/mysql.stop` | `mysql-stop` | `apiKey` | `json` | body.mysqlId | - |
| POST | `/mysql.update` | `mysql-update` | `apiKey` | `json` | body.mysqlId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `mysql-changeStatus`

- Method: `POST`
- Path: `/mysql.changeStatus`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mysqlId` | `required` | `string` | - |
| `body.applicationStatus` | `required` | `enum(idle, running, done, error)` | - |

### `mysql-create`

- Method: `POST`
- Path: `/mysql.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.dockerImage` | `optional` | `string` | default=mysql:8 |
| `body.environmentId` | `required` | `string` | - |
| `body.description` | `optional` | `string | null` | - |
| `body.databaseName` | `required` | `string` | minLength=1 |
| `body.databaseUser` | `required` | `string` | minLength=1 |
| `body.databasePassword` | `required` | `string` | pattern=^[a-zA-Z0-9@#%^&*()_+\-=[\]{}\|;:,.<>?~`]*$ |
| `body.databaseRootPassword` | `optional` | `string` | pattern=^[a-zA-Z0-9@#%^&*()_+\-=[\]{}\|;:,.<>?~`]*$ |
| `body.serverId` | `optional` | `string | null` | - |

### `mysql-deploy`

- Method: `POST`
- Path: `/mysql.deploy`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mysqlId` | `required` | `string` | - |

### `mysql-move`

- Method: `POST`
- Path: `/mysql.move`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mysqlId` | `required` | `string` | - |
| `body.targetEnvironmentId` | `required` | `string` | - |

### `mysql-one`

- Method: `GET`
- Path: `/mysql.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `mysqlId` | `query` | yes | `string` | minLength=1 |

### `mysql-rebuild`

- Method: `POST`
- Path: `/mysql.rebuild`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mysqlId` | `required` | `string` | - |

### `mysql-reload`

- Method: `POST`
- Path: `/mysql.reload`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mysqlId` | `required` | `string` | - |
| `body.appName` | `required` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |

### `mysql-remove`

- Method: `POST`
- Path: `/mysql.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mysqlId` | `required` | `string` | minLength=1 |

### `mysql-saveEnvironment`

- Method: `POST`
- Path: `/mysql.saveEnvironment`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mysqlId` | `required` | `string` | - |
| `body.env` | `required` | `string | null` | - |

### `mysql-saveExternalPort`

- Method: `POST`
- Path: `/mysql.saveExternalPort`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mysqlId` | `required` | `string` | - |
| `body.externalPort` | `required` | `number | null` | - |

### `mysql-search`

- Method: `GET`
- Path: `/mysql.search`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `q` | `query` | no | `string` | - |
| `name` | `query` | no | `string` | - |
| `appName` | `query` | no | `string` | - |
| `description` | `query` | no | `string` | - |
| `projectId` | `query` | no | `string` | - |
| `environmentId` | `query` | no | `string` | - |
| `limit` | `query` | no | `number` | minimum=1; maximum=100; default=20 |
| `offset` | `query` | no | `number` | minimum=0; default=0 |

### `mysql-start`

- Method: `POST`
- Path: `/mysql.start`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mysqlId` | `required` | `string` | minLength=1 |

### `mysql-stop`

- Method: `POST`
- Path: `/mysql.stop`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mysqlId` | `required` | `string` | minLength=1 |

### `mysql-update`

- Method: `POST`
- Path: `/mysql.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mysqlId` | `required` | `string` | minLength=1 |
| `body.name` | `optional` | `string` | minLength=1 |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.description` | `optional` | `string | null` | - |
| `body.databaseName` | `optional` | `string` | minLength=1 |
| `body.databaseUser` | `optional` | `string` | minLength=1 |
| `body.databasePassword` | `optional` | `string` | pattern=^[a-zA-Z0-9@#%^&*()_+\-=[\]{}\|;:,.<>?~`]*$ |
| `body.databaseRootPassword` | `optional` | `string` | pattern=^[a-zA-Z0-9@#%^&*()_+\-=[\]{}\|;:,.<>?~`]*$ |
| `body.dockerImage` | `optional` | `string` | default=mysql:8 |
| `body.command` | `optional` | `string | null` | - |
| `body.args` | `optional` | `array<string> | null` | - |
| `body.env` | `optional` | `string | null` | - |
| `body.memoryReservation` | `optional` | `string | null` | - |
| `body.memoryLimit` | `optional` | `string | null` | - |
| `body.cpuReservation` | `optional` | `string | null` | - |
| `body.cpuLimit` | `optional` | `string | null` | - |
| `body.externalPort` | `optional` | `number | null` | - |
| `body.applicationStatus` | `optional` | `enum(idle, running, done, error)` | - |
| `body.healthCheckSwarm` | `optional` | `object | null | null` | - |
| `body.restartPolicySwarm` | `optional` | `object | null | null` | - |
| `body.placementSwarm` | `optional` | `object | null | null` | - |
| `body.updateConfigSwarm` | `optional` | `object | null | null` | - |
| `body.rollbackConfigSwarm` | `optional` | `object | null | null` | - |
| `body.modeSwarm` | `optional` | `object | null | null` | - |
| `body.labelsSwarm` | `optional` | `object | null | null` | - |
| `body.networkSwarm` | `optional` | `array<object> | null | null` | - |
| `body.stopGracePeriodSwarm` | `optional` | `integer | null | null` | - |
| `body.endpointSpecSwarm` | `optional` | `object | null | null` | - |
| `body.ulimitsSwarm` | `optional` | `array<object> | null | null` | - |
| `body.replicas` | `optional` | `number` | - |
| `body.createdAt` | `optional` | `string` | - |
| `body.environmentId` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
