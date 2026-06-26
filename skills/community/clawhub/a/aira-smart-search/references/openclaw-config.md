# openclaw.json Configuration Reference

Full configuration block for smart-search. Add this under `skills` in your `~/.openclaw/openclaw.json`.

```json
{
  "env": {
    "GEMINI_API_KEY": "your-gemini-api-key-here",
    "BRAVE_API_KEY":  "your-brave-api-key-here"
  },
  "skills": {
    "smart-search": {
      "gemini_model": "gemini-2.0-flash",
      "default_provider": "brave",
      "strict_agents": false,
      "retry_max_attempts": 3,
      "retry_base_delay": 500,
      "finance_keywords": [
        "stock", "share price", "nse", "bse", "wse", "nyse", "nasdaq",
        "earnings", "ipo", "dividend", "funding round", "acquisition",
        "merger", "valuation", "competitor", "market share",
        "breaking", "just announced", "today", "hours ago"
      ],
      "brave_keywords": ["space", "astronomy", "nasa", "esa", "cosmos"],
      "providers": {
        "gemini": { "daily_limit": 1500 },
        "brave":  { "daily_limit": 66 }
      },
      "agent_allocations": {
        "general":        { "gemini": 20, "brave": 5  },
        "stock-analysis": { "gemini": 15, "brave": 0  },
        "tech-news":      { "gemini": 10, "brave": 10 },
        "research":       { "gemini": 20, "brave": 0  }
      }
    }
  }
}
```

## Key Notes

- **API keys** live in the top-level `env` block, not inside the skill config.
- **`strict_agents: true`** will reject any `agent_id` not listed in `agent_allocations`. Set to `false` during development.
- **`default_provider`** is used when no finance or brave keywords match the query. Defaults to `brave`.
- **`daily_limit`** is the total API budget per provider per day across all agents.
- **`agent_allocations`** carves that budget into per-agent slices. Unused quota is released to the shared pool when you call `search_mark_agent_complete`.
- Changes to `openclaw.json` take effect on the **next call** — no restart needed.

## Environment Variable Overrides

| Variable | Default | Effect |
|---|---|---|
| `SEARCH_QUOTA_PATH` | `~/.openclaw/workspace/shared/search-quota.json` | Override quota file location |
| `OPENCLAW_CONFIG_PATH` | `~/.openclaw/openclaw.json` | Override config file location |
