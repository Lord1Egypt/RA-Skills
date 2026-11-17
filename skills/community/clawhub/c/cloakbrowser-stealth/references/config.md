# CloakBrowser Configuration Reference

## Installation

CloakBrowser is a modified Chromium with 58 C++ patches for anti-bot stealth.

```bash
pip install cloakbrowser
```

Installed locally at: `~/.venv/cloakbrowser`

## Launch Options

| Parameter | Type | Default | Description |
|---|---|---|---|
| `headless` | bool | `True` | Run without GUI |
| `humanize` | bool | `False` | Bézier mouse movements, natural keyboard timing, realistic scroll |
| `proxy` | str | `None` | `http://user:pass@host:port` — auto-detects geo/timezone from proxy IP |
| `profile` | str | `None` | Persistent profile path for cookies/localStorage |

## Anti-Detection Capabilities

**What it bypasses:**
- WebDriver detection (selenium/playwright flags)
- Chrome automation flags
- PhantomJS detection
- Plugin enumeration checks
- WebGL fingerprinting (spoofs NVIDIA/Intel GPUs)
- Canvas fingerprinting (consistent hash)
- Navigator properties (vendor, platform, languages)
- Battery API / Memory API (returns normal values)
- Broken image dimensions check

**What it does NOT bypass:**
- IP reputation blocks (Cloudflare WAF, Reddit CDN)
- reCAPTCHA v3 behavioral scoring (improves from 0.1 to ~0.9)
- TLS fingerprinting
- Rate limiting
- Login requirements

## Common Targets

| Site | Status | Notes |
|---|---|---|
| Trustpilot | ✅ Works | Extracts reviews, scores |
| Reddit | ❌ CDN block | IP-level block, not fingerprint |
| Glassdoor | ✅ Likely | Standard bot detection |
| LinkedIn | ⚠️ Partial | Aggressive rate limits |
| Amazon | ✅ Works | Product pages accessible |

## Proxy Recommendations

For sites that block by IP (Reddit, some Cloudflare):
- Residential proxy required
- Rotating proxies recommended for scale
- Launch with `geoip=True` to auto-match timezone/locale to proxy location

## Comparison

| Tool | Detection Score | Cost | Notes |
|---|---|---|---|
| Standard Playwright | ~0.1 reCAPTCHA v3 | Free | Detected immediately |
| Puppeteer Stealth | ~0.5 | Free | JS patches only |
| CloakBrowser | ~0.9 | Free | C++ patches + stealth driver |
| Multilogin/GoLogin | ~0.9 | $$$ | Commercial, profile-based |
