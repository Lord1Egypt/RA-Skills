---
name: babata-browser
version: 3.1.0
description: |
  Babata Browser v3.1 — Lightweight browser automation with CloakBrowser anti-detection (C++-level stealth Chromium). Scan-first, act-second. Playwright fallback.
  Use when: JS-rendered pages, gov sites, form filling, screenshot evidence, interactive web.
  NOT for: static pages (use web_fetch), API queries (use CLI), text search (use web_search).
metadata:
  openclaw:
    emoji: 🦞
    requires:
      bins: [python]
      env: []
---

# Babata Browser 🦞 v3.1

> Lightweight browser automation with **CloakBrowser anti-detection** (C++-level stealth Chromium). Playwright fallback.
> reCAPTCHA v3: 0.9 | Cloudflare Turnstile: PASS | 30/30 bot tests

---

## Backend (v3.1)

| Backend | reCAPTCHA v3 | Cloudflare | gov sites | Default |
|:--------|:-----------:|:----------:|:---------:|:-------:|
| **CloakBrowser** | 0.9 | ✅ PASS | ✅ Strong | ✅ auto |
| Playwright | 0.1 | ❌ FAIL | ⚠️ Blocked | fallback |

- `backend='auto'` (default) → CloakBrowser if available → Playwright fallback
- `backend='cloakbrowser'` → force CloakBrowser, error if unavailable
- `backend='playwright'` → force Playwright

---

## When to Use ✅
Gov policy sites (JS-rendered) / SPA data collection / Form filling / Screenshot evidence / web_fetch returns <500 chars / WeChat articles

## When NOT to Use ❌
Static pages → `web_fetch` / API queries → `fetch()` / Text search → `web_search` (Tavily)

---

## Install

```bash
# CloakBrowser (recommended — anti-detection)
pip install cloakbrowser
cd skills/babata-browser && pip install -e .

# Playwright fallback (already installed)
pip install playwright && python -m playwright install chromium
```

---

## Core Principles

### 1. Scan First (from smart-browser best practice)
Never snapshot blindly. Find interactive elements with JS first:

```python
browser.execute_js(page, """
  (() => {
    const els = document.querySelectorAll('a[href], button, input, select, textarea, [role=button], [onclick]');
    return [...els]
      .filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.top < window.innerHeight; })
      .map((el, i) => ({ i, tag: el.tagName.toLowerCase(), text: (el.innerText || el.value || '').trim().slice(0, 50), id: el.id, href: el.href?.slice(0, 80) }));
  })()
""")
```

### 2. Click by Text, Not CSS
```python
browser.click(page, text='Latest Policy')  # ✅ Stable
# ❌ browser.click(page, selector='#content > div:nth-child(3) > a')
```

### 3. Smart Wait (Not Fixed Sleep)
```python
browser.execute_js(page, """
  new Promise(resolve => { let tries = 0;
    const t = setInterval(() => {
      if (document.body.innerText.includes('expected text') || ++tries > 30) { clearInterval(t); resolve(tries < 30 ? 'found' : 'timeout'); }
    }, 500);
  })
""")
```

### 4. Layered Extraction
```
Accessibility Snapshot → find target region → get_text(selector=region)
  → still unclear? → screenshot (last resort)
```

---

## Usage

### Quick (Natural Language)
```python
from scripts.babata_browser import execute_task
result = execute_task('Open https://example.com, search policy, extract top 5 titles')
```

### Precise Control
```python
from scripts.babata_browser import BabataBrowser
browser = BabataBrowser(headless=True); browser.start(); page = browser.new_page()
browser.goto(page, 'https://example.com')
browser.click(page, text='Agree')
browser.fill(page, 'input[name="q"]', 'query')
text = browser.get_text(page)
browser.screenshot(page, path='evidence.png')
browser.stop()  # ⚠️ Always close
```

### CLI
```bash
babata-browser 'Open GitHub Trending, extract top projects' --json
```

---

## Capabilities

| Action | Description | Use Case |
|------|------|---------|
| `goto(url)` | Navigate | Open target page |
| `get_text(sel?)` | Extract text (scoped optional) | Page body |
| `get_links(limit)` | All links | Navigation, search results |
| `click(text=, sel=)` | Click by text or CSS | Pagination, submit, nav |
| `fill(sel, val)` | Fill input | Search box, login form |
| `screenshot(path)` | Full-page screenshot | Evidence, visual verify |
| `scroll(n)` | Scroll | Lazy-loaded content |
| `execute_js(code)` | Run JS | Element scan, smart wait |
| `extract_table(sel)` | Table to dict list | Data tables |

---

## Errors

| Error | Fix |
|:----|:-----|
| `ERR_TIMED_OUT` | Increase timeout: `goto(page, url, timeout=60000)` |
| CloudFlare "Just a moment..." | Blocked — switch data source |
| `Element not found` | Scan first, click by text not CSS |
| `page.click: Timeout` | Use smart wait, not fixed sleep |
| Orphaned browser process | Always call `stop()` in try/finally |

## Security
- Never enter real credentials on untrusted sites
- Check content before screenshot (avoid capturing sensitive data)
- Default: `headless=True`
- Mandatory: `stop()` after use

---

## vs Playwright MCP

| | Playwright MCP | babata-browser v3.0 |
|---|---|---|
| Dependencies | Node + npx + Chromium | **Python + Playwright + Chromium** |
| AI decisions | MCP client | **Babata LLM direct** |
| Token efficiency | MCP protocol overhead | **CLI, zero protocol cost** |
| Best for | Long-running automation | **High-frequency interaction, sampling** |

---

## Changelog

| Version | Date | Changes |
|:----|:----|------|
| v2.1 | 2026-05-11 | Smart scan JS, smart wait, layered extraction, error table, security rules |
| v3.0 | 2026-05-11 | Full English localization, streamlined structure, version bump |
