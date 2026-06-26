---
name: smart-search
description: Intelligent web search routing across Gemini and Brave APIs with quota management, circuit breaker, and web_fetch fallback. Routes finance queries to Gemini, space/astronomy to Brave, with per-agent daily allocations and shared pool.

homepage: https://github.com/Spear-Fox-Technologies/smart-search

metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "os": ["darwin", "linux"],
        "requires": { "bins": [] },
        "install": []
      }
  }
---
# smart-search

## 1. WHAT THIS SKILL DOES

This skill routes search queries to the best available provider, manages daily API quota per agent, logs all searches, and degrades gracefully through web scraping when APIs are unavailable. It supports two execution strategies: scheduled agents that prioritise API calls for reliable results, and a general agent that preserves API quota by trying web scraping first. All quota state is persisted to a shared JSON file so multiple agents can coordinate without overrunning daily limits.

---

## 2. WHEN TO INVOKE THIS SKILL

Use this skill whenever an agent needs to search the web for information — news, research, stock data, general queries, or any topic requiring up-to-date results.

This skill exposes three tools:

| Tool | Purpose |
|---|---|
| `smart_search` | Execute a web search and return results |
| `search_quota_status` | Check remaining quota for an agent or the full system |
| `search_mark_agent_complete` | Release unused quota to the shared pool when an agent finishes |

---

## 3. TOOL REFERENCE

### `smart_search`

Executes a search query using the best available provider for the given agent.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | Yes | The search query. Max 1000 characters. No control characters. |
| `agent_id` | string | Yes | Lowercase letters, numbers, and hyphens only (e.g. `stock-analysis`). Use `general` for manual/chat searches. |
| `force_provider` | string | No | Override routing. Accepts `"gemini"` or `"brave"` only. |

**Return shape:**

```json
{
  "results": "<string or array>",
  "provider_used": "gemini | brave | web_fetch",
  "queries_remaining": 12,
  "quota_source": "agent_allocation | shared_pool | provider_direct | none",
  "fallback_used": false,
  "warning": null,
  "web_fetch_engine": null,
  "error": null
}
```

On failure `results` is `null` and `error` contains the reason.

---

### `search_quota_status`

Returns quota information for a specific agent or the full quota file.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | string | No | If omitted, returns the full quota object. |

**Return shape (single agent):**

```json
{
  "agent_id": "stock-analysis",
  "gemini": { "allocated": 15, "used": 3, "remaining": 12 },
  "brave":  { "allocated": 0,  "used": 0, "remaining": 0  },
  "completed": false
}
```

---

### `search_mark_agent_complete`

Marks an agent as done for the day and releases any unused allocation to the shared pool for other agents to use.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | string | Yes | The agent to mark complete. |

**Return shape:**

```json
{
  "agent_id": "tech-news",
  "released": { "gemini": 7, "brave": 0 },
  "message": "Agent marked complete. 7 Gemini calls released to shared pool."
}
```

---

## 4. TWO EXECUTION STRATEGIES

### Strategy A — Scheduled agents (any `agent_id` except `general`)

Used by automated agents with a known workload. Prioritises API quality; uses web scraping only as a last resort.

| Tier | Provider | Condition |
|---|---|---|
| 1 | Primary API (Gemini or Brave) | Agent has allocation remaining |
| 2 | Fallback API (opposite provider) | Primary exhausted or failed |
| 3 | DuckDuckGo web_fetch | Both APIs unavailable — **blocked for finance queries** |
| 4 | Error | All providers exhausted |

### Strategy B — General agent (`agent_id: "general"`)

Used for manual chat or ad-hoc queries. Preserves API quota by trying web scraping first. Finance queries are not blocked from web_fetch in this strategy.

| Tier | Provider | Condition |
|---|---|---|
| 1 | Google web_fetch | Always attempted first |
| 2 | Bing web_fetch | Google failed |
| 3 | API (Gemini or Brave) | Both web_fetch failed — quota consumed only here |
| 4 | Error | All providers exhausted |

---

## 5. PROVIDER ROUTING RULES

Routing is automatic based on query keywords. `force_provider` overrides all routing.

**Routes to Gemini:**

| Keyword |
|---|
| stock, share price, nse, bse, wse, nyse, nasdaq |
| earnings, ipo, dividend, funding round, acquisition |
| merger, valuation, competitor, market share |
| breaking, just announced, today, hours ago |
| spearfox, fifthspear |

**Routes to Brave:**

| Keyword |
|---|
| space, astronomy, nasa, esa, cosmos |

If no keywords match, the query routes to the configured `default_provider` (defaults to `brave`). Gemini always wins for finance queries regardless of other keywords.

Keyword lists are configurable in `openclaw.json` via `finance_keywords` and `brave_keywords` arrays.

---

## 6. WEB_FETCH ENGINES

| Engine | Used by | Role |
|---|---|---|
| Google | Strategy B (general) | Tier 1 — always tried first |
| Bing | Strategy B (general) | Tier 2 — tried if Google fails |
| DuckDuckGo | Strategy A (scheduled) | Last resort — blocked for finance queries |

