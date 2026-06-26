---
name: drillr
description: Access Drillr's financial research capabilities — agentic search over company financials, a high-signal market event feed, published analyst articles, and persistent per-user watchlists. Use this whenever the user asks about stock prices, company fundamentals, earnings, SEC filings, market signals, sector trends, or wants to track tickers over time. Requires a user-specific API key obtainable at https://drillr.ai/developer/keys.
version: 1.0.0
license: MIT
homepage: https://drillr.ai
metadata:
  openclaw:
    homepage: https://drillr.ai
    emoji: "📈"
---

# Drillr — Financial Research for Agents

Drillr exposes its AI research agent and financial data pipeline to
external agents through three equivalent channels: **MCP** (Streamable
HTTP), **REST API**, and a **command-line tool**. All three accept the
same `drl_*` API key and expose the same data.

## What you can do

- **search** — Ask natural-language questions about companies, sectors,
  tickers, filings, earnings. Runs server-side for 5-15s and returns a
  synthesized answer with source attribution.
- **signals** — Browse a curated feed of high-score market events
  (news + filings + alerts), filterable by ticker / sector / date.
- **articles** — Read published analyst articles with related-ticker,
  sector, and reference metadata.
- **watchlists** — Create, list, and mutate per-user ticker
  collections. Persisted across sessions on the user's Drillr account.

---

## Detecting the deployment context

Your onboarding path depends on ONE question:

> Can the user run shell commands on the machine where you are running,
> and see the output directly in the same conversation?

Physical hardware doesn't matter. A Mac mini, MacBook, home NAS,
Raspberry Pi, or cloud VM can all serve either path. What matters is
whether the user's current channel to you is **co-located with your
shell** or **relayed through a chat channel**.

### Path A — Indirect (relayed)

Signals that suggest Path A:

- User is chatting with you via Telegram / WhatsApp / Slack / Discord /
  a web chat UI / any IM
- Your input channel is text-only — you have no shared terminal
- User mentions they're on a phone, or away from the host machine
- Your runtime is a bot webhook (e.g. Telegram bot handler)
- The user cannot paste the output of `ls ~/.config/` back to you

→ Use **Onboarding A** below.

### Path B — Direct (co-located)

Signals that suggest Path B:

- You are running as Claude Code, a local Claude Agent SDK session, or
  any CLI the user is typing into right now
- You have a Bash / shell tool and anything you run is visible to the
  user in the same pane
- The user can copy-paste your suggested `export` or config-edit
  commands and run them immediately

→ Use **Onboarding B** below.

### When unsure, ask the user

> Quick setup question: are you talking to me through a terminal on the
> same machine I'm running on — where I can suggest shell commands for
> you to run — or through a separate channel like Telegram / WhatsApp /
> a web chat?

---

## Prerequisites — getting an API key

Do NOT attempt any tool call until you have a `drl_*` key accessible to
your runtime. If it's missing, run the onboarding path that matches
your deployment context.

### Onboarding A — Indirect (IM / web chat / remote host)

The user reaches you through a text-only relay and cannot touch your
filesystem. They will complete the key creation from whatever browser
they have (phone, tablet, or desktop) and paste the key back to you.

**Step 1 — Tell the user (verbatim):**

> To use Drillr I need an API key. From any browser (your phone is
> fine):
>
> 1. Open https://drillr.ai/developer/keys
> 2. Sign in — **Google sign-in is the quickest**; email/password also
>    works
> 3. Tap "Create API key" → give it a name (e.g. "my-agent") → copy
>    the `drl_...` string
> 4. Paste it back to me here. The key is shown only once.
>
> After I confirm it works, you can delete your message.

**Step 2 — When the key arrives, persist it:**

Write it to `~/.config/drillr/config.json` with file mode `0600`:

```json
{ "api_key": "drl_..." }
```

Equivalent shell:

```bash
mkdir -p ~/.config/drillr
umask 077
cat > ~/.config/drillr/config.json <<EOF
{ "api_key": "$KEY" }
EOF
chmod 600 ~/.config/drillr/config.json
```

**Step 3 — Verify the key works:**

