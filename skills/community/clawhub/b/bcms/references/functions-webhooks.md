## BCMS Functions and Webhooks

This document gives more detail about BCMS serverless functions and webhooks.

### Functions

- Functions are **Node.js handlers** that run inside BCMS.
- They are invoked via REST endpoints under `/api/{instanceId}/fn/{functionId}/call`.
- They return JSON responses and can perform arbitrary business logic.

Best‑practices:

- Keep functions small, focused and composable.
- Validate all inputs and reject malformed payloads.
- Use environment variables for secrets and external service credentials.
- Implement consistent error handling (structured JSON error responses).

See `scripts/call-function.ts` for a concrete example of invoking a function from a client.

### Webhooks

- Webhooks notify external services about BCMS events (e.g., entry created/updated/deleted, media changes).
- Triggers typically follow a **scope:type** pattern and can be configured per template or resource.

Security recommendations:

- Verify the `X-Bcms-Webhook-Signature` header using a shared secret.
- Reject requests that are too old to mitigate replay attacks.
- Make handlers idempotent; repeated delivery must not corrupt state.
- Apply rate limiting or backoff if many events arrive quickly.

Use this document in combination with the main `SKILL.md` guidelines and the official BCMS webhook documentation for precise trigger lists and payload formats.
