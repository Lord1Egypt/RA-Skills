# mariadb module

This module contains `14` endpoints in the `mariadb` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/mariadb.changeStatus` | `mariadb-changeStatus` | `apiKey` | `json` | body.mariadbId, body.applicationStatus | - |
| POST | `/mariadb.create` | `mariadb-create` | `apiKey` | `json` | body.name, body.environmentId, body.databaseName, body.databaseUser, body.databasePassword | - |
| POST | `/mariadb.deploy` | `mariadb-deploy` | `apiKey` | `json` | body.mariadbId | - |
| POST | `/mariadb.move` | `mariadb-move` | `apiKey` | `json` | body.mariadbId, body.targetEnvironmentId | - |
| GET | `/mariadb.one` | `mariadb-one` | `apiKey` | `params` | query.mariadbId | - |
| POST | `/mariadb.rebuild` | `mariadb-rebuild` | `apiKey` | `json` | body.mariadbId | - |
| POST | `/mariadb.reload` | `mariadb-reload` | `apiKey` | `json` | body.mariadbId, body.appName | - |
| POST | `/mariadb.remove` | `mariadb-remove` | `apiKey` | `json` | body.mariadbId | - |
| POST | `/mariadb.saveEnvironment` | `mariadb-saveEnvironment` | `apiKey` | `json` | body.mariadbId, body.env | - |
| POST | `/mariadb.saveExternalPort` | `mariadb-saveExternalPort` | `apiKey` | `json` | body.mariadbId, body.externalPort | - |
| GET | `/mariadb.search` | `mariadb-search` | `apiKey` | `params` | - | - |
| POST | `/mariadb.start` | `mariadb-start` | `apiKey` | `json` | body.mariadbId | - |
| POST | `/mariadb.stop` | `mariadb-stop` | `apiKey` | `json` | body.mariadbId | - |
| POST | `/mariadb.update` | `mariadb-update` | `apiKey` | `json` | body.mariadbId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `mariadb-changeStatus`

- Method: `POST`
- Path: `/mariadb.changeStatus`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mariadbId` | `required` | `string` | - |
| `body.applicationStatus` | `required` | `enum(idle, running, done, error)` | - |

### `mariadb-create`

- Method: `POST`
- Path: `/mariadb.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.dockerImage` | `optional` | `string` | default=mariadb:6 |
| `body.databaseRootPassword` | `optional` | `string` | pattern=^[a-zA-Z0-9@#%^&*()_+\-=[\]{}\|;:,.<>?~`]*$ |
| `body.environmentId` | `required` | `string` | - |
| `body.description` | `optional` | `string | null` | - |
| `body.databaseName` | `required` | `string` | minLength=1 |
| `body.databaseUser` | `required` | `string` | minLength=1 |
| `body.databasePassword` | `required` | `string` | pattern=^[a-zA-Z0-9@#%^&*()_+\-=[\]{}\|;:,.<>?~`]*$ |
| `body.serverId` | `optional` | `string | null` | - |

### `mariadb-deploy`

- Method: `POST`
- Path: `/mariadb.deploy`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mariadbId` | `required` | `string` | - |

### `mariadb-move`

- Method: `POST`
- Path: `/mariadb.move`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mariadbId` | `required` | `string` | - |
| `body.targetEnvironmentId` | `required` | `string` | - |

### `mariadb-one`

- Method: `GET`
- Path: `/mariadb.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `mariadbId` | `query` | yes | `string` | minLength=1 |

### `mariadb-rebuild`

- Method: `POST`
- Path: `/mariadb.rebuild`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mariadbId` | `required` | `string` | - |

### `mariadb-reload`

- Method: `POST`
- Path: `/mariadb.reload`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mariadbId` | `required` | `string` | - |
| `body.appName` | `required` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |

### `mariadb-remove`

- Method: `POST`
- Path: `/mariadb.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mariadbId` | `required` | `string` | minLength=1 |

### `mariadb-saveEnvironment`

- Method: `POST`
- Path: `/mariadb.saveEnvironment`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mariadbId` | `required` | `string` | - |
| `body.env` | `required` | `string | null` | - |

### `mariadb-saveExternalPort`

- Method: `POST`
- Path: `/mariadb.saveExternalPort`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mariadbId` | `required` | `string` | - |
| `body.externalPort` | `required` | `number | null` | - |

### `mariadb-search`

- Method: `GET`
- Path: `/mariadb.search`
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

### `mariadb-start`

- Method: `POST`
- Path: `/mariadb.start`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mariadbId` | `required` | `string` | minLength=1 |

### `mariadb-stop`

- Method: `POST`
- Path: `/mariadb.stop`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mariadbId` | `required` | `string` | minLength=1 |

### `mariadb-update`

- Method: `POST`
- Path: `/mariadb.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mariadbId` | `required` | `string` | minLength=1 |
| `body.name` | `optional` | `string` | minLength=1 |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.description` | `optional` | `string | null` | - |
| `body.databaseName` | `optional` | `string` | minLength=1 |
| `body.databaseUser` | `optional` | `string` | minLength=1 |
| `body.databasePassword` | `optional` | `string` | pattern=^[a-zA-Z0-9@#%^&*()_+\-=[\]{}\|;:,.<>?~`]*$ |
| `body.databaseRootPassword` | `optional` | `string` | pattern=^[a-zA-Z0-9@#%^&*()_+\-=[\]{}\|;:,.<>?~`]*$ |
| `body.dockerImage` | `optional` | `string` | default=mariadb:6 |
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
