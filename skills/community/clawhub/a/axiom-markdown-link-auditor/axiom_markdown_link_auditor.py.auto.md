# 📄 `axiom_markdown_link_auditor.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-markdown-link-auditor/axiom_markdown_link_auditor.py`  
**Size:** 6,079 bytes / 195 lines  
**Hash:** `60c2861e89240226`  
**Generated:** 2026-06-15T03:00:47.182001+00:00

## 📝 Module Docstring

```
🛠️ axiom-markdown-link-auditor — Markdown Link Checker
========================================================

⚠️ LIMITATIONS CONNUES :
- Pas de support JS-rendered pages
- Pas de validation des liens d'ancrage internes (#[...])
- HTTPS check ne suit pas les redirects (HEAD seulement)

AUDITE LES LIENS DANS UN FICHIER MARKDOWN
```

## 📦 Imports (7)

```python
import re
import sys
import urllib.request
import urllib.error
import argparse
import json
import json
```

## ⚡ Functions (4)

### `def extract_links(markdown_text):`
> Extract all links from markdown text.

Returns list of dicts: {type, text, url, line}

### `def check_url(url, timeout):`
> Check a single URL via HEAD request.

Returns dict with: url, status, ok, error

### `def audit(markdown_text, check_remote, timeout):`
> Audit a markdown text for links.

Returns dict with: total, by_type, broken (if check_remote), links

### `def main():`
