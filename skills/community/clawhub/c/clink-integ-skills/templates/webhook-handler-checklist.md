# Webhook Handler Checklist

- Subscribe to required events in `Merchant Dashboard > Developers > Webhooks`
- Register the HTTPS webhook endpoint
- Obtain the webhook signing key from `Merchant Dashboard > Developers > Webhooks` by selecting the registered endpoint, then store it securely as `CLINK_WEBHOOK_SIGNING_KEY`
- Verify `X-Clink-Timestamp`
- Verify `X-Clink-Signature`
- Preserve the raw event body before JSON parsing
- Verify HMAC SHA-256 over `X-Clink-Timestamp + "." + raw event body` with the webhook signing key
- Reject stale or replayed deliveries
- Make processing idempotent
- Handle retries safely
- Tolerate out-of-order event delivery
- Reconcile merchant order and refund state after webhook processing
