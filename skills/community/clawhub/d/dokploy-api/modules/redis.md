# redis module

This module contains `14` endpoints in the `redis` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/redis.changeStatus` | `redis-changeStatus` | `apiKey` | `json` | body.redisId, body.applicationStatus | - |
| POST | `/redis.create` | `redis-create` | `apiKey` | `json` | body.name, body.databasePassword, body.environmentId | - |
| POST | `/redis.deploy` | `redis-deploy` | `apiKey` | `json` | body.redisId | - |
| POST | `/redis.move` | `redis-move` | `apiKey` | `json` | body.redisId, body.targetEnvironmentId | - |
| GET | `/redis.one` | `redis-one` | `apiKey` | `params` | query.redisId | - |
| POST | `/redis.rebuild` | `redis-rebuild` | `apiKey` | `json` | body.redisId | - |
| POST | `/redis.reload` | `redis-reload` | `apiKey` | `json` | body.redisId, body.appName | - |
| POST | `/redis.remove` | `redis-remove` | `apiKey` | `json` | body.redisId | - |
| POST | `/redis.saveEnvironment` | `redis-saveEnvironment` | `apiKey` | `json` | body.redisId, body.env | - |
| POST | `/redis.saveExternalPort` | `redis-saveExternalPort` | `apiKey` | `json` | body.redisId, body.externalPort | - |
| GET | `/redis.search` | `redis-search` | `apiKey` | `params` | - | - |
| POST | `/redis.start` | `redis-start` | `apiKey` | `json` | body.redisId | - |
| POST | `/redis.stop` | `redis-stop` | `apiKey` | `json` | body.redisId | - |
| POST | `/redis.update` | `redis-update` | `apiKey` | `json` | body.redisId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `redis-changeStatus`

- Method: `POST`
- Path: `/redis.changeStatus`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.redisId` | `required` | `string` | - |
| `body.applicationStatus` | `required` | `enum(idle, running, done, error)` | - |

### `redis-create`

- Method: `POST`
- Path: `/redis.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.databasePassword` | `required` | `string` | - |
| `body.dockerImage` | `optional` | `string` | default=redis:8 |
| `body.environmentId` | `required` | `string` | - |
| `body.description` | `optional` | `string | null` | - |
| `body.serverId` | `optional` | `string | null` | - |

### `redis-deploy`

- Method: `POST`
- Path: `/redis.deploy`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.redisId` | `required` | `string` | - |

### `redis-move`

- Method: `POST`
- Path: `/redis.move`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.redisId` | `required` | `string` | - |
| `body.targetEnvironmentId` | `required` | `string` | - |

### `redis-one`

- Method: `GET`
- Path: `/redis.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `redisId` | `query` | yes | `string` | minLength=1 |

### `redis-rebuild`

- Method: `POST`
- Path: `/redis.rebuild`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.redisId` | `required` | `string` | - |

### `redis-reload`

- Method: `POST`
- Path: `/redis.reload`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.redisId` | `required` | `string` | - |
| `body.appName` | `required` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |

### `redis-remove`

- Method: `POST`
- Path: `/redis.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.redisId` | `required` | `string` | minLength=1 |

### `redis-saveEnvironment`

- Method: `POST`
- Path: `/redis.saveEnvironment`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.redisId` | `required` | `string` | - |
| `body.env` | `required` | `string | null` | - |

### `redis-saveExternalPort`

- Method: `POST`
- Path: `/redis.saveExternalPort`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.redisId` | `required` | `string` | - |
| `body.externalPort` | `required` | `number | null` | - |

### `redis-search`

- Method: `GET`
- Path: `/redis.search`
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

### `redis-start`

- Method: `POST`
- Path: `/redis.start`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.redisId` | `required` | `string` | minLength=1 |

### `redis-stop`

- Method: `POST`
- Path: `/redis.stop`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.redisId` | `required` | `string` | minLength=1 |

### `redis-update`

- Method: `POST`
- Path: `/redis.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.redisId` | `required` | `string` | minLength=1 |
| `body.name` | `optional` | `string` | minLength=1 |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.description` | `optional` | `string | null` | - |
| `body.databasePassword` | `optional` | `string` | - |
| `body.dockerImage` | `optional` | `string` | default=redis:8 |
| `body.command` | `optional` | `string | null` | - |
| `body.args` | `optional` | `array<string> | null` | - |
| `body.env` | `optional` | `string | null` | - |
| `body.memoryReservation` | `optional` | `string | null` | - |
| `body.memoryLimit` | `optional` | `string | null` | - |
| `body.cpuReservation` | `optional` | `string | null` | - |
| `body.cpuLimit` | `optional` | `string | null` | - |
| `body.externalPort` | `optional` | `number | null` | - |
| `body.createdAt` | `optional` | `string` | - |
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
| `body.environmentId` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
