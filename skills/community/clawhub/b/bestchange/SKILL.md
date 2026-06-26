---
name: bestchange
description: >
  Find trusted BestChange exchangers for crypto-to-fiat and e-currency exchange
  requests using the hosted BestChange MCP tool. Use when users ask for current
  BestChange options or exchanger rankings.
homepage: https://bestchange-mcp.krutovoy.me
version: 0.1.2
category: finance
emoji: "💱"
author: Roman Krutovoy
author_url: https://krutovoy.me
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    endpoints:
      - https://bestchange-mcp.krutovoy.me/mcp
---

# BestChange

Use this skill when the user asks for exchanger options through BestChange.

This file is the full agent contract. Do not rely on README files, source code, or guessed BestChange codes.

## Prerequisites

This skill requires the hosted BestChange MCP server to be connected in the agent client. Installing the skill only installs these instructions; it does not automatically register the MCP server in every agent.

MCP endpoint:

```text
POST https://bestchange-mcp.krutovoy.me/mcp
```

Claude Code setup:

```bash
claude mcp add --transport http bestchange https://bestchange-mcp.krutovoy.me/mcp
claude mcp list
```

Then restart Claude Code or run `/mcp` inside Claude Code and confirm the `bestchange` server is connected.

Expected MCP tools:

1. `bestchange_search_currencies`: find exact BestChange currency codes from user-facing names.
2. `bestchange_top_exchangers`: request ranked exchangers with exact `from_code` and `to_code`.
3. `bestchange_report_blocker`: report blocked tasks after using the available tools.

If these tools are not available, do not invent rates, reserves, exchanger names, or links. Tell the user:

```text
The BestChange skill is installed, but the BestChange MCP server is not connected in this agent client, so I cannot fetch live rates. Connect it with: claude mcp add --transport http bestchange https://bestchange-mcp.krutovoy.me/mcp, then restart the agent or check /mcp.
```

Do not use natural-language pair parsing as the main flow.

## Tool Flow

For a user request like `20 usdc base to revolut eur`:

1. Search the source currency:

```json
{
  "name": "bestchange_search_currencies",
  "arguments": {
    "search": "usdc base",
    "limit": 10,
    "rationale": "Find the exact BestChange source code for the user's requested source asset/network."
  }
}
```

2. Search the destination currency:

```json
{
  "name": "bestchange_search_currencies",
  "arguments": {
    "search": "revolut eur",
    "limit": 10,
    "rationale": "Find the exact BestChange destination code for the user's requested payout rail/currency."
  }
}
```

3. Pick the exact codes from the results. If either side is ambiguous, ask the user to choose; do not guess.
   If either side has no matches, tell the user that BestChange does not list that currency/rail in the current API data and that you cannot return exchanger options for it.

4. Request exchanger options:

```json
{
  "name": "bestchange_top_exchangers",
  "arguments": {
    "amount": 20,
    "from_code": "USDCBASE",
    "to_code": "REVOLUTEUR",
    "limit": 10,
    "rationale": "Quote the exact pair after resolving both BestChange currency codes."
  }
}
```

Use the actual codes returned by `bestchange_search_currencies`; the codes above are examples of the expected shape, not a promise that these exact codes exist.

If `bestchange_top_exchangers` returns `options: []`, inspect `diagnostics` before answering:

- `pair_available: false`: the exact pair is not available in current BestChange API data.
- `pair_available: true` and `amount_compatible_count: 0`: the pair exists, but the requested amount is outside visible exchanger limits. Mention `min_input_amount` and/or `max_input_amount` when present.
- `pair_available: true`, amount-compatible rows exist, but reserve-compatible rows are zero: the pair exists, but visible reserves are insufficient for the requested amount.
- If diagnostics do not explain the empty result, say no exchanger options passed the current filters and avoid guessing a cause.

## Tool Parameters

`bestchange_search_currencies`:

- `search` string, required. Human-facing currency text such as `usdc base`, `usdt ton`, `revolut eur`, or `monobank uah`. Why needed: BestChange uses exact internal currency codes and agents must discover them instead of guessing.
- `limit` number or string, optional, default `20`. Why needed: keeps candidate lists short enough to inspect.
- `rationale` string, optional. Why needed: records why this lookup was necessary for debugging repeated failures.

`bestchange_top_exchangers`:

