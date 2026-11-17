# AppSec — Reviewing An Application, An API Or A Pull Request

The bug classes that cause real incidents, in the order they actually occur — not the order a taxonomy lists them. For line-by-line secure-code fixes in a specific codebase, the sibling `security-best-practices` skill owns the diff; this file owns the judgement about what to look for and how hard.

**Before reviewing**, read `## Environment` in `~/Clawic/data/cybersecurity/memory.md` for the stack and the crown-jewel data this application touches, and any `artifacts/threat-model-*.md` the `## Boxes` index names for it — the paths somebody already ranked tell you which twenty lines of this diff matter.

**Contents:** [Where To Look First](#where-to-look-first) · [Authorization: The Number One Class](#authorization-the-number-one-class) · [Injection, Modernized](#injection-modernized) · [SSRF And The Metadata Service](#ssrf-and-the-metadata-service) · [Authentication And Session Handling](#authentication-and-session-handling) · [Secrets And Configuration](#secrets-and-configuration) · [File Upload](#file-upload) · [APIs Specifically](#apis-specifically) · [Business Logic And Race Conditions](#business-logic-and-race-conditions) · [Reviewing A Pull Request In Ten Minutes](#reviewing-a-pull-request-in-ten-minutes) · [Tooling And What Each One Misses](#tooling-and-what-each-one-misses)

## Where To Look First

Read the code in this order; the ordering reflects both frequency and severity in real incidents.

1. **Every route's authorization check** — not authentication, authorization. Who is allowed to touch *this* object?
2. **Every place user input reaches an interpreter**: SQL, shell, template, deserializer, XML parser, LDAP filter, NoSQL query, or a URL the server will fetch.
3. **Every trust boundary crossing**: the webhook receiver, the file upload, the admin endpoint, the internal service that assumes its caller is friendly.
4. **Anything touching money, entitlements or personal data.**
5. **The framework's escape hatches**: raw query builders, `dangerouslySetInnerHTML` and equivalents, `eval`, reflection, dynamic imports, disabled CSRF, `verify=False`. Grep for these first — they are where the framework's protection was deliberately turned off, and each one is a decision somebody made in a hurry.

**Broken access control leads the OWASP Top 10 (2021) and dominates real-world exploitation** for the simple reason that it needs no exotic technique: change the id and see what happens.

## Authorization: The Number One Class

- **Object-level authorization (IDOR/BOLA)**: `GET /invoices/1042` returns an invoice belonging to someone else. The test is trivial and the finding is everywhere. Every object fetched by an identifier from a request needs an ownership or tenancy check at the point of fetch.
- **Function-level authorization**: the admin endpoint that is only hidden by the UI not rendering a button. Enumerate the routes, not the interface.
- **Field-level and mass assignment**: the update endpoint that happily accepts `"role": "admin"` because it binds the request body straight onto the model. Allowlist the writable fields; never denylist.
- **Tenant isolation**: a missing `tenant_id` predicate leaks across customers, and it is the single worst finding a multi-tenant SaaS can have. The control is structural — a repository layer or a database row-level policy where the predicate cannot be omitted — never developer discipline.
- **The two-check pattern that fails**: authorization at the gateway plus a service that trusts the gateway's header. Anyone who reaches the service directly is now an admin. Verify a signed token at the service, not a header.

Grep-level heuristic that finds real bugs fast: for each route, is the identifier from the request used to *fetch* before it is used to *check*? Fetch-then-check is fine only if the check happens before anything is returned; fetch-and-return with the check somewhere else is where the bug lives.

## Injection, Modernized

| Class | Still real because | The structural fix |
|---|---|---|
| SQL injection | Dynamic query building survives in reporting, search filters, and ORM escape hatches | Parameterized queries everywhere; ban string concatenation into SQL at lint level |
| Command injection | Any shell-out with user input: filenames, ffmpeg/imagemagick arguments, archive names | Argument arrays, never a shell string; allowlist the values |
| Template injection | User-controlled templates in email, reports and page builders | Sandboxed template engine, or no user templates at all |
| Deserialization | Java, .NET, Python pickle, PHP unserialize, YAML loaders taking arbitrary objects | Data formats without object graphs; safe loaders; signed payloads |
| XXE | XML parsers with external entities on by default in older stacks | Disable DTDs and external entities at parser construction |
| NoSQL and query-object injection | Body parsers that let a JSON object reach the query where a string was expected | Type-check inputs before they touch the query |
| XSS | Everywhere that bypasses the framework's escaping, plus DOM sinks the server never sees | Auto-escaping framework, CSP as defence in depth, treat every escape hatch as a review item |

XSS deserves a note on impact: with `HttpOnly` session cookies, XSS still executes as the user through the application's own API, so "the cookie is protected" narrows the damage without removing it.

## SSRF And The Metadata Service

The class that turns a web bug into a cloud account compromise, and it deserves its own section because the impact is discontinuous.

- Any server-side fetch of a user-supplied URL — image import, webhook tester, PDF renderer, link preview, document converter, "import from URL" — is a candidate.
- The target is usually the cloud instance metadata endpoint or an internal service with no authentication. On AWS this is why IMDSv2 with a hop limit matters; on other providers the metadata endpoint requires a header that a naive SSRF cannot set. Enforcing the modern metadata protocol is the single control that converts most SSRF from critical to medium.
- Allowlist destinations rather than denylisting internal ranges. Denylists lose to DNS rebinding, redirects, IPv6 forms, decimal-encoded addresses and shortened URLs.
- Resolve the hostname, validate the resolved address, and connect to that address — validating the string and then letting the HTTP client resolve again is the classic time-of-check/time-of-use gap.
- Disable redirect following, or re-validate at every hop.
- Egress-filter the fetcher: a service that must reach two external hosts should be able to reach exactly two.

## Authentication And Session Handling

- Session identifiers: generated with a CSPRNG, rotated on privilege change and at login, invalidated server-side at logout. A JWT that cannot be revoked is a session you cannot end — pair short access-token lifetimes with a revocable refresh token, or keep a server-side session.
- **JWT specifics that keep appearing**: reject `alg: none`, pin the expected algorithm rather than trusting the header, verify `aud` and `iss`, check expiry with clock skew bounded, and never accept a key identifier that lets the caller choose the verification key.
- Password storage: a memory-hard algorithm (argon2id, scrypt) or bcrypt with a current cost factor. Anything faster is an offline-cracking gift, and a fast hash plus a breach is a credential-stuffing campaign against every other site the user visits.
- Rate limiting and lockout on login, password reset, MFA verification and any enumeration surface — per account *and* per source, since per-source alone loses to a botnet and per-account alone lets one source spray the whole user list.
- Password reset: single-use, short-lived, unguessable token; no user enumeration in the response or the timing; and the token invalidated when the password changes.
- Do not build the authentication flows here — the sibling `auth` skill owns that; this file owns finding them broken.

## Secrets And Configuration

- Grep the repository and its history: a secret removed in a later commit is still in the history and must be rotated, not deleted. Rotation is the fix; deletion is cosmetic.
- Client-side means public. Any key shipped in a mobile app, a single-page app bundle, or a browser-visible config is disclosed by definition — the only question is whether it grants anything.
- Environment-specific configuration must not default to permissive: debug mode, verbose errors, permissive CORS with credentials, wildcard origins, and disabled TLS verification all ship to production because the default was convenient.
- Error handling: stack traces and internal identifiers in responses are a reconnaissance gift. Log the detail server-side with a correlation id and return the id.
- **Logs are a data store.** Session tokens, authorization headers, full request bodies and personal data in application logs are a breach waiting for a log-access incident, and they are almost always avoidable with a redaction filter at the logger.

## File Upload

A dense cluster of severe bugs in one feature:

- Store outside the web root, serve from a separate origin or through a handler that never executes content, and never trust the client-supplied filename or content type.
- Generate the stored filename yourself. Path traversal, null bytes, unicode normalization and case-insensitive collisions all live in user-supplied names.
- Validate by parsing, not by extension. If it must be an image, decode it — and know that image and document parsers are themselves a memory-safety attack surface, which is the argument for processing in an isolated worker.
- Enforce size limits before buffering, and a decompression limit for archives and images (a small archive that expands to fill the disk is a one-request outage).
- Serve downloads with `Content-Disposition: attachment` and a restrictive content type; a stored HTML or SVG file served from your origin is stored XSS with a file extension.

## APIs Specifically

- **Object-level authorization is the top API risk** and it repeats per endpoint — a single missed route is the whole finding.
- Resource consumption: unbounded page sizes, expensive filters, and GraphQL query depth or complexity with no limit turn a read endpoint into a denial-of-service primitive. Depth limits, complexity budgets and pagination caps are the controls.
- Excessive data exposure: returning the whole object and letting the client render a subset. The response shape is an authorization decision, and the mobile app's unused fields are the attacker's.
- Versioning leaves old endpoints running with old authorization logic. Inventory `/v1` when you ship `/v2`, and decommission on a date.
- The undocumented surface: internal endpoints, debug routes, GraphQL introspection in production, and the staging host that shares the production database.
- Webhooks in both directions: verify the signature on what you receive (with a constant-time comparison), and treat what you send as an SSRF surface pointing at customer-controlled URLs.

## Business Logic And Race Conditions

The bugs no scanner reports, because the code is doing exactly what it says:

- **Race conditions on anything scarce**: coupon redemption, balance withdrawal, inventory decrement, invite consumption. Parallel requests against a check-then-act sequence is the whole exploit. The fix is a database-level constraint or an atomic operation, never an application-level lock that only works on one instance.
- Negative, zero, huge, and fractional quantities. Currency in floats. Integer overflow on a total.
- State machines with skippable steps: reaching the confirmation endpoint without the payment step.
- Multi-step workflows where an earlier step's value is re-submitted at a later one — price, discount and tenant identifiers sent by the client and trusted at the end.
- Abuse of correct behaviour: unlimited free-tier compute, an email endpoint that sends to arbitrary addresses with attacker-controlled content, a referral system with self-referral.

## Reviewing A Pull Request In Ten Minutes

1. **Does it touch authentication, authorization, money, personal data, file handling, or deployment?** No to all → skim and move on. That triage is what makes the deep reviews affordable.
2. Look at every new route or handler: what is the authorization check, and is the object-ownership check on the fetch?
3. Grep the diff for the escape hatches: raw SQL, shell invocation, `eval`, deserialization, disabled verification, new `except`/`catch` that swallows an error, `# nosec`-style suppressions.
4. Any new external call — is the URL user-influenced (SSRF), and is the response parsed safely?
5. Any new dependency — who owns it, how old is the release, and does it run install-time scripts (`supply-chain.md`)?
6. Any new secret, config default, or permission grant?
7. Comment with the concrete exploitation scenario, not the class name. "A user can pass another customer's `account_id` here and read their statements" gets fixed today; "potential IDOR" gets triaged next sprint.

## Tooling And What Each One Misses

| Tool | Finds | Blind to |
|---|---|---|
| SAST | Injection patterns, hardcoded secrets, unsafe API use | Authorization, business logic, anything requiring application context — and it drowns the signal in false positives unless tuned per repository |
| DAST | Reachable surface, misconfiguration, some injection | Everything behind authentication it cannot maintain, and every logic flaw |
| Dependency scanning | Known CVEs in declared dependencies | Whether the vulnerable code path is reachable (`supply-chain.md`) |
| Secret scanning | Committed credentials, including in history | Secrets in configuration systems, CI variables and client bundles |
| Fuzzing | Memory safety, parser crashes, unexpected inputs | Authorization and logic |
| A human reading routes | Authorization, logic, tenancy, abuse | Scale — which is why the triage in the previous section exists |

The two classes that dominate real incidents — broken authorization and business logic — are exactly the two no tool finds. Budget accordingly: tooling for coverage, humans for the classes that matter.

Write what the review produced (`memory-template.md`): each finding as a row in `## Findings` with the concrete exploitation scenario, the attack path it removes, an owner and a due date; the application's entry points, trust boundaries and the data it holds in `## Environment`; anything the team consciously ships unfixed in `## Risk Accepted` with an expiry and a `## Due` row; the detection for exploitation of a finding you cannot fix quickly in `## Detections`; and the review checklist once tuned to this codebase — its escape hatches, its authorization pattern, its known-risky modules — in `~/Clawic/data/cybersecurity/artifacts/` with its `## Boxes` line in the same turn, so the next review starts where this one ended. Credentials found during review are rotated, and recorded here only as a pointer: `env:STRIPE_API_KEY`, never the value.
