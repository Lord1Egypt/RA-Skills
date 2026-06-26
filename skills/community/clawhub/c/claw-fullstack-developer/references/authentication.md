# Authentication & Authorization

Auth is where apps get compromised. Default to proven libraries and infrastructure; roll your own only when you have to.

## Use a library. Seriously.

Bad: writing your own password hashing, session management, or OAuth flow.
Good: using one of:

| Option | Best for |
|---|---|
| **Clerk** | Fastest to ship. Good UI components. Paid after free tier. |
| **Auth.js (NextAuth)** | Open source, flexible, works with Next.js natively. DIY UI. |
| **Supabase Auth** | Bundled with Supabase DB. Good if you're already on Supabase. |
| **Auth0 / Okta** | Enterprise, SSO-heavy, compliance-heavy use cases. |
| **Lucia** | Lightweight, library-style, good if you want control without reinventing crypto. |
| **Passport.js** | Node ecosystem standard, lots of strategies. Lower-level. |
| **FusionAuth / Keycloak** | Self-hosted, full-featured, operationally heavier. |

Pick based on constraints:
- **Hosted or self-hosted?** Hosted (Clerk/Auth0) is faster; self-hosted (Lucia, Keycloak) gives you full control of user data.
- **Does the user data need to live in your DB?** If yes → Lucia / Auth.js / Supabase. If no → Clerk / Auth0 are fine.
- **Do you need SSO/SAML for enterprise customers?** Auth0 / WorkOS / Clerk's enterprise tier.

## Authentication flows

### Username + password
Still the most common. Must include:
- **Strong password hashing**: argon2id (preferred), or bcrypt with cost factor 12+. Never MD5, SHA-1, SHA-256 alone, or anything custom.
- **Email verification** before allowing login for sensitive apps.
- **Password reset**: email-delivered time-limited one-time token. Token expires in 15–60 min, single-use, invalidates on use.
- **Breach checks**: integrate with Have I Been Pwned API or similar to reject known-breached passwords at signup.
- **Rate limiting** on login and password reset endpoints.

### OAuth / Social login
"Sign in with Google/GitHub/Apple." Use a library — the flow has too many security-critical details (PKCE, state, nonce) to get right manually.
- **Always validate the state parameter** to prevent CSRF.
- **Use PKCE** for public clients (SPAs, mobile).
- **Account linking**: decide how you handle a user who signs up with email, then later tries to log in with Google using the same email. (Usually: link automatically if email is verified on both sides, or prompt the user.)

### Magic links (passwordless email)
Easy to implement, reduces password fatigue. Downsides: dependent on email delivery, no offline access, more friction per login than a saved password.
- **Tokens are short-lived** (15 min) and single-use.
- **Rate limit** link requests per email.

### Passkeys / WebAuthn
The future of auth. Native support in all modern browsers. Libraries (SimpleWebAuthn, Clerk, Supabase) make this straightforward.

### SSO (SAML, OIDC)
For enterprise customers. Use WorkOS, Auth0, or Keycloak. Don't implement SAML from scratch — the spec is a minefield.

### Multi-factor authentication (MFA)
- **TOTP** (Google Authenticator, Authy) — default choice. Libraries: `otplib`, `pyotp`.
- **SMS** — avoid as sole factor (SIM-swap vulnerable); OK as a backup.
- **WebAuthn / security keys** — strongest MFA.
- **Backup codes** — issue 8–10 one-time codes at MFA enrollment; users will lose their phone.

## Session management

Two models:

### Session tokens (stateful)
Store sessions server-side (DB or Redis). Send a random token (stored hashed in DB) as a cookie.

Pros: trivial to revoke (delete the row), easy to list active sessions, shorter cookies.
Cons: DB lookup per request (though trivial with Redis/indexed lookup).

**Default to this model** for most web apps.

### JWT (stateless)
Signed token carries claims. Server verifies signature, reads claims.

Pros: no DB lookup per request.
Cons: **can't be revoked** without additional infrastructure. Storing blocklists defeats the "stateless" benefit.

Use JWT when:
- You have multiple services that all need to authenticate users and you don't want a shared session DB
- Short expiration is acceptable (access tokens: 5–15 min; paired with refresh tokens)
- The "can't revoke" property is acceptable or mitigated

**Don't use JWT for long-lived sessions in a monolith.** The revocation problem is real.

