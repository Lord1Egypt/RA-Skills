# Brand Intelligence Plugin for OpenClaw

Search, compare, and analyze 5,600+ companies across 30 verticals. AI visibility scores, knowledge graph, competitive intelligence — all from [geo.sig.ai](https://geo.sig.ai).

## Install

```bash
openclaw plugins install openclaw-brand-intelligence
```

## Configure

Add to your `openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "sigai-brand-intelligence": {
        "enabled": true,
        "config": {
          "baseUrl": "https://geo.sig.ai",
          "apiKey": "YOUR_KEY_OR_OMIT_FOR_PUBLIC"
        }
      }
    }
  }
}
```

## Tools

All tools are read-only and available to agents by default (no `tools.allow` config needed).

| Tool | Description |
|---|---|
| `sigai_search_brands` | Search brands by name, vertical, keyword |
| `sigai_get_brand` | Full brand profile |
| `sigai_get_brand_brief` | Concise citation-ready summary |
| `sigai_get_brand_graph` | Knowledge graph: edges, capabilities, parent/children |
| `sigai_get_brand_digest` | Compact digest for multiple brands |
| `sigai_compare_brands` | Structured comparison with bottom-line summary |
| `sigai_find_alternatives` | Graph-powered alternatives with reasons |
| `sigai_get_landscape` | Vertical landscape: leaders, challengers, emerging |
| `sigai_find_by_capability` | Find brands by capability |

## Example Prompts

- "What is Cursor and how visible is it in AI search?"
- "Compare Salesforce and HubSpot"
- "Find alternatives to Datadog"
- "What are the top cybersecurity companies?"
- "Give me a weekly update on Stripe, Plaid, and Adyen"

## Links

- [geo.sig.ai](https://geo.sig.ai) — Brand intelligence platform
- [Methodology](https://geo.sig.ai/methodology) — How the knowledge graph works
- [API Docs](https://geo.sig.ai/api/public/openapi.json) — OpenAPI spec
