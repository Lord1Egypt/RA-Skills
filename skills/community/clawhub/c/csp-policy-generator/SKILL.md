---
name: csp-policy-generator
description: Generate, validate, and tighten Content Security Policy (CSP) headers for web applications. Analyze existing pages to discover resource origins, build least-privilege policies, test for violations, and migrate from report-only to enforcing.
---

# CSP Policy Generator

Build Content Security Policy headers that actually work. Analyze your web application to discover all resource origins (scripts, styles, images, fonts, frames, APIs), generate a least-privilege CSP, test for violations, and provide a safe migration path from report-only to enforcement.

Use when: "create CSP header", "content security policy", "fix CSP violations", "tighten CSP", "XSS prevention headers", "security headers", or when deploying CSP for the first time.

## Commands

### 1. `generate` — Build CSP from Page Analysis

#### Step 1: Discover Resource Origins

```bash
# Fetch the page and extract all resource URLs
curl -sL "https://$HOST" | python3 -c "
import sys, re
from urllib.parse import urlparse
html = sys.stdin.read()

sources = {
    'script-src': set(),
    'style-src': set(),
    'img-src': set(),
    'font-src': set(),
    'connect-src': set(),
    'frame-src': set(),
    'media-src': set(),
    'object-src': set(),
}

# Script sources
for m in re.finditer(r'<script[^>]*src=[\"\\x27]([^\"\\x27]+)', html):
    sources['script-src'].add(urlparse(m.group(1)).netloc or \"'self'\")

# Inline scripts
if re.search(r'<script(?!.*src)[^>]*>', html):
    sources['script-src'].add(\"'unsafe-inline'\")

# Style sources
for m in re.finditer(r'<link[^>]*href=[\"\\x27]([^\"\\x27]+)[\"\\x27][^>]*rel=[\"\\x27]stylesheet', html):
    sources['style-src'].add(urlparse(m.group(1)).netloc or \"'self'\")
for m in re.finditer(r'style=[\"\\x27]', html):
    sources['style-src'].add(\"'unsafe-inline'\")

# Image sources
for m in re.finditer(r'<img[^>]*src=[\"\\x27]([^\"\\x27]+)', html):
    sources['img-src'].add(urlparse(m.group(1)).netloc or \"'self'\")

# Font sources
for m in re.finditer(r'url\([\"\\x27]?([^)\"\\x27]+\\.(?:woff2?|ttf|eot|otf))', html):
    sources['font-src'].add(urlparse(m.group(1)).netloc or \"'self'\")

for directive, origins in sources.items():
    if origins:
        print(f'{directive}: {\" \".join(sorted(origins))}')
"
```

Also check JavaScript files for dynamic resource loading:
```bash
# Find fetch/XMLHttpRequest/import targets in JS files
curl -sL "https://$HOST/main.js" 2>/dev/null | \
  rg -o 'fetch\(["\x27]https?://[^"]*' 2>/dev/null
```

#### Step 2: Build Least-Privilege Policy

Starting from a deny-all baseline, add only discovered origins:

```
default-src 'none';
script-src 'self' [discovered script origins];
style-src 'self' [discovered style origins];
img-src 'self' data: [discovered image origins];
font-src 'self' [discovered font origins];
connect-src 'self' [discovered API origins];
frame-src [discovered frame origins];
frame-ancestors 'none';
base-uri 'self';
form-action 'self';
upgrade-insecure-requests;
```

#### Step 3: Security Recommendations

For each directive, flag concerns:
- `'unsafe-inline'` in script-src → recommend nonce-based approach or hash
- `'unsafe-eval'` → flag as high risk, identify which library needs it
- `*` wildcards → replace with specific domains
- `data:` in script-src → XSS risk
- Missing `frame-ancestors` → clickjacking risk
- Missing `upgrade-insecure-requests` → mixed content risk

#### Step 4: Output

```markdown
# CSP Policy for $HOST

## Recommended Policy (Report-Only — start here)
```
Content-Security-Policy-Report-Only: default-src 'none'; script-src 'self' cdn.example.com; style-src 'self' 'unsafe-inline' fonts.googleapis.com; img-src 'self' data: images.example.com; font-src 'self' fonts.gstatic.com; connect-src 'self' api.example.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests; report-uri /csp-report
```

## Enforcement Policy (after monitoring report-only)
```
Content-Security-Policy: [same as above without -Report-Only]
```

## Migration Path
1. Deploy report-only policy (above)
2. Monitor /csp-report for 1-2 weeks
3. Fix any violations found
4. Switch to enforcing mode
5. Remove 'unsafe-inline' from style-src (use nonces instead)

## Warnings
- 🟡 `'unsafe-inline'` in style-src — fix by adding nonces
- 🟢 No `'unsafe-eval'` — good
- 🟢 `frame-ancestors 'none'` — clickjacking protected
```

### 2. `validate` — Test Existing CSP

Check a live site's CSP for weaknesses:
```bash
curl -sI "https://$HOST" | grep -i "content-security-policy" 2>&1
```

Parse the policy and flag:
- Directives with `'unsafe-inline'` or `'unsafe-eval'`
- Overly broad wildcards (`*.example.com` or `*`)
- Missing directives (default-src without coverage)
- report-uri vs report-to configuration

### 3. `nonce` — Generate Nonce-Based CSP Setup

For frameworks that support it, generate nonce middleware:

```javascript
// Express middleware example
const crypto = require('crypto');
app.use((req, res, next) => {
  res.locals.nonce = crypto.randomBytes(16).toString('base64');
  res.setHeader('Content-Security-Policy',
    `script-src 'nonce-${res.locals.nonce}' 'strict-dynamic'; style-src 'self' 'nonce-${res.locals.nonce}'`
  );
  next();
});
```

### 4. `hash` — Generate Hash-Based CSP for Static Sites

For static sites where nonces aren't practical, hash all inline scripts/styles:
```bash
# Hash each inline script
grep -oP '(?<=<script>).*?(?=</script>)' index.html | while read script; do
  echo -n "$script" | openssl dgst -sha256 -binary | openssl enc -base64
done
```
