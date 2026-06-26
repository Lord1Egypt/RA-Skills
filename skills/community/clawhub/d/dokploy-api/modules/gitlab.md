# gitlab module

This module contains `7` endpoints in the `gitlab` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/gitlab.create` | `gitlab-create` | `apiKey` | `json` | body.authId, body.name, body.gitlabUrl | - |
| GET | `/gitlab.getGitlabBranches` | `gitlab-getGitlabBranches` | `apiKey` | `params` | query.owner, query.repo | - |
| GET | `/gitlab.getGitlabRepositories` | `gitlab-getGitlabRepositories` | `apiKey` | `params` | query.gitlabId | - |
| GET | `/gitlab.gitlabProviders` | `gitlab-gitlabProviders` | `apiKey` | `none` | - | - |
| GET | `/gitlab.one` | `gitlab-one` | `apiKey` | `params` | query.gitlabId | - |
| POST | `/gitlab.testConnection` | `gitlab-testConnection` | `apiKey` | `json` | body.gitlabId | - |
| POST | `/gitlab.update` | `gitlab-update` | `apiKey` | `json` | body.name, body.gitlabId, body.gitlabUrl, body.gitProviderId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `gitlab-create`

- Method: `POST`
- Path: `/gitlab.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `optional` | `string` | - |
| `body.secret` | `optional` | `string` | - |
| `body.groupName` | `optional` | `string` | - |
| `body.gitProviderId` | `optional` | `string` | - |
| `body.redirectUri` | `optional` | `string` | - |
| `body.authId` | `required` | `string` | minLength=1 |
| `body.name` | `required` | `string` | minLength=1 |
| `body.gitlabUrl` | `required` | `string` | minLength=1 |
| `body.gitlabInternalUrl` | `optional` | `string | null` | - |

### `gitlab-getGitlabBranches`

- Method: `GET`
- Path: `/gitlab.getGitlabBranches`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `id` | `query` | no | `number` | - |
| `owner` | `query` | yes | `string` | - |
| `repo` | `query` | yes | `string` | - |
| `gitlabId` | `query` | no | `string` | - |

### `gitlab-getGitlabRepositories`

- Method: `GET`
- Path: `/gitlab.getGitlabRepositories`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `gitlabId` | `query` | yes | `string` | minLength=1 |

### `gitlab-gitlabProviders`

- Method: `GET`
- Path: `/gitlab.gitlabProviders`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `gitlab-one`

- Method: `GET`
- Path: `/gitlab.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `gitlabId` | `query` | yes | `string` | minLength=1 |

### `gitlab-testConnection`

- Method: `POST`
- Path: `/gitlab.testConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.gitlabId` | `required` | `string` | minLength=1 |
| `body.groupName` | `optional` | `string` | - |

### `gitlab-update`

- Method: `POST`
- Path: `/gitlab.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `optional` | `string` | - |
| `body.secret` | `optional` | `string` | - |
| `body.groupName` | `optional` | `string` | - |
| `body.redirectUri` | `optional` | `string` | - |
| `body.name` | `required` | `string` | minLength=1 |
| `body.gitlabId` | `required` | `string` | minLength=1 |
| `body.gitlabUrl` | `required` | `string` | minLength=1 |
| `body.gitProviderId` | `required` | `string` | minLength=1 |
| `body.gitlabInternalUrl` | `optional` | `string | null` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
