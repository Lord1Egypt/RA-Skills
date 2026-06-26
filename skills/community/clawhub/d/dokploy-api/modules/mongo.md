# mongo module

This module contains `14` endpoints in the `mongo` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/mongo.changeStatus` | `mongo-changeStatus` | `apiKey` | `json` | body.mongoId, body.applicationStatus | - |
| POST | `/mongo.create` | `mongo-create` | `apiKey` | `json` | body.name, body.environmentId, body.databaseUser, body.databasePassword | - |
| POST | `/mongo.deploy` | `mongo-deploy` | `apiKey` | `json` | body.mongoId | - |
| POST | `/mongo.move` | `mongo-move` | `apiKey` | `json` | body.mongoId, body.targetEnvironmentId | - |
| GET | `/mongo.one` | `mongo-one` | `apiKey` | `params` | query.mongoId | - |
| POST | `/mongo.rebuild` | `mongo-rebuild` | `apiKey` | `json` | body.mongoId | - |
| POST | `/mongo.reload` | `mongo-reload` | `apiKey` | `json` | body.mongoId, body.appName | - |
| POST | `/mongo.remove` | `mongo-remove` | `apiKey` | `json` | body.mongoId | - |
| POST | `/mongo.saveEnvironment` | `mongo-saveEnvironment` | `apiKey` | `json` | body.mongoId, body.env | - |
| POST | `/mongo.saveExternalPort` | `mongo-saveExternalPort` | `apiKey` | `json` | body.mongoId, body.externalPort | - |
| GET | `/mongo.search` | `mongo-search` | `apiKey` | `params` | - | - |
| POST | `/mongo.start` | `mongo-start` | `apiKey` | `json` | body.mongoId | - |
| POST | `/mongo.stop` | `mongo-stop` | `apiKey` | `json` | body.mongoId | - |
| POST | `/mongo.update` | `mongo-update` | `apiKey` | `json` | body.mongoId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `mongo-changeStatus`

- Method: `POST`
- Path: `/mongo.changeStatus`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mongoId` | `required` | `string` | - |
| `body.applicationStatus` | `required` | `enum(idle, running, done, error)` | - |

### `mongo-create`

- Method: `POST`
- Path: `/mongo.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.dockerImage` | `optional` | `string` | default=mongo:15 |
| `body.environmentId` | `required` | `string` | - |
| `body.description` | `optional` | `string | null` | - |
| `body.databaseUser` | `required` | `string` | minLength=1 |
| `body.databasePassword` | `required` | `string` | pattern=^[a-zA-Z0-9@#%^&*()_+\-=[\]{}\|;:,.<>?~`]*$ |
| `body.serverId` | `optional` | `string | null` | - |
| `body.replicaSets` | `optional` | `boolean | null` | - |

### `mongo-deploy`

- Method: `POST`
- Path: `/mongo.deploy`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mongoId` | `required` | `string` | - |

### `mongo-move`

- Method: `POST`
- Path: `/mongo.move`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mongoId` | `required` | `string` | - |
| `body.targetEnvironmentId` | `required` | `string` | - |

### `mongo-one`

- Method: `GET`
- Path: `/mongo.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `mongoId` | `query` | yes | `string` | minLength=1 |

### `mongo-rebuild`

- Method: `POST`
- Path: `/mongo.rebuild`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mongoId` | `required` | `string` | - |

### `mongo-reload`

- Method: `POST`
- Path: `/mongo.reload`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mongoId` | `required` | `string` | - |
| `body.appName` | `required` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |

### `mongo-remove`

- Method: `POST`
- Path: `/mongo.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mongoId` | `required` | `string` | minLength=1 |

### `mongo-saveEnvironment`

- Method: `POST`
- Path: `/mongo.saveEnvironment`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mongoId` | `required` | `string` | - |
| `body.env` | `required` | `string | null` | - |

### `mongo-saveExternalPort`

- Method: `POST`
- Path: `/mongo.saveExternalPort`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mongoId` | `required` | `string` | - |
| `body.externalPort` | `required` | `number | null` | - |

### `mongo-search`

- Method: `GET`
- Path: `/mongo.search`
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

### `mongo-start`

- Method: `POST`
- Path: `/mongo.start`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mongoId` | `required` | `string` | minLength=1 |

### `mongo-stop`

- Method: `POST`
- Path: `/mongo.stop`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mongoId` | `required` | `string` | minLength=1 |

### `mongo-update`

- Method: `POST`
- Path: `/mongo.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.mongoId` | `required` | `string` | minLength=1 |
| `body.name` | `optional` | `string` | minLength=1 |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.description` | `optional` | `string | null` | - |
| `body.databaseUser` | `optional` | `string` | minLength=1 |
| `body.databasePassword` | `optional` | `string` | pattern=^[a-zA-Z0-9@#%^&*()_+\-=[\]{}\|;:,.<>?~`]*$ |
| `body.dockerImage` | `optional` | `string` | default=mongo:15 |
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
| `body.replicaSets` | `optional` | `boolean | null` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
