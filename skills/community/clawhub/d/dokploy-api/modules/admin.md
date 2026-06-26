# admin module

This module contains `1` endpoints in the `admin` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/admin.setupMonitoring` | `admin-setupMonitoring` | `apiKey` | `json` | body.metricsConfig | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `admin-setupMonitoring`

- Method: `POST`
- Path: `/admin.setupMonitoring`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.metricsConfig` | `required` | `object` | - |
| `body.metricsConfig.server` | `required` | `object` | - |
| `body.metricsConfig.server.refreshRate` | `required` | `number` | minimum=2 |
| `body.metricsConfig.server.port` | `required` | `number` | minimum=1 |
| `body.metricsConfig.server.token` | `required` | `string` | - |
| `body.metricsConfig.server.urlCallback` | `required` | `string` | format=uri |
| `body.metricsConfig.server.retentionDays` | `required` | `number` | minimum=1 |
| `body.metricsConfig.server.cronJob` | `required` | `string` | minLength=1 |
| `body.metricsConfig.server.thresholds` | `required` | `object` | - |
| `body.metricsConfig.server.thresholds.cpu` | `required` | `number` | minimum=0 |
| `body.metricsConfig.server.thresholds.memory` | `required` | `number` | minimum=0 |
| `body.metricsConfig.containers` | `required` | `object` | - |
| `body.metricsConfig.containers.refreshRate` | `required` | `number` | minimum=2 |
| `body.metricsConfig.containers.services` | `required` | `object` | - |
| `body.metricsConfig.containers.services.include` | `optional` | `array<string>` | - |
| `body.metricsConfig.containers.services.include[]` | `optional` | `string` | - |
| `body.metricsConfig.containers.services.exclude` | `optional` | `array<string>` | - |
| `body.metricsConfig.containers.services.exclude[]` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
