# Event Spec

## Shape

Create a JSON file accepted by `POST /v1/projects/{projectId}/event-schemas`:

```json
{
  "eventType": "payment.success",
  "fields": {
    "orderId": { "type": "string", "required": true },
    "amount": { "type": "number", "required": true },
    "currency": {
      "type": "enum",
      "required": true,
      "values": ["CNY", "USD"]
    },
    "product": { "type": "string" },
    "customer": { "type": "string", "sensitive": true }
  },
  "notification": {
    "title": "{{ product | default: 'Payment received' }}",
    "body": "{{ currency }} {{ amount }}",
    "sound": "default",
    "group": "revenue",
    "priority": "normal"
  }
}
```

## Field types

Use only `string`, `number`, `boolean`, `datetime`, `url`, and `enum`. Enum fields require a non-empty string `values` array. Field names must start with a letter and contain only letters, digits, and underscores.

Unknown event fields are rejected. Keep the schema deliberately small.

## Templates

Templates support field interpolation and a quoted default value:

```text
{{ product }}
{{ product | default: 'New event' }}
```

Templates cannot reference fields marked `sensitive`. Keep titles below 80 visible characters and bodies below 180 even though the API accepts up to 240.

## Test event

```json
{
  "type": "payment.success",
  "data": {
    "orderId": "ord_test_1721466000",
    "amount": 28,
    "currency": "CNY",
    "product": "VideoSays Pro"
  },
  "occurredAt": "2026-07-20T09:30:00Z"
}
```

Use clearly synthetic identifiers and no real customer data in test events.
