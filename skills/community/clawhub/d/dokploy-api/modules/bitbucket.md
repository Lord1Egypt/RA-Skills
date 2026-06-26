# bitbucket module

This module contains `7` endpoints in the `bitbucket` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/bitbucket.bitbucketProviders` | `bitbucket-bitbucketProviders` | `apiKey` | `none` | - | - |
| POST | `/bitbucket.create` | `bitbucket-create` | `apiKey` | `json` | body.authId, body.name | - |
| GET | `/bitbucket.getBitbucketBranches` | `bitbucket-getBitbucketBranches` | `apiKey` | `params` | query.owner, query.repo | - |
| GET | `/bitbucket.getBitbucketRepositories` | `bitbucket-getBitbucketRepositories` | `apiKey` | `params` | query.bitbucketId | - |
| GET | `/bitbucket.one` | `bitbucket-one` | `apiKey` | `params` | query.bitbucketId | - |
| POST | `/bitbucket.testConnection` | `bitbucket-testConnection` | `apiKey` | `json` | body.bitbucketId | - |
| POST | `/bitbucket.update` | `bitbucket-update` | `apiKey` | `json` | body.bitbucketId, body.gitProviderId, body.name | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `bitbucket-bitbucketProviders`

- Method: `GET`
- Path: `/bitbucket.bitbucketProviders`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `bitbucket-create`

- Method: `POST`
- Path: `/bitbucket.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.bitbucketId` | `optional` | `string` | - |
| `body.bitbucketUsername` | `optional` | `string` | - |
| `body.bitbucketEmail` | `optional` | `string` | format=email; pattern=^(?!\.)(?!.*\.\.)([A-Za-z0-9_'+\-\.]*)[A-Za-z0-9_+-]@([A-Za-z0-9][A-Za-z0-9\-]*\.)+[A-Za-z]{2,}$ |
| `body.appPassword` | `optional` | `string` | - |
| `body.apiToken` | `optional` | `string` | - |
| `body.bitbucketWorkspaceName` | `optional` | `string` | - |
| `body.gitProviderId` | `optional` | `string` | - |
| `body.authId` | `required` | `string` | minLength=1 |
| `body.name` | `required` | `string` | minLength=1 |

### `bitbucket-getBitbucketBranches`

- Method: `GET`
- Path: `/bitbucket.getBitbucketBranches`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `owner` | `query` | yes | `string` | - |
| `repo` | `query` | yes | `string` | - |
| `bitbucketId` | `query` | no | `string` | - |

### `bitbucket-getBitbucketRepositories`

- Method: `GET`
- Path: `/bitbucket.getBitbucketRepositories`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `bitbucketId` | `query` | yes | `string` | minLength=1 |

### `bitbucket-one`

- Method: `GET`
- Path: `/bitbucket.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `bitbucketId` | `query` | yes | `string` | minLength=1 |

### `bitbucket-testConnection`

- Method: `POST`
- Path: `/bitbucket.testConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.bitbucketId` | `required` | `string` | minLength=1 |
| `body.bitbucketUsername` | `optional` | `string` | - |
| `body.bitbucketEmail` | `optional` | `string` | format=email; pattern=^(?!\.)(?!.*\.\.)([A-Za-z0-9_'+\-\.]*)[A-Za-z0-9_+-]@([A-Za-z0-9][A-Za-z0-9\-]*\.)+[A-Za-z]{2,}$ |
| `body.workspaceName` | `optional` | `string` | - |
| `body.apiToken` | `optional` | `string` | - |
| `body.appPassword` | `optional` | `string` | - |

### `bitbucket-update`

- Method: `POST`
- Path: `/bitbucket.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.bitbucketId` | `required` | `string` | minLength=1 |
| `body.bitbucketUsername` | `optional` | `string` | - |
| `body.bitbucketEmail` | `optional` | `string` | format=email; pattern=^(?!\.)(?!.*\.\.)([A-Za-z0-9_'+\-\.]*)[A-Za-z0-9_+-]@([A-Za-z0-9][A-Za-z0-9\-]*\.)+[A-Za-z]{2,}$ |
| `body.appPassword` | `optional` | `string` | - |
| `body.apiToken` | `optional` | `string` | - |
| `body.bitbucketWorkspaceName` | `optional` | `string` | - |
| `body.gitProviderId` | `required` | `string` | - |
| `body.name` | `required` | `string` | minLength=1 |
| `body.organizationId` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
