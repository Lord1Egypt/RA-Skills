# settings module

This module contains `49` endpoints in the `settings` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/settings.assignDomainServer` | `settings-assignDomainServer` | `apiKey` | `json` | body.host, body.certificateType | - |
| GET | `/settings.checkGPUStatus` | `settings-checkGPUStatus` | `apiKey` | `params` | - | - |
| POST | `/settings.cleanAll` | `settings-cleanAll` | `apiKey` | `json` | - | - |
| POST | `/settings.cleanAllDeploymentQueue` | `settings-cleanAllDeploymentQueue` | `apiKey` | `none` | - | - |
| POST | `/settings.cleanDockerBuilder` | `settings-cleanDockerBuilder` | `apiKey` | `json` | - | - |
| POST | `/settings.cleanDockerPrune` | `settings-cleanDockerPrune` | `apiKey` | `json` | - | - |
| POST | `/settings.cleanMonitoring` | `settings-cleanMonitoring` | `apiKey` | `none` | - | - |
| POST | `/settings.cleanRedis` | `settings-cleanRedis` | `apiKey` | `none` | - | - |
| POST | `/settings.cleanSSHPrivateKey` | `settings-cleanSSHPrivateKey` | `apiKey` | `none` | - | - |
| POST | `/settings.cleanStoppedContainers` | `settings-cleanStoppedContainers` | `apiKey` | `json` | - | - |
| POST | `/settings.cleanUnusedImages` | `settings-cleanUnusedImages` | `apiKey` | `json` | - | - |
| POST | `/settings.cleanUnusedVolumes` | `settings-cleanUnusedVolumes` | `apiKey` | `json` | - | - |
| GET | `/settings.getDokployCloudIps` | `settings-getDokployCloudIps` | `apiKey` | `none` | - | - |
| GET | `/settings.getDokployVersion` | `settings-getDokployVersion` | `apiKey` | `none` | - | - |
| GET | `/settings.getIp` | `settings-getIp` | `apiKey` | `none` | - | - |
| GET | `/settings.getLogCleanupStatus` | `settings-getLogCleanupStatus` | `apiKey` | `none` | - | - |
| GET | `/settings.getOpenApiDocument` | `settings-getOpenApiDocument` | `apiKey` | `none` | - | - |
| GET | `/settings.getReleaseTag` | `settings-getReleaseTag` | `apiKey` | `none` | - | - |
| GET | `/settings.getTraefikPorts` | `settings-getTraefikPorts` | `apiKey` | `params` | - | - |
| POST | `/settings.getUpdateData` | `settings-getUpdateData` | `apiKey` | `none` | - | - |
| GET | `/settings.getWebServerSettings` | `settings-getWebServerSettings` | `apiKey` | `none` | - | - |
| GET | `/settings.haveActivateRequests` | `settings-haveActivateRequests` | `apiKey` | `none` | - | - |
| GET | `/settings.haveTraefikDashboardPortEnabled` | `settings-haveTraefikDashboardPortEnabled` | `apiKey` | `params` | - | - |
| GET | `/settings.health` | `settings-health` | `apiKey` | `none` | - | - |
| GET | `/settings.isCloud` | `settings-isCloud` | `apiKey` | `none` | - | - |
| GET | `/settings.isUserSubscribed` | `settings-isUserSubscribed` | `apiKey` | `none` | - | - |
| GET | `/settings.readDirectories` | `settings-readDirectories` | `apiKey` | `params` | - | - |
| GET | `/settings.readMiddlewareTraefikConfig` | `settings-readMiddlewareTraefikConfig` | `apiKey` | `none` | - | - |
| GET | `/settings.readTraefikConfig` | `settings-readTraefikConfig` | `apiKey` | `none` | - | - |
| GET | `/settings.readTraefikEnv` | `settings-readTraefikEnv` | `apiKey` | `params` | - | - |
| GET | `/settings.readTraefikFile` | `settings-readTraefikFile` | `apiKey` | `params` | query.path | - |
| GET | `/settings.readWebServerTraefikConfig` | `settings-readWebServerTraefikConfig` | `apiKey` | `none` | - | - |
| POST | `/settings.reloadRedis` | `settings-reloadRedis` | `apiKey` | `none` | - | - |
| POST | `/settings.reloadServer` | `settings-reloadServer` | `apiKey` | `none` | - | - |
| POST | `/settings.reloadTraefik` | `settings-reloadTraefik` | `apiKey` | `json` | - | - |
| POST | `/settings.saveSSHPrivateKey` | `settings-saveSSHPrivateKey` | `apiKey` | `json` | body.sshPrivateKey | - |
| POST | `/settings.setupGPU` | `settings-setupGPU` | `apiKey` | `json` | - | - |
| POST | `/settings.toggleDashboard` | `settings-toggleDashboard` | `apiKey` | `json` | - | - |
| POST | `/settings.toggleRequests` | `settings-toggleRequests` | `apiKey` | `json` | body.enable | - |
| POST | `/settings.updateDockerCleanup` | `settings-updateDockerCleanup` | `apiKey` | `json` | body.enableDockerCleanup | - |
| POST | `/settings.updateLogCleanup` | `settings-updateLogCleanup` | `apiKey` | `json` | body.cronExpression | - |
| POST | `/settings.updateMiddlewareTraefikConfig` | `settings-updateMiddlewareTraefikConfig` | `apiKey` | `json` | body.traefikConfig | - |
| POST | `/settings.updateServer` | `settings-updateServer` | `apiKey` | `none` | - | - |
| POST | `/settings.updateServerIp` | `settings-updateServerIp` | `apiKey` | `json` | body.serverIp | - |
| POST | `/settings.updateTraefikConfig` | `settings-updateTraefikConfig` | `apiKey` | `json` | body.traefikConfig | - |
| POST | `/settings.updateTraefikFile` | `settings-updateTraefikFile` | `apiKey` | `json` | body.path, body.traefikConfig | - |
| POST | `/settings.updateTraefikPorts` | `settings-updateTraefikPorts` | `apiKey` | `json` | body.additionalPorts | - |
| POST | `/settings.updateWebServerTraefikConfig` | `settings-updateWebServerTraefikConfig` | `apiKey` | `json` | body.traefikConfig | - |
| POST | `/settings.writeTraefikEnv` | `settings-writeTraefikEnv` | `apiKey` | `json` | body.env | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `settings-assignDomainServer`

- Method: `POST`
- Path: `/settings.assignDomainServer`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.host` | `required` | `string` | - |
| `body.certificateType` | `required` | `enum(letsencrypt, none, custom)` | - |
| `body.letsEncryptEmail` | `optional` | `string | null` | - |
| `body.https` | `optional` | `boolean` | - |

