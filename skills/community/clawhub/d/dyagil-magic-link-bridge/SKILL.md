---
name: dyagil-magic-link-bridge
description: Generate Supabase magic-links that land directly on a custom portal subpath (e.g. `/portal/`) instead of being silently rewritten to the project Site URL by Supabase's redirect whitelist. Use whenever a customer reports the login link sent them to the homepage instead of their personal area, or when designing a new magic-link flow on a subpath, or to work around in-app browser bugs (WhatsApp/Instagram WebView) that drop URL hash fragments.
version: 1.0.0
license: MIT
author: dyagil
---

# Magic-Link Bridge (token_hash flow)

## Problem This Solves

Supabase's standard magic-link flow:

1. Server calls `auth.admin.generate_link({ type: 'magiclink', email, options: { redirect_to: 'https://site/portal/' } })`.
2. Customer clicks the resulting `https://<ref>.supabase.co/auth/v1/verify?...` URL.
3. Supabase verifies, then 302-redirects to `redirect_to` **with** `#access_token=<jwt>&type=magiclink` in the URL fragment.

This breaks in two real-world scenarios:

- **Redirect not whitelisted.** If `https://site/portal/` is not in the project's Redirect URL allow-list, Supabase silently rewrites the redirect to the Site URL (`https://site/`). The customer lands on the marketing homepage with a hash full of tokens — and your portal code never sees them.
- **WhatsApp / Instagram / FB Messenger in-app browsers.** WebViews routinely strip URL fragments across navigations, so even when the redirect IS whitelisted the tokens vanish before your JS can read them.

## Fix

Don't go through Supabase's `/auth/v1/verify` endpoint at all. Generate the link manually so it lands directly on the portal page, then have the portal exchange the token via `auth.verifyOtp({ token_hash, type })`.

The final link looks like:

```
https://site/portal/?token_hash=<hashed_token>&type=magiclink
```

`hashed_token` comes from the same `admin/generate_link` response — Supabase returns it alongside `action_link`.

## Server (API endpoint)

```js
// POST /api/send-portal-link  (Vercel serverless or any backend)
const gen = await fetch(
  `${SUPABASE_URL}/auth/v1/admin/generate_link`,
  {
    method: 'POST',
    headers: {
      apikey: SUPABASE_SERVICE_ROLE_KEY,
      Authorization: 'Bearer ' + SUPABASE_SERVICE_ROLE_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ type: 'magiclink', email: customer.email }),
  }
).then(r => r.json());

const u = new URL('https://site/portal/');
u.searchParams.set('token_hash', gen.hashed_token);
u.searchParams.set('type',       gen.verification_type || 'magiclink');
const magicLink = u.toString();

// Send magicLink via WhatsApp / SMS / email. The portal page handles the rest.
```

Keep a fallback to `gen.action_link` if `hashed_token` is missing — some older Supabase auth versions don't return it.

## Client (portal page)

The portal page must:

1. Detect `?token_hash=...&type=...` on load.
2. Call `verifyOtp({ token_hash, type })`.
3. Strip the params from the URL (they're single-use; a refresh would replay them).
4. Handle `?error=...` / `?error_description=...` with a friendly alert.

See [scripts/portal-bridge.js](scripts/portal-bridge.js) for a drop-in snippet.

The Supabase client itself should be configured with:

```js
window.supabase.createClient(URL, ANON_KEY, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,   // picks up hash-fragment flows automatically
    flowType: 'pkce',           // ?code=... flow as well
    storageKey: 'site-portal-auth',
  },
});
```

## Why Also Keep a Bridge in `/index.html`?

Even after deploying this skill, an older email/SMS may still hold a Supabase-style verify URL that was minted before the fix. Add a safety net at the site root that detects either `#access_token=` (hash flow) or `?code=`/`?error=` (PKCE / error redirects) and forwards to `/portal/`. See [scripts/index-redirect.js](scripts/index-redirect.js).

## Testing

1. Generate a link as admin (curl with `service_role`).
2. Open it headless (curl / Playwright) and confirm it lands on `/portal/` with the user logged in (Supabase session present in `localStorage`).
3. If the page shows `#access_token=...` on the homepage instead — the bridge in `index.html` is missing or stale, not this server-side fix.

## Common Pitfalls

- **One-time tokens replay on refresh.** Always strip the query params after `verifyOtp` succeeds, with `history.replaceState`. Otherwise refreshing the page tries to verify a now-expired token and shows an error.
- **PKCE state must match.** `flowType: 'pkce'` requires the same browser to generate and consume the code — so `?code=` flows only work when the link is opened in the same browser that initiated the auth. Magic links opened in a different browser must use the `token_hash` path (default).
- **Hash + query both present.** When forwarding from `index.html`, concatenate as `'/portal/' + window.location.search + window.location.hash` so neither half is lost.
