---
name: automated-lead-scraper
description: Extract publicly listed business contact emails (and phone numbers) from a list of company website URLs, with crash-safe checkpoint/resume. Use when the user gives websites/domains/a CSV of URLs and asks to find contact emails, build a lead list, or "scrape these sites for emails". Website-only, polite rate limits, no logins, no CAPTCHA bypass. Not for social networks, people search, or private data.
---

# Automated Lead Scraper (website → business contact emails)

Reads a CSV of website URLs, visits each site's home page plus a few standard contact pages (`/contact`, `/about`, `/team`, …), and writes the publicly listed emails to `output.csv`. Progress is checkpointed per URL, so interrupted runs resume without re-fetching.

**Never invent results.** Every email you report must come from `output.csv` / `suspicious.csv` produced by an actual run. If a run failed or found nothing, say so.

## When to use / not use

Use: "Scrape these websites and extract publicly available business contact emails", "find contact emails for this list of companies' sites".
Do not use for: Facebook/Instagram/LinkedIn or other logged-in sources, finding personal emails of individuals, bypassing CAPTCHAs/blocks, or sites the user has no legitimate reason to contact.

## 1. Get the input (ask — don't guess)

You need a list of **website URLs or domains** (CSV with a `url` column, a `.txt` with one per line, or URLs pasted in chat). If the user hasn't provided any, ask for them. Do not make up sites or search for sites unless asked.

## 2. Choose a working directory

Use a fresh folder per job, e.g. `lead-scraper-runs/<job-name>/` (or one the user names). All input, cache, logs and outputs go there. Never write into a folder that already has `output.csv`/`cache.json` unless you are deliberately resuming (step 6) or the user approved `--fresh` (step 7).

## 3. Validate the URLs

```bash
node scripts/validate-input.js <their-file> --write-clean <workdir>/input.csv
```

It reports valid / duplicate / invalid counts, rejects non-http(s), localhost/private addresses, adds `https://` to bare domains, warns about social-media URLs and long jobs (~12 s/URL). Exit code 2 = nothing usable → show the user the reasons and ask for a corrected list. It will not overwrite an existing target without `--force`.
Tell the user the counts (valid / duplicates removed / rejected, with reasons) before scraping. For lists over ~200 URLs, confirm they want the full run (hours) or a batch.

## 4. Install dependencies (once)

```bash
cd <skill-dir> && npm install      # Node >= 18; installs axios, cheerio, csv-parse, csv-stringify only
```

## 5. Run

```bash
node scripts/email-scraper.js --workdir <workdir> > <workdir>/run.log 2>&1
```
Options: `--input <file>` (default `<workdir>/input.csv`), `--concurrency 1-4` (default 2), `--fresh`, `--fancy` (original ANSI banner; not needed).
- Small jobs (≲30 URLs): run in the foreground.
- Large jobs: run in the background (`&` on macOS/Linux, `Start-Process` on Windows) and poll.

**Monitor**: the log has one `PROGRESS n/total found=… not_found=… blocked=… errors=…` line per finished URL (`tail -n 5 <workdir>/run.log`). For a structured view at any time:
```bash
node scripts/summarize-run.js --workdir <workdir>        # add --json for machine-readable
```
Exit 0 + `RUN COMPLETE` = done. `RUN STOPPED EARLY` = interrupted (resume).

## 6. Resume an interrupted run

If the run was interrupted (Ctrl+C, crash, timeout) run the **exact same command** again. The scraper reads `cache.json`, prints `Resume from : N already done`, and only processes the remainder. Check `summarize-run.js` first: `can_resume: true` / `pending > 0`. If `cache.json` is missing or unreadable, there is nothing to resume — it will restart from URL 1 (tell the user).
Do not edit `input.csv` between interrupted runs except by appending new URLs (cache is keyed by the exact URL string).

## 7. Start a fresh run safely

Only when the user wants to redo everything: add `--fresh`. It **archives** `cache.json`, `output.csv`, `suspicious.csv` as `*_archived_<timestamp>.*` (nothing is deleted) and starts at 0. Otherwise use a new working directory.

## 8. Report results

Run `node scripts/summarize-run.js --workdir <workdir>` and report:
- **Completed** (found / not found), **failed** (`errors`, with `error` text), **blocked** (site returned 429/403/503 — not retried), **pending/skipped** (not yet processed), plus URLs rejected during validation.
- Give the user `<workdir>/output.csv` (and `suspicious.csv` if non-empty). State unique emails found.
Offer a short preview (first rows) but never fabricate or "complete" missing rows.

### Reading `output.csv` (one row per email; one row for sites with none)
`url, business_name, email, phone, email_count, email_source, confidence, suspicious, notes, source_page, fb_page_url, channel, status, error, scraped_at`
- `status`: `found` | `not_found` | `blocked` | `error`.
- `confidence`: `high` (mailto / JSON-LD / data-email / Cloudflare-decoded) · `medium` (visible text, attributes, `[at]`/`[dot]` de-obfuscated) · `low` (raw HTML match only). Prefer high/medium for outreach; mention low-confidence rows.
- `suspicious.csv`: emails with typo TLDs/provider domains (`.con`, `gmial.com` …). They are **flagged, never auto-corrected** — tell the user to review them manually.
- `fb_page_url`: a Facebook link the site itself publishes (a hint only; Facebook is not accessed).
Full column reference: `references/output-columns.md`.

## 9. Errors

| Symptom | Action |
|---|---|
| `ERROR: input file not found` / `no url column` / exit 2 | Fix the input (step 3). Header must be `url`, `website`, `link`, `domain` or `site`. |
| `HTTP 429/403/503 … not retrying this site` | The site is rate-limiting/blocking. Do **not** retry, rotate IPs, or bypass. Report those URLs as blocked. Concurrency is already reduced to 1. |
| Many `error` rows (timeouts / DNS) | Check the user's network; verify a couple of URLs are reachable; re-run only after fixing (use a new workdir or `--fresh` to retry them, since errors are cached). |
| `Cannot find module 'axios'` | Run `npm install` in the skill directory. |
| Selftest/other crash | Show the error text to the user; don't paper over it. More: `references/troubleshooting.md`. |

## 10. Self-tests

```bash
node scripts/email-scraper.js --selftest   # pure-function checks, no network. Baseline: 7/8 pass (see below)
npm test                                   # offline end-to-end suite on local fake sites (32 checks)
```
Known baseline: the original script's self-test case `&#105;nfo&#64;example.org` expects "blacklisted" but `example.org` is not in the blacklist, so `--selftest` reports 7/8. This is pre-existing and unchanged; see `references/adaptation-notes.md`.

## Responsible-scraping rules (always)

- Public pages only; no logins, no CAPTCHA/anti-bot bypass, no proxy rotation, no credentials of any kind.
- Keep the built-in delays and ≤ 4 concurrency; stop when a site blocks you.
- Collect only what's needed: business contact emails (and business phones the site publishes). Do not collect or report personal/sensitive data, and tell the user they remain responsible for complying with the sites' terms, robots.txt and applicable law (e.g. CAN-SPAM, GDPR/PECR, CASL) when emailing the results.
- Note: this scraper does **not** read robots.txt; for sensitive targets, check it yourself and skip disallowed sites.
