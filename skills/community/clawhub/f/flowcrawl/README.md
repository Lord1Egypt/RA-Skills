# 🕷️ FlowCrawl — Stealth Web Scraper for OpenClaw

> Like Firecrawl. But free.

**Firecrawl** charges up to $333/month. **FlowCrawl** is open source, runs locally, and costs $0. Same idea — scrape any site, get clean markdown — but without the subscription, the rate limits, or the API key.

```
  ███████╗██╗      ██████╗ ██╗    ██╗███████╗ ██████╗██████╗  █████╗ ██████╗ 
  ██╔════╝██║     ██╔═══██╗██║    ██║██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
  █████╗  ██║     ██║   ██║██║ █╗ ██║███████╗██║     ██████╔╝███████║██████╔╝
  ██╔══╝  ██║     ██║   ██║██║███╗██║╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ 
  ██║     ███████╗╚██████╔╝╚███╔███╔╝███████║╚██████╗██║  ██║██║  ██║██║     
  ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     
```

**FlowCrawl** is a stealth web scraper for [OpenClaw](https://github.com/openclaw/openclaw). Give it a URL — any URL — and it extracts clean content using a three-tier bot-bypass escalation system. No CDP Chrome. No proxies. No config. Powered by [Scrapling](https://github.com/D4Vinci/Scrapling).

---

## 🎯 The Problem

Most scrapers fail against modern bot protection. Cloudflare, Imperva, DataDome, PerimeterX — they detect headless browsers, TLS signatures, and automation patterns. Your scraper returns a 403, a CAPTCHA wall, or "Just a moment..." and dies.

**FlowCrawl doesn't.**

It uses a smart escalation cascade that starts lightweight and only pulls out the heavy weapons when it needs to.

---

## ⚡ How It Works

FlowCrawl tries three fetcher tiers in order — stopping the moment it gets clean content:

```
  URL
   │
   ▼
┌──────────────────────────────────┐
│  Tier 1: Plain HTTP              │  Fastest. Works on ~60% of sites.
│  Scrapling Fetcher               │  Zero overhead, instant results.
└──────────────┬───────────────────┘
               │ Blocked? (403/503/Cloudflare)
               ▼
┌──────────────────────────────────┐
│  Tier 2: Stealth + TLS Spoof     │  Bypasses Cloudflare & basic WAFs.
│  StealthyFetcher                 │  Spoofs TLS fingerprint, mimics
│  (Playwright + stealth plugins)  │  real browser traffic patterns.
└──────────────┬───────────────────┘
               │ Still blocked? (JS-heavy / aggressive WAF)
               ▼
┌──────────────────────────────────┐
│  Tier 3: Full JS Execution       │  Nuclear option. Renders the page
│  DynamicFetcher                  │  like a real browser, executes all
│  (Playwright + JS runtime)       │  JavaScript, waits for content.
└──────────────────────────────────┘
```

No Chrome DevTools Protocol. No external proxy services. Pure Python + Scrapling.

---

## 🚀 Quick Start

### Install

```bash
# Clone into your OpenClaw skills directory
git clone https://github.com/windseeker1111/flowcrawl.git ~/clawd/skills/flowcrawl

# Install Scrapling
pip install scrapling

# Add alias
echo 'alias flowcrawl="python3 ~/clawd/skills/flowcrawl/scripts/flowcrawl.py"' >> ~/.zshrc
source ~/.zshrc
```

### Run

```bash
# Scrape a single page — output to terminal
flowcrawl https://example.com

# Spider a whole site
flowcrawl https://example.com --deep

# Spider with limits — save & combine into one file
flowcrawl https://example.com --deep --limit 30 --combine --output ./data

# JSON output for piping into other tools
flowcrawl https://example.com --json
```

---

## 📋 All Commands

| Command | Description |
|---------|-------------|
| `flowcrawl <url>` | Scrape one page, print markdown to stdout |
| `flowcrawl <url> --deep` | Spider the whole site |
| `flowcrawl <url> --deep --limit N` | Cap at N pages (default: 50) |
| `flowcrawl <url> --deep --depth N` | Max N hops from homepage (default: 3) |
| `flowcrawl <url> --combine` | Merge all pages into `slug-combined.md` |
| `flowcrawl <url> --format txt` | Plain text output instead of markdown |
| `flowcrawl <url> --output ./dir` | Custom output directory |
| `flowcrawl <url> --json` | Structured JSON output (url, tier, length, content) |
| `flowcrawl <url> --quiet` | Silent mode — no progress logs |

---

## 🔬 Tier Details

### Tier 1 — Plain HTTP (Fetcher)
Standard HTTP request using Scrapling's `Fetcher`. No browser overhead. Handles redirects, cookies, and basic headers automatically. Works on most public websites with no bot protection.

### Tier 2 — Stealth Mode (StealthyFetcher)
Uses Playwright with stealth plugins that:
- Spoof TLS fingerprints to look like a real Chrome browser
- Randomize browser properties (`navigator.webdriver`, `navigator.languages`, etc.)
- Apply canvas fingerprint noise
- Pass Cloudflare's browser integrity checks

Handles ~95% of Cloudflare-protected sites.

### Tier 3 — Dynamic Mode (DynamicFetcher)
Full JavaScript execution with Playwright. Renders the page completely, waits for dynamic content to load, and captures the final DOM. Use case: SPAs (React, Vue, Next.js) and sites that check for JS execution before showing content.

---

## 📊 What You Get

**Single URL mode** — prints clean markdown to stdout:
```
$ flowcrawl https://scrapling.dev

  ███████╗██╗      ██████╗ ...
  Stealth web scraper. Cloudflare? Not today.

→ https://scrapling.dev
  [T1] Plain HTTP...
  ✓ Tier 1 succeeded

────────────────────────────────────────────────

# https://scrapling.dev

## The Python Scraping Library That Understands The Web

Scrapling is a high-performance, intelligent web scraping library for Python...
```

**Deep crawl mode** — saves per-page markdown files:
```
flowcrawl-output/
├── page-001.md      ← homepage
├── page-002.md      ← /about
├── page-003.md      ← /docs
├── page-004.md      ← /docs/quickstart
└── slug-combined.md ← all pages merged (--combine)
```

**JSON mode** — pipe into anything:
```json
{
  "url": "https://example.com",
  "tier": 1,
  "length": 4823,
  "content": "# https://example.com\n\n## Domain\n\nThis domain..."
}
```

---

## 🏗️ Architecture

```
flowcrawl/
├── SKILL.md                  # OpenClaw skill manifest
├── README.md                 # This file
├── LICENSE                   # MIT
├── requirements.txt          # scrapling
└── scripts/
    └── flowcrawl.py          # Main CLI (single file, zero deps outside scrapling)
```

Single-file design. Drop it anywhere, it works.

---

## 🤝 Use Cases

- **AI knowledge bases** — scrape any site into clean markdown for RAG pipelines
- **Competitive intelligence** — monitor competitor sites without getting blocked
- **Research** — extract content from Cloudflare-protected sources
- **Data pipelines** — `--json` output pipes cleanly into jq, Python, or any ETL
- **VAPI/voice agents** — feed hotel, business, or product sites into your AI assistant (see [FlowKnow](https://github.com/windseeker1111/flowknow))

---

## ⚠️ Responsible Use

FlowCrawl is built for legitimate research, AI enrichment, and personal use cases. Respect `robots.txt`, rate limits, and terms of service. The built-in 0.5s delay between requests is there for a reason.

---

## 📜 License

MIT — see [LICENSE](LICENSE)

---

<p align="center">
  🕷️<br>
  <i>A skill for <a href="https://github.com/openclaw/openclaw">OpenClaw</a></i><br>
  <i>Stealth web scraping. Any site. Any protection.</i>
</p>
