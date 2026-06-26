# Financial Modeling Prep (FMP) Skill — README

## What this is

This folder is an **agent skill** for Financial Modeling Prep (FMP). It is **instructional knowledge** — Markdown that teaches an AI agent *how to use FMP well*: how to resolve symbols, pull financial data, keep numbers honest, cite sources, handle errors and rate limits, protect the API key, and stay compliant (not investment advice).

It is **not executable code** and not the API client itself. It is the "operating manual" the agent reads before and while it works with FMP.

## Skill vs MCP server (important distinction)

- The **`financialmodelingprep-mcp` server** is the *tooling* — it exposes callable tools (e.g. `fmp_search`, `fmp_quote`, `fmp_company_profile`, `fmp_income_statement`, `fmp_key_metrics`, `fmp_historical_prices`) that actually hit the FMP API over HTTP. It *does* things.
- This **skill** is the *knowledge* — it tells the agent *when* and *how* to call those tools, *what the responses mean*, and *what rules to never break*. It *guides* behavior.

They pair together: the MCP server provides the hands, this skill provides the judgment. The skill also works when the agent calls FMP via plain HTTP GET instead of the MCP server.

## Folder map

```
skill/
├── SKILL.md                      # MAIN file — the full operating guide (start here)
├── README.md                     # this file
├── reference/
│   ├── endpoints.md              # each key endpoint: purpose, path, params, response, cost
│   ├── parameters.md             # query params: meaning, defaults, when to change
│   ├── response-fields.md        # common response fields and how to cite/use them
│   ├── common-errors.md          # error shapes + the agent's correct reaction
│   └── best-practices.md         # distilled checklist
├── recipes/
│   ├── company-snapshot.md       # quote + profile + key-metrics → snapshot
│   ├── fundamentals-analysis.md  # multi-year statements + ratios → cited analysis
│   ├── valuation-check.md        # DCF vs price, with caveats + disclaimer
│   └── earnings-watch.md         # earnings-calendar monitoring for a watchlist
├── prompts/
│   ├── symbol-resolution.md      # resolve a company name to the right ticker
│   ├── financial-summary.md      # grounded, cited summary from returned data only
│   └── numeric-integrity-check.md# verify every cited number against API output
└── tests/
    ├── skill-evaluation.md       # scenarios + rubric + pass criteria
    ├── expected-behaviors.md     # GOOD behaviors with examples
    └── failure-cases.md          # BAD behaviors with bad-vs-corrected output
```

## How an agent / host loads this skill

1. The host (e.g. an agent framework or Claude-style harness) discovers the skill folder.
2. It loads **`SKILL.md`** as the primary instruction set into the agent's working context.
3. `reference/`, `recipes/`, and `prompts/` are loaded on demand when the agent needs deeper detail or a reusable template.
4. `tests/` is used to evaluate the agent's adherence, not loaded as runtime guidance.

Treat `SKILL.md` as authoritative; the other files expand on it.

## How it pairs with the financialmodelingprep-mcp server

- Ensure `FMP_API_KEY` is set in the environment the MCP server runs in (the skill never hardcodes it).
- The agent reads this skill, then calls the MCP tools to fetch data.
- Map the skill's operations to tools: search → `fmp_search`; quote → `fmp_quote`; profile → `fmp_company_profile`; statements → `fmp_income_statement` (+ balance/cash flow); metrics → `fmp_key_metrics`; history → `fmp_historical_prices`. Endpoints lacking a named tool can be reached via HTTP GET on `https://financialmodelingprep.com/stable/`.
- The skill's rules (numeric integrity, citation, error handling, compliance) apply regardless of whether tools or raw HTTP are used.

## How to keep it updated

- Re-verify endpoints, params, and free-tier limits against https://site.financialmodelingprep.com/developer/docs.
- Keep MCP tool names in sync with the server's actual tool list.
- Resolve any "Verification needed" markers as the docs are confirmed.
- Update `tests/` when behavior expectations change.
