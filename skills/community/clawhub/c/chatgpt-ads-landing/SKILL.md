---
name: chatgpt-ads-landing
slug: chatgpt-ads-landing
displayName: ChatGPT 广告落地页
version: 1.0.1
summary: 为 ChatGPT / OpenAI 广告制作静态落地页：26 项上线前检查、按国家跳转并保留 UTM 与 oppref、Pixel 事件回传、线上验证。
license: MIT
compatibility: Node 22+、pnpm；线上验证需要 Google Chrome；验证事件能否回传 OpenAI 需要海外网络。
description: Build, deploy and verify static landing pages for ChatGPT / OpenAI Ads campaigns — any advertiser, any vertical — using the chatgpt-ads-landing engine (pages/<slug>/ + page.json → build → check → zip) and an optional compatible site-hosting platform. Covers intake of client material, page content, OpenAI Measurement Pixel events (oaiq), UTM/oppref forwarding, per-country geo routing (time zone + IP), footer privacy links, cookie consent for UK/EU, packaging, first-deploy URL backfill, and live verification (pixel really reaches OpenAI, crawlers get 200, live == build). Use this whenever someone wants to 做/改/上线/检测 an OpenAI 或 ChatGPT 广告落地页, mentions chatgpt-ads-landing, oaiq / OpenAI pixel, OAI-AdsBot, "pixel 能触发吗", "UTM 生效了吗", "是否符合 OpenAI 落地页要求", 一键部署 / 自动上线, 落地页体检, 按国家/IP 跳转, or a new client's 落地页 for ChatGPT ads — even if they don't name the skill.
---

# ChatGPT Ads landing pages (chatgpt-ads-landing)

One engine, many clients: each campaign is a `pages/<slug>/` folder (static `index.html` +
`page.json`), built into a self-contained site, zipped, and deployed as one site on a
site-hosting platform. The bundled `assets/starter-page` is the reference starting point — copy it when you need a full example.

Why it is built this way: OpenAI reviews the landing page with its crawler (OAI-AdsBot), so
the page must be fully readable as static HTML and must never redirect itself; everything
dynamic (country routing, pixel events, consent) is progressive enhancement in `lp.js`.

## Where things are

- Repo: ask the user where their landing-page repo is . If one exists, work there — it may be newer than this
  skill's copy (`diff -rq <repo>/shared <skill>/assets/engine/shared` to tell).
- No repo on this machine → `node <skill>/scripts/init-repo.mjs <dir>` (copies
  `assets/engine/`, refuses non-empty dirs), then `pnpm install` in it.
- New page → `node <skill>/scripts/new-page.mjs <repo> <slug>` (copies `assets/starter-page/`,
  a vertical-neutral page whose blanks are `填【…】` — check.js fails until all are filled).
- Verify anything live → `node <skill>/scripts/verify.mjs <url> [--dist <repo>/dist/<slug>] [--proxy http://<your-proxy>]`.
- Re-read OpenAI's rules → `node <skill>/scripts/fetch-official.mjs --proxy …`.
- Deploy + platform audit via the open API → `node <skill>/scripts/publish.mjs login | deploy | audit | ship`
  (device-code login once; then no manual zip upload). See platform-deploy.md §Open API.

`<skill>` = this skill's directory. Prerequisites — check them before the first run and tell
the user what is missing: Node ≥ 22, pnpm, Google Chrome, and for any check against OpenAI an
overseas network exit. Ask the user for their proxy URL rather than assuming one (for example
`http://127.0.0.1:7890`, whatever their local proxy listens on); without a proxy, a system-wide overseas VPN works and `--proxy` can
be omitted. Run network scripts with the sandbox disabled so the proxy is reachable.

References — read the one you need, when you need it:
| File | Read when |
|---|---|
| `references/page-config.md` | writing/editing page.json or index.html (fields, tokens, content rules) |
| `references/pixel-events.md` | mapping the client's conversion events; pixel debugging |
| `references/openai-requirements.md` | any "does this meet OpenAI's requirements" question; category limits |
| `references/privacy-consent.md` | choosing consent countries / privacy links per market; banner behaviour |
| `references/platform-deploy.md` | packaging, first deploy, URL backfill, platform limits |
| `references/lessons.md` | before starting — the mistakes already made once and the user's preferences |

## Workflow A — new client page

