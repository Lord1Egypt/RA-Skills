# server module

This module contains `16` endpoints in the `server` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/server.all` | `server-all` | `apiKey` | `none` | - | - |
| GET | `/server.buildServers` | `server-buildServers` | `apiKey` | `none` | - | - |
| GET | `/server.count` | `server-count` | `apiKey` | `none` | - | - |
| POST | `/server.create` | `server-create` | `apiKey` | `json` | body.name, body.description, body.ipAddress, body.port, body.username, body.sshKeyId, body.serverType | - |
| GET | `/server.getDefaultCommand` | `server-getDefaultCommand` | `apiKey` | `params` | query.serverId | - |
| GET | `/server.getServerMetrics` | `server-getServerMetrics` | `apiKey` | `params` | query.url, query.token, query.dataPoints | - |
| GET | `/server.getServerTime` | `server-getServerTime` | `apiKey` | `none` | - | - |
| GET | `/server.one` | `server-one` | `apiKey` | `params` | query.serverId | - |
| GET | `/server.publicIp` | `server-publicIp` | `apiKey` | `none` | - | - |
| POST | `/server.remove` | `server-remove` | `apiKey` | `json` | body.serverId | - |
| GET | `/server.security` | `server-security` | `apiKey` | `params` | query.serverId | - |
| POST | `/server.setup` | `server-setup` | `apiKey` | `json` | body.serverId | - |
| POST | `/server.setupMonitoring` | `server-setupMonitoring` | `apiKey` | `json` | body.serverId, body.metricsConfig | - |
| POST | `/server.update` | `server-update` | `apiKey` | `json` | body.name, body.description, body.serverId, body.ipAddress, body.port, body.username, body.sshKeyId, body.serverType | - |
| GET | `/server.validate` | `server-validate` | `apiKey` | `params` | query.serverId | - |
| GET | `/server.withSSHKey` | `server-withSSHKey` | `apiKey` | `none` | - | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `server-all`

- Method: `GET`
- Path: `/server.all`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `server-buildServers`

- Method: `GET`
- Path: `/server.buildServers`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `server-count`

- Method: `GET`
- Path: `/server.count`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `server-create`

- Method: `POST`
- Path: `/server.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.description` | `required` | `string | null` | - |
| `body.ipAddress` | `required` | `string` | - |
| `body.port` | `required` | `number` | - |
| `body.username` | `required` | `string` | - |
| `body.sshKeyId` | `required` | `string | null` | - |
| `body.serverType` | `required` | `enum(deploy, build)` | - |

### `server-getDefaultCommand`

- Method: `GET`
- Path: `/server.getDefaultCommand`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | yes | `string` | minLength=1 |

### `server-getServerMetrics`

- Method: `GET`
- Path: `/server.getServerMetrics`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `url` | `query` | yes | `string` | - |
| `token` | `query` | yes | `string` | - |
| `dataPoints` | `query` | yes | `string` | - |

### `server-getServerTime`

- Method: `GET`
- Path: `/server.getServerTime`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `server-one`

- Method: `GET`
- Path: `/server.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | yes | `string` | minLength=1 |

### `server-publicIp`

- Method: `GET`
- Path: `/server.publicIp`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `server-remove`

- Method: `POST`
- Path: `/server.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverId` | `required` | `string` | minLength=1 |

### `server-security`

- Method: `GET`
- Path: `/server.security`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | yes | `string` | minLength=1 |

### `server-setup`

- Method: `POST`
- Path: `/server.setup`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverId` | `required` | `string` | minLength=1 |

### `server-setupMonitoring`

- Method: `POST`
- Path: `/server.setupMonitoring`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverId` | `required` | `string` | minLength=1 |
| `body.metricsConfig` | `required` | `object` | - |
| `body.metricsConfig.server` | `required` | `object` | - |
| `body.metricsConfig.server.refreshRate` | `required` | `number` | minimum=2 |
| `body.metricsConfig.server.port` | `required` | `number` | minimum=1 |
| `body.metricsConfig.server.token` | `required` | `string` | - |
| `body.metricsConfig.server.urlCallback` | `required` | `string` | format=uri |
| `body.metricsConfig.server.retentionDays` | `required` | `number` | minimum=1 |
| `body.metricsConfig.server.cronJob` | `required` | `string` | minLength=1 |
| `body.metricsConfig.server.thresholds` | `required` | `object` | - |
| `body.metricsConfig.server.thresholds.cpu` | `required` | `number` | minimum=0 |
| `body.metricsConfig.server.thresholds.memory` | `required` | `number` | minimum=0 |
| `body.metricsConfig.containers` | `required` | `object` | - |
| `body.metricsConfig.containers.refreshRate` | `required` | `number` | minimum=2 |
| `body.metricsConfig.containers.services` | `required` | `object` | - |
| `body.metricsConfig.containers.services.include` | `optional` | `array<string>` | - |
| `body.metricsConfig.containers.services.include[]` | `optional` | `string` | - |
| `body.metricsConfig.containers.services.exclude` | `optional` | `array<string>` | - |
| `body.metricsConfig.containers.services.exclude[]` | `optional` | `string` | - |

### `server-update`

- Method: `POST`
- Path: `/server.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.description` | `required` | `string | null` | - |
| `body.serverId` | `required` | `string` | minLength=1 |
| `body.ipAddress` | `required` | `string` | - |
| `body.port` | `required` | `number` | - |
| `body.username` | `required` | `string` | - |
| `body.sshKeyId` | `required` | `string | null` | - |
| `body.serverType` | `required` | `enum(deploy, build)` | - |
| `body.command` | `optional` | `string` | - |

### `server-validate`

- Method: `GET`
- Path: `/server.validate`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | yes | `string` | minLength=1 |

### `server-withSSHKey`

- Method: `GET`
- Path: `/server.withSSHKey`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