### `settings-checkGPUStatus`

- Method: `GET`
- Path: `/settings.checkGPUStatus`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | no | `string` | - |

### `settings-cleanAll`

- Method: `POST`
- Path: `/settings.cleanAll`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverId` | `optional` | `string` | - |

### `settings-cleanAllDeploymentQueue`

- Method: `POST`
- Path: `/settings.cleanAllDeploymentQueue`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-cleanDockerBuilder`

- Method: `POST`
- Path: `/settings.cleanDockerBuilder`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverId` | `optional` | `string` | - |

### `settings-cleanDockerPrune`

- Method: `POST`
- Path: `/settings.cleanDockerPrune`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverId` | `optional` | `string` | - |

### `settings-cleanMonitoring`

- Method: `POST`
- Path: `/settings.cleanMonitoring`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-cleanRedis`

- Method: `POST`
- Path: `/settings.cleanRedis`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-cleanSSHPrivateKey`

- Method: `POST`
- Path: `/settings.cleanSSHPrivateKey`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-cleanStoppedContainers`

- Method: `POST`
- Path: `/settings.cleanStoppedContainers`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverId` | `optional` | `string` | - |

### `settings-cleanUnusedImages`

- Method: `POST`
- Path: `/settings.cleanUnusedImages`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverId` | `optional` | `string` | - |

### `settings-cleanUnusedVolumes`

- Method: `POST`
- Path: `/settings.cleanUnusedVolumes`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverId` | `optional` | `string` | - |

### `settings-getDokployCloudIps`

- Method: `GET`
- Path: `/settings.getDokployCloudIps`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-getDokployVersion`

- Method: `GET`
- Path: `/settings.getDokployVersion`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-getIp`

- Method: `GET`
- Path: `/settings.getIp`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-getLogCleanupStatus`

- Method: `GET`
- Path: `/settings.getLogCleanupStatus`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-getOpenApiDocument`

- Method: `GET`
- Path: `/settings.getOpenApiDocument`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-getReleaseTag`

- Method: `GET`
- Path: `/settings.getReleaseTag`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-getTraefikPorts`

- Method: `GET`
- Path: `/settings.getTraefikPorts`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | no | `string` | - |

### `settings-getUpdateData`

