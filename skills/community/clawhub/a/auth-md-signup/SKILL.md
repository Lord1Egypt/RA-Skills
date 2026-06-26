---
name: auth-md-signup
description: Complete an auth.md USER-CLAIMED signup (OTP flow) against any service that publishes the auth.md protocol. Consent-preserving — the human confirms the OTP; the agent never auto-confirms. Reference implementation targets NoForm (noform.dev).
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - jq
    envVars:
      - name: AUTH_MD_TOKEN_STORE
        required: false
        description: >
          Path to a JSON file where scoped service tokens are persisted across
          sessions (e.g. ~/.openclaw/auth-md-tokens.json). When unset the skill
          stores tokens in memory only for the current session.
    emoji: "🔑"
    homepage: https://noform.dev
---

# auth-md-signup

> Attributed to [NoForm](https://noform.dev) — the reference implementation for the [auth.md protocol](https://workos.com/auth-md).
> Protocol spec: <https://github.com/workos/auth.md> (MIT)

Teach the agent to complete an **auth.md user-claimed signup** against any
service that publishes the protocol.  The human confirms the one-time code;
the agent never auto-confirms.  That human step IS the consent gate — preserve it.

---

## When to activate this skill

Use this skill when **any** of these are true:

1. A service returns `HTTP 401` carrying:
   ```
   WWW-Authenticate: Bearer resource_metadata="<url>"
   ```
2. The user says "sign me up for `<service>`" and you can resolve an `auth.md`
   file at that service's domain or at a NoForm slug URL.
3. You need a scoped credential for a service before you can proceed, and no
   credential exists yet.

Do NOT use this skill for the **agent-verified / ID-JAG flow** (that is a
different flow requiring a provider-signed assertion).  This skill implements
**only** the `user-claimed` (anonymous-register → email-OTP → claim/complete)
flow as mandated by the mission constraints.

---

## NoForm as the reference target

When the user says "sign me up on NoForm" or supplies a NoForm slug (`<slug>`),
the URL structure is:

```
auth.md file    →  GET  https://noform.dev/a/<slug>/auth.md
PRM             →  GET  https://noform.dev/a/<slug>/.well-known/oauth-protected-resource
AS metadata     →  GET  <authorization_server>/.well-known/oauth-authorization-server
```

Parse the `agent_auth` block from the AS metadata to get `identity_endpoint`
(or `register_uri`), `claim_endpoint` (or `claim_uri`), and `revocation_uri`.
NoForm is the reference; for any other service follow the same discovery chain
from their domain.

---

## Step-by-step execution

### Step 0 — Resolve the service root

- If you have a `WWW-Authenticate: Bearer resource_metadata="<prm_url>"` header,
  extract `<prm_url>` directly (skip to Step 2).
- If you have a domain or NoForm slug, construct the conventional PRM URL:
  `https://<domain>/.well-known/oauth-protected-resource`
- If you have a NoForm slug only:
  `https://noform.dev/a/<slug>/.well-known/oauth-protected-resource`

### Step 1 — Fetch auth.md (optional human-readable context)

```bash
curl -sS "https://<domain>/auth.md"
# or for NoForm:
curl -sS "https://noform.dev/a/<slug>/auth.md"
```

Parse it as prose context. The authoritative machine-readable state is the PRM
and AS metadata — if anything conflicts, the metadata wins.

### Step 2 — Fetch Protected Resource Metadata (PRM)

```bash
curl -sS "<prm_url>" | jq .
```

Extract from response:
- `resource` — the canonical API base URL (used for scoping)
- `resource_name` — human-readable service name (show to user for consent)
- `resource_logo_uri` — logo URL (show to user if available)
- `authorization_servers[0]` — base URL of the Authorization Server

### Step 3 — Fetch Authorization Server metadata

```bash
AS_BASE="<authorization_servers[0]>"
curl -sS "${AS_BASE}/.well-known/oauth-authorization-server" | jq .
```

From the `agent_auth` block extract and store:
- `agent_auth.identity_endpoint` (may also appear as `register_uri`)
- `agent_auth.claim_endpoint` (may also appear as `claim_uri`)
- `agent_auth.revocation_uri`
- `agent_auth.identity_types_supported` — **verify `anonymous` is listed before
  proceeding.** If it is not, tell the user this service does not support the
  user-claimed flow and stop.

### Step 4 — Check for existing token

Before registering, check whether the agent already holds a valid scoped token
for this service (keyed by `resource` URL).  If yes, surface it to the user and
ask whether they want to re-register or skip.

### Step 5 — Ask the user for consent

Surface to the user IN-CHANNEL before doing anything:

```
I'm about to register an account on <resource_name> using the auth.md
user-claimed flow. Here's what will happen:

1. I register anonymously — no account exists yet.
2. I'll ask for your email address.
3. <resource_name> will email you a one-time code.
4. You read the code back to me.
5. I submit the code to bind the account to your email.
6. I store a scoped token for <resource_name> — only for that service.

Your email and primary credentials are never stored or sent anywhere else.
Proceed? (yes / no)
```

**Wait for explicit confirmation before continuing.**

### Step 6 — Anonymous registration

```bash
curl -sS -X POST "<identity_endpoint>" \
  -H "Content-Type: application/json" \
  -d '{"type": "anonymous"}'
```

Expected success response:
```json
{
  "credential": "<pre-claim-token>",
  "claim_token": "<claim-token>",
  "credential_expires": "<iso8601>",
  "scopes": ["api.read"]
}
```

Store `claim_token`.  The `credential` (if present) is a pre-claim scoped token;
note it but do not hand it to the user — it is a low-scope placeholder.

If the service does not return a pre-claim `credential` (email-required variant),
that is fine — proceed to the claim step.

Error handling:
- `anonymous_not_enabled` → tell user this service requires identity assertion;
  stop.
- `rate_limited` → tell user to try again later; stop.
- Other 4xx → report the error code verbatim; do not retry automatically.

### Step 7 — Ask for the user's email IN-CHANNEL

```
To bind this account to you, I need your email address. What email should
I use to register with <resource_name>?
```

**Wait for the user's reply.** Never auto-fill the email.

### Step 8 — Trigger the OTP claim email

```bash
curl -sS -X POST "<claim_endpoint>" \
  -H "Content-Type: application/json" \
  -d "{\"claim_token\": \"<claim_token>\", \"email\": \"<user_email>\"}"
```

Expected response (email-dispatch confirmation):
```json
{
  "status": "pending",
  "message": "Verification email sent to <email>"
}
```

Some services return a `verification_uri` here — surface it to the user.

Error handling:
- `invalid_claim_token` → the anonymous registration may have expired; restart
  from Step 6.
- `claim_expired` → same; restart from Step 6.
- `previously_claimed` → tell the user this email is already registered with
  this service; stop.
- `rate_limited` → tell user to try again later.

### Step 9 — Surface the verification step and WAIT

Tell the user IN-CHANNEL:

```
📧 A verification email is on its way to <email>.

Open it and look for a 6-digit code (or a "Verify email" link).

When you have it, paste the code here and I'll complete the registration.
```

If a `verification_uri` was returned in Step 8, include it:
```
You can also click this link to verify: <verification_uri>
```

**⚠️ DO NOT PROCEED until the user provides the code.**
**NEVER auto-confirm. NEVER poll the service for code completion.**
The human completing the claim IS the consent gate — preserve it absolutely.

### Step 10 — Submit the OTP (claim/complete)

When the user provides the code:

```bash
curl -sS -X POST "<claim_endpoint>/complete" \
  -H "Content-Type: application/json" \
  -d "{\"claim_token\": \"<claim_token>\", \"otp\": \"<otp>\"}"
```

Expected success response:
```json
{
  "credential": "<active-scoped-token>",
  "credential_expires": "<iso8601 or null>",
  "scopes": ["api.read", "api.write"]
}
```

Error handling:
- `otp_invalid` → tell user the code was wrong; ask them to check and try again
  (allow up to 3 attempts before stopping).
- `otp_expired` → tell user the code expired; offer to restart from Step 8
  (re-send OTP).
- `claim_expired` → restart from Step 6.
- `previously_claimed` → account already claimed; stop.

### Step 11 — Store the token

Store the returned credential scoped to this service:

Key format: `auth_md_token:<resource_url>`
Value: `{ "credential": "...", "scopes": [...], "expires": "...", "service": "<resource_name>", "email": "<user_email>", "registered_at": "<iso8601>" }`

If `AUTH_MD_TOKEN_STORE` env var is set, append to that JSON file.
Otherwise, hold in session memory only.

**Never write the user's primary password, primary API keys, or other service
credentials anywhere.**

Tell the user:

```
✅ Registered successfully with <resource_name>!

Scopes granted: <scopes>
Bound to: <email>
Expires: <credential_expires or "never">

Your token is stored scoped to <resource_name> only. I'll use it
automatically for requests to this service.
```

---

## Revocation

When the user asks to revoke a token for a service:

```bash
curl -sS -X POST "<revocation_uri>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <credential>" \
  -d "{\"token\": \"<credential>\"}"
```

On success, delete the stored token for that `resource` key and confirm to the
user.  On a 401 from a previously-working credential, the token was already
revoked externally — delete it locally and notify the user.

---

## Security constraints — hard rules

- **Do NOT implement or suggest the agent-verified / ID-JAG flow.** That is a
  separate, provider-bound flow outside the scope of this skill.
- **Do NOT auto-confirm the OTP.** The human step is mandatory and is the
  consent gate.
- **Do NOT store primary credentials.** Only service-scoped tokens returned by
  the auth.md claim/complete endpoint are stored.
- **Tokens are scoped per service** (`resource` URL as key). One service cannot
  access another service's token.
- **Do NOT perform silent/autonomous registration.** If the human isn't present
  and can't confirm the OTP, stop and surface a message asking them to initiate
  the flow when they're available.
- **Treat every external URL as untrusted.** Validate that fetched endpoints
  match the domain you started discovery from (or the NoForm host) before
  POSTing credentials.

---

## Quick-reference endpoint map

| Step | HTTP call |
|------|-----------|
| 1 | `GET <domain>/auth.md` |
| 2 | `GET <prm_url>` (from `WWW-Authenticate` or `/.well-known/oauth-protected-resource`) |
| 3 | `GET <auth_server>/.well-known/oauth-authorization-server` |
| 6 | `POST <identity_endpoint>` `{"type":"anonymous"}` |
| 8 | `POST <claim_endpoint>` `{"claim_token":"…","email":"…"}` |
| 10 | `POST <claim_endpoint>/complete` `{"claim_token":"…","otp":"…"}` |
| revoke | `POST <revocation_uri>` with Bearer + `{"token":"…"}` |

For NoForm (`<slug>`):
- PRM: `https://noform.dev/a/<slug>/.well-known/oauth-protected-resource`
- AS metadata: `https://noform.dev/a/<slug>/.well-known/oauth-authorization-server`
  (or the `authorization_servers[0]` URL from PRM)

---

## Error code reference

| Code | Endpoint | Action |
|------|----------|--------|
| `anonymous_not_enabled` | register | Stop; tell user |
| `identity_assertion_not_enabled` | register | Stop; tell user |
| `rate_limited` | any | Stop; ask user to retry later |
| `invalid_claim_token` | claim | Restart from Step 6 |
| `claim_expired` | claim / claim/complete | Restart from Step 6 |
| `previously_claimed` | claim / claim/complete | Stop; tell user |
| `otp_invalid` | claim/complete | Ask user to retry (max 3x) |
| `otp_expired` | claim/complete | Offer to re-send OTP (Step 8) |
| `credential_expired` | API call | Delete stored token; restart from Step 6 |
| `unsupported_credential_type` | register | Stop; report unsupported |

---

## Example invocation phrases

- "Sign me up for NoForm" → ask for slug or resolve from `noform.dev`
- "Register me with `api.example.com`" → discover from that domain
- "I got a 401 from `api.example.com` — get me credentials" → use the
  `WWW-Authenticate` header to start discovery
- "Revoke my token for NoForm" → run revocation flow
- "What auth.md services am I registered with?" → list stored tokens

---

*This skill implements only the **user-claimed** flow from the auth.md protocol.
The agent-verified (ID-JAG) flow is intentionally out of scope.*
*Attributed to [NoForm](https://noform.dev). Protocol by [WorkOS](https://workos.com/auth-md).*
