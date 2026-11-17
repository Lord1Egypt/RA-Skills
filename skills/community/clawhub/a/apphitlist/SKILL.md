---
name: apphitlist
description: Research iOS App Store apps with the AppHitlist MCP server. Use when the user asks which new apps already make money, what earns the most in a category, which apps are climbing or entering the daily App Store charts, how much an app makes, how long an app's Meta ads have run, or what users complain about in an app or category. Covers niche discovery, competitor analysis, ad research and complaint-based opportunity finding. Needs the AppHitlist MCP server connected.
---

# AppHitlist MCP

AppHitlist is an App Store research tool for indie developers. This skill tells you which of its nine MCP tools to call for which question, how to chain them, and how to read the results. Coverage is iOS only.

## Before you start

- The server is `apphitlist` (endpoint `https://apphitlist.com/api/mcp`, API key as `Authorization: Bearer <key>`). If its tools are not available, tell the user to connect it: create a free key at https://apphitlist.com/dashboard/mcp and add it with `claude mcp add --transport http apphitlist https://apphitlist.com/api/mcp --header "Authorization: Bearer YOUR_API_KEY"` (or the Cursor, VS Code or Codex equivalent). Never ask the user to paste a key into the chat and never write one into a file you create.
- A free key allows 20 tool calls per month. Plan the questions so each call counts, and say so when a task needs many calls.

## Free key vs Pro key

| | Free key | Pro key |
|---|---|---|
| Revenue and downloads | Bands: `revenueRange` (for example `$10K–$25K`, `$1M+`) and `downloadsRange` (for example `5K–10K`) | One monthly figure: `latestRevenueUsd`, `latestDownloads` |
| Price, rating, rating count | Not returned | Returned by `find_top_earning_apps`, `search_apps`, `find_chart_movers`, `get_app` |
| `get_app` extras | None | Price, currency, rating, in-app purchase flag, store URL, description, 30-day chart rank summary |
| Ad and complaint tools | Return `{"error": "subscription_required", "upgradeUrl": ...}` | Available |
| Limits | 20 calls a month | 60 calls a minute, no monthly cap |

How to behave:

- Free key: report bands as bands. Do not turn a band into a single number, a midpoint or a precise estimate. A `null` range means the app is below the lowest band, or the app shows no figure.
- Do not call a Pro-only tool on a free key to "try it": the call is spent and returns `subscription_required`. If the user needs ads or complaints and you only know they are on a free key, say what the tool would give and that it needs Pro, or try once and report the result.
- Pro key: figures are single monthly numbers in USD (revenue) and counts (downloads). Say "monthly" every time.
- The `note` field in responses states that figures come from AppHitlist's own model. Present figures as AppHitlist figures, not as the developer's reported numbers.

## Which tool for which question

| User asks | Call |
|---|---|
| "What new apps are already earning?" "Any new hits in fitness?" | `find_new_winning_apps` (optional `category`) |
| "What earns the most in Finance?" "Biggest apps in a category" | `find_top_earning_apps` (optional `category`) |
| "What is climbing the charts today?" "What just entered the top grossing in the UK?" | `find_chart_movers` (`country`, `chart`, optional `category`, `date`, `days`) |
| "Find the app called X" or only a name or developer is known | `search_apps` (`query`) |
| "How much does X make?" "Tell me about this App Store link" | `get_app` (`app`: URL, numeric id or name) |
| "Which ads has X been running longest?" | `get_app_ads` (`app`), Pro |
| "Which ads work in the Food & Drink category?" | `find_longest_running_ads` (optional `category`), Pro |
| "What do users hate about X?" | `get_app_complaints` (`app`), Pro |
| "What do users complain about in category Y?" "Pricing or billing complaints?" | `get_category_complaints` (`category`, optional `kind`: `product`, `billing` or `price`), Pro |

Parameter facts, all verified against the tool schemas:

- `category` accepts a name ("Health & Fitness"), a short name ("fitness", "puzzle games") or a numeric genre id. On `category_not_found` the response lists valid names: pick one and retry.
- `app` accepts an App Store URL, a numeric id or a name. A name resolves to the top search match, so for common names run `search_apps` first and use the numeric id or URL.
- `limit` ranges: 1–50 for `find_new_winning_apps`, `find_top_earning_apps` and `find_chart_movers`; 1–10 for `search_apps`; 1–20 for the two ad tools; 1–30 for `get_category_complaints`.
- `find_chart_movers`: `chart` is `grossing` (default), `free` or `paid`; `country` is a two-letter code (default `us`, 36 supported); `days` is 1–28 (1 is day over day, 7 is week over week); `date` is `YYYY-MM-DD` in UTC, default latest.
- `find_new_winning_apps` leaves games out unless `category` is `Games`.
- Category chart lists are not available everywhere: `us`, `gb`, `de` have grossing, free and paid; many mid-size countries have grossing and free; the rest only grossing. On `chart_not_available`, read the `hint` and retry with an overall list (no `category`) or another chart.