- Method: `POST`
- Path: `/settings.getUpdateData`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-getWebServerSettings`

- Method: `GET`
- Path: `/settings.getWebServerSettings`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-haveActivateRequests`

- Method: `GET`
- Path: `/settings.haveActivateRequests`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-haveTraefikDashboardPortEnabled`

- Method: `GET`
- Path: `/settings.haveTraefikDashboardPortEnabled`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | no | `string` | - |

### `settings-health`

- Method: `GET`
- Path: `/settings.health`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-isCloud`

- Method: `GET`
- Path: `/settings.isCloud`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-isUserSubscribed`

- Method: `GET`
- Path: `/settings.isUserSubscribed`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-readDirectories`

- Method: `GET`
- Path: `/settings.readDirectories`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | no | `string` | - |

### `settings-readMiddlewareTraefikConfig`

- Method: `GET`
- Path: `/settings.readMiddlewareTraefikConfig`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-readTraefikConfig`

- Method: `GET`
- Path: `/settings.readTraefikConfig`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-readTraefikEnv`

- Method: `GET`
- Path: `/settings.readTraefikEnv`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | no | `string` | - |

### `settings-readTraefikFile`

- Method: `GET`
- Path: `/settings.readTraefikFile`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `path` | `query` | yes | `string` | minLength=1 |
| `serverId` | `query` | no | `string` | - |

### `settings-readWebServerTraefikConfig`

- Method: `GET`
- Path: `/settings.readWebServerTraefikConfig`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-reloadRedis`

- Method: `POST`
- Path: `/settings.reloadRedis`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-reloadServer`

- Method: `POST`
- Path: `/settings.reloadServer`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-reloadTraefik`

- Method: `POST`
- Path: `/settings.reloadTraefik`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverId` | `optional` | `string` | - |

### `settings-saveSSHPrivateKey`

- Method: `POST`
- Path: `/settings.saveSSHPrivateKey`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.sshPrivateKey` | `required` | `string` | - |

### `settings-setupGPU`

- Method: `POST`
- Path: `/settings.setupGPU`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverId` | `optional` | `string` | - |

### `settings-toggleDashboard`

- Method: `POST`
- Path: `/settings.toggleDashboard`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.enableDashboard` | `optional` | `boolean` | - |
| `body.serverId` | `optional` | `string` | - |

### `settings-toggleRequests`

- Method: `POST`
- Path: `/settings.toggleRequests`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.enable` | `required` | `boolean` | - |

### `settings-updateDockerCleanup`

- Method: `POST`
- Path: `/settings.updateDockerCleanup`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.enableDockerCleanup` | `required` | `boolean` | - |
| `body.serverId` | `optional` | `string` | - |

### `settings-updateLogCleanup`

- Method: `POST`
- Path: `/settings.updateLogCleanup`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.cronExpression` | `required` | `string | null` | - |

### `settings-updateMiddlewareTraefikConfig`

- Method: `POST`
- Path: `/settings.updateMiddlewareTraefikConfig`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.traefikConfig` | `required` | `string` | minLength=1 |

### `settings-updateServer`

- Method: `POST`
- Path: `/settings.updateServer`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `settings-updateServerIp`

- Method: `POST`
- Path: `/settings.updateServerIp`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverIp` | `required` | `string` | - |

### `settings-updateTraefikConfig`

- Method: `POST`
- Path: `/settings.updateTraefikConfig`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.traefikConfig` | `required` | `string` | minLength=1 |

### `settings-updateTraefikFile`

- Method: `POST`
- Path: `/settings.updateTraefikFile`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.path` | `required` | `string` | minLength=1 |
| `body.traefikConfig` | `required` | `string` | minLength=1 |
| `body.serverId` | `optional` | `string` | - |

### `settings-updateTraefikPorts`

- Method: `POST`
- Path: `/settings.updateTraefikPorts`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverId` | `optional` | `string` | - |
| `body.additionalPorts` | `required` | `array<object>` | - |
| `body.additionalPorts[].targetPort` | `required` | `number` | - |
| `body.additionalPorts[].publishedPort` | `required` | `number` | - |
| `body.additionalPorts[].protocol` | `required` | `enum(tcp, udp, sctp)` | - |

### `settings-updateWebServerTraefikConfig`

- Method: `POST`
- Path: `/settings.updateWebServerTraefikConfig`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.traefikConfig` | `required` | `string` | minLength=1 |

### `settings-writeTraefikEnv`

- Method: `POST`
- Path: `/settings.writeTraefikEnv`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.env` | `required` | `string` | - |
| `body.serverId` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
