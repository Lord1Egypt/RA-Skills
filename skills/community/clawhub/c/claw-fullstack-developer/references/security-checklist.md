# Security Checklist

Walk through this before declaring an app production-ready. Most items are quick. The cost of a missed item is often orders of magnitude larger than the cost of checking.

## Authentication & sessions
- [ ] Passwords hashed with argon2id or bcrypt (cost ≥12). No MD5, SHA-1, SHA-256-alone.
- [ ] Login failures return a generic error ("invalid credentials"), not "user not found."
- [ ] Rate limit on login, signup, password reset, and any other auth-adjacent endpoint.
- [ ] MFA available for accounts (TOTP minimum); required for admin accounts.
- [ ] Sessions expire. Long sessions via refresh tokens, not long-lived access tokens.
- [ ] Logout actually invalidates the server-side session.
- [ ] Force logout on password change, email change, and role change.
- [ ] Suspicious-login notifications (new device/IP) sent to user.

## Authorization
- [ ] Every endpoint that reads or writes data checks the caller's permissions.
- [ ] Permission checks happen server-side, not just in the UI.
- [ ] Multi-tenant apps scope every DB query by tenant — ideally enforced in a single repository layer, not scattered across endpoints.
- [ ] Admin endpoints are clearly separated (e.g., `/admin/*`) and have stricter auth + logging.
- [ ] Direct object references (`/orders/{id}`) verify the authed user can access that specific object. (IDOR is the #1 bug class on bug bounty platforms.)

## Input validation & injection
- [ ] Every request body, query param, path param, and header you trust is validated (Zod, Pydantic, etc.).
- [ ] All DB queries use parameterized queries / ORM. No string-concatenated SQL. Ever.
- [ ] HTML output is escaped by default (React/Vue/Svelte do this; `dangerouslySetInnerHTML` is audited).
- [ ] File uploads: validate MIME and extension, cap size, scan for malware for user-facing files, store outside the webroot (e.g., S3), serve via signed URLs or a handler that enforces access.
- [ ] User-supplied URLs (avatars, embeds) fetched from the server go through SSRF protection — block RFC1918 IPs, cloud metadata endpoints (169.254.169.254), localhost.
- [ ] Command execution or `eval`-adjacent functions do NOT take user input. If they must, whitelist with extreme prejudice.

## Secrets management
- [ ] No secrets in git (including history — scrub if found).
- [ ] `.env` in `.gitignore`. `.env.example` committed with placeholder values.
- [ ] Production secrets in a managed store (AWS Secrets Manager, GCP Secret Manager, Vault, Doppler, Infisical).
- [ ] Dev, staging, prod have different secrets. Rotate on employee offboarding and suspected compromise.
- [ ] App validates required secrets at boot and fails loud if missing.
- [ ] Nothing secret is logged (passwords, tokens, card numbers, API keys). Logging middleware redacts known sensitive fields.

## HTTPS & transport
- [ ] HTTPS everywhere. HTTP redirects to HTTPS.
- [ ] HSTS header (`Strict-Transport-Security: max-age=31536000; includeSubDomains`) on production.
- [ ] TLS 1.2 minimum; TLS 1.3 preferred. Weak ciphers disabled.
- [ ] Cookies marked `Secure` (HTTPS only) and `HttpOnly`.
- [ ] Cookies have a `SameSite` attribute. Default to `Lax` or `Strict`.

## Web security headers
Set these at the edge or in middleware:
- [ ] `Content-Security-Policy` — most impactful. Start strict (`default-src 'self'`), loosen as needed.
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `X-Frame-Options: DENY` (or `SAMEORIGIN`) — prevent clickjacking. CSP `frame-ancestors` is the modern equivalent.
- [ ] `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] `Permissions-Policy` to opt out of APIs (camera, mic, geolocation) unless needed.

Tools like [securityheaders.com](https://securityheaders.com) grade the setup.

## CORS
- [ ] CORS configured explicitly. Default-deny; allowlist specific origins.
- [ ] `Access-Control-Allow-Origin: *` only for truly public, non-credentialed APIs.
- [ ] `Access-Control-Allow-Credentials: true` only when you need to accept cookies from a specific origin — never combined with wildcard.

## CSRF
- [ ] For cookie-based session auth: CSRF tokens on state-changing endpoints, or rely on `SameSite=Lax/Strict` cookies (which are effective for most modern attacks).
- [ ] For bearer-token auth (Authorization header): CSRF is not a concern — browsers don't auto-attach Authorization headers.

## Rate limiting & abuse
- [ ] Per-endpoint rate limits sized to the threat (strict on auth, looser on reads).
- [ ] Global rate limit as a backstop.
- [ ] CAPTCHA on signup and password reset for public-facing apps.
- [ ] WAF in front (Cloudflare, AWS WAF) — not a substitute, a layer.

## Dependency security
- [ ] Lockfile committed (`package-lock.json`, `poetry.lock`, `go.sum`).
- [ ] `npm audit` / `pip-audit` / `govulncheck` in CI. Fail on high-severity.
- [ ] Dependabot or Renovate configured for weekly updates.
- [ ] Snyk / GitHub Advanced Security / Socket.dev for deeper SCA on sensitive apps.
- [ ] Pin Docker base images to a specific tag, not `latest`. Rebuild regularly.

## Logs, errors, and data leakage
- [ ] Error responses don't leak stack traces, SQL, file paths, or internal hostnames to users. Full detail stays in logs.
- [ ] Error reporting (Sentry) scrubs PII and secrets — configure data scrubbing rules.
- [ ] Logs stored with access controls; PII in logs minimized or redacted.
- [ ] Sourcemaps uploaded to error tracker but NOT served to users in prod (or served with restrictive source-map auth).

## Database & backups
- [ ] Database not exposed publicly — private network or IP allowlist.
- [ ] Least-privilege DB credentials per service; no using the superuser from the app.
- [ ] Automated daily backups with PITR (or equivalent) enabled.
- [ ] Backups encrypted at rest.
- [ ] Restore tested in the last 90 days.
- [ ] PII columns identified and handled per compliance needs (encryption at rest, access logs).

## File storage
- [ ] Uploaded files stored outside the app server (S3, GCS). Not in the webroot.
- [ ] Served via signed, short-lived URLs — not permanent public links (unless truly public).
- [ ] Per-file content-type and content-disposition set correctly to prevent browser sniffing attacks.
- [ ] Antivirus scan for user uploads distributed to other users.

## Third-party integrations
- [ ] Webhook payloads verified by signature before processing.
- [ ] OAuth state parameter validated; PKCE used for public clients.
- [ ] API keys to third parties stored in secrets manager; rotated per vendor recommendation.
- [ ] Outbound requests have timeouts and circuit breakers — a hung third party must not bring down your app.

## Infrastructure / platform
- [ ] IAM policies follow least privilege. No wildcard `*` permissions in production roles.
- [ ] SSH keys, not passwords, for server access. MFA on cloud consoles.
- [ ] Database encryption at rest enabled.
- [ ] VPC / private networking for inter-service communication.
- [ ] DNS, domain registrar, and cloud accounts protected by MFA and account-recovery process.

## Observability for security
- [ ] Login events logged with IP and user-agent.
- [ ] Permission-denied events (403s) logged — unusual spikes are interesting.
- [ ] Admin actions logged to an append-only audit log.
- [ ] Alerts on anomalies: spike in 5xx, spike in failed logins, new admin account created, IAM policy changed.

## Incident response
- [ ] Runbook for: compromised credential, data breach, DDoS, rogue dependency.
- [ ] Known point of contact for security reports (`security@yourapp.com`, security.txt).
- [ ] Communication plan: status page, customer email template, timeline of who decides what.

## Pre-launch checks
- [ ] Remove all `console.log`s that might dump secrets or user data.
- [ ] Disable verbose error pages (Django `DEBUG=False`, no stack traces in prod responses).
- [ ] Remove dev shortcuts (`/admin/become-user`, test-only endpoints).
- [ ] Close ports not needed by the app (Postgres not exposed to the internet, etc.).
- [ ] Scan with something like OWASP ZAP baseline scan, or a commercial scanner, on staging.
- [ ] Document the data you collect and why — privacy policy reflects reality.

## Compliance quick-reference
If any of these apply, the scope of this checklist expands significantly:
- **GDPR** — any EU user data. Add: data-subject rights (access, deletion, portability), lawful basis for processing, DPA with subprocessors, breach notification within 72h.
- **HIPAA** — any US health data. BAAs with everyone touching PHI, encryption, access audit logs, strict retention.
- **PCI-DSS** — handling card data. Use a tokenization provider (Stripe, Adyen) and stay out of PCI scope if at all possible.
- **SOC 2** — enterprise B2B often asks. Not a one-time audit — it's an operating pattern. Plan months ahead.

## The 80/20 of security
If you only had time for ten things, do these:
1. Use a reputable auth library; don't roll your own.
2. Parameterize every SQL query.
3. Validate every input at the boundary.
4. Check authorization on every endpoint, for the specific resource.
5. Store secrets in a secrets manager; never in git.
6. HTTPS everywhere + secure cookies.
7. Dependency updates automated + audited.
8. Rate limit auth endpoints.
9. Centralized error tracking with PII scrubbing.
10. Backups, tested.

Everything else is marginal improvements on top of these.
