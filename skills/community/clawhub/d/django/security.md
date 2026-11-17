# Security — The Django-Specific Attack Surface

Django's defaults are good: escaping is on, CSRF is on, the ORM parameterizes, passwords are hashed properly. Nearly every Django vulnerability in the wild is a place where someone turned one of those off, or a layer Django cannot protect for you — authorization on the row.

## Start Here

`python manage.py check --deploy` audits the security settings of the *current* settings module. Run it in CI against production settings, not against dev.

| Setting | Production value | What it prevents |
|---|---|---|
| `DEBUG` | `False` | The debug page prints settings, environment, SQL, and local variables |
| `ALLOWED_HOSTS` | Explicit list | Host-header poisoning of password-reset links and absolute URLs |
| `SECRET_KEY` | From the environment, never in git | Forged sessions, forged password-reset tokens, forged signed cookies |
| `SECURE_SSL_REDIRECT` | `True` | Plaintext requests (needs `SECURE_PROXY_SSL_HEADER` behind a proxy) |
| `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` | `True` | Cookies leaking over HTTP |
| `SESSION_COOKIE_SAMESITE` | `"Lax"` (or `"Strict"`) | Cross-site cookie attachment |
| `SECURE_HSTS_SECONDS` | Ramp up from a small value | Downgrade attacks — set it too high too early and you cannot undo it for returning browsers |
| `SECURE_CONTENT_TYPE_NOSNIFF` | `True` (default) | Uploaded files being sniffed as HTML |
| `X_FRAME_OPTIONS` | `"DENY"` (default) | Clickjacking |
| `CSRF_TRUSTED_ORIGINS` | Full origins with scheme | Legitimate cross-origin POSTs failing, then being "fixed" with `@csrf_exempt` |

## Authorization Is Not Authentication

The vulnerability Django cannot prevent: a logged-in user requesting someone else's ID.

```python
# Broken: any authenticated user reads any order
order = get_object_or_404(Order, pk=pk)

# Correct: the queryset is the boundary
order = get_object_or_404(Order, pk=pk, customer=request.user.customer)
```

- Scope in `get_queryset()` once, and list, detail, update and delete are all covered.
- The same applies to related fields: a form or serializer offering `ModelChoiceField(queryset=Project.objects.all())` lets a user attach their object to another tenant's parent. Scope the queryset in `__init__`.
- Permission checks in templates are cosmetics. `{% if perms.shop.change_order %}` hides a button; it does not protect the POST endpoint behind it.
- Sequential IDs are not the vulnerability — the missing check is. UUIDs raise the cost of enumeration and change nothing about the fix.

## Injection

- The ORM parameterizes everything. Injection enters through `raw()`, `extra()`, `RawSQL`, and `cursor.execute()` built with f-strings or `%`. Pass parameters: `cursor.execute("... WHERE id = %s", [pk])`.
- `%s` is the placeholder on every backend, including PostgreSQL — it is not Python formatting, and quoting it yourself (`'%s'`) breaks the parameterization.
- Column and table names cannot be parameterized. If a name comes from user input, validate it against an allowlist of known columns; there is no escaping path that is safe.
- `filter(**request.GET.dict())` is lookup injection: a caller supplies `password__startswith` and turns your endpoint into an oracle, or traverses relations you never exposed. Build the filter from a fixed mapping.
- `order_by(request.GET["sort"])` accepts related paths and lets a caller force expensive sorts. Allowlist.

## XSS

