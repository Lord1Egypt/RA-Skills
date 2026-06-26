---
name: free-local-web-search
description: 100% FREE local web search for OpenClaw. Secure localhost-only SearXNG deployment. Supports hidden --dev flag.
license: MIT
metadata:
  version: 1.0.7
  openclaw:
    requires:
      bins:
        - docker
        - python3
  keywords:
    - free web search
    - local web search
    - brave alternative
    - no api key
    - zero cost
    - secure search
    - localhost only
    - searxng
---

# 🌐 Free Local Web Search (Secure)

✅ Completely FREE

### Python Dependency

The runtime scripts require the Python package `requests`.

Install if missing:

```
pip install requests
```
  
✅ Localhost-only deployment  
✅ Limiter + safe_search enabled  

Dev mode available:

python scripts/install.py --dev

⚠ Dev mode disables safe_search and limiter (reduced safety). For local development only.

Powered by local-search-pro.

⚠ Installation deploys a persistent Docker container (`searxng-local`) with `--restart unless-stopped`.
To remove it:

```
docker rm -f searxng-local
```
