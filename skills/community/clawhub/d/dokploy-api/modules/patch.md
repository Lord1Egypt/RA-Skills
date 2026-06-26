# patch module

This module contains `12` endpoints in the `patch` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/patch.byEntityId` | `patch-byEntityId` | `apiKey` | `params` | query.id, query.type | - |
| POST | `/patch.cleanPatchRepos` | `patch-cleanPatchRepos` | `apiKey` | `json` | - | - |
| POST | `/patch.create` | `patch-create` | `apiKey` | `json` | body.filePath, body.content | - |
| POST | `/patch.delete` | `patch-delete` | `apiKey` | `json` | body.patchId | - |
| POST | `/patch.ensureRepo` | `patch-ensureRepo` | `apiKey` | `json` | body.id, body.type | - |
| POST | `/patch.markFileForDeletion` | `patch-markFileForDeletion` | `apiKey` | `json` | body.id, body.type, body.filePath | - |
| GET | `/patch.one` | `patch-one` | `apiKey` | `params` | query.patchId | - |
| GET | `/patch.readRepoDirectories` | `patch-readRepoDirectories` | `apiKey` | `params` | query.id, query.type, query.repoPath | - |
| GET | `/patch.readRepoFile` | `patch-readRepoFile` | `apiKey` | `params` | query.id, query.type, query.filePath | - |
| POST | `/patch.saveFileAsPatch` | `patch-saveFileAsPatch` | `apiKey` | `json` | body.id, body.type, body.filePath, body.content | - |
| POST | `/patch.toggleEnabled` | `patch-toggleEnabled` | `apiKey` | `json` | body.patchId, body.enabled | - |
| POST | `/patch.update` | `patch-update` | `apiKey` | `json` | body.patchId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `patch-byEntityId`

- Method: `GET`
- Path: `/patch.byEntityId`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `id` | `query` | yes | `string` | - |
| `type` | `query` | yes | `enum(application, compose)` | - |

### `patch-cleanPatchRepos`

- Method: `POST`
- Path: `/patch.cleanPatchRepos`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverId` | `optional` | `string` | - |

### `patch-create`

- Method: `POST`
- Path: `/patch.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.filePath` | `required` | `string` | minLength=1 |
| `body.content` | `required` | `string` | - |
| `body.type` | `optional` | `enum(create, update, delete)` | - |
| `body.enabled` | `optional` | `boolean` | - |
| `body.applicationId` | `optional` | `string | null` | - |
| `body.composeId` | `optional` | `string | null` | - |

### `patch-delete`

- Method: `POST`
- Path: `/patch.delete`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.patchId` | `required` | `string` | minLength=1 |

### `patch-ensureRepo`

- Method: `POST`
- Path: `/patch.ensureRepo`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.id` | `required` | `string` | - |
| `body.type` | `required` | `enum(application, compose)` | - |

### `patch-markFileForDeletion`

- Method: `POST`
- Path: `/patch.markFileForDeletion`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.id` | `required` | `string` | minLength=1 |
| `body.type` | `required` | `enum(application, compose)` | - |
| `body.filePath` | `required` | `string` | - |

### `patch-one`

- Method: `GET`
- Path: `/patch.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `patchId` | `query` | yes | `string` | minLength=1 |

### `patch-readRepoDirectories`

- Method: `GET`
- Path: `/patch.readRepoDirectories`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `id` | `query` | yes | `string` | minLength=1 |
| `type` | `query` | yes | `enum(application, compose)` | - |
| `repoPath` | `query` | yes | `string` | - |

### `patch-readRepoFile`

- Method: `GET`
- Path: `/patch.readRepoFile`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `id` | `query` | yes | `string` | minLength=1 |
| `type` | `query` | yes | `enum(application, compose)` | - |
| `filePath` | `query` | yes | `string` | - |

### `patch-saveFileAsPatch`

- Method: `POST`
- Path: `/patch.saveFileAsPatch`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.id` | `required` | `string` | minLength=1 |
| `body.type` | `required` | `enum(application, compose)` | - |
| `body.filePath` | `required` | `string` | - |
| `body.content` | `required` | `string` | - |
| `body.patchType` | `optional` | `enum(create, update)` | default=update |

### `patch-toggleEnabled`

- Method: `POST`
- Path: `/patch.toggleEnabled`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.patchId` | `required` | `string` | minLength=1 |
| `body.enabled` | `required` | `boolean` | - |

### `patch-update`

- Method: `POST`
- Path: `/patch.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.patchId` | `required` | `string` | minLength=1 |
| `body.type` | `optional` | `enum(create, update, delete)` | - |
| `body.filePath` | `optional` | `string` | minLength=1 |
| `body.enabled` | `optional` | `boolean` | - |
| `body.content` | `optional` | `string` | - |
| `body.createdAt` | `optional` | `string` | - |
| `body.updatedAt` | `optional` | `string | null` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