### Cookie settings
If using cookies (and you usually should for web):
- `HttpOnly` — inaccessible to JS, prevents XSS-based theft
- `Secure` — HTTPS only
- `SameSite=Lax` (default) or `SameSite=Strict` for higher security
- `SameSite=None; Secure` only when you truly need cross-site (third-party embed contexts)
- Short `Max-Age` for session cookies; rotate on privilege changes

### Refresh tokens
Access token (short-lived, 5–15 min) + refresh token (long-lived, 30–90 days).
- Store refresh tokens server-side so you can revoke them.
- Rotate refresh tokens on use (one-time-use) — detects token theft.
- On detected reuse, revoke the whole session family.

## Authorization (what the user is allowed to do)

Authentication proves who. Authorization decides what they can do. They're different concerns — don't conflate them.

### Models by complexity

**Role-based (RBAC)** — users have roles, roles have permissions:
```
user.role = "admin" | "editor" | "viewer"
```
Simplest. Fits most B2C and small B2B apps.

**Attribute-based (ABAC)** — permissions depend on attributes of user and resource:
```
can_edit_post(user, post) =
  user.id == post.author_id
  OR user.role == "admin"
  OR (user.role == "editor" AND post.org_id == user.org_id)
```
Use when rules involve relationships between users and specific resources.

**Relationship-based (ReBAC)** — permissions follow graph relationships (Google Docs, GitHub):
"Users who have 'editor' on the folder containing this file can edit the file."
Tools: OpenFGA, Oso, Permit.io.

### Where to enforce
**At every layer that handles data:**
1. **API layer**: reject unauthorized requests with 401/403 before doing any DB work.
2. **Service layer**: centralize `can_user_do_X(user, resource)` checks. Never scatter role checks across the codebase.
3. **Data layer**: if using multi-tenant schema, enforce tenant scoping in the repo layer — one forgotten filter = data leak. For Postgres, row-level security (RLS) can be an additional defense.

**Never trust the frontend.** The UI hiding the delete button does not mean the user can't DELETE. Re-check on every mutation.

### Role check pattern
Bad:
```ts
if (user.role === 'admin') { ... }   // scattered across 40 files
```

Good:
```ts
// lib/permissions.ts — one place
export function canDeletePost(user: User, post: Post): boolean {
  return user.role === 'admin' || post.authorId === user.id;
}

// in the service
if (!canDeletePost(user, post)) throw new ForbiddenError();
```

When the rule changes, you change it in one place.

## Common auth mistakes

- **Storing passwords in plain text or with weak hashing.** Use argon2id or bcrypt. Always.
- **Leaking user existence** via different error messages ("no such user" vs. "wrong password"). Use the same message for both.
- **Sending auth tokens in URL query strings.** They end up in access logs, referrers, browser history. Use headers or body.
- **No logout.** Actually delete the session server-side on logout, not just the client cookie.
- **Missing rate limits** on login, signup, password reset. Brute-force central.
- **JWT with long expiration and no revocation story.** The stolen token works until it expires.
- **Trusting the `Authorization` header without verifying the signature.** Verify every time — never cache the "yes, this token is valid" result across requests unnecessarily.
- **Using the same secret across environments.** Prod JWT secret must not be the same as staging or dev. Rotate on breach.
- **Not rotating secrets after an employee leaves** or on suspected compromise.
- **Giving every authenticated user admin access in dev** "for convenience," then accidentally deploying that flag to prod. Never ship dev shortcuts.

## Session takeover / account recovery — design for the bad day

- **Account recovery flow**: what happens when a user loses access to their email? Have a documented process, even if it's "contact support." Don't invent a recovery mechanism under duress after a real user reports it.
- **Suspicious activity**: log ips, user-agents, login times. Email the user on first login from a new device/location.
- **Force logout on password change** (and optionally on role/email change) — invalidate all sessions.
- **Credential stuffing protection**: monitor for patterns (many logins from one IP, many failures on distinct emails). Integrate a CAPTCHA after N failures.

## Secrets management

- Never commit secrets. `.gitignore` `.env`. Use `.env.example` with placeholder values.
- In CI/CD: use the platform's secret store (GitHub Actions secrets, Vercel env vars, AWS Secrets Manager).
- In production: AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, Doppler, or Infisical. Rotate on a schedule and on any suspected compromise.
- At boot, validate all required secrets are present — fail fast with a clear error message. Don't silently fall back to a dev default.
