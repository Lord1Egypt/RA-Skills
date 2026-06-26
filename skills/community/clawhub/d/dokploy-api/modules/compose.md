# compose module

This module contains `28` endpoints in the `compose` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/compose.cancelDeployment` | `compose-cancelDeployment` | `apiKey` | `json` | body.composeId | - |
| POST | `/compose.cleanQueues` | `compose-cleanQueues` | `apiKey` | `json` | body.composeId | - |
| POST | `/compose.clearDeployments` | `compose-clearDeployments` | `apiKey` | `json` | body.composeId | - |
| POST | `/compose.create` | `compose-create` | `apiKey` | `json` | body.name, body.environmentId | - |
| POST | `/compose.delete` | `compose-delete` | `apiKey` | `json` | body.composeId, body.deleteVolumes | - |
| POST | `/compose.deploy` | `compose-deploy` | `apiKey` | `json` | body.composeId | - |
| POST | `/compose.deployTemplate` | `compose-deployTemplate` | `apiKey` | `json` | body.environmentId, body.id | - |
| POST | `/compose.disconnectGitProvider` | `compose-disconnectGitProvider` | `apiKey` | `json` | body.composeId | - |
| POST | `/compose.fetchSourceType` | `compose-fetchSourceType` | `apiKey` | `json` | body.composeId | - |
| GET | `/compose.getConvertedCompose` | `compose-getConvertedCompose` | `apiKey` | `params` | query.composeId | - |
| GET | `/compose.getDefaultCommand` | `compose-getDefaultCommand` | `apiKey` | `params` | query.composeId | - |
| GET | `/compose.getTags` | `compose-getTags` | `apiKey` | `params` | - | - |
| POST | `/compose.import` | `compose-import` | `apiKey` | `json` | body.base64, body.composeId | - |
| POST | `/compose.isolatedDeployment` | `compose-isolatedDeployment` | `apiKey` | `json` | body.composeId | - |
| POST | `/compose.killBuild` | `compose-killBuild` | `apiKey` | `json` | body.composeId | - |
| GET | `/compose.loadMountsByService` | `compose-loadMountsByService` | `apiKey` | `params` | query.composeId, query.serviceName | - |
| GET | `/compose.loadServices` | `compose-loadServices` | `apiKey` | `params` | query.composeId | - |
| POST | `/compose.move` | `compose-move` | `apiKey` | `json` | body.composeId, body.targetEnvironmentId | - |
| GET | `/compose.one` | `compose-one` | `apiKey` | `params` | query.composeId | - |
| POST | `/compose.processTemplate` | `compose-processTemplate` | `apiKey` | `json` | body.base64, body.composeId | - |
| POST | `/compose.randomizeCompose` | `compose-randomizeCompose` | `apiKey` | `json` | body.composeId | - |
| POST | `/compose.redeploy` | `compose-redeploy` | `apiKey` | `json` | body.composeId | - |
| POST | `/compose.refreshToken` | `compose-refreshToken` | `apiKey` | `json` | body.composeId | - |
| GET | `/compose.search` | `compose-search` | `apiKey` | `params` | - | - |
| POST | `/compose.start` | `compose-start` | `apiKey` | `json` | body.composeId | - |
| POST | `/compose.stop` | `compose-stop` | `apiKey` | `json` | body.composeId | - |
| GET | `/compose.templates` | `compose-templates` | `apiKey` | `params` | - | - |
| POST | `/compose.update` | `compose-update` | `apiKey` | `json` | body.composeId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `compose-cancelDeployment`

- Method: `POST`
- Path: `/compose.cancelDeployment`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |

### `compose-cleanQueues`

- Method: `POST`
- Path: `/compose.cleanQueues`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |

### `compose-clearDeployments`

- Method: `POST`
- Path: `/compose.clearDeployments`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |

### `compose-create`

- Method: `POST`
- Path: `/compose.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.description` | `optional` | `string | null` | - |
| `body.environmentId` | `required` | `string` | - |
| `body.composeType` | `optional` | `enum(docker-compose, stack)` | - |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.serverId` | `optional` | `string | null` | - |
| `body.composeFile` | `optional` | `string` | - |

### `compose-delete`

- Method: `POST`
- Path: `/compose.delete`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |
| `body.deleteVolumes` | `required` | `boolean` | - |

### `compose-deploy`

- Method: `POST`
- Path: `/compose.deploy`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |
| `body.title` | `optional` | `string` | - |
| `body.description` | `optional` | `string` | - |

### `compose-deployTemplate`

- Method: `POST`
- Path: `/compose.deployTemplate`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.environmentId` | `required` | `string` | - |
| `body.serverId` | `optional` | `string` | - |
| `body.id` | `required` | `string` | - |
| `body.baseUrl` | `optional` | `string` | - |

### `compose-disconnectGitProvider`

- Method: `POST`
- Path: `/compose.disconnectGitProvider`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |

### `compose-fetchSourceType`

- Method: `POST`
- Path: `/compose.fetchSourceType`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |

### `compose-getConvertedCompose`

- Method: `GET`
- Path: `/compose.getConvertedCompose`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `composeId` | `query` | yes | `string` | minLength=1 |

### `compose-getDefaultCommand`

- Method: `GET`
- Path: `/compose.getDefaultCommand`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `composeId` | `query` | yes | `string` | minLength=1 |

### `compose-getTags`

- Method: `GET`
- Path: `/compose.getTags`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `baseUrl` | `query` | no | `string` | - |

### `compose-import`

- Method: `POST`
- Path: `/compose.import`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.base64` | `required` | `string` | - |
| `body.composeId` | `required` | `string` | minLength=1 |

