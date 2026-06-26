# ai module

This module contains `9` endpoints in the `ai` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/ai.create` | `ai-create` | `apiKey` | `json` | body.name, body.apiUrl, body.apiKey, body.model, body.isEnabled | - |
| POST | `/ai.delete` | `ai-delete` | `apiKey` | `json` | body.aiId | - |
| POST | `/ai.deploy` | `ai-deploy` | `apiKey` | `json` | body.environmentId, body.id, body.dockerCompose, body.envVariables, body.name, body.description | - |
| GET | `/ai.get` | `ai-get` | `apiKey` | `params` | query.aiId | - |
| GET | `/ai.getAll` | `ai-getAll` | `apiKey` | `none` | - | - |
| GET | `/ai.getModels` | `ai-getModels` | `apiKey` | `params` | query.apiUrl, query.apiKey | - |
| GET | `/ai.one` | `ai-one` | `apiKey` | `params` | query.aiId | - |
| POST | `/ai.suggest` | `ai-suggest` | `apiKey` | `json` | body.aiId, body.input | - |
| POST | `/ai.update` | `ai-update` | `apiKey` | `json` | body.aiId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `ai-create`

- Method: `POST`
- Path: `/ai.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.apiUrl` | `required` | `string` | format=uri |
| `body.apiKey` | `required` | `string` | - |
| `body.model` | `required` | `string` | minLength=1 |
| `body.isEnabled` | `required` | `boolean` | - |

### `ai-delete`

- Method: `POST`
- Path: `/ai.delete`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.aiId` | `required` | `string` | - |

### `ai-deploy`

- Method: `POST`
- Path: `/ai.deploy`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.environmentId` | `required` | `string` | minLength=1 |
| `body.id` | `required` | `string` | minLength=1 |
| `body.dockerCompose` | `required` | `string` | minLength=1 |
| `body.envVariables` | `required` | `string` | - |
| `body.serverId` | `optional` | `string` | - |
| `body.name` | `required` | `string` | minLength=1 |
| `body.description` | `required` | `string` | - |
| `body.domains` | `optional` | `array<object>` | - |
| `body.domains[].host` | `required-if-body-present` | `string` | minLength=1 |
| `body.domains[].port` | `required-if-body-present` | `number` | minimum=1 |
| `body.domains[].serviceName` | `required-if-body-present` | `string` | minLength=1 |
| `body.configFiles` | `optional` | `array<object>` | - |
| `body.configFiles[].filePath` | `required-if-body-present` | `string` | minLength=1 |
| `body.configFiles[].content` | `required-if-body-present` | `string` | minLength=1 |

### `ai-get`

- Method: `GET`
- Path: `/ai.get`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `aiId` | `query` | yes | `string` | - |

### `ai-getAll`

- Method: `GET`
- Path: `/ai.getAll`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `ai-getModels`

- Method: `GET`
- Path: `/ai.getModels`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `apiUrl` | `query` | yes | `string` | minLength=1 |
| `apiKey` | `query` | yes | `string` | - |

### `ai-one`

- Method: `GET`
- Path: `/ai.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `aiId` | `query` | yes | `string` | - |

### `ai-suggest`

- Method: `POST`
- Path: `/ai.suggest`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.aiId` | `required` | `string` | - |
| `body.input` | `required` | `string` | - |
| `body.serverId` | `optional` | `string` | - |

### `ai-update`

- Method: `POST`
- Path: `/ai.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.aiId` | `required` | `string` | minLength=1 |
| `body.name` | `optional` | `string` | minLength=1 |
| `body.apiUrl` | `optional` | `string` | format=uri |
| `body.apiKey` | `optional` | `string` | - |
| `body.model` | `optional` | `string` | minLength=1 |
| `body.isEnabled` | `optional` | `boolean` | - |
| `body.createdAt` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
