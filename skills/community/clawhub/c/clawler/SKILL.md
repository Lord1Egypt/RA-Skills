---
name: clawler
description: "Use when you want current web information through the Clawler OpenClaw plugin."
read_when:
  - You are asked to look something up online
  - You need to reason about which search provider to use
  - You need to explain Clawler configuration or setup
metadata:
  openclaw:
    homepage: https://github.com/maxpetretta/clawler
    requires:
      bins:
        - openclaw
---

# Clawler Skill

Clawler is an optional web-search surface for this project. Use it when the plugin is installed and the operator wants Clawler to handle web search.

## Setup

If Clawler is available in the current OpenClaw environment:

1. Run the setup flow if the plugin CLI is available:
   - `openclaw clawler setup`
2. Choose one default provider and configure credentials for that provider.
4. Verify availability:
   - `openclaw clawler status`

Optional:
- If you want Clawler to replace the built-in `web_search` tool for that OpenClaw installation, add `web_search` to `tools.deny`.
- This changes installation-wide search behavior and should only be done deliberately.

If the setup CLI is not available, make sure OpenClaw is configured so:

- the Clawler plugin is installed and enabled
- one provider is selected
- that provider API key is available through plugin config or environment variables
- `tools.deny` includes `web_search` only when you intentionally want to disable the built-in search tool for that OpenClaw installation

## Credentials

Clawler supports multiple providers. No single provider credential is universally required for this skill; configure one provider in plugin config or provide one of these env vars for the provider you choose:

- `BRAVE_API_KEY`
- `EXA_API_KEY`
- `TAVILY_API_KEY`
- `PERPLEXITY_API_KEY`
- `OPENROUTER_API_KEY`
- `PARALLEL_API_KEY`
- `GEMINI_API_KEY`
- `GOOGLE_AI_API_KEY`
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`

Provider-specific settings can also be stored in the Clawler plugin config inside the OpenClaw config file instead of environment variables. Because the operator chooses the provider, these env vars are optional alternatives rather than universally required metadata for the skill.

## Tool

The default tool name is `search_web`.

Use it with:

```json
{
  "query": "latest OpenAI web search docs",
  "provider": "openai",
  "count": 5,
  "freshness": "pm",
  "country": "us",
  "search_lang": "en",
  "topic": "general",
  "include_domains": ["developers.openai.com"],
  "exclude_domains": ["example.com"]
}
```

Supported parameters:

- `query`: required search string
- `provider`: optional per-call provider override such as `exa`, `openai`, `brave`, or `anthropic`
- `count`: max number of results to request
- `freshness`: relative or explicit date filter such as `pd`, `pw`, `pm`, `py`, or `YYYY-MM-DDtoYYYY-MM-DD`
- `country`: country hint such as `us`
- `search_lang`: language hint such as `en`
- `topic`: provider-level topical hint such as `general`, `news`, or `finance`
- `include_domains`: allow-list domains
- `exclude_domains`: deny-list domains

## Usage Rules

1. Treat `search_web` as the preferred search tool only when Clawler has been intentionally configured as the active search surface.
2. Use provider-neutral instructions unless the user explicitly wants a provider comparison or a specific backend.
3. Use the per-call `provider` override when the query clearly benefits from a specific backend.
4. For technical or doc-heavy queries, use domain allow-lists when official sources matter.
5. If the query needs a synthesized answer with citations, prefer answer-native providers such as OpenAI, Anthropic, Gemini, Tavily, or Perplexity.
6. If the query mainly needs fast retrieval of links, traditional search providers such as Exa, Brave, or Parallel can be enough.
7. Treat changes to `tools.deny` as an optional installation-wide behavior change, not a routine default. Only recommend it when the operator explicitly wants Clawler to replace the built-in search surface.

## Provider Notes

- `auto` picks the first available configured provider.
- API keys can come from plugin config or environment variables.
- Shared filters are applied at the plugin level and translated per provider when native support exists.
- Some providers enforce domain filters natively; others treat them as best-effort guidance.