All engines enforce a 2-second minimum delay between consecutive calls to avoid rate-limiting. Responses are capped at 10,000 characters to protect the model context window. Prompt injection patterns are stripped from all results before they are returned.

---

## 7. QUOTA SYSTEM

Each provider has a daily limit set in `openclaw.json`. Each agent has its own allocation drawn from that pool. Quota is tracked separately per provider (`gemini_used`, `brave_used`).

**Deduction flow for a single search call:**

1. **Agent allocation** — deducted first if the agent has remaining quota for the provider
2. **Shared pool** — used if the agent allocation is exhausted but other agents have released unused quota
3. **Provider direct** — used if the shared pool is empty but the provider daily limit has remaining headroom
4. **Fallback provider** — if all sources for the primary provider are exhausted, the opposite provider is tried through the same flow
5. **web_fetch** — used if both APIs are unavailable (scheduled agents only; blocked for finance queries)
6. **Error** — returned if all paths are exhausted

Config owns the ceilings (daily limits, per-agent allocations). The quota file owns the live counters. Changes to `openclaw.json` take effect on the next call without restart.

General agent quota is only consumed when both web_fetch attempts fail.

---

## 8. CONFIG-DRIVEN BEHAVIOUR

All allocations, limits, and behaviour flags live in `openclaw.json` under `skills.smart-search`. Changes take effect on the next skill invocation with no restart required.

```json
{
  "skills": {
    "smart-search": {
      "gemini_model": "gemini-2.0-flash",
      "default_provider": "brave",
      "strict_agents": false,
      "retry_max_attempts": 3,
      "retry_base_delay": 500,
      "finance_keywords": ["stock", "earnings"],
      "brave_keywords": ["space", "astronomy"],
      "providers": {
        "gemini": { "daily_limit": 1500 },
        "brave":  { "daily_limit": 66 }
      },
      "agent_allocations": {
        "stock-analysis": { "gemini": 15, "brave": 0 },
        "general":        { "gemini": 20, "brave": 5 }
      }
    }
  }
}
```

| Key | Default | Effect |
|---|---|---|
| `gemini_model` | `gemini-2.0-flash` | Gemini model used for all API calls |
| `default_provider` | `brave` | Fallback provider when no keywords match |
| `strict_agents` | `false` | When `true`, rejects agent IDs not defined in config |
| `retry_max_attempts` | `3` | Maximum API retry attempts per call |
| `retry_base_delay` | `500` | Base delay in ms for exponential backoff |
| `finance_keywords` | Built-in list | Keywords that force Gemini routing |
| `brave_keywords` | Built-in list | Keywords that force Brave routing |

---

## 9. API KEY SECURITY

API keys are read from the `env` block in `openclaw.json` and held in memory only for the duration of the call. They are never logged to any file, never included in any error message, and never returned in any response object. Keys are not written to disk by this skill.

---

## 10. MANUAL CHAT USAGE

For manual or chat-initiated searches, OpenClaw must pass `agent_id: "general"`. The skill automatically uses web_fetch first for this agent, so API quota is only consumed if both Google and Bing scraping fail. This is an OpenClaw configuration responsibility — the skill does not infer the agent from context.

---

## 11. LOG ROTATION

Each day's searches are written to a `.jsonl` file in the `logs/` subdirectory alongside the quota file:

```
~/.openclaw/workspace/shared/logs/search-YYYY-MM-DD.jsonl
```

Each line is a JSON object with: `timestamp`, `agent_id`, `query`, `provider_used`, `force_provider`, `quota_source`, `queries_remaining`, `success`, `response_summary` (capped at 500 chars), `error`, `fallback_used`, `web_fetch_engine`.

Log files older than 30 days are deleted automatically based on the filename date, not the filesystem modification time.

---

## 12. ERROR REFERENCE

