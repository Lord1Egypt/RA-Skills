# certificates module

This module contains `4` endpoints in the `certificates` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/certificates.all` | `certificates-all` | `apiKey` | `none` | - | - |
| POST | `/certificates.create` | `certificates-create` | `apiKey` | `json` | body.name, body.certificateData, body.privateKey, body.organizationId | - |
| GET | `/certificates.one` | `certificates-one` | `apiKey` | `params` | query.certificateId | - |
| POST | `/certificates.remove` | `certificates-remove` | `apiKey` | `json` | body.certificateId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `certificates-all`

- Method: `GET`
- Path: `/certificates.all`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `certificates-create`

- Method: `POST`
- Path: `/certificates.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.certificateId` | `optional` | `string` | - |
| `body.name` | `required` | `string` | minLength=1 |
| `body.certificateData` | `required` | `string` | minLength=1 |
| `body.privateKey` | `required` | `string` | minLength=1 |
| `body.certificatePath` | `optional` | `string` | - |
| `body.autoRenew` | `optional` | `boolean | null` | - |
| `body.organizationId` | `required` | `string` | - |
| `body.serverId` | `optional` | `string | null` | - |

### `certificates-one`

- Method: `GET`
- Path: `/certificates.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `certificateId` | `query` | yes | `string` | minLength=1 |

### `certificates-remove`

- Method: `POST`
- Path: `/certificates.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.certificateId` | `required` | `string` | minLength=1 |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
