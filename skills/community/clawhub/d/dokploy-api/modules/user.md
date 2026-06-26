# user module

This module contains `19` endpoints in the `user` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/user.all` | `user-all` | `apiKey` | `none` | - | - |
| POST | `/user.assignPermissions` | `user-assignPermissions` | `apiKey` | `json` | body.id, body.accessedProjects, body.accessedEnvironments, body.accessedServices, body.canCreateProjects, body.canCreateServices, body.canDeleteProjects, body.canDeleteServices, body.canAccessToDocker, body.canAccessToTraefikFiles, body.canAccessToAPI, body.canAccessToSSHKeys, body.canAccessToGitProviders, body.canDeleteEnvironments, body.canCreateEnvironments | - |
| GET | `/user.checkUserOrganizations` | `user-checkUserOrganizations` | `apiKey` | `params` | query.userId | - |
| POST | `/user.createApiKey` | `user-createApiKey` | `apiKey` | `json` | body.name, body.metadata | - |
| POST | `/user.deleteApiKey` | `user-deleteApiKey` | `apiKey` | `json` | body.apiKeyId | - |
| POST | `/user.generateToken` | `user-generateToken` | `apiKey` | `none` | - | - |
| GET | `/user.get` | `user-get` | `apiKey` | `none` | - | - |
| GET | `/user.getBackups` | `user-getBackups` | `apiKey` | `none` | - | - |
| GET | `/user.getContainerMetrics` | `user-getContainerMetrics` | `apiKey` | `params` | query.url, query.token, query.appName, query.dataPoints | - |
| GET | `/user.getInvitations` | `user-getInvitations` | `apiKey` | `none` | - | - |
| GET | `/user.getMetricsToken` | `user-getMetricsToken` | `apiKey` | `none` | - | - |
| GET | `/user.getServerMetrics` | `user-getServerMetrics` | `apiKey` | `none` | - | - |
| GET | `/user.getUserByToken` | `user-getUserByToken` | `apiKey` | `params` | query.token | - |
| GET | `/user.haveRootAccess` | `user-haveRootAccess` | `apiKey` | `none` | - | - |
| GET | `/user.one` | `user-one` | `apiKey` | `params` | query.userId | - |
| POST | `/user.remove` | `user-remove` | `apiKey` | `json` | body.userId | - |
| POST | `/user.sendInvitation` | `user-sendInvitation` | `apiKey` | `json` | body.invitationId, body.notificationId | - |
| GET | `/user.session` | `user-session` | `apiKey` | `none` | - | - |
| POST | `/user.update` | `user-update` | `apiKey` | `json` | - | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `user-all`

- Method: `GET`
- Path: `/user.all`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `user-assignPermissions`

- Method: `POST`
- Path: `/user.assignPermissions`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.id` | `required` | `string` | minLength=1 |
| `body.accessedProjects` | `required` | `array<string>` | - |
| `body.accessedProjects[]` | `required` | `string` | - |
| `body.accessedEnvironments` | `required` | `array<string>` | - |
| `body.accessedEnvironments[]` | `required` | `string` | - |
| `body.accessedServices` | `required` | `array<string>` | - |
| `body.accessedServices[]` | `required` | `string` | - |
| `body.canCreateProjects` | `required` | `boolean` | - |
| `body.canCreateServices` | `required` | `boolean` | - |
| `body.canDeleteProjects` | `required` | `boolean` | - |
| `body.canDeleteServices` | `required` | `boolean` | - |
| `body.canAccessToDocker` | `required` | `boolean` | - |
| `body.canAccessToTraefikFiles` | `required` | `boolean` | - |
| `body.canAccessToAPI` | `required` | `boolean` | - |
| `body.canAccessToSSHKeys` | `required` | `boolean` | - |
| `body.canAccessToGitProviders` | `required` | `boolean` | - |
| `body.canDeleteEnvironments` | `required` | `boolean` | - |
| `body.canCreateEnvironments` | `required` | `boolean` | - |

### `user-checkUserOrganizations`

- Method: `GET`
- Path: `/user.checkUserOrganizations`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `userId` | `query` | yes | `string` | - |

### `user-createApiKey`

