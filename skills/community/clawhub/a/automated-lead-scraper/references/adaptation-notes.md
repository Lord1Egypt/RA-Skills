# Adaptation notes (dashboard project → portable skill)

Source repo: `CLI-Script-Dashboard-Automated-Lead-Scraper`. The original files at the repo root are untouched.

## Architecture of the original
- **Scraping engine:** `email-scraper.js` (single CLI file). Pipeline: website (home + priority/contact pages) → [Facebook direct link → Facebook search].
- **Dashboard only (excluded):** `server-core.js`, `server.js`, `server.ts`, `public/`, `index.html`, `src/` (React/Vite/Tailwind), `vite.config.ts`, `tsconfig.json`, `metadata.json`, `.env.example` (Gemini/AI-Studio vars), `bun.lock`. Express/multer/cors/dotenv/react/vite/tailwind/@google/genai/etc. are not needed.
- **Dashboard functions replaced by tiny CLI equivalents:** upload / paste URLs → `scripts/validate-input.js`; start/stop → run command + Ctrl+C handler; status/preview/downloads → `scripts/summarize-run.js` + files in workdir; "Start Fresh" (renames cache to backup) → `--fresh` archiving; self-test button → `--selftest`.
- **Scraper dependencies actually used by the website channel:** `axios`, `cheerio`, `csv-parse`, `csv-stringify`. (`puppeteer`, `puppeteer-extra`, stealth plugin were used only for Facebook.)

## What `scripts/email-scraper.js` changes (search for `SKILL:` comments)
1. Paths: input/output/cache/suspicious now resolve inside `--workdir` (default: current dir) — no hardcoded paths. `--input`, `--concurrency` (1–4), `--fresh`, `--fancy` added.
2. Plain output by default (no ANSI, no `console.clear`, no animated status bar, one `PROGRESS` line per URL) for agent/log use. `--fancy` restores the original banner and panel.
3. **Facebook channel and hardcoded credentials removed** (see below).
4. 429/403/503 handling: site is marked `blocked`, never retried; concurrency drops to 1.
5. Input errors exit with code 2 and clear messages (original crashed on header-only CSV: `rows[0]` undefined).
6. SIGINT/SIGTERM: stop queueing, finish in-flight URLs, print resume hint.
7. `not_found` rows now carry the Facebook link the website itself publishes in `fb_page_url` (hint only).

## Unchanged (verified by tests)
Email extraction (mailto, JSON-LD, attributes, Cloudflare decode, visible text, raw HTML, `[at]`/`[dot]`), `normalizeEmail`, blacklist, de-duplication/confidence ranking, suspicious TLD/domain flagging, CSV columns/order, cache format (array of rows per URL) and resume logic, self-test cases, delays (200–500 ms between page requests, 0.5–1.2 s between URLs).

## Why Facebook was removed
- The original source contained a **hardcoded Facebook login (phone number + password) as the default** for `FB_EMAIL`/`FB_PASSWORD`. Publishing that would leak a credential. **If that repo was ever public or shared, change that Facebook password now.**
- The channel logged in with an account, used stealth/anti-detection settings, and walked the user through CAPTCHA/checkpoint prompts. That conflicts with the skill's rules (public sources only, no access-control or CAPTCHA bypass) and with Facebook's terms.
- It also pulled in puppeteer (~hundreds of MB, needs a visible browser).
If you want it back as an opt-in for your *own* use, keep it in the original dashboard project rather than the published skill.

## Known issues in the ORIGINAL logic (intentionally NOT changed)
1. `--selftest` baseline is 7/8: case `&#105;nfo&#64;example.org` expects `null` but `example.org` isn't in `EMAIL_BLACKLIST` (only `example.com` is). Either add `example.org`/`example.net` to the blacklist or change the expectation.
2. `EMAIL_BLACKLIST` uses substring matching on the whole address with short tokens (`js`, `css`, `png`, `gif`, `apple`, `google`, `ttf`…). Legit addresses such as `jsmith@company.com` or `info@pineapplefarm.com` are silently dropped. Likely cause of missed emails.
3. `normalizeUrl` treats any string starting with `http` as already having a scheme (`httpbin.org` → broken). Worked around by `validate-input.js`.
4. robots.txt is not consulted; user-agent is a generic Chrome string.
5. Static HTML only (no JS rendering).