| Error | Cause | Resolution |
|---|---|---|
| `query is required and must be a non-empty string.` | Missing or blank query | Pass a non-empty string |
| `query exceeds maximum length of 1000 characters.` | Query too long | Shorten the query |
| `query contains invalid control characters.` | Null bytes or control chars in query | Strip control characters before calling |
| `agent_id is required and must be a non-empty string.` | Missing agent_id | Pass a valid agent_id |
| `agent_id must contain only lowercase letters, numbers, and hyphens.` | Invalid characters in agent_id | Use only `[a-z0-9-]` |
| `Unknown agent: "...". Add it to openclaw.json to use it.` | strict_agents is true, agent not in config | Add agent to config or disable strict_agents |
| `Invalid force_provider: "...". Use "gemini" or "brave".` | Unknown provider name | Use `gemini` or `brave` only |
| `Perplexity is not yet implemented.` | force_provider set to `perplexity` | Use `gemini` or `brave` |
| `GEMINI_API_KEY is not configured in openclaw.json.` | Missing API key | Add key to openclaw.json env block |
| `Brave Search is not configured. Add BRAVE_API_KEY to openclaw.json to enable it.` | Missing API key | Add key to openclaw.json env block |
| `Gemini model ... is unavailable.` | Model name incorrect or deprecated | Update `gemini_model` in config |
| `Gemini API error: 4xx` | Bad request or auth failure | Check API key and query |
| `Brave API error: 4xx` | Bad request or auth failure | Check API key |
| `Gemini returned an empty response.` | API responded but returned no text | Retry or check query |
| `Brave returned no results.` | API returned empty results array | Try a different query |
| `Finance and time-sensitive queries require Gemini or Brave API.` | Finance query hit the web_fetch fallback block | Ensure API quota is available for finance queries |
| `All search providers exhausted or unavailable.` | All tiers failed | Check API keys, quota, and network |
| `... circuit is open. Try again later.` | Provider hit 3 consecutive failures | Wait 60 seconds for circuit to reset |
| `Quota file is locked. Try again.` | Concurrent write contention | Retry the call |
| `Cannot read openclaw.json. Check OPENCLAW_CONFIG_PATH.` | Config file missing or unreadable | Check file path and permissions |
| `Invalid JSON input.` | stdin payload was not valid JSON | Ensure the harness sends valid JSON |
| `Unknown tool: ...` | Tool name not recognised | Use `smart_search`, `search_quota_status`, or `search_mark_agent_complete` |
| `Agent ... not found in quota.` | agent_id not in quota file | Call smart_search first to register the agent |
| `Agent ... is already marked complete for today.` | Double-complete call | No action needed; agent is already released |

---

## 13. EXAMPLES

### Example 1 — Manual chat finance query, Google web_fetch succeeds

```json
{ "tool": "smart_search", "args": { "query": "today AAPL stock price", "agent_id": "general" } }
```

Strategy B: Google web_fetch is tried first. Succeeds. Zero API quota consumed.

```json
{
  "results": "<html content from Google>",
  "provider_used": "web_fetch",
  "queries_remaining": 20,
  "quota_source": "none",
  "fallback_used": true,
  "warning": "Result retrieved via web scraping. Quality may be lower than API results.",
  "web_fetch_engine": "google"
}
```

---

### Example 2 — Manual chat finance query, both web_fetch fail, API fallback triggered

```json
{ "tool": "smart_search", "args": { "query": "today AAPL stock price", "agent_id": "general" } }
```

Strategy B: Google fails, Bing fails. Gemini API is called (finance keyword routes to Gemini). Quota consumed.

```json
{
  "results": "Apple (AAPL) is trading at $189.42...",
  "provider_used": "gemini",
  "queries_remaining": 19,
  "quota_source": "agent_allocation",
  "fallback_used": false,
  "warning": null,
  "web_fetch_engine": null
}
```

---

### Example 3 — Manual chat general query, Google web_fetch succeeds

```json
{ "tool": "smart_search", "args": { "query": "best noise-cancelling headphones 2025", "agent_id": "general" } }
```

Strategy B: No finance keywords. Google web_fetch tried first. Succeeds. Zero API quota consumed.

```json
{
  "results": "<html content from Google>",
  "provider_used": "web_fetch",
  "queries_remaining": 20,
  "quota_source": "none",
  "fallback_used": true,
  "warning": "Result retrieved via web scraping. Quality may be lower than API results.",
  "web_fetch_engine": "google"
}
```

---

### Example 4 — Scheduled agent finance query, Gemini API, agent has allocation

```json
{ "tool": "smart_search", "args": { "query": "NSE market open today", "agent_id": "stock-analysis" } }
```

Strategy A: Finance keyword routes to Gemini. Agent has 12 remaining. API call succeeds.

```json
{
  "results": "The NSE opened at 22,450 points today...",
  "provider_used": "gemini",
  "queries_remaining": 11,
  "quota_source": "agent_allocation",
  "fallback_used": false,
  "warning": null,
  "web_fetch_engine": null
}
```

---

### Example 5 — Scheduled agent, both APIs exhausted, finance query → hard error

```json
{ "tool": "smart_search", "args": { "query": "NSE market open today", "agent_id": "stock-analysis" } }
```

Strategy A: Gemini exhausted, Brave exhausted. Finance keyword blocks DuckDuckGo fallback.

```json
{
  "results": null,
  "provider_used": null,
  "queries_remaining": 0,
  "quota_source": "none",
  "fallback_used": false,
  "warning": null,
  "web_fetch_engine": null,
  "error": "Finance and time-sensitive queries require Gemini or Brave API. web_fetch fallback is not permitted for this query type."
}
```

---

### Example 6 — Scheduled agent, both APIs exhausted, general query → DuckDuckGo web_fetch

```json
{ "tool": "smart_search", "args": { "query": "latest AI research papers", "agent_id": "tech-news" } }
```

Strategy A: Gemini exhausted, Brave exhausted. No finance keywords — DuckDuckGo web_fetch is permitted.

```json
{
  "results": "<html content from DuckDuckGo>",
  "provider_used": "web_fetch",
  "queries_remaining": 0,
  "quota_source": "none",
  "fallback_used": true,
  "warning": "Result retrieved via web scraping. Quality may be lower than API results.",
  "web_fetch_engine": "duckduckgo"
}
```


