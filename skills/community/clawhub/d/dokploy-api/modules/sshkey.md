# sshKey module

This module contains `6` endpoints in the `sshKey` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/sshKey.all` | `sshKey-all` | `apiKey` | `none` | - | - |
| POST | `/sshKey.create` | `sshKey-create` | `apiKey` | `json` | body.name, body.privateKey, body.publicKey, body.organizationId | - |
| POST | `/sshKey.generate` | `sshKey-generate` | `apiKey` | `json` | - | - |
| GET | `/sshKey.one` | `sshKey-one` | `apiKey` | `params` | query.sshKeyId | - |
| POST | `/sshKey.remove` | `sshKey-remove` | `apiKey` | `json` | body.sshKeyId | - |
| POST | `/sshKey.update` | `sshKey-update` | `apiKey` | `json` | body.sshKeyId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `sshKey-all`

- Method: `GET`
- Path: `/sshKey.all`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `sshKey-create`

- Method: `POST`
- Path: `/sshKey.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.description` | `optional` | `string | null` | - |
| `body.privateKey` | `required` | `string` | - |
| `body.publicKey` | `required` | `string` | - |
| `body.organizationId` | `required` | `string` | - |

### `sshKey-generate`

- Method: `POST`
- Path: `/sshKey.generate`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.type` | `optional` | `enum(rsa, ed25519)` | - |

### `sshKey-one`

- Method: `GET`
- Path: `/sshKey.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `sshKeyId` | `query` | yes | `string` | minLength=1 |

### `sshKey-remove`

- Method: `POST`
- Path: `/sshKey.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.sshKeyId` | `required` | `string` | - |

### `sshKey-update`

- Method: `POST`
- Path: `/sshKey.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `optional` | `string` | minLength=1 |
| `body.description` | `optional` | `string | null` | - |
| `body.lastUsedAt` | `optional` | `string | null` | - |
| `body.sshKeyId` | `required` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
