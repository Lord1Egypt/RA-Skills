# stripe module

This module contains `7` endpoints in the `stripe` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/stripe.canCreateMoreServers` | `stripe-canCreateMoreServers` | `apiKey` | `none` | - | - |
| POST | `/stripe.createCheckoutSession` | `stripe-createCheckoutSession` | `apiKey` | `json` | body.tier, body.productId, body.serverQuantity, body.isAnnual | - |
| POST | `/stripe.createCustomerPortalSession` | `stripe-createCustomerPortalSession` | `apiKey` | `none` | - | - |
| GET | `/stripe.getCurrentPlan` | `stripe-getCurrentPlan` | `apiKey` | `none` | - | - |
| GET | `/stripe.getInvoices` | `stripe-getInvoices` | `apiKey` | `none` | - | - |
| GET | `/stripe.getProducts` | `stripe-getProducts` | `apiKey` | `none` | - | - |
| POST | `/stripe.upgradeSubscription` | `stripe-upgradeSubscription` | `apiKey` | `json` | body.tier, body.serverQuantity, body.isAnnual | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `stripe-canCreateMoreServers`

- Method: `GET`
- Path: `/stripe.canCreateMoreServers`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `stripe-createCheckoutSession`

- Method: `POST`
- Path: `/stripe.createCheckoutSession`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.tier` | `required` | `enum(legacy, hobby, startup)` | - |
| `body.productId` | `required` | `string` | - |
| `body.serverQuantity` | `required` | `number` | minimum=1 |
| `body.isAnnual` | `required` | `boolean` | - |

### `stripe-createCustomerPortalSession`

- Method: `POST`
- Path: `/stripe.createCustomerPortalSession`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `stripe-getCurrentPlan`

- Method: `GET`
- Path: `/stripe.getCurrentPlan`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `stripe-getInvoices`

- Method: `GET`
- Path: `/stripe.getInvoices`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `stripe-getProducts`

- Method: `GET`
- Path: `/stripe.getProducts`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `stripe-upgradeSubscription`

- Method: `POST`
- Path: `/stripe.upgradeSubscription`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.tier` | `required` | `enum(hobby, startup)` | - |
| `body.serverQuantity` | `required` | `number` | minimum=1 |
| `body.isAnnual` | `required` | `boolean` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
