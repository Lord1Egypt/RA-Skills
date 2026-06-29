---
name: axiom-url-canonicalizer
description: Canonicaliseur d'URL — normalise les URLs pour SEO et comparaison : host en lowercase, trie les params, strip le tracking, décode/normalise le percent-encoding. Utilisez pour avoir une forme canonique. Stdlib pur, sans LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-url-canonicalizer

**Version:** 0.1.2
**Axioma Tools**

Normalise les URLs en forme canonique pour SEO et comparaison.

## What this skill does

- Host en lowercase (path préservé)
- Trie les query params
- Strip les ports par défaut (80, 443)
- Optionnel : strip les params tracking (utm_*, fbclid, gclid)
- Optionnel : normalise le percent-encoding
- Supprime le trailing slash sur root

## When to use this skill

- ✅ Générer des URLs canoniques pour SEO
- ✅ Dédupliquer des listes d'URLs
- ✅ Comparer des URLs en ignorant le bruit tracking
- ❌ Suivre les redirects (lib séparée)
- ❌ Parser du HTML pour URLs (utilise BeautifulSoup)

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
