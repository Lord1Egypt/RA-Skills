# application module

This module contains `29` endpoints in the `application` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/application.cancelDeployment` | `application-cancelDeployment` | `apiKey` | `json` | body.applicationId | - |
| POST | `/application.cleanQueues` | `application-cleanQueues` | `apiKey` | `json` | body.applicationId | - |
| POST | `/application.clearDeployments` | `application-clearDeployments` | `apiKey` | `json` | body.applicationId | - |
| POST | `/application.create` | `application-create` | `apiKey` | `json` | body.name, body.environmentId | - |
| POST | `/application.delete` | `application-delete` | `apiKey` | `json` | body.applicationId | - |
| POST | `/application.deploy` | `application-deploy` | `apiKey` | `json` | body.applicationId | - |
| POST | `/application.disconnectGitProvider` | `application-disconnectGitProvider` | `apiKey` | `json` | body.applicationId | - |
| POST | `/application.killBuild` | `application-killBuild` | `apiKey` | `json` | body.applicationId | - |
| POST | `/application.markRunning` | `application-markRunning` | `apiKey` | `json` | body.applicationId | - |
| POST | `/application.move` | `application-move` | `apiKey` | `json` | body.applicationId, body.targetEnvironmentId | - |
| GET | `/application.one` | `application-one` | `apiKey` | `params` | query.applicationId | - |
| GET | `/application.readAppMonitoring` | `application-readAppMonitoring` | `apiKey` | `params` | query.appName | - |
| GET | `/application.readTraefikConfig` | `application-readTraefikConfig` | `apiKey` | `params` | query.applicationId | - |
| POST | `/application.redeploy` | `application-redeploy` | `apiKey` | `json` | body.applicationId | - |
| POST | `/application.refreshToken` | `application-refreshToken` | `apiKey` | `json` | body.applicationId | - |
| POST | `/application.reload` | `application-reload` | `apiKey` | `json` | body.appName, body.applicationId | - |
| POST | `/application.saveBitbucketProvider` | `application-saveBitbucketProvider` | `apiKey` | `json` | body.bitbucketBranch, body.bitbucketBuildPath, body.bitbucketOwner, body.bitbucketRepository, body.bitbucketRepositorySlug, body.bitbucketId, body.applicationId | - |
| POST | `/application.saveBuildType` | `application-saveBuildType` | `apiKey` | `json` | body.applicationId, body.buildType, body.dockerfile, body.dockerContextPath, body.dockerBuildStage, body.herokuVersion, body.railpackVersion | - |
| POST | `/application.saveDockerProvider` | `application-saveDockerProvider` | `apiKey` | `json` | body.dockerImage, body.applicationId, body.username, body.password, body.registryUrl | - |
| POST | `/application.saveEnvironment` | `application-saveEnvironment` | `apiKey` | `json` | body.applicationId, body.env, body.buildArgs, body.buildSecrets, body.createEnvFile | - |
| POST | `/application.saveGitProvider` | `application-saveGitProvider` | `apiKey` | `json` | body.customGitBranch, body.applicationId, body.customGitBuildPath, body.customGitUrl, body.watchPaths | - |
| POST | `/application.saveGiteaProvider` | `application-saveGiteaProvider` | `apiKey` | `json` | body.applicationId, body.giteaBranch, body.giteaBuildPath, body.giteaOwner, body.giteaRepository, body.giteaId | - |
| POST | `/application.saveGithubProvider` | `application-saveGithubProvider` | `apiKey` | `json` | body.applicationId, body.repository, body.branch, body.owner, body.buildPath, body.githubId, body.triggerType | - |
| POST | `/application.saveGitlabProvider` | `application-saveGitlabProvider` | `apiKey` | `json` | body.applicationId, body.gitlabBranch, body.gitlabBuildPath, body.gitlabOwner, body.gitlabRepository, body.gitlabId, body.gitlabProjectId, body.gitlabPathNamespace | - |
| GET | `/application.search` | `application-search` | `apiKey` | `params` | - | - |
| POST | `/application.start` | `application-start` | `apiKey` | `json` | body.applicationId | - |
| POST | `/application.stop` | `application-stop` | `apiKey` | `json` | body.applicationId | - |
| POST | `/application.update` | `application-update` | `apiKey` | `json` | body.applicationId | - |
| POST | `/application.updateTraefikConfig` | `application-updateTraefikConfig` | `apiKey` | `json` | body.applicationId, body.traefikConfig | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `application-cancelDeployment`

- Method: `POST`
- Path: `/application.cancelDeployment`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | minLength=1 |

### `application-cleanQueues`

- Method: `POST`
- Path: `/application.cleanQueues`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | minLength=1 |

### `application-clearDeployments`

- Method: `POST`
- Path: `/application.clearDeployments`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | minLength=1 |

### `application-create`

- Method: `POST`
- Path: `/application.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.description` | `optional` | `string | null` | - |
| `body.environmentId` | `required` | `string` | - |
| `body.serverId` | `optional` | `string | null` | - |

### `application-delete`

- Method: `POST`
- Path: `/application.delete`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | minLength=1 |

### `application-deploy`

- Method: `POST`
- Path: `/application.deploy`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | minLength=1 |
| `body.title` | `optional` | `string` | - |
| `body.description` | `optional` | `string` | - |

### `application-disconnectGitProvider`

- Method: `POST`
- Path: `/application.disconnectGitProvider`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | minLength=1 |

### `application-killBuild`

- Method: `POST`
- Path: `/application.killBuild`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | minLength=1 |

### `application-markRunning`

- Method: `POST`
- Path: `/application.markRunning`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | minLength=1 |

### `application-move`

- Method: `POST`
- Path: `/application.move`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | - |
| `body.targetEnvironmentId` | `required` | `string` | - |

### `application-one`

- Method: `GET`
- Path: `/application.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `applicationId` | `query` | yes | `string` | minLength=1 |

