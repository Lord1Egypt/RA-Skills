# 📄 `axiom_url_canonicalizer.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-url-canonicalizer/axiom_url_canonicalizer.py`  
**Size:** 8,039 bytes / 271 lines  
**Hash:** `1d9c03d5417fb125`  
**Generated:** 2026-06-15T03:00:47.168131+00:00

## 📝 Module Docstring

```
🛠️ axiom-url-canonicalizer — URL Normalizer
============================================

⚠️ LIMITATIONS CONNUES :
- Pas de résolution DNS (seulement normalisation)
- Pas de validation SSL/TLS
- IDN/percent-encoding partiel
- Pas de support pour javascript: / mailto: / data: schemes

NORMALISE LES URLs POUR SEO ET CACHE

Usage CLI:
    python3 axiom_url_canonicalizer.py "HTTP://Example.COM:80/Path/?b=2&a=1#frag"
    python3 axiom_url_canonicalizer.py --json "..."
```

## 📦 Imports (9)

```python
import re
import sys
import urllib.parse.urlparse
import urllib.parse.urlunparse
import urllib.parse.parse_qsl
import urllib.parse.urlencode
import urllib.parse.unquote
import argparse
import json
```

## ⚡ Functions (4)

### `def canonicalize(url, sort_query, strip_fragment, strip_default_port, force_https, force_trailing_slash, remove_tracking_params):`
> Canonicalize a URL.

Args:
    url: the URL to normalize
    sort_query: sort query parameters alphabetically
    strip_fragment: remove #fragment
    strip_default_port: remove :80 for http, :443 for

### `def urls_equivalent(url_a, url_b):`
> Check if two URLs are canonically equivalent.

### `def analyze(url):`
> Analyse une URL avec sa forme canonique.

### `def main():`
