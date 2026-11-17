---
name: geo-scan
description: Audit the answer-engine readiness (ChatGPT, Perplexity, Claude, Gemini, AI Overviews) of one public website URL and produce a prioritised fix list. Use when someone gives a public site or page URL and asks whether AI engines can crawl, cite or quote it, or wants its robots.txt / snippet-permission / schema check or quotability score. Not for - private or intranet hosts, JS-rendered SPAs, SEO keyword research, writing content to beat competitors. English and German quotability scoring. No API key, no account, Python stdlib only.
version: 1.2.7
license: MIT
permissions:
  network: "outbound HTTP(S) GET only; public hosts by default; ftp:, file: and every other scheme are refused before a socket opens; robots.txt obeyed with RFC 9309 matching (wildcards, end anchors, Crawl-delay, pacing held across redirects); max 25 pages; hard 120 s ceiling that also bounds connect, TLS and download; the Hermes plugin asks for 90 s"
  filesystem: "read plugin dir only; write only the named report files under out_dir (--out-dir, which must sit inside the working directory; the plugin confines it to ~/.hermes/cache or cwd), and only when save=true"
  no_credentials: "reads, sends and stores no credentials or secrets"
metadata:
  author: Aurelius
  homepage: https://github.com/AureliusClaw/geo-scan
---

# geo-scan — answer-engine readiness audit

Scores a public website **0–100** for how readily an AI answer engine can crawl it,
parse it, and quote from it. Every score carries the evidence line that produced it,
so the report is checkable rather than advisory.

## When to use this skill

- "Can ChatGPT / Perplexity / Gemini see or cite my site?"
- "Why isn't my site showing up in AI answers?"
- "Review my robots.txt / llms.txt / schema.org / structured data."
- "Score how quotable this site is" for a given public URL.
- Before and after a content change, to measure whether answer-engine readiness moved.

Not for: private, intranet or loopback hosts (**refused before any socket opens**, see
"Security"); JS-rendered SPAs (no JS rendering, so the page reads as near-empty); SEO
keyword research; writing content to outrank competitors.

**Language coverage:** quotability scoring matches definitional, comparison and
question phrases in **English and German** (German patterns added in 1.2.3 after a
45-site Oldenburg batch showed all 45 scanned sites at ≤ 8/20 on that axis — a real gap,
partly an artefact of an English-only phrase list). Re-measured with the same URLs at
`pages=2` (44 sites re-scanned, 1 unreachable): sites at ≤ 8/20 fell **44 → 39**, median quotability **4.0 → 6.0**, median
total **61.6 → 62.4**. Other languages still score lower on that axis, and the report
notes the page language. The scan sends a fixed
`Accept-Language: en,en-US;q=0.8,de;q=0.6` header.

## How to run

```bash
python3 geo_scan.py https://example.com                      # report to stdout
python3 geo_scan.py --url https://example.com --pages 20 \
        --md audit.md --json audit.json                      # both, into out/
python3 geo_scan.py https://example.com --out-dir reports \
        --md audit.md                                        # a different out_dir, inside cwd
python3 geo_scan.py https://example.com --quiet              # no output, exit code only
```

`--json`/`--md` name a file **inside `--out-dir`** (default `out/`): an absolute path,
a `..` escape or an existing symlink is refused with exit 2. `--budget` is clamped to
10–120 s and `--pages` to 1–25 — the declared ceiling is the ceiling.

Exit 0: a report was produced. A low score is a finding, not a failure. Exit 2: nothing
usable could be fetched (DNS or TLS failure, unreachable robots.txt, robots.txt
disallows `geo-scan`, a refused non-public host, or no analysable page). The reason goes
to stderr unless `--quiet`.

Inside a Hermes session with the plugin installed, the same audit is the
`geo_scan` tool: `{ "url": "https://example.com", "pages": 12, "save": true }`.
The plugin always runs with `public_only=True` and stops after 90 s.

## Security

geo-scan is a read-only HTTP(S) client pointed at one public host. What enforces that:

