# Security Checklist — Architecture Critic

A targeted security review for AI-assisted builds. These are the failure modes that appear most often when AI generates or accelerates code.

---

## 🔑 Secret & Key Exposure

- [ ] **No hardcoded secrets** — API keys, tokens, passwords absent from source code and committed files
- [ ] **Environment variable scope** — secrets in `.env.local` (not `.env`) for Next.js; server-side only, never exposed to client
- [ ] **Client-side leak check** — no `NEXT_PUBLIC_` prefix on sensitive vars; no secrets in `window.*`, `localStorage`, or frontend bundles
- [ ] **`.gitignore` coverage** — `.env*` files excluded; `git log --all --diff-filter=A -- '*.env*'` shows nothing
- [ ] **Vercel env var audit** — sensitive vars set to "Server" scope only, not "Client" or "Edge"
- [ ] **Log sanitization** — secrets not logged in error messages, debug output, or analytics payloads
- [ ] **Key rotation plan** — rotation procedure documented; old keys invalidated on rotation, not just abandoned
- [ ] **Third-party service keys** — principle of least privilege applied; Stripe read-only key for dashboards, write key for charge flows only

---

## 💉 Injection Risks

### SQL Injection
- [ ] **Parameterized queries only** — no string interpolation into SQL; `$1` placeholders, not `${variable}`
- [ ] **ORM usage review** — raw query escape hatches (`$queryRaw`, `db.query()`) audited individually
- [ ] **Input type validation** — IDs validated as integers/UUIDs before use in queries

### Prompt Injection
- [ ] **User content never in system prompt** — user-supplied text enters only the user message slot
- [ ] **Instruction delimiters** — XML tags or clear separators between system instructions and user content
- [ ] **Output used as code** — if AI output is executed or eval'd, it passes a schema check first
- [ ] **Tool call validation** — AI-generated function names and parameters validated against allowed list before execution

### Command Injection
- [ ] **No `exec(user_input)`** — user data never passes directly to shell, eval, or subprocess
- [ ] **File path traversal** — `..` sequences stripped from user-supplied paths; paths resolved and validated against allowed root

---

## 🔐 Auth Bypass Vectors

- [ ] **JWT validation complete** — signature verified, `exp` checked, `aud` and `iss` validated
- [ ] **No client-side auth decisions** — authorization checks on server/middleware, not just hidden UI elements
- [ ] **Session fixation** — session token regenerated on privilege change (login, sudo, role change)
- [ ] **IDOR protection** — resource ownership verified server-side; user can't access `/api/orders/123` belonging to another user
- [ ] **Role escalation** — user cannot self-assign elevated roles via API parameter (`role: 'admin'` in request body)
- [ ] **Auth middleware coverage** — all routes requiring auth are covered; no accidental public exposure of protected routes
- [ ] **Token storage** — JWTs in `httpOnly` cookies, not `localStorage`; refresh tokens never in client storage
- [ ] **OAuth state parameter** — CSRF token used and validated in OAuth flows

---

## 🌐 CORS & CSP Misconfiguration

- [ ] **CORS origin whitelist** — not `*`; explicit list of allowed origins for APIs handling auth or mutations
- [ ] **CORS credentials** — `Access-Control-Allow-Credentials: true` only paired with specific origins, never with `*`
- [ ] **Content Security Policy** — `default-src 'self'`; `script-src` allows no inline scripts or `unsafe-eval` unless justified
- [ ] **CSP frame protection** — `frame-ancestors 'none'` or restricted to trusted domains; prevents clickjacking
- [ ] **Referrer policy** — `Referrer-Policy: strict-origin-when-cross-origin` or stricter
- [ ] **Cookie `SameSite`** — session cookies set to `SameSite=Strict` or `Lax`; `None` only if cross-site and `Secure`

---

## 🚦 Rate Limiting & Abuse Vectors

- [ ] **Auth endpoints rate-limited** — login, password reset, OTP verification have per-IP request caps
- [ ] **AI endpoints rate-limited** — LLM call endpoints protected; cost-per-request means abuse = direct money burn
- [ ] **Account enumeration** — login and password reset return identical responses for valid/invalid accounts
- [ ] **Webhook replay** — webhook endpoints reject replayed requests (timestamp + signature validation)
- [ ] **Form submission limits** — public forms (contact, signup) rate-limited per IP and/or require captcha
- [ ] **Resource consumption** — file upload size limits; AI input token caps enforced server-side

---

## 📤 Data Exfiltration Risks

- [ ] **Response field filtering** — API responses return only fields the caller needs; no accidental `SELECT *` leaking to client
- [ ] **PII in logs** — emails, names, SSNs, payment data not logged in plaintext
- [ ] **Error message leakage** — production errors return generic messages; stack traces and DB errors suppressed
- [ ] **Bulk export protection** — list endpoints paginated; no unauthenticated endpoint can dump the full user/contact list
- [ ] **Download URL security** — file download URLs are signed and time-limited, not permanent public S3 links

---

## 📦 Third-Party Dependency Risks

- [ ] **Dependency audit** — `npm audit` / `pip-audit` run; no high/critical vulnerabilities in direct dependencies
- [ ] **Lock file committed** — `package-lock.json` or `yarn.lock` in repo; CI installs from lockfile only
- [ ] **Supply chain** — no packages installed directly from GitHub branches or non-registry sources without pinned commit hash
- [ ] **License review** — GPL/AGPL dependencies flagged if commercial use applies
- [ ] **Minimal permissions** — third-party SDKs granted only required OAuth scopes; not `admin:*` when `read:user` suffices

---

## OWASP Top 10 Quick Hits (AI Build Specific)

| OWASP Risk | AI Build Manifestation | Check |
|---|---|---|
| A01 Broken Access Control | AI generates CRUD without ownership checks | Server-side auth on every mutation |
| A02 Cryptographic Failures | AI uses MD5/SHA1, stores passwords in plain text | bcrypt/argon2 for passwords; TLS everywhere |
| A03 Injection | AI concatenates inputs into queries/prompts | Parameterized queries; prompt delimiters |
| A05 Security Misconfiguration | Default configs, CORS `*`, debug mode in prod | Env-specific config; CSP headers |
| A06 Vulnerable Components | AI uses outdated packages in examples | `npm audit`; lock file discipline |
| A07 Auth Failures | AI skips session validation in "simple" routes | Auth middleware on all protected routes |
| A09 Logging Failures | AI logs full request bodies containing secrets | Log sanitization; never log auth tokens |
