# swarm module

This module contains `3` endpoints in the `swarm` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/swarm.getNodeApps` | `swarm-getNodeApps` | `apiKey` | `params` | - | - |
| GET | `/swarm.getNodeInfo` | `swarm-getNodeInfo` | `apiKey` | `params` | query.nodeId | - |
| GET | `/swarm.getNodes` | `swarm-getNodes` | `apiKey` | `params` | - | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `swarm-getNodeApps`

- Method: `GET`
- Path: `/swarm.getNodeApps`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | no | `string` | - |

### `swarm-getNodeInfo`

- Method: `GET`
- Path: `/swarm.getNodeInfo`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `nodeId` | `query` | yes | `string` | - |
| `serverId` | `query` | no | `string` | - |

### `swarm-getNodes`

- Method: `GET`
- Path: `/swarm.getNodes`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `serverId` | `query` | no | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
