# Browser — CORS and Calling APIs From Frontend Code

## CORS Decoded

- CORS is enforced by the browser alone: curl and server-side code never see it. "Blocked by CORS policy" means the API does not allow browser calls from your origin — for most third-party APIs that is intentional, and the fix is calling from your backend, not fighting the header.
- The console masks the real failure: any response without CORS headers — including a plain 401 or 500 — reports as a "CORS error". Reproduce with curl first (SKILL.md Core Rule 1); if curl shows a normal error, fix that error, the CORS message was noise.
- Preflight: JSON `Content-Type`, an `Authorization` header, or any custom header triggers an OPTIONS request first, and preflights carry no auth — a backend requiring auth on OPTIONS manufactures a fake CORS failure (→ `auth.md` Headers).
- `mode: 'no-cors'` fixes nothing: it returns an opaque response — status 0, unreadable body. It is never the solution to a CORS error.

## Keys Must Not Ship to the Browser

- Anything in frontend code is public: bundles, source maps, and the network tab expose every key to every visitor. A secret key in a React app is a leaked key that hasn't been noticed yet.
- Exceptions exist by design, not by hope: publishable keys (Stripe `pk_*`), domain-restricted keys (Google Maps), anon keys backed by row-level security (Supabase). The provider's docs say which key type is browser-safe; when they don't say, it isn't.
- The pattern for everything else: your backend endpoint holds the secret, receives the browser's request, adds auth, calls the API. Scope it to the operations your frontend needs — a blind pass-through proxy is an open relay spending your quota and your reputation.
- The proxy inherits the client's problems: rate-limit it per user and validate inputs, or one visitor's loop exhausts your provider quota for everyone (→ `rate-limits.md`).

## Tokens in the Browser

- User-facing OAuth: authorization code + PKCE (flow table: `auth.md`). Keep access tokens in memory; persist sessions via an httpOnly cookie against your own backend — a token in localStorage is readable by any injected script.
- Never place tokens in URLs: history, referrer headers, and analytics all capture them (same law as `auth.md` Bearer Token).

## Streaming and Uploads From the Browser

- `EventSource` cannot send an `Authorization` header — authenticated SSE needs fetch + ReadableStream with manual event parsing, under the same buffering laws (→ `streaming.md`).
- Large uploads: have your backend mint a presigned URL, then PUT directly from the browser to storage — the file never transits your server and your function-size limits stop mattering (→ `files.md` Large Files).