```bash
curl -sS -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer drl_..." \
  https://gateway.drillr.ai/api/v1/watchlists
```

Expect HTTP `200`. On `401`, the key is invalid — apologize, ask the
user to regenerate, and rerun Step 1.

**Step 4 — Confirm to the user, masked:**

> Stored `drl_xxxxxxxx_...e9f2`. You can safely delete your message now.

**Rules:**

- Never echo the full key back to the user
- Never write the key into conversation logs, prompts, or scratchpads
- Never commit it to any file other than `~/.config/drillr/config.json`
- If storage fails (permission denied, etc.), tell the user the exact
  error — don't silently hold the key in memory

### Onboarding B — Direct (terminal co-located with user)

The user can run shell commands and see their output. Pick ONE of the
three equivalent options and instruct the user accordingly. All three
expect the same `drl_*` key created at
<https://drillr.ai/developer/keys>.

**B1. MCP via Claude Code (recommended for Claude Code users)**

Tell the user:

> 1. Create an API key at <https://drillr.ai/developer/keys> (Google
>    sign-in is easiest)
> 2. Add to `~/.claude.json` (or merge into the existing `mcpServers`
>    object):
>
>    ```json
>    {
>      "mcpServers": {
>        "drillr": {
>          "type": "http",
>          "url": "https://gateway.drillr.ai/mcp",
>          "headers": {
>            "Authorization": "Bearer ${DRILLR_API_KEY}"
>          }
>        }
>      }
>    }
>    ```
>
> 3. Add `export DRILLR_API_KEY=drl_...` to your shell rc
>    (`~/.zshrc` / `~/.bashrc`) and restart the shell
> 4. Restart Claude Code. `/mcp` should list `drillr` as connected.

**B2. CLI**

```
npm install -g drillr-cli
drillr auth set-key drl_...
drillr watchlist list     # verify: should list (or print "no watchlists yet")
```

**B3. REST with env var**

```
export DRILLR_API_KEY=drl_...
curl -H "Authorization: Bearer $DRILLR_API_KEY" \
     https://gateway.drillr.ai/api/v1/watchlists
```

---

## Choosing a channel (after onboarding completes)

Pick based on your runtime's capabilities:

| Runtime characteristic              | Preferred channel    |
| ----------------------------------- | -------------------- |
| Has native MCP client support       | **MCP**              |
| HTTP only (no MCP, no shell)        | **REST**             |
| Shell / subprocess available        | **CLI** or **REST**  |

All three are equivalent in data and rate limit. MCP tool names
operate by natural names (e.g. watchlist by name); REST uses UUIDs.

---

## Capabilities

### Research & data lookup — `search`

Ask natural-language questions about companies, tickers, sectors,
filings, earnings. Runs 5-15s server-side and returns markdown text
with source references.

| Channel | Call                                                            |
| ------- | --------------------------------------------------------------- |
| MCP     | `search({ question, session_id?, context? })`                   |
| REST    | `POST /api/v1/search` with `{ question, session_id?, stream? }` |
| CLI     | `drillr search "<question>"`                                    |

**Session continuity:** pass the returned `session_id` in the next
call to continue the same research conversation. Use `context` to
pass background info that refines the answer.

**Data coverage:**
- **Market data** — real-time quotes, historical OHLCV, index prices
  & composition (S&P 500, Dow, NASDAQ 100)
- **Fundamentals** — income / balance / cash flow statements
  (quarterly & annual), valuation ratios, company snapshots
- **Earnings** — call transcripts with AI summaries, calendar with
  EPS/revenue estimates vs actuals
- **Analyst research** — ratings & price targets (~550K events from
  500+ firms), consensus rollups
- **SEC filings** — semantic search across 10-K, 10-Q, 8-K, 20-F,
  6-K, S-1, F-1
- **Corporate events** — M&A, debt issuance, securities offerings
- **People & governance** — executive profiles, compensation,
  appointments & departures
- **Ownership** — insider trades (Form 3/4/5), institutional
  holdings (13F-HR, 13D/G)
- **News** — aggregated financial news with importance scoring
- **Company discovery** — by industry, product, technology, business
  model, supply chain
