---
name: developer-oss-research
description: Researches GitHub repos/users/orgs and Chrome Web Store extensions via the Crawlora API — search, profiles, contributors, releases, trending, and extension detail/reviews/permissions — returning clean JSON. Use when the user wants a repo or developer's GitHub profile/stats, what's trending on GitHub, or a Chrome extension's details, permissions, or reviews.
---

# Developer & open-source research

Look up GitHub repos, users, and orgs, plus Chrome Web Store extensions, as
normalized JSON from the Crawlora API — no scraping github.com or the
Chrome Web Store.

## When to use this skill

- "Tell me about this GitHub repo/user/org" (stars, languages, followers).
- "What's trending on GitHub right now?" (by language).
- "Who contributes to this repo?" / "what are its releases?"
- "Tell me about this Chrome extension" (permissions, privacy, reviews).
- "Search extensions for <keyword>" or "what's similar to this extension?"

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **GitHub repos** — `/github/search/repositories` (`q`, GitHub search
   syntax works) to find one; `/github/repo/{owner}/{repo}` for detail, plus
   `/contributors`, `/languages`, `/releases`, `/forks`.
2. **GitHub users/orgs** — `/github/search/users` (`q`); `/github/user/{username}`
   (+ `/followers`, `/following`, `/repos`, `/events`, `/pinned`) or
   `/github/org/{org}` (+ `/repos`). `/github/trending` and
   `/github/trending/developers` (filter by `language`, `since`) cover
   what's hot right now.
3. **Chrome Web Store** — `/chromewebstore/search` (`term`) to find an
   extension `id`; `/chromewebstore/item` for detail, `/permissions`,
   `/privacy`, `/reviews`, `/similar`. `/chromewebstore/charts` and
   `/chromewebstore/category` cover browsing/trending; `/chromewebstore/developer`
   lists everything one publisher ships.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# GitHub:
scripts/crawlora.sh /github/search/repositories q="language:go stars:>1000" | jq '.'
scripts/crawlora.sh /github/repo/anthropics/claude-code | jq '.'
scripts/crawlora.sh /github/trending language=python | jq '.'

# Chrome Web Store:
scripts/crawlora.sh /chromewebstore/search term="ad blocker" | jq '.'
scripts/crawlora.sh /chromewebstore/item id=<extension-id> | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every GitHub and
Chrome Web Store endpoint this skill uses.

## Examples

- **Repo due diligence:** `/github/repo/{owner}/{repo}` + `/contributors` +
  `/releases` to gauge activity and maintenance health before depending on it.
- **Trending scan:** `/github/trending` (by language) + `/github/trending/developers`
  for a daily/weekly pulse on what's gaining traction.
- **Extension safety check:** `/chromewebstore/item` + `/permissions` +
  `/privacy` before recommending or installing a browser extension.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public profile/repo/extension pages.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **GitHub search accepts GitHub's own search qualifiers** (`language:`,
  `stars:>N`, `org:`, …) inside `q` — same syntax as github.com's search bar.
- List endpoints are paginated (`page`/`per_page`) — walk pages for full coverage.
