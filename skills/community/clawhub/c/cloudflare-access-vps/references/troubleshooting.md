# Cloudflare Access Troubleshooting

## "Access Denied" After Successful Login

**Symptom:** User logs in, Cloudflare shows a success screen, then immediately shows "Access Denied."

**Cause:** The Access policy `Include` rule doesn't match the authenticated identity.

**Fix:**
1. Zero Trust → Access → Applications → [app] → Edit → Policies
2. Check the Include rule — is the email/domain exactly right?
3. For email OTP: the email used to log in must match the policy exactly (case-sensitive)
4. For Google SSO: confirm the Google identity provider is enabled in Settings → Authentication
5. Add a catch-all for testing: Include → Everyone (then tighten after confirming Access works)

---

## WebSocket Connection Fails After Adding Access

**Symptom:** OpenClaw UI loads (GET requests pass), but the WebSocket fails to connect. Error in browser console: `WebSocket connection failed` or `401`.

**Cause:** Browser WebSocket upgrade requests don't automatically send the Cloudflare Access JWT cookie. Cloudflare Access uses a cookie (`CF_Authorization`) set at the browser level — this IS sent automatically on same-origin WebSocket connections from an authenticated browser session.

**If the WS still fails:**
1. Confirm you're using `wss://` not `ws://` — Cloudflare requires TLS
2. Clear browser cookies and re-authenticate through Access
3. Check the Access Application session hasn't expired (Zero Trust → Applications → session duration)
4. If using a native/CLI client (not a browser), use a Service Token instead — see `service-tokens.md`

---

## Service Token Not Working

**Symptom:** Requests with `CF-Access-Client-Id` / `CF-Access-Client-Secret` headers return 403.

**Checklist:**
1. Both headers present? (`CF-Access-Client-Id` AND `CF-Access-Client-Secret`)
2. The Client ID ends in `.access` (e.g. `abc123.access`) — include the `.access` suffix
3. A policy exists on the application that explicitly allows this service token (not just the human login policy)
4. Token hasn't been revoked: Zero Trust → Access → Service Auth → confirm token is listed as active
5. The application domain matches exactly — service tokens are scoped per application

---

## Cloudflare Access Blocks the OpenClaw `?token=` URL

**Symptom:** Sharing a pre-authenticated URL like `https://koda.teamplayers.ai?token=abc` doesn't work because Cloudflare intercepts before the `?token=` reaches OpenClaw.

**Behavior:** This is correct and expected. Cloudflare Access runs before the request reaches OpenClaw. Users must authenticate through Access first, then OpenClaw's token can be entered in the UI or pre-filled after the Cloudflare session is established.

**Workaround for setup links:** Share the URL without the token. After the user logs into Cloudflare Access, they can enter the OpenClaw token in the connection screen.

---

## "Loop Detected" or Infinite Redirect

**Symptom:** Browser redirects infinitely between the Access login page and the application URL.

**Cause:** Usually caused by cookie settings or the application path matching too broadly.

**Fix:**
1. Ensure cookies are allowed for `*.cloudflareaccess.com` and your domain
2. Check if a path-based policy is conflicting with the root application policy
3. Try in a private window with extensions disabled (ad blockers can interfere with cookie setting)
4. Zero Trust → Settings → Custom Pages — check if a custom login page is misconfigured

---

## Bypassing Access for Local Development

Cloudflare Access only applies to traffic routed through Cloudflare. Local connections to `localhost:18789` bypass Access entirely.

```bash
# Direct localhost connection — no Access check
curl http://localhost:18789/api/health \
  -H "Authorization: Bearer <openclaw-token>"
```

For CLI tools on the VPS itself, use `gateway.mode = "local"` in `openclaw.json` so the CLI connects directly to `localhost:18789`.

---

## Checking Access Logs

**Zero Trust → Logs → Access** shows every authentication event:
- Who authenticated (email/identity)
- When
- What application they accessed
- Whether service token or human login
- Rejection reasons

Use this to debug policy mismatches and confirm service tokens are (or aren't) being used.

---

## Removing Access (Rollback)

To disable Cloudflare Access without affecting the tunnel:

1. Zero Trust → Access → Applications → [app] → Edit
2. Change the policy Action from **Allow** to **Bypass** for `Everyone`
   — OR —
   Delete the application entirely

Traffic flows through the tunnel without any authentication check. OpenClaw token + pairing remain active as the only auth layers.
