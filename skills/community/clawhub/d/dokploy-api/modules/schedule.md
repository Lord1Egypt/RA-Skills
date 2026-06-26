# schedule module

This module contains `6` endpoints in the `schedule` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/schedule.create` | `schedule-create` | `apiKey` | `json` | body.name, body.cronExpression, body.command | - |
| POST | `/schedule.delete` | `schedule-delete` | `apiKey` | `json` | body.scheduleId | - |
| GET | `/schedule.list` | `schedule-list` | `apiKey` | `params` | query.id, query.scheduleType | - |
| GET | `/schedule.one` | `schedule-one` | `apiKey` | `params` | query.scheduleId | - |
| POST | `/schedule.runManually` | `schedule-runManually` | `apiKey` | `json` | body.scheduleId | - |
| POST | `/schedule.update` | `schedule-update` | `apiKey` | `json` | body.scheduleId, body.name, body.cronExpression, body.command | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `schedule-create`

- Method: `POST`
- Path: `/schedule.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.scheduleId` | `optional` | `string` | - |
| `body.name` | `required` | `string` | - |
| `body.cronExpression` | `required` | `string` | - |
| `body.appName` | `optional` | `string` | - |
| `body.serviceName` | `optional` | `string | null` | - |
| `body.shellType` | `optional` | `enum(bash, sh)` | - |
| `body.scheduleType` | `optional` | `enum(application, compose, server, dokploy-server)` | - |
| `body.command` | `required` | `string` | - |
| `body.script` | `optional` | `string | null` | - |
| `body.applicationId` | `optional` | `string | null` | - |
| `body.composeId` | `optional` | `string | null` | - |
| `body.serverId` | `optional` | `string | null` | - |
| `body.userId` | `optional` | `string | null` | - |
| `body.enabled` | `optional` | `boolean` | - |
| `body.timezone` | `optional` | `string | null` | - |
| `body.createdAt` | `optional` | `string` | - |

### `schedule-delete`

- Method: `POST`
- Path: `/schedule.delete`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.scheduleId` | `required` | `string` | - |

### `schedule-list`

- Method: `GET`
- Path: `/schedule.list`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `id` | `query` | yes | `string` | - |
| `scheduleType` | `query` | yes | `enum(application, compose, server, dokploy-server)` | - |

### `schedule-one`

- Method: `GET`
- Path: `/schedule.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `scheduleId` | `query` | yes | `string` | - |

### `schedule-runManually`

- Method: `POST`
- Path: `/schedule.runManually`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.scheduleId` | `required` | `string` | minLength=1 |

### `schedule-update`

- Method: `POST`
- Path: `/schedule.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.scheduleId` | `required` | `string` | minLength=1 |
| `body.name` | `required` | `string` | - |
| `body.cronExpression` | `required` | `string` | - |
| `body.appName` | `optional` | `string` | - |
| `body.serviceName` | `optional` | `string | null` | - |
| `body.shellType` | `optional` | `enum(bash, sh)` | - |
| `body.scheduleType` | `optional` | `enum(application, compose, server, dokploy-server)` | - |
| `body.command` | `required` | `string` | - |
| `body.script` | `optional` | `string | null` | - |
| `body.applicationId` | `optional` | `string | null` | - |
| `body.composeId` | `optional` | `string | null` | - |
| `body.serverId` | `optional` | `string | null` | - |
| `body.userId` | `optional` | `string | null` | - |
| `body.enabled` | `optional` | `boolean` | - |
| `body.timezone` | `optional` | `string | null` | - |
| `body.createdAt` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
