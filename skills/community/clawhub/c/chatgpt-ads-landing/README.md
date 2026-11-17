# chatgpt-ads-landing

A skill (a Markdown manual + Node scripts) for building, checking and verifying **static landing pages
for ChatGPT / OpenAI Ads** campaigns. Not affiliated with OpenAI — OpenAI's own documents are the
source of truth; this repo only turns their requirements into repeatable checks.

## What it does
- Builds a static page from a `page.json` + `index.html` (the body text is in the HTML source, so
  the ad crawler **OAI-AdsBot** can read it with JavaScript off).
- Runs ~26 offline checks before packaging (robots.txt, sitemap, structured data, one `h1`,
  placeholder text, Pixel installed, cookie-consent order for UK/EU, asset files exist, ...).
- Sends the OpenAI Pixel events (`oaiq`), keeps the client's UTM and OpenAI's `oppref` when it
  sends visitors to per-country destination URLs.
- `verify.mjs` checks the live page with a real Chrome: crawler user-agents get 200, the live files
  equal your build, events reach OpenAI (HTTP 202), per-country redirects, cookie-consent flow.
- Optional: `publish.mjs` deploys to a compatible hosting platform through its open API
  (you must set `BV_API_BASE` and `BV_APP_ID`; nothing is configured by default).

## Quick start (any AI assistant that supports skills, or just the command line)
Requirements: Node 22+, pnpm; Google Chrome for `verify.mjs`; an overseas network only for the
"events reach OpenAI" check.

```bash
node scripts/init-repo.mjs ./my-landing        # copy the engine into a working folder
node scripts/new-page.mjs ./my-landing my-page # create pages/my-page from the starter
cd my-landing && pnpm install
pnpm build && pnpm check my-page               # fill page.json / index.html first
pnpm package my-page                           # → out/my-page-<time>.zip
node ../scripts/verify.mjs https://your-site.example.com/ --dist dist/my-page --proxy http://<your-proxy>
```
With an assistant: copy this folder into its skills directory and ask in plain language, e.g.
"make a ChatGPT ads landing page for <client>, countries US and UK, material is here ...".
Only Claude Code and one DeepSeek-Harness-based assistant have been tried; others are untested.

## Limits
- The 300-word rule and similar numbers are heuristics, not OpenAI rules.
- Country routing uses ~40 time zones plus IP; add a row in `assets/engine/shared/geo.js` for other countries.
- Real-ad results from one airline campaign are small-sample and have no control group.

## License
MIT — see `LICENSE`.
