# Deploying on a compatible site-hosting platform (optional)

This document describes the optional `publish.mjs` flow. It only works with a hosting platform that
exposes the same open API; set `BV_API_BASE` and `BV_APP_ID` for your platform. Everything else in
this skill (build, check, package, verify) works without it.

## How the platform serves a site
- One site = one subdomain `https://<sub>-<random>.<platform-domain>/`; the URL is only known
  **after** the first deploy.
- `/` and extension-less paths return the entry file. A sub-directory `xxx/` does **not**
  resolve to `xxx/index.html` → one page per site, `index.html` at the zip root.
- Extension whitelist (others silently skipped): html htm css js mjs json map png jpg jpeg
  gif svg webp ico bmp woff woff2 ttf eot otf mp4 webm mp3 wav txt xml pdf. Unzipped ≤ 50MB.
- Hosted on Tencent COS (`server: tencent-cos`) behind EdgeOne. **No Cloudflare in front**
  → no first-party `/cdn-cgi/trace`; IP country has to come from a public endpoint.
- Query strings are fine; OAI-AdsBot UA gets 200.
- The platform keeps 3 versions; rollback is one click.

## Zip rules (scripts/package.js does this)
- Zip the *contents* of `dist/<slug>/`, never the folder itself.
- No `__MACOSX/` or dotfiles: a Finder-made zip contains `__MACOSX/._index.html`, and the
  platform may pick it as the entry file.
- Output `out/<slug>-<yyyymmdd-hhmm>.zip` (UTC stamp). Old zips stay in `out/` — always
  hand the user the newest one by path, and say which older ones are obsolete.

## First deploy (URL unknown yet)
1. `node scripts/package.js <slug> --force` — check fails only on the url placeholder at
   this point; everything else (content, pixel) should already be real.
2. Platform → 新建部署: upload zip, 主入口文件 `index.html`, **加密访问 off**
   (with it on, OAI-AdsBot cannot crawl and the ad fails review).
3. Put the assigned URL into `page.json` `url` (site root, trailing slash).
4. `node scripts/package.js <slug>` — must pass with no `--force`.
5. Same site → 部署新版本 with the new zip. Ads use this URL.

`url` feeds canonical, og:image, robots `Sitemap:` and sitemap.xml. A zip built before the
url was filled still contains `REPLACE_WITH_SUBDOMAIN` in all four — the classic "I uploaded
the latest zip but canonical is still a placeholder" (the user had uploaded an older zip).

## Every later change
Edit → `node scripts/package.js <slug>` → 部署新版本 → `verify.mjs <url> --dist dist/<slug>`
to prove the live files equal the build (no-cache fetch, byte compare) before testing.

## Open API (publish.mjs) — deploy and audit without the web UI

The backend's global auth middleware accepts an `api-key` header on every route, so the
script calls the same endpoints as the platform's site-hosting and audit pages.

| Step | Endpoint |
|---|---|
| login (once) | `POST /v1/open-api/device/code {app_id}` → user approves at `verification_url` → poll `POST /v1/open-api/device/token` (errCode `AUTHORIZATION_PENDING` until approved) → api-key saved to `~/.config/chatgpt-ads-landing/credentials.json` (0600) |
| upload | `GET /v1/site-hosting/site/deploy-credential` → STS key + one-off `dir` (`staging/{owner}/{nonce}/`) → PUT each file of `dist/<slug>/` to COS at `dir + relative path` |
| first deploy | `POST /v1/site-hosting/site {name, subdomain_hint, entry, password_enabled:false, pending_dir, version_remark}` → `site_id`, `site_url` |
| new version | `PUT /v1/site-hosting/site {site_id, name, entry, password_enabled, password, pending_dir, version_remark}` — always send name and password fields: omitted fields are treated as "clear" |
| audit | `POST /v1/async_job/submit {job_type:"gpt_landing_audit", payloads:[{url, site_id, target_countries, language}]}` → poll `/status` → `/result {batch_id, id}` |

- `page.json` gets `"deploy": {"siteId": "…"}` after the first deploy. build.js ignores it
  (only routing/ctas/links/consent/pixelEvents reach `LP_CONFIG`), so it never ships to the page.
- A page with a real `url` but no `siteId` is matched by URL in the user's own site list; a
  URL owned by someone else is refused — log in as the site owner.
- There is no default API base: pass `--api-base` or set `BV_API_BASE`.
- The audit runs on the platform's own workers (exit country in the report). It covers
  crawlability, content, credibility, conversion path and tech, but **not** pixel delivery,
  geo routing or the consent flow — verify.mjs still has to run.
- Known backend quirk (2026-10-21): the device-code `verification_url` hard-codes one
  app_id (`open_api_manage.go`), so the approve page may show another app's name. Polling
  works regardless.
- Device login gives an api-key that can list sites and run the audit. CreateSite / UpdateSite through the API
  are still untested here — confirm the site name with the user before the first real `deploy`.
- Platform-level audit finding on every page on the platform's shared domain: `tech_https` "HTTP 访问未跳转到
  HTTPS". The page cannot fix this; it is the platform's edge config — say so instead of
  editing the page. It is a training-framework item, not an OpenAI requirement.