- **Alternative data** — energy, data centers, semiconductors,
  compute & inference pricing, AI model development, platform
  adoption, sentiment, macro & trade, patents

**When to use `search`:**
- Stock prices, company financials, market data
- SEC filing content (risk factors, revenue breakdown, MD&A)
- Earnings summaries or analyst consensus
- Insider trading or institutional ownership
- Alternative data (AI value chain, energy, semiconductors)
- Compare companies or sectors

**Example questions that work well:**
- "What is AAPL's current PE ratio, and how does it compare to MSFT?"
- "Summarize NVDA's latest 10-Q earnings"
- "Which semiconductor companies had insider buying this month?"

### Signals — `signals`

A curated investment-event feed. Each signal is **one market event**
(one SUBJECT × one ACTION × one TIME), already aggregated across
outlets — you get one record per event, not one per article.

**Coverage** — sources rolled into the feed:

- News & wires: Finnhub, NewsAPI, GDELT, FMP, Bloomberg, Reuters,
  WSJ, FT, CNBC
- Filings: SEC 8-K, 13D/G, 6-K (foreign issuers), structured 8-K
  earnings data, earnings-call summaries
- Corporate disclosure: press releases
- Macro & policy: Fed / FOMC / BOJ / ECB / SEC / White House /
  Truth Social
- Market microstructure: analyst ratings, insider trading, intraday
  price movers
- Social: select financial subreddits

**Freshness**: signals appear within ~3–5 minutes of the originating
event.

| Channel | Call                                                                         |
| ------- | ---------------------------------------------------------------------------- |
| MCP     | `signals({ tickers?, sector?, since?, limit?, offset? })`                    |
| REST    | `GET /api/v1/signals?tickers=AAPL,MSFT&sector=Technology&since=...&limit=20` |
| CLI     | `drillr signals --tickers AAPL,MSFT --limit 5`                               |

Response shape: `{ headline, summary, suggested_tickers[], sector[], created_at }`, ordered newest first.

### Articles — `article_list` / `article_get`

Research articles spanning company-specific analysis, event coverage,
and industry trackers.

**What you'll find**:

- **Company & thesis** — focused single-name or small-group analysis
  (1–3 tickers), peer comparisons, annual ticker theses, SEC-filing
  follow-ups
- **Event coverage** — postmortems on what just happened, watch-pieces
  on pending events (policy decisions, upcoming earnings, lawsuits),
  follow-up checkpoints on previously covered events, macro-event
  analysis
- **Industry & sector** — thematic industry pieces (≥5 names),
  recurring sector trackers


| Channel | Call                                                                     |
| ------- | ------------------------------------------------------------------------ |
| MCP     | `article_list({ ticker?, tag?, limit?, offset? })` / `article_get({ article_id })` |
| REST    | `GET /api/v1/articles?ticker=NVDA&limit=10` / `GET /api/v1/articles/:id` |
| CLI     | `drillr articles list --ticker NVDA` / `drillr articles get <uuid>`      |

`article_get` returns the article body (markdown), plus `topics` and
`references` arrays. `article_list` returns 11 public fields per row
(id, title, summary, content, related_tickers, tags, sector, citation,
published_at, created_at, word_count).

### Watchlists

Per-user ticker collections. Owner-isolated (RLS): each key only sees
and mutates its owner's watchlists. Attempting to access another user's
watchlist by UUID returns `404`, not `403`.

| MCP (by name)                                        | REST (by UUID)                                    |
| ---------------------------------------------------- | ------------------------------------------------- |
| `watchlist_list`                                     | `GET /api/v1/watchlists`                          |
| `watchlist_create({ name, tickers? })`               | `POST /api/v1/watchlists`                         |
| `watchlist_add({ ticker, watchlist_name? })`         | `POST /api/v1/watchlists/:id/tickers`             |
| `watchlist_remove({ ticker, watchlist_name? })`      | `DELETE /api/v1/watchlists/:id/tickers/:ticker`   |
| `watchlist_delete({ watchlist_name })`               | `DELETE /api/v1/watchlists/:id`                   |

