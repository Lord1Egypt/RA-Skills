# postgres module

This module contains `14` endpoints in the `postgres` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/postgres.changeStatus` | `postgres-changeStatus` | `apiKey` | `json` | body.postgresId, body.applicationStatus | - |
| POST | `/postgres.create` | `postgres-create` | `apiKey` | `json` | body.name, body.databaseName, body.databaseUser, body.databasePassword, body.environmentId | - |
| POST | `/postgres.deploy` | `postgres-deploy` | `apiKey` | `json` | body.postgresId | - |
| POST | `/postgres.move` | `postgres-move` | `apiKey` | `json` | body.postgresId, body.targetEnvironmentId | - |
| GET | `/postgres.one` | `postgres-one` | `apiKey` | `params` | query.postgresId | - |
| POST | `/postgres.rebuild` | `postgres-rebuild` | `apiKey` | `json` | body.postgresId | - |
| POST | `/postgres.reload` | `postgres-reload` | `apiKey` | `json` | body.postgresId, body.appName | - |
| POST | `/postgres.remove` | `postgres-remove` | `apiKey` | `json` | body.postgresId | - |
| POST | `/postgres.saveEnvironment` | `postgres-saveEnvironment` | `apiKey` | `json` | body.postgresId, body.env | - |
| POST | `/postgres.saveExternalPort` | `postgres-saveExternalPort` | `apiKey` | `json` | body.postgresId, body.externalPort | - |
| GET | `/postgres.search` | `postgres-search` | `apiKey` | `params` | - | - |
| POST | `/postgres.start` | `postgres-start` | `apiKey` | `json` | body.postgresId | - |
| POST | `/postgres.stop` | `postgres-stop` | `apiKey` | `json` | body.postgresId | - |
| POST | `/postgres.update` | `postgres-update` | `apiKey` | `json` | body.postgresId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `postgres-changeStatus`

- Method: `POST`
- Path: `/postgres.changeStatus`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.postgresId` | `required` | `string` | - |
| `body.applicationStatus` | `required` | `enum(idle, running, done, error)` | - |

### `postgres-create`

- Method: `POST`
- Path: `/postgres.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.databaseName` | `required` | `string` | minLength=1 |
| `body.databaseUser` | `required` | `string` | minLength=1 |
| `body.databasePassword` | `required` | `string` | pattern=^[a-zA-Z0-9@#%^&*()_+\-=[\]{}\|;:,.<>?~`]*$ |
| `body.dockerImage` | `optional` | `string` | default=postgres:18 |
| `body.environmentId` | `required` | `string` | - |
| `body.description` | `optional` | `string | null` | - |
| `body.serverId` | `optional` | `string | null` | - |

### `postgres-deploy`

- Method: `POST`
- Path: `/postgres.deploy`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.postgresId` | `required` | `string` | - |

### `postgres-move`

- Method: `POST`
- Path: `/postgres.move`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.postgresId` | `required` | `string` | - |
| `body.targetEnvironmentId` | `required` | `string` | - |

### `postgres-one`

- Method: `GET`
- Path: `/postgres.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `postgresId` | `query` | yes | `string` | minLength=1 |

### `postgres-rebuild`

- Method: `POST`
- Path: `/postgres.rebuild`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.postgresId` | `required` | `string` | - |

### `postgres-reload`

- Method: `POST`
- Path: `/postgres.reload`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.postgresId` | `required` | `string` | - |
| `body.appName` | `required` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |

### `postgres-remove`

- Method: `POST`
- Path: `/postgres.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.postgresId` | `required` | `string` | minLength=1 |

### `postgres-saveEnvironment`

- Method: `POST`
- Path: `/postgres.saveEnvironment`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.postgresId` | `required` | `string` | - |
| `body.env` | `required` | `string | null` | - |

### `postgres-saveExternalPort`

- Method: `POST`
- Path: `/postgres.saveExternalPort`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.postgresId` | `required` | `string` | - |
| `body.externalPort` | `required` | `number | null` | - |

### `postgres-search`

- Method: `GET`
- Path: `/postgres.search`
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

### `postgres-start`

- Method: `POST`
- Path: `/postgres.start`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.postgresId` | `required` | `string` | minLength=1 |

### `postgres-stop`

- Method: `POST`
- Path: `/postgres.stop`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.postgresId` | `required` | `string` | minLength=1 |

### `postgres-update`

- Method: `POST`
- Path: `/postgres.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.postgresId` | `required` | `string` | minLength=1 |
| `body.name` | `optional` | `string` | minLength=1 |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.databaseName` | `optional` | `string` | minLength=1 |
| `body.databaseUser` | `optional` | `string` | minLength=1 |
| `body.databasePassword` | `optional` | `string` | pattern=^[a-zA-Z0-9@#%^&*()_+\-=[\]{}\|;:,.<>?~`]*$ |
| `body.description` | `optional` | `string | null` | - |
| `body.dockerImage` | `optional` | `string` | default=postgres:18 |
| `body.command` | `optional` | `string | null` | - |
| `body.args` | `optional` | `array<string> | null` | - |
| `body.env` | `optional` | `string | null` | - |
| `body.memoryReservation` | `optional` | `string | null` | - |
| `body.externalPort` | `optional` | `number | null` | - |
| `body.memoryLimit` | `optional` | `string | null` | - |
| `body.cpuReservation` | `optional` | `string | null` | - |
| `body.cpuLimit` | `optional` | `string | null` | - |
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
