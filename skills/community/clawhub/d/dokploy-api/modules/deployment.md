# deployment module

This module contains `8` endpoints in the `deployment` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/deployment.all` | `deployment-all` | `apiKey` | `params` | query.applicationId | - |
| GET | `/deployment.allByCompose` | `deployment-allByCompose` | `apiKey` | `params` | query.composeId | - |
| GET | `/deployment.allByServer` | `deployment-allByServer` | `apiKey` | `params` | query.serverId | - |
| GET | `/deployment.allByType` | `deployment-allByType` | `apiKey` | `params` | query.id, query.type | - |
| GET | `/deployment.allCentralized` | `deployment-allCentralized` | `apiKey` | `none` | - | - |
| POST | `/deployment.killProcess` | `deployment-killProcess` | `apiKey` | `json` | body.deploymentId | - |
| GET | `/deployment.queueList` | `deployment-queueList` | `apiKey` | `none` | - | - |
| POST | `/deployment.removeDeployment` | `deployment-removeDeployment` | `apiKey` | `json` | body.deploymentId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `deployment-all`

- Method: `GET`
- Path: `/deployment.all`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `applicationId` | `query` | yes | `string` | minLength=1 |

### `deployment-allByCompose`

- Method: `GET`
- Path: `/deployment.allByCompose`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `composeId` | `query` | yes | `string` | minLength=1 |

### `deployment-allByServer`

- Method: `GET`
- Path: `/deployment.allByServer`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | yes | `string` | minLength=1 |

### `deployment-allByType`

- Method: `GET`
- Path: `/deployment.allByType`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `id` | `query` | yes | `string` | minLength=1 |
| `type` | `query` | yes | `enum(application, compose, server, schedule, previewDeployment, backup, ...)` | - |

### `deployment-allCentralized`

- Method: `GET`
- Path: `/deployment.allCentralized`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `deployment-killProcess`

- Method: `POST`
- Path: `/deployment.killProcess`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.deploymentId` | `required` | `string` | minLength=1 |

### `deployment-queueList`

- Method: `GET`
- Path: `/deployment.queueList`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `deployment-removeDeployment`

- Method: `POST`
- Path: `/deployment.removeDeployment`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.deploymentId` | `required` | `string` | minLength=1 |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