CLI: `drillr watchlist {list|create|add|remove|delete}` — see
`drillr watchlist --help`.

> MCP tools accept watchlist **names** (chat-friendly). REST uses
> **UUIDs** (URL-friendly). If `watchlist_name` is omitted on add, a
> default "My Watchlist" is used (created on miss).

---

## Typical workflows

### "Daily research briefing"

User: "Can you do a daily morning briefing on my portfolio?"

1. `watchlist_list` — see what tickers the user already tracks
2. If empty, ask the user for tickers; then `watchlist_create`
3. Each morning, execute in order:
   - `signals({ tickers: [...watchlist_tickers], since: "<24h-ago ISO>" })`
   - For any high-interest signal, `search({ question: "Deeper context on <headline>" })`
   - `article_list({ ticker: ... })` for any ticker with fresh activity
4. Synthesize into a chat-sized briefing (headline + 1-2 sentences + links)

### "Quick lookup"

User: "What's Nvidia's market cap?"

1. `search({ question: "What is NVDA's current market cap?" })`
2. Relay the answer and any cited sources

### "Sector scan"

User: "Any interesting biotech moves this week?"

1. `signals({ sector: ["Health Care"], since: "<7d-ago ISO>", limit: 30 })`
2. For each signal the user asks about, `article_list({ ticker })` or
   a follow-up `search` with `session_id` from the prior call

---

## Error handling

| HTTP | `code` string                | What to do                                                                                  |
| ---- | ---------------------------- | ------------------------------------------------------------------------------------------- |
| 400  | `invalid_body` / `invalid_query` / `invalid_id` | Fix parameter shape and retry (don't pester the user)                   |
| 401  | `unauthenticated` / `key_invalid` | Re-read the stored key; if still 401, rerun Prerequisites — the key is absent or wrong |
| 401  | `key_revoked`                | Tell the user their key was revoked; they need to create a new one at the developer portal |
| 401  | `key_expired`                | Tell the user their key expired; same fix                                                   |
| 403  |                              | Key is valid but lacks `external` scope — user needs to issue a different key               |
| 404  | `not_found`                  | Resource doesn't exist, or RLS hides it (someone else's). Do NOT assume just-deleted        |
| 429  |                              | Inspect `retry_after_seconds` in the body; sleep and retry                                  |
| 502  | `upstream_error`             | Transient data-source failure; retry once after 2-3s, then surface to user                  |

**On any 401: re-read `~/.config/drillr/config.json` or the
`DRILLR_API_KEY` env var BEFORE asking the user.** You have the
configuration — diagnose first, then instruct.

**Never** tell the user to "check their configuration."

---

## Rate limits

30 requests per minute per API key. On `429` the response body
includes `retry_after_seconds` (1-60s). For workflows that fan out
(e.g., scanning a 50-ticker watchlist), pace at ≤0.5 req/s or batch
via a single `search` or `signals` call with multiple tickers.

---

## Advanced

Drillr also supports OAuth 2.1 for MCP clients that implement Dynamic
Client Registration (e.g., Claude Code's built-in MCP OAuth). This
skill deliberately does **not** cover that path because:

- OAuth access tokens expire hourly and require client-side refresh
  that not all MCP runtimes implement correctly
- The browser callback step assumes the user and agent share a
  machine; Path A deployments (remote host / IM-driven) cannot
  complete it

For agent automation, prefer the `drl_*` API key flow above. If you
are a human user setting up Claude Code on your own laptop and prefer
the OAuth UX, see the Drillr developer portal
(<https://drillr.ai/developer/docs>).

---

## Reference

- Developer portal: <https://drillr.ai/developer>
- Create / manage API keys: <https://drillr.ai/developer/keys>
- Full API reference: <https://drillr.ai/developer/docs>
- Gateway base URL: `https://gateway.drillr.ai`
- MCP endpoint: `https://gateway.drillr.ai/mcp`
- CLI on npm: `drillr-cli` (`npm install -g drillr-cli`)

Tracks External API **v1** (2026-04). Breaking changes will ship as
`/api/v2/*` alongside `/api/v1/*`.