- Autoescaping covers `{{ value }}` in HTML body context and nothing else. It is disabled by `|safe`, `mark_safe()`, and `{% autoescape off %}`.
- Escaped HTML is not safe JavaScript. Values crossing into a `<script>` block go through `{{ data|json_script:"id" }}`.
- `href="{{ url }}"` still allows `javascript:` — validate the scheme in Python before rendering a user-supplied URL.
- `format_html()` for any HTML built in Python (admin display methods, custom template tags). `mark_safe()` on a string containing user data is the vulnerability itself.
- Stored XSS via uploads: an uploaded `.html` or `.svg` served from your origin executes with your cookies. Serve user content from a separate domain, or force `Content-Disposition: attachment` plus `X-Content-Type-Options: nosniff`.
- Rich text needs sanitizing at write time with an allowlist parser. Storing raw HTML and rendering it with `|safe` moves the vulnerability, it does not remove it.

## CSRF

- Enabled by `CsrfViewMiddleware`. Every POST/PUT/PATCH/DELETE from a browser form needs `{% csrf_token %}`; AJAX needs the `X-CSRFToken` header read from the cookie.
- Cross-origin POSTs (a separate frontend domain, or HTTPS termination changing the perceived origin) need `CSRF_TRUSTED_ORIGINS` entries **with the scheme** (`https://app.example.com`) since Django >=4.0. This is the single most common reason people reach for `@csrf_exempt`.
- `CSRF_COOKIE_HTTPONLY = True` prevents JavaScript from reading the token — which breaks the standard AJAX pattern. Either keep it False (the default, and the token is not a secret in the session-fixation sense) or render the token into the page instead.
- `@csrf_exempt` is defensible only where a different, non-cookie credential authenticates the request (a signed webhook, a bearer token). On a cookie-authenticated endpoint it is a hole. Verify webhook signatures with `hmac.compare_digest`.
- DRF's `SessionAuthentication` enforces CSRF; token and JWT authentication do not, because they do not ride on cookies.

## Secrets And Configuration

- `SECRET_KEY` from the environment or a secrets manager. In git it means anyone with the repo can forge sessions and password-reset tokens for production.
- Rotating it logs everyone out and invalidates pending reset links; `SECRET_KEY_FALLBACKS` (Django >=4.1) covers the transition window.
- Database credentials, API keys and signing keys are environment configuration, never settings literals.
- `DEBUG = True` in production exposes the whole settings module through the error page. Also verify no third-party debug toolbar is enabled by an environment variable someone set once.
- Mask sensitive values in error reports with `@sensitive_variables()` and `@sensitive_post_parameters()`; without them, a 500 mail or an error-tracking payload contains the posted password.

## Files And Redirects

- `upload_to` built from user input triggers `SuspiciousFileOperation` or writes outside the storage root. Sanitize, or generate the name yourself and keep the original only as metadata.
- Validate uploads by content, not by extension or the client-declared `content_type` — both are attacker-controlled.
- Open redirect: `redirect(request.GET["next"])` sends users anywhere. Guard with `url_has_allowed_host_and_scheme(url, allowed_hosts={request.get_host()}, require_https=request.is_secure())`.
- SSRF: any view that fetches a user-supplied URL can reach internal services and cloud metadata endpoints. Allowlist hosts, resolve and check the IP, and disable redirects on the outbound client.

## Rate Limiting And Enumeration

- Django ships no rate limiting. Login, password reset, signup, and any expensive endpoint need throttling at the proxy, at the view, or with a dedicated package.
- Password reset and signup leak account existence when they answer differently for known and unknown addresses. Django's built-in reset view returns the same response either way — custom versions usually lose that property.
- Constant-time comparison (`hmac.compare_digest`) for tokens, signatures and API keys; `==` on secrets leaks length and prefix through timing.
- Log authentication failures with enough context to detect credential stuffing, and never log the credential itself.

## Dependencies

- Running an end-of-life Django series means known, published, unpatched vulnerabilities: the support window is a security control, not a maintenance preference. SKILL.md Quick Reference routes the upgrade mechanics.
- `pip-audit`/`safety`-style scanning in CI catches the dependency half; Django's own advisories cover the framework half. Both are needed.
- Pin versions in a lockfile and rebuild regularly rather than pinning and forgetting — a pin held for a year is a year of unapplied fixes.
