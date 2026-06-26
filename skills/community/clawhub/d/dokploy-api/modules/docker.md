# docker module

This module contains `7` endpoints in the `docker` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/docker.getConfig` | `docker-getConfig` | `apiKey` | `params` | query.containerId | - |
| GET | `/docker.getContainers` | `docker-getContainers` | `apiKey` | `params` | - | - |
| GET | `/docker.getContainersByAppLabel` | `docker-getContainersByAppLabel` | `apiKey` | `params` | query.appName, query.type | - |
| GET | `/docker.getContainersByAppNameMatch` | `docker-getContainersByAppNameMatch` | `apiKey` | `params` | query.appName | - |
| GET | `/docker.getServiceContainersByAppName` | `docker-getServiceContainersByAppName` | `apiKey` | `params` | query.appName | - |
| GET | `/docker.getStackContainersByAppName` | `docker-getStackContainersByAppName` | `apiKey` | `params` | query.appName | - |
| POST | `/docker.restartContainer` | `docker-restartContainer` | `apiKey` | `json` | body.containerId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `docker-getConfig`

- Method: `GET`
- Path: `/docker.getConfig`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `containerId` | `query` | yes | `string` | minLength=1; pattern=^[a-zA-Z0-9.\-_]+$ |
| `serverId` | `query` | no | `string` | - |

### `docker-getContainers`

- Method: `GET`
- Path: `/docker.getContainers`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | no | `string` | - |

### `docker-getContainersByAppLabel`

- Method: `GET`
- Path: `/docker.getContainersByAppLabel`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `appName` | `query` | yes | `string` | minLength=1; pattern=^[a-zA-Z0-9.\-_]+$ |
| `serverId` | `query` | no | `string` | - |
| `type` | `query` | yes | `enum(standalone, swarm)` | - |

### `docker-getContainersByAppNameMatch`

- Method: `GET`
- Path: `/docker.getContainersByAppNameMatch`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `appType` | `query` | no | `enum(stack, docker-compose)` | - |
| `appName` | `query` | yes | `string` | minLength=1; pattern=^[a-zA-Z0-9.\-_]+$ |
| `serverId` | `query` | no | `string` | - |

### `docker-getServiceContainersByAppName`

- Method: `GET`
- Path: `/docker.getServiceContainersByAppName`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `appName` | `query` | yes | `string` | minLength=1; pattern=^[a-zA-Z0-9.\-_]+$ |
| `serverId` | `query` | no | `string` | - |

### `docker-getStackContainersByAppName`

- Method: `GET`
- Path: `/docker.getStackContainersByAppName`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `appName` | `query` | yes | `string` | minLength=1; pattern=^[a-zA-Z0-9.\-_]+$ |
| `serverId` | `query` | no | `string` | - |

### `docker-restartContainer`

- Method: `POST`
- Path: `/docker.restartContainer`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.containerId` | `required` | `string` | minLength=1; pattern=^[a-zA-Z0-9.\-_]+$ |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
