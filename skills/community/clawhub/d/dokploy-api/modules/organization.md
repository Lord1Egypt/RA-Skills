# organization module

This module contains `10` endpoints in the `organization` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/organization.active` | `organization-active` | `apiKey` | `none` | - | - |
| GET | `/organization.all` | `organization-all` | `apiKey` | `none` | - | - |
| GET | `/organization.allInvitations` | `organization-allInvitations` | `apiKey` | `none` | - | - |
| POST | `/organization.create` | `organization-create` | `apiKey` | `json` | body.name | - |
| POST | `/organization.delete` | `organization-delete` | `apiKey` | `json` | body.organizationId | - |
| GET | `/organization.one` | `organization-one` | `apiKey` | `params` | query.organizationId | - |
| POST | `/organization.removeInvitation` | `organization-removeInvitation` | `apiKey` | `json` | body.invitationId | - |
| POST | `/organization.setDefault` | `organization-setDefault` | `apiKey` | `json` | body.organizationId | - |
| POST | `/organization.update` | `organization-update` | `apiKey` | `json` | body.organizationId, body.name | - |
| POST | `/organization.updateMemberRole` | `organization-updateMemberRole` | `apiKey` | `json` | body.memberId, body.role | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `organization-active`

- Method: `GET`
- Path: `/organization.active`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `organization-all`

- Method: `GET`
- Path: `/organization.all`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `organization-allInvitations`

- Method: `GET`
- Path: `/organization.allInvitations`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `organization-create`

- Method: `POST`
- Path: `/organization.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | - |
| `body.logo` | `optional` | `string` | - |

### `organization-delete`

- Method: `POST`
- Path: `/organization.delete`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.organizationId` | `required` | `string` | - |

### `organization-one`

- Method: `GET`
- Path: `/organization.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `organizationId` | `query` | yes | `string` | - |

### `organization-removeInvitation`

- Method: `POST`
- Path: `/organization.removeInvitation`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.invitationId` | `required` | `string` | - |

### `organization-setDefault`

- Method: `POST`
- Path: `/organization.setDefault`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.organizationId` | `required` | `string` | minLength=1 |

### `organization-update`

- Method: `POST`
- Path: `/organization.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.organizationId` | `required` | `string` | - |
| `body.name` | `required` | `string` | - |
| `body.logo` | `optional` | `string` | - |

### `organization-updateMemberRole`

- Method: `POST`
- Path: `/organization.updateMemberRole`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.memberId` | `required` | `string` | - |
| `body.role` | `required` | `enum(admin, member)` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
