# Lessons from the first airline build

Each item is something that actually went wrong or that the user corrected.

## Working with the user
- **"只做内容的增删，不要动我的样式"** — when asked to apply new content (a Feishu doc, a
  V2 design), change copy and sections only. Restyling uninvited got reverted
  ("我不是让你把样式改了…给我退回到上一版本"). If a layout change seems necessary, ask.
- **Don't invent copy.** A coupon heading ("30 CNY off · 80 CNY off") was made up to fill a
  card and had to be removed. Every number/claim must come from the client's material.
- **No client logo without authorisation** ("能不用他们的logo吗，但是要有一个logo") — build a
  simple own mark (favicon.svg + 64px png + 180px apple-touch-icon).
- When the user only wants content read from a specific source ("只使用 lark-cli 读取…"),
  use exactly that source (lark-doc skill / lark-cli for Feishu docs).
- The user answers in Chinese and tests with screenshots; give exact click paths for the
  Chinese UI (DevTools: ⋮ → 更多工具 → 传感器).
- When they say "这就是投放域名" after you flag a placeholder, they may think you don't
  know the domain — explain *where* the placeholder still is (live files vs build).

## Verification traps
- "I uploaded the latest zip" ≠ live is the latest build. Byte-compare live vs `dist/`
  (verify.mjs `--dist`) before debugging anything else; read the zip itself
  (`unzip -p out/x.zip index.html | grep …`) to prove which zip contains what.
- Ads Manager 事件流 shows only ~15 minutes of events; an "empty" stream an hour after the
  test proves nothing. In DevTools, search `events` and open the payload — event names are
  not in the request URL.
- sitemap.xml `<lastmod>` is the build date, so every rebuild changes it even with no content
  change. verify.mjs `--dist` ignores it; don't treat a lastmod-only diff as "not deployed".
- Check the proxy exit country first. From CN the OpenAI SDK, openai.com policy pages and
  help center return 403; the same proxy can exit CN one day and UK the next.
- A system proxy (Clash) also captures a Chrome launched "without proxy" — use
  `--no-proxy-server` to really test a direct (CN) visitor.
- Cloudflare-protected OpenAI pages need a *visible* Chrome (fetch-official.mjs).
- Brand booking sites of large airlines sit behind Incapsula: curl gets a challenge page, real
  browsers work. Verify destinations in Chrome, not curl.
- `file://` pages: localStorage works, cookies don't — pixel cookies won't appear.
- Killing Chrome loses localStorage; close gracefully (lib/cdp.mjs does) for revisit tests.
- Smooth scrolling (`scroll-behavior: smooth`) makes screenshots catch mid-scroll; set it to
  `auto` first. `scrollIntoView` on the footer does not reveal padding below it.

## Claims
- Never present the internal checklist (or the old six-dimension check) as "OpenAI
  requires". Fetch the official text and quote it; mark the rest as recommendation.
- The six-dimension `check.js` from the old skill keys on its own template class names
  (`btn-primary`, `hero-stats`, top-level `Offer`) — on hand-built pages it reports false
  failures. Read the page before repeating a failure.
- The page already had a 24-hour airport hotline; "no contact info" was a regex miss.

## Geo
- Static site → no server-side IP. Time zone is the default signal (distinguishes US/CA);
  IP lookup (Cloudflare trace → country.is, 2 s timeout each) is an optional override,
  applied after load, and only wins when the IP country is a listed site.
- Visitors in no listed country get `routing.fallback` — for the first airline build that was the **US**
  site, not the airline's home-market site. State the actual fallback when describing routing.
- The consent banner never uses IP (decided before pixel init). When describing consent,
  say "UK time zone / language", and mention the UK-IP-but-other-zone gap.
- "按 IP 跳转" from the user means: geo CTA must land on *the same URL as that country's
  fixed Book-now CTA*; other countries keep the old fallback. Confirm by comparing hrefs
  (verify.mjs geo group), not hostnames alone.