- Method: `POST`
- Path: `/user.createApiKey`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.prefix` | `optional` | `string` | - |
| `body.expiresIn` | `optional` | `number` | - |
| `body.metadata` | `required` | `object` | - |
| `body.metadata.organizationId` | `required` | `string` | - |
| `body.rateLimitEnabled` | `optional` | `boolean` | - |
| `body.rateLimitTimeWindow` | `optional` | `number` | - |
| `body.rateLimitMax` | `optional` | `number` | - |
| `body.remaining` | `optional` | `number` | - |
| `body.refillAmount` | `optional` | `number` | - |
| `body.refillInterval` | `optional` | `number` | - |

### `user-deleteApiKey`

- Method: `POST`
- Path: `/user.deleteApiKey`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.apiKeyId` | `required` | `string` | - |

### `user-generateToken`

- Method: `POST`
- Path: `/user.generateToken`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `user-get`

- Method: `GET`
- Path: `/user.get`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `user-getBackups`

- Method: `GET`
- Path: `/user.getBackups`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `user-getContainerMetrics`

- Method: `GET`
- Path: `/user.getContainerMetrics`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `url` | `query` | yes | `string` | - |
| `token` | `query` | yes | `string` | - |
| `appName` | `query` | yes | `string` | - |
| `dataPoints` | `query` | yes | `string` | - |

### `user-getInvitations`

- Method: `GET`
- Path: `/user.getInvitations`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `user-getMetricsToken`

- Method: `GET`
- Path: `/user.getMetricsToken`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `user-getServerMetrics`

- Method: `GET`
- Path: `/user.getServerMetrics`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `user-getUserByToken`

- Method: `GET`
- Path: `/user.getUserByToken`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `token` | `query` | yes | `string` | minLength=1 |

### `user-haveRootAccess`

- Method: `GET`
- Path: `/user.haveRootAccess`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `user-one`

- Method: `GET`
- Path: `/user.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `userId` | `query` | yes | `string` | - |

### `user-remove`

- Method: `POST`
- Path: `/user.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.userId` | `required` | `string` | - |

### `user-sendInvitation`

- Method: `POST`
- Path: `/user.sendInvitation`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.invitationId` | `required` | `string` | minLength=1 |
| `body.notificationId` | `required` | `string` | minLength=1 |

### `user-session`

- Method: `GET`
- Path: `/user.session`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `user-update`

- Method: `POST`
- Path: `/user.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.id` | `optional` | `string` | minLength=1 |
| `body.firstName` | `optional` | `string` | - |
| `body.lastName` | `optional` | `string` | - |
| `body.isRegistered` | `optional` | `boolean` | - |
| `body.expirationDate` | `optional` | `string` | - |
| `body.createdAt2` | `optional` | `string` | - |
| `body.createdAt` | `optional` | `string | null` | - |
| `body.twoFactorEnabled` | `optional` | `boolean | null` | - |
| `body.email` | `optional` | `string` | format=email; minLength=1; pattern=^(?!\.)(?!.*\.\.)([A-Za-z0-9_'+\-\.]*)[A-Za-z0-9_+-]@([A-Za-z0-9][A-Za-z0-9\-]*\.)+[A-Za-z]{2,}$ |
| `body.emailVerified` | `optional` | `boolean` | - |
| `body.image` | `optional` | `string | null` | - |
| `body.banned` | `optional` | `boolean | null` | - |
| `body.banReason` | `optional` | `string | null` | - |
| `body.banExpires` | `optional` | `string | null` | - |
| `body.updatedAt` | `optional` | `string` | - |
| `body.enablePaidFeatures` | `optional` | `boolean` | - |
| `body.allowImpersonation` | `optional` | `boolean` | - |
| `body.enableEnterpriseFeatures` | `optional` | `boolean` | - |
| `body.licenseKey` | `optional` | `string | null` | - |
| `body.stripeCustomerId` | `optional` | `string | null` | - |
| `body.stripeSubscriptionId` | `optional` | `string | null` | - |
| `body.serversQuantity` | `optional` | `number` | - |
| `body.password` | `optional` | `string` | - |
| `body.currentPassword` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