| rule | how |
|---|---|
| public addresses only | every address is validated **at connect time** and the validated address is the address the socket opens — a second DNS answer (rebinding) cannot move the request |
| refused ranges | loopback, RFC 1918, link-local incl. `169.254.169.254`, unique-local, CGNAT, reserved, multicast, unspecified; IPv6 that embeds any of them (v4-mapped, 6to4, Teredo) too |
| no proxy | the opener is built with proxies off; `HTTP_PROXY`/`ALL_PROXY` cannot reroute the audit |
| scheme | `http:` and `https:` only, checked at the top of `fetch()` **and** by the opener's handler list: `build_opener()`'s defaults (FTPHandler, FileHandler, DataHandler) are deliberately not registered, so no `ftp://` or `file://` URL can reach a handler at all |
| robots.txt | RFC 9309 matching in `Robots`: `*` wildcards, `$` end anchors, longest-match with `Allow` winning ties, most-specific `User-agent` record, `Crawl-delay` honoured. `Sitemap:` lines are read but only fetched if same-host http(s) |
| scope | stays on the audited host (`www.`/apex), redirects re-checked |
| report paths | `--json`/`--md` resolve inside `--out-dir` (inside the working directory); absolute names, `..` escapes and existing symlinks refused; the plugin's `out_dir` must sit under `~/.hermes/cache` or cwd |
| bypass | `--allow-private` only, typed on the command line, never an environment variable; it widens **http(s) addresses** to private ranges and nothing else — ftp:, file: and every other scheme stay refused. It prints a warning and records `public_only: false` in the report. The Hermes plugin never passes it |

Refused hosts exit 2 with the refused address in the message.

## What it checks (100 points; the weights are our judgement, not validated against citations)

| axis | pts | what earns it |
|---|---|---|
| Crawler access | 20 | robots.txt lets search/retrieval agents (Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, PerplexityBot, Perplexity-User, Claude-SearchBot, Claude-User) fetch the root and sampled pages. Training crawlers (GPTBot, ClaudeBot, Google-Extended, CCBot, …) are reported but not scored. If every search agent is blocked, the total is this axis alone. |
| Machine readability | 15 | a sitemap (robots.txt `Sitemap:`, `/sitemap.xml`, `/wp-sitemap.xml`) with `<lastmod>` coverage; `llms.txt` / `llms-full.txt` (4 pts, speculative) |
| Snippet permissions | 10 | no `noindex` / `nosnippet` / `max-snippet:0` in meta robots or `X-Robots-Tag`; `data-nosnippet` costs a little |
| Page structure | 25 | one `<h1>`, article-level schema.org JSON-LD, meta description, author, ≥300 words, lists, canonical |
| Quotability | 20 | definitional phrases, hard figures, tables, question-form titles, `<h2>` sections (English + German phrase lists) |
| Freshness | 10 | median of each sampled page's newest JSON-LD date (else median sitemap `<lastmod>`); future dates discarded |

Grades: A ≥ 80 · B ≥ 65 · C ≥ 50 · D ≥ 35 · F below.

## Output contract

Markdown report: score, grade, one table row per axis with `score / max / status /
evidence`, then a prioritised action list (high/medium/low), then a per-page table
(url, words, h1 count, schema types, figure hits, quotable hits, robots directives),
then notes. JSON mirrors the same structure. Keep the evidence column in anything you
hand to a client — it is the part that can be re-checked.

## Limits worth stating up front

- **Quotability scoring covers English and German phrases** (German added in 1.2.3): other
  pages score lower on that axis; the report notes the page language.
- Read-only HTTP(S) GETs of public pages (the plugin's `save=true` additionally writes the
  Markdown + JSON report into `out_dir`, confined to `~/.hermes/cache` or the working
  directory). `--pages` defaults to 8 and is clamped to 1–25; `--budget` defaults to 120 s
  and is clamped to 10–120 s at every layer, the plugin asking for 90 s. geo-scan obeys
  robots.txt for `geo-scan` with RFC 9309 matching, waits at least 1 s between requests
  (more if `Crawl-delay` asks), stays on the audited host and caps downloads.
- It measures **technical** readiness, not whether an engine actually cites the site.
- CDN or WAF bot blocking (e.g. Cloudflare's AI-crawler blocking) is invisible to it: an
  open robots.txt does not prove crawlers get through.
- There is no JS rendering; near-empty, script-heavy pages are flagged.
- It is a single automated sample with no human review. Use the same `--pages` value for
  before/after comparisons.
- Sent with `User-Agent: geo-scan/<version>` — the running version, currently
  `geo-scan/1.2.7 (+https://github.com/AureliusClaw/geo-scan; answer-engine readiness audit)` —
  so a site owner can find this run in their own logs. They can opt out with
  `User-agent: geo-scan` / `Disallow: /`.
