# gitea module

This module contains `8` endpoints in the `gitea` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/gitea.create` | `gitea-create` | `apiKey` | `json` | body.giteaUrl, body.name | - |
| GET | `/gitea.getGiteaBranches` | `gitea-getGiteaBranches` | `apiKey` | `params` | query.owner, query.repositoryName | - |
| GET | `/gitea.getGiteaRepositories` | `gitea-getGiteaRepositories` | `apiKey` | `params` | query.giteaId | - |
| GET | `/gitea.getGiteaUrl` | `gitea-getGiteaUrl` | `apiKey` | `params` | query.giteaId | - |
| GET | `/gitea.giteaProviders` | `gitea-giteaProviders` | `apiKey` | `none` | - | - |
| GET | `/gitea.one` | `gitea-one` | `apiKey` | `params` | query.giteaId | - |
| POST | `/gitea.testConnection` | `gitea-testConnection` | `apiKey` | `json` | - | - |
| POST | `/gitea.update` | `gitea-update` | `apiKey` | `json` | body.giteaId, body.giteaUrl, body.gitProviderId, body.name | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `gitea-create`

- Method: `POST`
- Path: `/gitea.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.giteaId` | `optional` | `string` | - |
| `body.giteaUrl` | `required` | `string` | minLength=1 |
| `body.giteaInternalUrl` | `optional` | `string | null` | - |
| `body.redirectUri` | `optional` | `string` | - |
| `body.clientId` | `optional` | `string` | - |
| `body.clientSecret` | `optional` | `string` | - |
| `body.gitProviderId` | `optional` | `string` | - |
| `body.accessToken` | `optional` | `string` | - |
| `body.refreshToken` | `optional` | `string` | - |
| `body.expiresAt` | `optional` | `number` | - |
| `body.scopes` | `optional` | `string` | - |
| `body.lastAuthenticatedAt` | `optional` | `number` | - |
| `body.name` | `required` | `string` | minLength=1 |
| `body.giteaUsername` | `optional` | `string` | - |
| `body.organizationName` | `optional` | `string` | - |

### `gitea-getGiteaBranches`

- Method: `GET`
- Path: `/gitea.getGiteaBranches`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `owner` | `query` | yes | `string` | minLength=1 |
| `repositoryName` | `query` | yes | `string` | minLength=1 |
| `giteaId` | `query` | no | `string` | - |

### `gitea-getGiteaRepositories`

- Method: `GET`
- Path: `/gitea.getGiteaRepositories`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `giteaId` | `query` | yes | `string` | minLength=1 |

### `gitea-getGiteaUrl`

- Method: `GET`
- Path: `/gitea.getGiteaUrl`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `giteaId` | `query` | yes | `string` | minLength=1 |

### `gitea-giteaProviders`

- Method: `GET`
- Path: `/gitea.giteaProviders`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `gitea-one`

- Method: `GET`
- Path: `/gitea.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `giteaId` | `query` | yes | `string` | minLength=1 |

### `gitea-testConnection`

- Method: `POST`
- Path: `/gitea.testConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.giteaId` | `optional` | `string` | - |
| `body.organizationName` | `optional` | `string` | - |

### `gitea-update`

- Method: `POST`
- Path: `/gitea.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.giteaId` | `required` | `string` | minLength=1 |
| `body.giteaUrl` | `required` | `string` | minLength=1 |
| `body.giteaInternalUrl` | `optional` | `string | null` | - |
| `body.redirectUri` | `optional` | `string` | - |
| `body.clientId` | `optional` | `string` | - |
| `body.clientSecret` | `optional` | `string` | - |
| `body.gitProviderId` | `required` | `string` | - |
| `body.accessToken` | `optional` | `string` | - |
| `body.refreshToken` | `optional` | `string` | - |
| `body.expiresAt` | `optional` | `number` | - |
| `body.scopes` | `optional` | `string` | - |
| `body.lastAuthenticatedAt` | `optional` | `number` | - |
| `body.name` | `required` | `string` | minLength=1 |
| `body.giteaUsername` | `optional` | `string` | - |
| `body.organizationName` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
