# Troubleshooting

**`ERROR: no url column found`** – the CSV header must be one of `url, website, link, domain, site` (case-insensitive). Use `scripts/validate-input.js` to build a clean file.

**Exit code 2** – input problem (missing file, no URL column, no rows). Exit code 1 – unexpected crash (message printed after `FATAL:`).

**Everything is `not_found`** – many sites hide emails behind contact forms or JavaScript rendering. This skill fetches static HTML only (no headless browser), so JS-rendered emails are invisible to it. This is a limitation, not a bug.

**`blocked` rows** – the site answered 429/403/503. The scraper stops requesting that site and lowers concurrency to 1. Do not retry in a loop; wait and re-run later with a new workdir if the user still wants those sites, and respect the site's terms.

**Timeouts / `error` rows** – 12 s per request. Check connectivity; errors are cached, so use `--fresh` (archives old files) or a new workdir to retry.

**Resume didn't skip anything** – the cache key is the URL string exactly as in the CSV (trimmed). If you changed `url` values, they are treated as new. Also check `--workdir` is the same as before.

**Bare domain like `httpbin.org` mis-handled** – the original `normalizeUrl` only checks `startsWith('http')`, so domains starting with "http" get no scheme. `validate-input.js --write-clean` always writes full `https://` URLs, which avoids it.

**Garbled output on Windows terminals** – default output is plain text; if you used `--fancy`, use Windows Terminal or drop the flag.

**Ctrl+C** – the scraper finishes in-flight URLs, saves, and tells you to re-run to resume; press Ctrl+C twice to exit immediately (cache is saved after every URL anyway).

**`Cannot find module`** – run `npm install` inside the skill directory (Node ≥ 18).