1. **Intake.** Collect, and ask only for what is missing:
   - brand + campaign, offer facts, eligibility/terms, FAQ (source: brief, Feishu doc via
     lark-doc, a design HTML, or the client's site);
   - target countries and, per country, the client's tracked landing URL (with UTM) — use
     them verbatim; plus a fallback URL for everyone else;
   - pixel ID and the Ads Manager data source's event list (snippets are fine);
   - per-country privacy (and cookie) policy URLs from the client's site;
   - whether the client's logo may be used (default: our own mark);
   - category check: is the vertical allowed (openai-requirements.md §2)? Flag early.
2. **Scaffold.** `new-page.mjs <repo> <slug>`.
3. **Content.** Fill `index.html` from the material only — no invented numbers, headings or
   claims; leave `填【…】` and ask when something is missing. Keep JSON-LD word-for-word with
   the visible copy. If the client supplied a design, follow it; otherwise the starter's
   structure (hero with h1 + facts + CTA → benefits → details → FAQ → footer).
4. **Config.** `page.json`: `routing.sites` per country, `ctas` (`hero` = `geo`, one fixed
   CTA per country if the page lists countries), `links.privacy` (+ `cookies`), `consent`
   for UK/EU targets, `pixelEvents` mapped from the client's events (pixel-events.md).
   New country? Make sure its time zones are in `shared/geo.js`.
5. **Local check.** `pnpm dev` (http://localhost:4123/) and `node scripts/check.js <slug>`;
   then `verify.mjs http://localhost:4123/<slug>/ --proxy …` for pixel/geo/consent.
   **Stop `pnpm dev` (dev.js) before step 6.** dev.js rebuilds `dist/` on every file change;
   `publish.mjs ship` / `package.js` rewrite `page.json` (url, siteId) and rebuild at the same
   time, so two builds write `dist/` concurrently and images/favicon get overwritten →
   check fails ("引用的本地资源都存在" ✗) and nothing is deployed. Never "fix" it with `--force`;
   kill dev.js, run `node scripts/build.js` once, `check.js` must pass, then ship.
6. **Deploy.** Preferred — `publish.mjs ship <repo> <slug>`: creates the site, backfills
   `url` + `deploy.siteId` into page.json, redeploys with the real URL, then runs the
   platform's landing-page audit (countries = `routing.sites`). `publish.mjs whoami` first; if not
   logged in, run `publish.mjs login` and tell the user to open the printed link and approve
   (they need the platform's app_id and API address — ask, or set `BV_APP_ID` / `BV_API_BASE`; this step is optional and only works with a compatible platform). Creating a site is outward-facing: confirm
   the site name / subdomain with the user before the first `ship` (`deploy --dry-run` shows
   the plan).
   Manual fallback (no login possible): `node scripts/package.js <slug> --force` → user
   uploads via 新建部署 (entry `index.html`, 加密访问 off) → user sends the assigned URL → put
   it in `page.json` `url` → `node scripts/package.js <slug>` (must pass) → user uploads with
   部署新版本. Always give the exact zip path and say older zips are obsolete.
7. **Live verification.** `verify.mjs <url> --dist <repo>/dist/<slug> --proxy …` — the
   platform audit does not test pixel delivery, geo routing or consent. Report per group; if
   the exit is CN, say pixel delivery is unverified and ask for an overseas node rather than
   presenting skipped checks as passes.
8. **Hand-off.** Changelog (template below) and what the client still owes (copy review,
   banner text, legal sign-off).

## Workflow B — change an existing page
Edit → `publish.mjs deploy <repo> <slug> --remark "<what changed>"` (or `package.js <slug>` →
user uploads with 部署新版本) → `verify.mjs --dist`. For content updates, change
content only and leave styling alone unless asked. Adding a country = `routing.sites` +
fixed CTA + `links` entries + time zones in `geo.js` (+ `consent.countries` if UK/EU).

## Workflow C — "does it work / is it compliant?"
Run `verify.mjs` first; answer from its output. For a fuller content review add
`publish.mjs audit <url> --countries …` (the platform's 6-dimension audit; works for any URL,
not only our sites). Its items carry `basis`: only `openai_official` items are OpenAI rules —
`training` items are the training framework's recommendations and must be labelled so. For compliance, separate three kinds of
statement and label each: **OpenAI requires** (quote openai-requirements.md / fetched text),
**law in that market usually expects** (privacy-consent.md, not legal advice), **our
checklist recommends**. Never escalate a recommendation to "OpenAI requires".

## Reporting results to the user
- Lead with the verdict, then a short table (event/country → result). Distinguish
  "verified live", "verified locally", "not verified (why)".
- `202` from `bzr.openai.com` = OpenAI accepted the event; matching to a conversion is
  confirmed in Ads Manager, not by us.
- Name things the user can act on: exact zip path, exact platform button, exact DevTools path.

## Changelog template
```
## <Client> <page> 更新记录
站点 / 上传包 / 对比版本
### 新增   (user-visible behaviour first, one bullet per capability)
### 修复
### 工程改动 (files touched, one line each)
### 验证   (what was verified, where: local / live, with which exit country)
### 已知限制
### 待办   (deploy, client confirmations, git commit)
```
