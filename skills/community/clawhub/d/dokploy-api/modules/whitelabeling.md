# whitelabeling module

This module contains `4` endpoints in the `whitelabeling` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/whitelabeling.get` | `whitelabeling-get` | `apiKey` | `none` | - | - |
| GET | `/whitelabeling.getPublic` | `whitelabeling-getPublic` | `apiKey` | `none` | - | - |
| POST | `/whitelabeling.reset` | `whitelabeling-reset` | `apiKey` | `none` | - | - |
| POST | `/whitelabeling.update` | `whitelabeling-update` | `apiKey` | `json` | body.whitelabelingConfig | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `whitelabeling-get`

- Method: `GET`
- Path: `/whitelabeling.get`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `whitelabeling-getPublic`

- Method: `GET`
- Path: `/whitelabeling.getPublic`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `whitelabeling-reset`

- Method: `POST`
- Path: `/whitelabeling.reset`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `whitelabeling-update`

- Method: `POST`
- Path: `/whitelabeling.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.whitelabelingConfig` | `required` | `object` | - |
| `body.whitelabelingConfig.appName` | `required` | `string | null` | - |
| `body.whitelabelingConfig.appDescription` | `required` | `string | null` | - |
| `body.whitelabelingConfig.logoUrl` | `required` | `string | null` | - |
| `body.whitelabelingConfig.faviconUrl` | `required` | `string | null` | - |
| `body.whitelabelingConfig.customCss` | `required` | `string | null` | - |
| `body.whitelabelingConfig.loginLogoUrl` | `required` | `string | null` | - |
| `body.whitelabelingConfig.supportUrl` | `required` | `string | null` | - |
| `body.whitelabelingConfig.docsUrl` | `required` | `string | null` | - |
| `body.whitelabelingConfig.errorPageTitle` | `required` | `string | null` | - |
| `body.whitelabelingConfig.errorPageDescription` | `required` | `string | null` | - |
| `body.whitelabelingConfig.metaTitle` | `required` | `string | null` | - |
| `body.whitelabelingConfig.footerText` | `required` | `string | null` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
