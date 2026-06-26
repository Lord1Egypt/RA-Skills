# github module

This module contains `6` endpoints in the `github` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/github.getGithubBranches` | `github-getGithubBranches` | `apiKey` | `params` | query.repo, query.owner | - |
| GET | `/github.getGithubRepositories` | `github-getGithubRepositories` | `apiKey` | `params` | query.githubId | - |
| GET | `/github.githubProviders` | `github-githubProviders` | `apiKey` | `none` | - | - |
| GET | `/github.one` | `github-one` | `apiKey` | `params` | query.githubId | - |
| POST | `/github.testConnection` | `github-testConnection` | `apiKey` | `json` | body.githubId | - |
| POST | `/github.update` | `github-update` | `apiKey` | `json` | body.githubId, body.name, body.gitProviderId, body.githubAppName | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `github-getGithubBranches`

- Method: `GET`
- Path: `/github.getGithubBranches`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `repo` | `query` | yes | `string` | minLength=1 |
| `owner` | `query` | yes | `string` | minLength=1 |
| `githubId` | `query` | no | `string` | - |

### `github-getGithubRepositories`

- Method: `GET`
- Path: `/github.getGithubRepositories`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `githubId` | `query` | yes | `string` | minLength=1 |

### `github-githubProviders`

- Method: `GET`
- Path: `/github.githubProviders`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `github-one`

- Method: `GET`
- Path: `/github.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `githubId` | `query` | yes | `string` | minLength=1 |

### `github-testConnection`

- Method: `POST`
- Path: `/github.testConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.githubId` | `required` | `string` | minLength=1 |

### `github-update`

- Method: `POST`
- Path: `/github.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.githubId` | `required` | `string` | minLength=1 |
| `body.name` | `required` | `string` | minLength=1 |
| `body.gitProviderId` | `required` | `string` | minLength=1 |
| `body.githubAppName` | `required` | `string` | minLength=1 |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
