## BCMS API Basics

This document expands on the high‑level notes from `SKILL.md` and focuses on:

- API key structure and environments
- Client initialisation options
- Recommended security practices

### API keys and environments

- BCMS API keys are used as a **single three‑part string** `keyId.secret.instanceId` (see [BCMS docs](https://thebcms.com/docs)).
- Create **separate keys per environment** (development, staging, production).
- Use dedicated **media / public** keys for browser delivery when possible (second env var with another three‑part key, as in the [Next.js](https://thebcms.com/docs/integrations/next-js) and [Nuxt](https://thebcms.com/docs/integrations/nuxt-js) guides).

**Environment variables** (aligned with [thebcms.com/docs/integrations](https://thebcms.com/docs/integrations)):

- **`BCMS_API_KEY`** — full private key string for server-side `Client` (default when using `new Client({ injectSvg: true })`).
- **Public key** — e.g. `NEXT_PUBLIC_BCMS_API_KEY`, `NUXT_PUBLIC_BCMS_API_KEY`, or `VITE_BCMS_API_KEY` passed as `apiKey: process.env....` / `import.meta.env....` for public clients.

Never commit these values to source control.

### Client initialisation

The official SDK is `@thebcms/client`. Common options:

- `injectSvg`: inline SVG icons directly into returned HTML.
- `useMemCache`: enable in‑memory caching of responses.
- `enableSocket`: toggle real‑time updates over websockets.

[Integration guides](https://thebcms.com/docs/integrations) use the **options‑only** constructor: `new Client({ injectSvg: true })` with `BCMS_API_KEY` set, or `new Client({ apiKey: process.env...., injectSvg: true })` for a public key.

See `SKILL.md` and [`ai/scripts/init-client.ts`](../scripts/init-client.ts) for concise examples.

### General best‑practices

- Rotate API keys regularly.
- Scope keys to the minimum templates/functions/media required.
- Use HTTPS only and validate TLS certificates in production.

Refer to [thebcms.com/docs](https://thebcms.com/docs) for the latest details on authentication and client configuration.
