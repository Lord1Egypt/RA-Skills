# port module

This module contains `4` endpoints in the `port` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/port.create` | `port-create` | `apiKey` | `json` | body.publishedPort, body.publishMode, body.targetPort, body.protocol, body.applicationId | - |
| POST | `/port.delete` | `port-delete` | `apiKey` | `json` | body.portId | - |
| GET | `/port.one` | `port-one` | `apiKey` | `params` | query.portId | - |
| POST | `/port.update` | `port-update` | `apiKey` | `json` | body.portId, body.publishedPort, body.publishMode, body.targetPort, body.protocol | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `port-create`

- Method: `POST`
- Path: `/port.create`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.publishedPort` | `required` | `number` | - |
| `body.publishMode` | `required` | `enum(ingress, host)` | default=ingress |
| `body.targetPort` | `required` | `number` | - |
| `body.protocol` | `required` | `enum(tcp, udp)` | default=tcp |
| `body.applicationId` | `required` | `string` | minLength=1 |

### `port-delete`

- Method: `POST`
- Path: `/port.delete`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.portId` | `required` | `string` | minLength=1 |

### `port-one`

- Method: `GET`
- Path: `/port.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `portId` | `query` | yes | `string` | minLength=1 |

### `port-update`

- Method: `POST`
- Path: `/port.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.portId` | `required` | `string` | minLength=1 |
| `body.publishedPort` | `required` | `number` | - |
| `body.publishMode` | `required` | `enum(ingress, host)` | default=ingress |
| `body.targetPort` | `required` | `number` | - |
| `body.protocol` | `required` | `enum(tcp, udp)` | default=tcp |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
