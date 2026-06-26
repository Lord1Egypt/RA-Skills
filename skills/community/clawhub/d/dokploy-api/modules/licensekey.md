# licenseKey module

This module contains `6` endpoints in the `licenseKey` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/licenseKey.activate` | `licenseKey-activate` | `apiKey` | `json` | body.licenseKey | - |
| POST | `/licenseKey.deactivate` | `licenseKey-deactivate` | `apiKey` | `none` | - | - |
| GET | `/licenseKey.getEnterpriseSettings` | `licenseKey-getEnterpriseSettings` | `apiKey` | `none` | - | - |
| GET | `/licenseKey.haveValidLicenseKey` | `licenseKey-haveValidLicenseKey` | `apiKey` | `none` | - | - |
| POST | `/licenseKey.updateEnterpriseSettings` | `licenseKey-updateEnterpriseSettings` | `apiKey` | `json` | - | - |
| POST | `/licenseKey.validate` | `licenseKey-validate` | `apiKey` | `none` | - | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `licenseKey-activate`

- Method: `POST`
- Path: `/licenseKey.activate`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.licenseKey` | `required` | `string` | minLength=1 |

### `licenseKey-deactivate`

- Method: `POST`
- Path: `/licenseKey.deactivate`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `licenseKey-getEnterpriseSettings`

- Method: `GET`
- Path: `/licenseKey.getEnterpriseSettings`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `licenseKey-haveValidLicenseKey`

- Method: `GET`
- Path: `/licenseKey.haveValidLicenseKey`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `licenseKey-updateEnterpriseSettings`

- Method: `POST`
- Path: `/licenseKey.updateEnterpriseSettings`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.enableEnterpriseFeatures` | `optional` | `boolean` | - |

### `licenseKey-validate`

- Method: `POST`
- Path: `/licenseKey.validate`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
