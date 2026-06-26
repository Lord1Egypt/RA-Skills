# cluster module

This module contains `4` endpoints in the `cluster` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/cluster.addManager` | `cluster-addManager` | `apiKey` | `params` | - | - |
| GET | `/cluster.addWorker` | `cluster-addWorker` | `apiKey` | `params` | - | - |
| GET | `/cluster.getNodes` | `cluster-getNodes` | `apiKey` | `params` | - | - |
| POST | `/cluster.removeWorker` | `cluster-removeWorker` | `apiKey` | `json` | body.nodeId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `cluster-addManager`

- Method: `GET`
- Path: `/cluster.addManager`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | no | `string` | - |

### `cluster-addWorker`

- Method: `GET`
- Path: `/cluster.addWorker`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | no | `string` | - |

### `cluster-getNodes`

- Method: `GET`
- Path: `/cluster.getNodes`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | no | `string` | - |

### `cluster-removeWorker`

- Method: `POST`
- Path: `/cluster.removeWorker`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.nodeId` | `required` | `string` | - |
| `body.serverId` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
