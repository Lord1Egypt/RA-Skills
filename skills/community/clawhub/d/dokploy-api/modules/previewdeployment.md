# previewDeployment module

This module contains `4` endpoints in the `previewDeployment` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/previewDeployment.all` | `previewDeployment-all` | `apiKey` | `params` | query.applicationId | - |
| POST | `/previewDeployment.delete` | `previewDeployment-delete` | `apiKey` | `json` | body.previewDeploymentId | - |
| GET | `/previewDeployment.one` | `previewDeployment-one` | `apiKey` | `params` | query.previewDeploymentId | - |
| POST | `/previewDeployment.redeploy` | `previewDeployment-redeploy` | `apiKey` | `json` | body.previewDeploymentId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `previewDeployment-all`

- Method: `GET`
- Path: `/previewDeployment.all`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `applicationId` | `query` | yes | `string` | minLength=1 |

### `previewDeployment-delete`

- Method: `POST`
- Path: `/previewDeployment.delete`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.previewDeploymentId` | `required` | `string` | - |

### `previewDeployment-one`

- Method: `GET`
- Path: `/previewDeployment.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `previewDeploymentId` | `query` | yes | `string` | - |

### `previewDeployment-redeploy`

- Method: `POST`
- Path: `/previewDeployment.redeploy`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.previewDeploymentId` | `required` | `string` | - |
| `body.title` | `optional` | `string` | - |
| `body.description` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
