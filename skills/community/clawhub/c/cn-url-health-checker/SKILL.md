---
slug: cn-url-health-checker
name: URL Health Checker
version: "1.0.0"
description: "Check URL health status (HTTP response code, redirect chain). Detect broken links and server errors. Pure Python standard library, no API key required."
keywords: url, http, status, health, check
license: MIT-0
tags:
  - tools
---

# URL Health Checker

Check the health status of any URL.

## Features

- Get HTTP status code (200, 404, 500, etc.)
- Follow redirect chains
- Detect server errors
- Report final URL after redirects
- Pure Python, no external dependencies

## HTTP Status Codes

- 200: OK (working)
- 301/302: Redirect (may need attention)
- 404: Not Found (broken link)
- 500: Server Error (problem on server side)
- Other codes: Various issues

## Usage

```
python3 scripts/url_health.py --url https://example.com
```

## Example Output

```json
{
  "url": "https://example.com",
  "status": 200,
  "final_url": "https://example.com",
  "redirects": [],
  "error": null
}
```

## Example (Broken Link)

```json
{
  "url": "https://example.com/nonexistent",
  "status": 404,
  "error": "HTTP Error 404: Not Found"
}
```

## Use Cases

- Check if your website pages are accessible
- Find broken links in your content
- Monitor external resource availability

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