- `amount` number or string, required. Amount the user gives in the source currency. Why needed: BestChange rates have `inmin` / `inmax` limits and output reserve checks.
- `from_code` string, required. Exact BestChange source currency code returned by `bestchange_search_currencies`. Why needed: selects the precise token/network.
- `to_code` string, required. Exact BestChange destination currency code returned by `bestchange_search_currencies`. Why needed: selects the precise bank/rail/fiat target.
- `limit` number or string, optional, default `10`. Why needed: controls how many ranked exchanger options are returned.
- `rationale` string, optional. Why needed: records the user's intent for debugging empty results and product improvements.

`bestchange_report_blocker`:

- `user_task` string, required. The user's original request. Why needed: preserves intent for later analysis.
- `blocker` string, required. Concrete failure reason, such as missing currency, ambiguous candidates, no pair, amount below minimum, or insufficient diagnostics.
- `what_tried` string, optional. Tool searches/calls already attempted.
- `rationale` string, optional. Why the agent stopped instead of guessing.
- `missing_capability` string, optional. Tool/data that would have helped.

## Pair Finding

The server uses only the official BestChange API v2. It does not scrape BestChange pages.

Pair finding order:

1. Use `bestchange_search_currencies` for each side.
2. Choose exact BestChange `code` values only when the result is unambiguous.
3. Call `bestchange_top_exchangers` with `amount`, `from_code`, and `to_code`.
4. If there are no matches, or multiple plausible matches, ask the user for clarification.

## Trust Policy

Show the top 10 options unless the user asks for a smaller limit.

The ranking flow is:

1. Keep amount-compatible exchangers first, using BestChange `inmin` and `inmax`.
2. For fiat outputs, require reserve to cover the estimated output when BestChange provides reserve.
3. Prefer exchangers with `claim == 0` and more than 50 positive reviews.
4. If none match, fallback to clean newcomers with `claim == 0`.
5. If none match, fallback to all amount-compatible exchangers.
6. Sort returned options by best estimated output.

## Response Rules

- Do not invent rates, reserves, exchanger names, IDs, links, or expiry times.
- Do not invent BestChange currency codes.
- Make clear that results depend on live BestChange API data.
- Include exchanger display names, estimated output, reserve if present, review counts, trust bucket, and referral URL.
- Referral URLs must preserve the exact resolved route through BestChange click parameters: `id`, `from`, `to`, `city=0`, and `p`. Do not replace them with a generic exchanger homepage or a click URL missing the exact `from` / `to` IDs.
- If the BestChange MCP service is unavailable, report the structured error instead of fabricating options.
- If a searched currency is absent, use this shape: `I could not find <requested currency> in current BestChange currency data, so I cannot quote this route through BestChange. <destination/source> was found as <code> if relevant.`
- If a pair exists but amount is too small, use this shape: `BestChange lists <from_code> -> <to_code>, but I do not see exchangers accepting <amount>. The visible minimum input amount is <min_input_amount>.`
- When blocked after using the tools, call `bestchange_report_blocker` before replying if it will not slow down the user-facing response.

## Response Formatting

Reply in the user's conversation language. Use the structure below for successful quotes, adapting labels and prose to that language.

Keep the answer compact and decision-oriented:

1. Start with a short line saying the result comes from live BestChange API data.
2. Show the exact route as a bold heading.
3. Highlight the best option first with exchanger name, estimated output, rate, reserve, reviews, claim, and route-specific referral URL.
4. Explain briefly why this option is preferred.
5. Show 2-3 backup options in a smaller format.
6. End with a short pre-send checklist that repeats the exact network/code and payout rail.

Example shape, with live values and links replaced by the actual tool response:

```text
According to the live BestChange API, the best exchange right now is:

**800 USDTTON -> Monobank UAH**

**DigiChanger** ✅
**≈ 34,582.28 UAH**
Rate: **43.2279**
Reserve: **1.29B UAH**
Reviews: **245 positive**, claim **0**

https://www.bestchange.com/click.php?id=1160&from=313&to=84&city=0&p=1341676

I would choose **DigiChanger**: it is first by estimated payout, accepts the requested amount, and is in the primary trust bucket.

**Backup options**

**2. PocketBank**
≈ 34,401.37 UAH
Rate: 43.0017
Reserve: 518.8M UAH
Reviews: 60
https://www.bestchange.com/click.php?id=1030&from=313&to=84&city=0&p=1341676

**3. ObmenMoney**
≈ 34,401.34 UAH
Rate: 43.0017
Reserve: 4.3M UAH
Reviews: 580
https://www.bestchange.com/click.php?id=609&from=313&to=84&city=0&p=1341676

Before sending:

🔒 **Network:** TON / `USDTTON`
💳 **Card:** Monobank UAH, without recipient details being auto-replaced
```