### `application-readAppMonitoring`

- Method: `GET`
- Path: `/application.readAppMonitoring`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `appName` | `query` | yes | `string` | minLength=1 |

### `application-readTraefikConfig`

- Method: `GET`
- Path: `/application.readTraefikConfig`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `applicationId` | `query` | yes | `string` | minLength=1 |

### `application-redeploy`

- Method: `POST`
- Path: `/application.redeploy`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | minLength=1 |
| `body.title` | `optional` | `string` | - |
| `body.description` | `optional` | `string` | - |

### `application-refreshToken`

- Method: `POST`
- Path: `/application.refreshToken`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | minLength=1 |

### `application-reload`

- Method: `POST`
- Path: `/application.reload`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appName` | `required` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.applicationId` | `required` | `string` | - |

### `application-saveBitbucketProvider`

- Method: `POST`
- Path: `/application.saveBitbucketProvider`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.bitbucketBranch` | `required` | `string | null` | - |
| `body.bitbucketBuildPath` | `required` | `string | null` | - |
| `body.bitbucketOwner` | `required` | `string | null` | - |
| `body.bitbucketRepository` | `required` | `string | null` | - |
| `body.bitbucketRepositorySlug` | `required` | `string | null` | - |
| `body.bitbucketId` | `required` | `string | null` | - |
| `body.applicationId` | `required` | `string` | - |
| `body.enableSubmodules` | `optional` | `boolean` | - |
| `body.watchPaths` | `optional` | `array<string> | null` | - |

### `application-saveBuildType`

- Method: `POST`
- Path: `/application.saveBuildType`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | - |
| `body.buildType` | `required` | `enum(dockerfile, heroku_buildpacks, paketo_buildpacks, nixpacks, static, railpack)` | - |
| `body.dockerfile` | `required` | `string | null` | - |
| `body.dockerContextPath` | `required` | `string | null` | - |
| `body.dockerBuildStage` | `required` | `string | null` | - |
| `body.herokuVersion` | `required` | `string | null` | - |
| `body.railpackVersion` | `required` | `string | null` | - |
| `body.publishDirectory` | `optional` | `string | null` | - |
| `body.isStaticSpa` | `optional` | `boolean | null` | - |

### `application-saveDockerProvider`

- Method: `POST`
- Path: `/application.saveDockerProvider`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.dockerImage` | `required` | `string | null` | - |
| `body.applicationId` | `required` | `string` | - |
| `body.username` | `required` | `string | null` | - |
| `body.password` | `required` | `string | null` | - |
| `body.registryUrl` | `required` | `string | null` | - |

### `application-saveEnvironment`

- Method: `POST`
- Path: `/application.saveEnvironment`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | - |
| `body.env` | `required` | `string | null` | - |
| `body.buildArgs` | `required` | `string | null` | - |
| `body.buildSecrets` | `required` | `string | null` | - |
| `body.createEnvFile` | `required` | `boolean` | - |

### `application-saveGitProvider`