### `compose-isolatedDeployment`

- Method: `POST`
- Path: `/compose.isolatedDeployment`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |
| `body.suffix` | `optional` | `string` | - |

### `compose-killBuild`

- Method: `POST`
- Path: `/compose.killBuild`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |

### `compose-loadMountsByService`

- Method: `GET`
- Path: `/compose.loadMountsByService`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `composeId` | `query` | yes | `string` | minLength=1 |
| `serviceName` | `query` | yes | `string` | minLength=1 |

### `compose-loadServices`

- Method: `GET`
- Path: `/compose.loadServices`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `composeId` | `query` | yes | `string` | minLength=1 |
| `type` | `query` | no | `enum(fetch, cache)` | default=cache |

### `compose-move`

- Method: `POST`
- Path: `/compose.move`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | - |
| `body.targetEnvironmentId` | `required` | `string` | - |

### `compose-one`

- Method: `GET`
- Path: `/compose.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `composeId` | `query` | yes | `string` | minLength=1 |

### `compose-processTemplate`

- Method: `POST`
- Path: `/compose.processTemplate`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.base64` | `required` | `string` | - |
| `body.composeId` | `required` | `string` | minLength=1 |

### `compose-randomizeCompose`

- Method: `POST`
- Path: `/compose.randomizeCompose`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |
| `body.suffix` | `optional` | `string` | - |

### `compose-redeploy`

- Method: `POST`
- Path: `/compose.redeploy`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |
| `body.title` | `optional` | `string` | - |
| `body.description` | `optional` | `string` | - |

### `compose-refreshToken`

- Method: `POST`
- Path: `/compose.refreshToken`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |

### `compose-search`

- Method: `GET`
- Path: `/compose.search`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `q` | `query` | no | `string` | - |
| `name` | `query` | no | `string` | - |
| `appName` | `query` | no | `string` | - |
| `description` | `query` | no | `string` | - |
| `projectId` | `query` | no | `string` | - |
| `environmentId` | `query` | no | `string` | - |
| `limit` | `query` | no | `number` | minimum=1; maximum=100; default=20 |
| `offset` | `query` | no | `number` | minimum=0; default=0 |

### `compose-start`

- Method: `POST`
- Path: `/compose.start`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |

### `compose-stop`

- Method: `POST`
- Path: `/compose.stop`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | minLength=1 |

### `compose-templates`

- Method: `GET`
- Path: `/compose.templates`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `baseUrl` | `query` | no | `string` | - |

### `compose-update`

- Method: `POST`
- Path: `/compose.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.composeId` | `required` | `string` | - |
| `body.name` | `optional` | `string` | minLength=1 |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.description` | `optional` | `string | null` | - |
| `body.env` | `optional` | `string | null` | - |
| `body.composeFile` | `optional` | `string` | - |
| `body.refreshToken` | `optional` | `string | null` | - |
| `body.sourceType` | `optional` | `enum(git, github, gitlab, bitbucket, gitea, raw)` | - |
| `body.composeType` | `optional` | `enum(docker-compose, stack)` | - |
| `body.repository` | `optional` | `string | null` | - |
| `body.owner` | `optional` | `string | null` | - |
| `body.branch` | `optional` | `string | null` | - |
| `body.autoDeploy` | `optional` | `boolean | null` | - |
| `body.gitlabProjectId` | `optional` | `number | null` | - |
| `body.gitlabRepository` | `optional` | `string | null` | - |
| `body.gitlabOwner` | `optional` | `string | null` | - |
| `body.gitlabBranch` | `optional` | `string | null` | - |
| `body.gitlabPathNamespace` | `optional` | `string | null` | - |
| `body.bitbucketRepository` | `optional` | `string | null` | - |
| `body.bitbucketRepositorySlug` | `optional` | `string | null` | - |
| `body.bitbucketOwner` | `optional` | `string | null` | - |
| `body.bitbucketBranch` | `optional` | `string | null` | - |
| `body.giteaRepository` | `optional` | `string | null` | - |
| `body.giteaOwner` | `optional` | `string | null` | - |
| `body.giteaBranch` | `optional` | `string | null` | - |
| `body.customGitUrl` | `optional` | `string | null` | - |
| `body.customGitBranch` | `optional` | `string | null` | - |
| `body.customGitSSHKeyId` | `optional` | `string | null` | - |
| `body.command` | `optional` | `string` | - |
| `body.enableSubmodules` | `optional` | `boolean` | - |
| `body.composePath` | `optional` | `string` | minLength=1 |
| `body.suffix` | `optional` | `string` | - |
| `body.randomize` | `optional` | `boolean` | - |
| `body.isolatedDeployment` | `optional` | `boolean` | - |
| `body.isolatedDeploymentsVolume` | `optional` | `boolean` | - |
| `body.triggerType` | `optional` | `enum(push, tag) | null` | - |
| `body.composeStatus` | `optional` | `enum(idle, running, done, error)` | - |
| `body.environmentId` | `optional` | `string` | - |
| `body.createdAt` | `optional` | `string` | - |
| `body.watchPaths` | `optional` | `array<string> | null` | - |
| `body.githubId` | `optional` | `string | null` | - |
| `body.gitlabId` | `optional` | `string | null` | - |
| `body.bitbucketId` | `optional` | `string | null` | - |
| `body.giteaId` | `optional` | `string | null` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
