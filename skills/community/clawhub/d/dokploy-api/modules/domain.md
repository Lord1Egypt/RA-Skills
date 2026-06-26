# domain module

This module contains `9` endpoints in the `domain` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/domain.byApplicationId` | `domain-byApplicationId` | `apiKey` | `params` | query.applicationId | - |
| GET | `/domain.byComposeId` | `domain-byComposeId` | `apiKey` | `params` | query.composeId | - |
| GET | `/domain.canGenerateTraefikMeDomains` | `domain-canGenerateTraefikMeDomains` | `apiKey` | `params` | query.serverId | - |
| POST | `/domain.create` | `domain-create` | `apiKey` | `json` | body.host | - |
| POST | `/domain.delete` | `domain-delete` | `apiKey` | `json` | body.domainId | - |
| POST | `/domain.generateDomain` | `domain-generateDomain` | `apiKey` | `json` | body.appName | - |
| GET | `/domain.one` | `domain-one` | `apiKey` | `params` | query.domainId | - |
| POST | `/domain.update` | `domain-update` | `apiKey` | `json` | body.host, body.domainId | - |
| POST | `/domain.validateDomain` | `domain-validateDomain` | `apiKey` | `json` | body.domain | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `domain-byApplicationId`

- Method: `GET`
- Path: `/domain.byApplicationId`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `applicationId` | `query` | yes | `string` | minLength=1 |

### `domain-byComposeId`

- Method: `GET`
- Path: `/domain.byComposeId`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `composeId` | `query` | yes | `string` | minLength=1 |

### `domain-canGenerateTraefikMeDomains`

- Method: `GET`
- Path: `/domain.canGenerateTraefikMeDomains`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | yes | `string` | - |

### `domain-create`

- Method: `POST`
- Path: `/domain.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.host` | `required` | `string` | minLength=1 |
| `body.path` | `optional` | `string | null` | - |
| `body.port` | `optional` | `number | null` | - |
| `body.https` | `optional` | `boolean` | - |
| `body.applicationId` | `optional` | `string | null` | - |
| `body.certificateType` | `optional` | `enum(letsencrypt, none, custom)` | - |
| `body.customCertResolver` | `optional` | `string | null` | - |
| `body.composeId` | `optional` | `string | null` | - |
| `body.serviceName` | `optional` | `string | null` | - |
| `body.domainType` | `optional` | `enum(compose, application, preview) | null` | - |
| `body.previewDeploymentId` | `optional` | `string | null` | - |
| `body.internalPath` | `optional` | `string | null` | - |
| `body.stripPath` | `optional` | `boolean` | - |

### `domain-delete`

- Method: `POST`
- Path: `/domain.delete`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.domainId` | `required` | `string` | minLength=1 |

### `domain-generateDomain`

- Method: `POST`
- Path: `/domain.generateDomain`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appName` | `required` | `string` | - |
| `body.serverId` | `optional` | `string` | - |

### `domain-one`

- Method: `GET`
- Path: `/domain.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `domainId` | `query` | yes | `string` | minLength=1 |

### `domain-update`

- Method: `POST`
- Path: `/domain.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.host` | `required` | `string` | minLength=1 |
| `body.path` | `optional` | `string | null` | - |
| `body.port` | `optional` | `number | null` | - |
| `body.https` | `optional` | `boolean` | - |
| `body.certificateType` | `optional` | `enum(letsencrypt, none, custom)` | - |
| `body.customCertResolver` | `optional` | `string | null` | - |
| `body.serviceName` | `optional` | `string | null` | - |
| `body.domainType` | `optional` | `enum(compose, application, preview) | null` | - |
| `body.internalPath` | `optional` | `string | null` | - |
| `body.stripPath` | `optional` | `boolean` | - |
| `body.domainId` | `required` | `string` | - |

### `domain-validateDomain`

- Method: `POST`
- Path: `/domain.validateDomain`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.domain` | `required` | `string` | - |
| `body.serverIp` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