- Method: `POST`
- Path: `/application.saveGitProvider`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.customGitBranch` | `required` | `string | null` | - |
| `body.applicationId` | `required` | `string` | - |
| `body.customGitBuildPath` | `required` | `string | null` | - |
| `body.customGitUrl` | `required` | `string | null` | - |
| `body.watchPaths` | `required` | `array<string> | null` | - |
| `body.enableSubmodules` | `optional` | `boolean` | - |
| `body.customGitSSHKeyId` | `optional` | `string | null` | - |

### `application-saveGiteaProvider`

- Method: `POST`
- Path: `/application.saveGiteaProvider`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | - |
| `body.giteaBranch` | `required` | `string | null` | - |
| `body.giteaBuildPath` | `required` | `string | null` | - |
| `body.giteaOwner` | `required` | `string | null` | - |
| `body.giteaRepository` | `required` | `string | null` | - |
| `body.giteaId` | `required` | `string | null` | - |
| `body.enableSubmodules` | `optional` | `boolean` | - |
| `body.watchPaths` | `optional` | `array<string> | null` | - |

### `application-saveGithubProvider`

- Method: `POST`
- Path: `/application.saveGithubProvider`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | - |
| `body.repository` | `required` | `string | null` | - |
| `body.branch` | `required` | `string | null` | - |
| `body.owner` | `required` | `string | null` | - |
| `body.buildPath` | `required` | `string | null` | - |
| `body.githubId` | `required` | `string | null` | - |
| `body.triggerType` | `required` | `enum(push, tag)` | default=push |
| `body.enableSubmodules` | `optional` | `boolean` | - |
| `body.watchPaths` | `optional` | `array<string> | null` | - |

### `application-saveGitlabProvider`

- Method: `POST`
- Path: `/application.saveGitlabProvider`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | - |
| `body.gitlabBranch` | `required` | `string | null` | - |
| `body.gitlabBuildPath` | `required` | `string | null` | - |
| `body.gitlabOwner` | `required` | `string | null` | - |
| `body.gitlabRepository` | `required` | `string | null` | - |
| `body.gitlabId` | `required` | `string | null` | - |
| `body.gitlabProjectId` | `required` | `number | null` | - |
| `body.gitlabPathNamespace` | `required` | `string | null` | - |
| `body.enableSubmodules` | `optional` | `boolean` | - |
| `body.watchPaths` | `optional` | `array<string> | null` | - |

### `application-search`

- Method: `GET`
- Path: `/application.search`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `q` | `query` | no | `string` | - |
| `name` | `query` | no | `string` | - |
| `appName` | `query` | no | `string` | - |
| `description` | `query` | no | `string` | - |
| `repository` | `query` | no | `string` | - |
| `owner` | `query` | no | `string` | - |
| `dockerImage` | `query` | no | `string` | - |
| `projectId` | `query` | no | `string` | - |
| `environmentId` | `query` | no | `string` | - |
| `limit` | `query` | no | `number` | minimum=1; maximum=100; default=20 |
| `offset` | `query` | no | `number` | minimum=0; default=0 |

### `application-start`

- Method: `POST`
- Path: `/application.start`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | minLength=1 |

### `application-stop`

- Method: `POST`
- Path: `/application.stop`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | minLength=1 |

### `application-update`

- Method: `POST`
- Path: `/application.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | minLength=1 |
| `body.name` | `optional` | `string` | minLength=1 |
| `body.appName` | `optional` | `string` | minLength=1; maxLength=63; pattern=^[a-zA-Z0-9._-]+$ |
| `body.description` | `optional` | `string | null` | - |
| `body.env` | `optional` | `string | null` | - |
| `body.previewEnv` | `optional` | `string | null` | - |
| `body.watchPaths` | `optional` | `array<string> | null` | - |
| `body.previewBuildArgs` | `optional` | `string | null` | - |
| `body.previewBuildSecrets` | `optional` | `string | null` | - |
| `body.previewLabels` | `optional` | `array<string> | null` | - |
| `body.previewWildcard` | `optional` | `string | null` | - |
| `body.previewPort` | `optional` | `number | null` | - |
| `body.previewHttps` | `optional` | `boolean` | - |
| `body.previewPath` | `optional` | `string | null` | - |
| `body.previewCertificateType` | `optional` | `enum(letsencrypt, none, custom)` | - |
| `body.previewCustomCertResolver` | `optional` | `string | null` | - |
| `body.previewLimit` | `optional` | `number | null` | - |
| `body.isPreviewDeploymentsActive` | `optional` | `boolean | null` | - |
| `body.previewRequireCollaboratorPermissions` | `optional` | `boolean | null` | - |
| `body.rollbackActive` | `optional` | `boolean | null` | - |
| `body.buildArgs` | `optional` | `string | null` | - |
| `body.buildSecrets` | `optional` | `string | null` | - |
| `body.memoryReservation` | `optional` | `string | null` | - |
| `body.memoryLimit` | `optional` | `string | null` | - |
| `body.cpuReservation` | `optional` | `string | null` | - |
| `body.cpuLimit` | `optional` | `string | null` | - |
| `body.title` | `optional` | `string | null` | - |
| `body.enabled` | `optional` | `boolean | null` | - |
| `body.subtitle` | `optional` | `string | null` | - |
| `body.command` | `optional` | `string | null` | - |
| `body.args` | `optional` | `array<string> | null` | - |
| `body.refreshToken` | `optional` | `string | null` | - |
| `body.sourceType` | `optional` | `enum(github, docker, git, gitlab, bitbucket, gitea, ...)` | - |
| `body.cleanCache` | `optional` | `boolean | null` | - |
| `body.repository` | `optional` | `string | null` | - |
| `body.owner` | `optional` | `string | null` | - |
| `body.branch` | `optional` | `string | null` | - |
| `body.buildPath` | `optional` | `string | null` | - |
| `body.triggerType` | `optional` | `enum(push, tag) | null` | - |
| `body.autoDeploy` | `optional` | `boolean | null` | - |
| `body.gitlabProjectId` | `optional` | `number | null` | - |
| `body.gitlabRepository` | `optional` | `string | null` | - |
| `body.gitlabOwner` | `optional` | `string | null` | - |
| `body.gitlabBranch` | `optional` | `string | null` | - |
| `body.gitlabBuildPath` | `optional` | `string | null` | - |
| `body.gitlabPathNamespace` | `optional` | `string | null` | - |
| `body.giteaRepository` | `optional` | `string | null` | - |
| `body.giteaOwner` | `optional` | `string | null` | - |
| `body.giteaBranch` | `optional` | `string | null` | - |
| `body.giteaBuildPath` | `optional` | `string | null` | - |
| `body.bitbucketRepository` | `optional` | `string | null` | - |
| `body.bitbucketRepositorySlug` | `optional` | `string | null` | - |
| `body.bitbucketOwner` | `optional` | `string | null` | - |
| `body.bitbucketBranch` | `optional` | `string | null` | - |
| `body.bitbucketBuildPath` | `optional` | `string | null` | - |
| `body.username` | `optional` | `string | null` | - |
| `body.password` | `optional` | `string | null` | - |
| `body.dockerImage` | `optional` | `string | null` | - |
| `body.registryUrl` | `optional` | `string | null` | - |
| `body.customGitUrl` | `optional` | `string | null` | - |
| `body.customGitBranch` | `optional` | `string | null` | - |
| `body.customGitBuildPath` | `optional` | `string | null` | - |
| `body.customGitSSHKeyId` | `optional` | `string | null` | - |
| `body.enableSubmodules` | `optional` | `boolean` | - |
| `body.dockerfile` | `optional` | `string | null` | - |
| `body.dockerContextPath` | `optional` | `string | null` | - |
| `body.dockerBuildStage` | `optional` | `string | null` | - |
| `body.dropBuildPath` | `optional` | `string | null` | - |
| `body.healthCheckSwarm` | `optional` | `object | null | null` | - |
| `body.restartPolicySwarm` | `optional` | `object | null | null` | - |
| `body.placementSwarm` | `optional` | `object | null | null` | - |
| `body.updateConfigSwarm` | `optional` | `object | null | null` | - |
| `body.rollbackConfigSwarm` | `optional` | `object | null | null` | - |
| `body.modeSwarm` | `optional` | `object | null | null` | - |
| `body.labelsSwarm` | `optional` | `object | null | null` | - |
| `body.networkSwarm` | `optional` | `array<object> | null | null` | - |
| `body.stopGracePeriodSwarm` | `optional` | `integer | null | null` | - |
| `body.endpointSpecSwarm` | `optional` | `object | null | null` | - |
| `body.ulimitsSwarm` | `optional` | `array<object> | null | null` | - |
| `body.replicas` | `optional` | `number` | - |
| `body.applicationStatus` | `optional` | `enum(idle, running, done, error)` | - |
| `body.buildType` | `optional` | `enum(dockerfile, heroku_buildpacks, paketo_buildpacks, nixpacks, static, railpack)` | - |
| `body.railpackVersion` | `optional` | `string | null` | - |
| `body.herokuVersion` | `optional` | `string | null` | - |
| `body.publishDirectory` | `optional` | `string | null` | - |
| `body.isStaticSpa` | `optional` | `boolean | null` | - |
| `body.createEnvFile` | `optional` | `boolean` | - |
| `body.createdAt` | `optional` | `string` | - |
| `body.registryId` | `optional` | `string | null` | - |
| `body.rollbackRegistryId` | `optional` | `string | null` | - |
| `body.environmentId` | `optional` | `string` | - |
| `body.githubId` | `optional` | `string | null` | - |
| `body.gitlabId` | `optional` | `string | null` | - |
| `body.giteaId` | `optional` | `string | null` | - |
| `body.bitbucketId` | `optional` | `string | null` | - |
| `body.buildServerId` | `optional` | `string | null` | - |
| `body.buildRegistryId` | `optional` | `string | null` | - |

### `application-updateTraefikConfig`

- Method: `POST`
- Path: `/application.updateTraefikConfig`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.applicationId` | `required` | `string` | - |
| `body.traefikConfig` | `required` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
