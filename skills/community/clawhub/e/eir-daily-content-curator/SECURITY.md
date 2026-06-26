# Security & Privacy

## Modes

|  | Standalone | Eir |
|---|---|---|
| Search API calls | ✅ Brave, Tavily, etc. | ✅ Same |
| Crawl (fetch URLs) | ✅ | ✅ |
| Eir API calls | ❌ None | ✅ Opt-in |
| Personalization | ❌ Off (default) | Optional opt-in |
| Personal data leaves machine | ❌ Never | Only generated content (see below) |

## Standalone Mode — What is sent

- **Search queries** to your configured search API (e.g. Brave, Tavily)
- **HTTP requests** to crawl source URLs for content
- **Nothing else.** No other external communication.

## Eir Mode — What is sent

| Data | Sent to Eir API | Notes |
|------|:---:|-------|
| Generated content (dot, l1, l2) | ✅ | LLM-generated summaries |
| l2.context, eir_take | Optional | Only included if user enables these fields |
| Interest categories | ✅ | Topic slugs only (e.g. "ai-agents") |
| Source URLs + metadata | ✅ | For attribution |
| **User profile data** | **❌ Never** | Agent may use local context for generation, but raw profile data is not transmitted |
| **Raw conversation text** | **❌ Never** | Not accessed by pipeline |
| **System credentials** | **❌ Never** | |
| **File paths / machine identifiers** | **❌ Never** | |

### Personalization

> ⚠️ **Personalization is OFF by default and requires explicit opt-in.**

The user can optionally provide audience context to the agent for more relevant content. This context is used locally during LLM generation only. Generated fields like `l2.context` and `eir_take` are optional — users can disable them in their settings.

**To keep all content generic:** leave personalization disabled (the default) and omit `l2.context`/`eir_take` from generated content.

### Interest Extraction

This skill includes a reference prompt (`references/interest-extraction-prompt.md`) that helps your agent learn your interests from conversation. It extracts only **de-identified topic labels and keywords** (e.g. "AI Agents", "autonomous vehicles") and saves them locally to `config/interests.json`. No personal identifiers are stored or transmitted.

If you already have an interest or topic configuration, you can use that instead.

## Credential Storage

All credentials are stored locally in config files (gitignored). No secrets are hardcoded.

| File | Contains | Committed |
|------|----------|-----------|
| `config/eir.json` | Eir API key, user ID | ❌ gitignored |
| `config/settings.json` | Search API key, mode, preferences | ❌ gitignored |
| `config/interests.json` | Topic labels and keywords | ✅ no secrets |

### Environment Variables (optional overrides)

| Variable | Purpose | Required? |
|----------|---------|----------|
| `EIR_API_KEY` | Eir API bearer token | No — defaults to `config/eir.json` |
| `EIR_API_URL` | Eir API base URL | No — defaults to `https://api.heyeir.com` |
| `SEARCH_API_KEY` | Search provider API key | No — defaults to `config/settings.json` |
| `EIR_WORKSPACE` | Override workspace directory | No — auto-detected |

These are convenience overrides only. The standard setup stores credentials in `config/eir.json` (created by `python3 scripts/connect.py`).

## File Access

Pipeline scripts read/write only within the skill's `data/` and `config/` directories.

## Reporting Vulnerabilities

Open an issue at [github.com/heyeir/openeir](https://github.com/heyeir/openeir/issues) or email security concerns directly.
