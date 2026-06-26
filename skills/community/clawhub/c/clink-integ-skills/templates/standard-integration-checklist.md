# Standard Integration Checklist

- Confirm backend stack: {{STACK_NOTE}}
- Confirm product mode: registered or non-registered
- Create or confirm local merchant order before checkout session creation
- Map merchant `order_id` to `merchantReferenceId`
- Implement merchant-side idempotency outside Clink
- Decide checkout vs customer portal for subscription-aware paths
- Configure `CLINK_SECRET_KEY` from `Merchant Dashboard > Developers > API Keys` by clicking `Initialize Key`, copying the Secret Key once, and storing it securely
- Configure dashboard webhook subscriptions and endpoint registration
- Configure `CLINK_WEBHOOK_SIGNING_KEY` from `Merchant Dashboard > Developers > Webhooks` by registering or selecting the HTTPS endpoint and copying the endpoint signing key
- Verify `X-Clink-Timestamp` and `X-Clink-Signature`
- Handle idempotency, retry safety, and out-of-order delivery
- Separate payment confirmation from downstream merchant fulfillment
- Model refund as a lifecycle, not as a guaranteed public create API
