---
name: axiom-url-canonicalizer
description: URL canonicalizer — normalize URLs for SEO and comparison: lowercase host, sort params, strip tracking, decode/normalize percent-encoding. Use when you need canonical URL form. Pure stdlib, no LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-url-canonicalizer

**Version:** 0.1.2
**Axioma Tools**

Normalizes URLs to a canonical form suitable for SEO and comparison.

## What this skill does

- Lowercases host (preserves path case)
- Sorts query parameters
- Strips default ports (80, 443)
- Optional: strip tracking params (utm_*, fbclid, gclid)
- Optional: normalize percent-encoding
- Removes trailing slash on root

## When to use this skill

- ✅ Generate canonical URLs for SEO
- ✅ Deduplicate URL lists
- ✅ Compare URLs ignoring tracking noise
- ❌ Follow redirects (separate lib)
- ❌ Parse HTML for URLs (use BeautifulSoup)

## Usage

```bash
python3 axiom_url_canonicalizer.py "HTTPS://Example.com:443/Path/?b=2&a=1&utm_source=tw"
python3 axiom_url_canonicalizer.py urls.txt --strip-tracking
```

```python
from axiom_url_canonicalizer import canonicalize
canonicalize('HTTPS://Example.com/?b=2&a=1')
# 'https://example.com/?a=1&b=2'
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 20 cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
