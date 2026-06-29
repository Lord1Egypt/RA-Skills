# No-Secret Policy

Default operation uses no API keys, cookies, sessions, payment credentials, or account tokens.

Rules:

- Do not read `.env` files.
- Do not print environment variables.
- Do not persist request headers.
- Do not store cookies.
- Do not store GitHub tokens if a token is later used for rate-limit expansion.
- Do not include user IDs, private account metadata, invoices, payment links, or KYC information in snapshots.

If a future paid hosted API is added, it must live outside this free skill and use a separate secret boundary.