## Typical workflows

### Niche discovery (is there money in this space?)

1. `find_new_winning_apps` for the category: who got to $10K a month within six months?
2. `find_top_earning_apps` for the same category: what does the established ceiling look like?
3. `find_chart_movers` with `chart: "grossing"`, `category`, and `days: 7`: is anything rising right now?
4. Summarize: how many new winners, how crowded the top is, what kinds of apps rise. Name specific apps with their `profileUrl`.

Cost: 3 calls.

### Competitor analysis

1. `search_apps` to get the right app (skip if you already have a URL or id).
2. `get_app` for the profile. On Pro it includes the 30-day `rankSummary`: use best vs latest rank to say whether the app is growing or fading.
3. Find peers: `find_top_earning_apps` or `find_new_winning_apps` in the app's `category`, and compare revenue and release dates.
4. Optional Pro follow-ups: `get_app_ads` and `get_app_complaints`.

### Ad research (Pro)

1. `find_longest_running_ads` for the category, or `get_app_ads` for one app.
2. Sort by `daysRunning`. Long-running active ads usually mean the ad pays for itself, so they are the best creative to study. Report `format`, `cta`, `platforms`, the hook in `title` and `body`, and `copies` (how many variants).
3. Treat short-lived ads as tests, not signals. Do not claim an ad's spend or results: only its runtime is known.

### Complaints to opportunity (Pro)

1. `get_category_complaints` for the category. Run it again with `kind: "billing"` or `"price"` if the user cares about monetization.
2. For the top two or three apps in the category (from `find_top_earning_apps`), `get_app_complaints` to see whether the category themes show up in the leaders.
3. Turn themes into opportunities: a theme with high `reviewCount` across many apps (see the example apps in the result) is a gap in the category. Pair it with step 1 of niche discovery: a gap in a category where new apps already earn is the strongest finding.

### Daily or weekly watch

`find_chart_movers` for the user's country and category, `days: 1` for a daily check, `days: 7` for a weekly one. Report risers (`previousRank` to `rank`, `change`) and new entries separately, and check any unknown app with `get_app`.

## Reading the results

- `profileUrl` links to the AppHitlist profile of the app: include it so the user can click through.
- Bands are coarse by design. Compare apps by band, say "same band" instead of ranking inside a band, and never compute growth rates or per-user figures from bands.
- Revenue is monthly and in USD. It is a model figure, not an audited one. Round claims accordingly ("roughly", "in the $50K–$100K band").
- `releasedAt` matters for "new winners": an old app that rose in the charts is a different story from a six-month-old app at $10K.
- Chart `change` is places climbed between the two chart dates; `comparedWith` tells you which earlier day was used. If `warning` is set, repeat it to the user: for countries outside the core markets a new entry can simply be new to AppHitlist's catalog.
- Complaint `reviewCount` counts 1 and 2 star reviews that mention a theme, not all reviews. Say "of the low-star reviews analysed", not "users in general".
- `daysRunning` is how long the ad has been active; `copies` is the number of variants of it.
- An empty list is a result: say the filter matched nothing and offer a wider one (no category, longer `days`, another country).

## Errors

| Response | What to do |
|---|---|
| HTTP 401 or tool unavailable | The key is missing, mistyped or revoked: tell the user to create a new key |
| "used all 20 free calls" message | Monthly cap reached. Give the reset time from the message and stop calling tools |
| "Rate limit reached" message | Pro rate limit (60 per minute): wait until the time given |
| `subscription_required` | The tool needs Pro: report that instead of retrying |
| `app_not_found` | Use `search_apps` and pass the numeric id |
| `category_not_found` | Retry with a name from the returned `categories` |
| `chart_not_available` | Read `hint` and `latestChartDate`; retry with another chart or without `category` |

## What AppHitlist does not give you

Do not promise or invent anything outside the tools: no Android data, no keyword or ASO ranking tool in this MCP server, no download or revenue time series, no developer contact details, no way to write or change anything. If a user asks for one of these, say the MCP server does not provide it.
