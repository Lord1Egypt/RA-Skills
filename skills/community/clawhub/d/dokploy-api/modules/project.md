# project module

This module contains `8` endpoints in the `project` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/project.all` | `project-all` | `apiKey` | `none` | - | - |
| GET | `/project.allForPermissions` | `project-allForPermissions` | `apiKey` | `none` | - | - |
| POST | `/project.create` | `project-create` | `apiKey` | `json` | body.name | - |
| POST | `/project.duplicate` | `project-duplicate` | `apiKey` | `json` | body.sourceEnvironmentId, body.name | - |
| GET | `/project.one` | `project-one` | `apiKey` | `params` | query.projectId | - |
| POST | `/project.remove` | `project-remove` | `apiKey` | `json` | body.projectId | - |
| GET | `/project.search` | `project-search` | `apiKey` | `params` | - | - |
| POST | `/project.update` | `project-update` | `apiKey` | `json` | body.projectId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `project-all`

- Method: `GET`
- Path: `/project.all`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `project-allForPermissions`

- Method: `GET`
- Path: `/project.allForPermissions`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `project-create`

- Method: `POST`
- Path: `/project.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.name` | `required` | `string` | minLength=1 |
| `body.description` | `optional` | `string | null` | - |
| `body.env` | `optional` | `string` | - |

### `project-duplicate`

- Method: `POST`
- Path: `/project.duplicate`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.sourceEnvironmentId` | `required` | `string` | - |
| `body.name` | `required` | `string` | - |
| `body.description` | `optional` | `string` | - |
| `body.includeServices` | `optional` | `boolean` | default=True |
| `body.selectedServices` | `optional` | `array<object>` | - |
| `body.selectedServices[].id` | `required-if-body-present` | `string` | - |
| `body.selectedServices[].type` | `required-if-body-present` | `enum(application, postgres, mariadb, mongo, mysql, redis, ...)` | - |
| `body.duplicateInSameProject` | `optional` | `boolean` | default=False |

### `project-one`

- Method: `GET`
- Path: `/project.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `projectId` | `query` | yes | `string` | minLength=1 |

### `project-remove`

- Method: `POST`
- Path: `/project.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.projectId` | `required` | `string` | minLength=1 |

### `project-search`

- Method: `GET`
- Path: `/project.search`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `q` | `query` | no | `string` | - |
| `name` | `query` | no | `string` | - |
| `description` | `query` | no | `string` | - |
| `limit` | `query` | no | `number` | minimum=1; maximum=100; default=20 |
| `offset` | `query` | no | `number` | minimum=0; default=0 |

### `project-update`

- Method: `POST`
- Path: `/project.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.projectId` | `required` | `string` | minLength=1 |
| `body.name` | `optional` | `string` | minLength=1 |
| `body.description` | `optional` | `string | null` | - |
| `body.createdAt` | `optional` | `string` | - |
| `body.organizationId` | `optional` | `string` | - |
| `body.env` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
