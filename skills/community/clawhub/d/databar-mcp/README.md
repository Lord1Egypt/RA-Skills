# Databar MCP Skill

A [Hermes Agent](https://hermes-agent.nousresearch.com/) skill for driving [Databar](https://databar.ai/) through its official MCP server — lead enrichment, waterfalls, scraping, company intelligence, and table pipelines, with cost discipline built in.

Databar connects 160+ data providers (email finders, verifiers, Google Maps, job postings, tech-stack lookups, LinkedIn data, SERP, YouTube) behind one API. This skill teaches an agent the correct workflow: **discover → price → run → poll → persist → export**, so it never spends credits blind.

## What's inside

```
SKILL.md                            # Workflow, tool map, cost discipline, pitfalls
references/
  recipes.md                        # Sales/lead-gen core: lead lists, Maps,
                                    # hiring signals, tech stacks, scheduled sources
  recipes-marketing-social.md       # SEO/PPC teardown, ad intel, social listening,
                                    # review mining, price watch, news/PR monitoring
  recipes-people-research.md        # Decision-makers, warm intros, job search,
                                    # company dossiers, research sourcing
  recipes-finance-app.md            # Funding rounds, public-company teardowns,
                                    # app revenue estimates, domain/traffic intel
```

## Requirements

- A [Databar](https://databar.ai/registration) account with credits (free tier available)
- The Databar MCP server connected to your agent. Hosted endpoint (recommended): `https://mcp.databar.ai/mcp` — API key from your Databar workspace → Integrations, sent as `Authorization: Bearer <key>`. Full setup: [docs.databar.ai/mcp-server](https://docs.databar.ai/mcp-server)

### Hermes Agent

```bash
hermes mcp add databar --url https://mcp.databar.ai/mcp --auth header
# paste your API key when prompted, then (from ClawHub):
hermes skills install clawhub/dennisrongo/databar-mcp
# or straight from this repo:
hermes skills install https://raw.githubusercontent.com/dennisrongo/databar-skill/main/SKILL.md
```

The skill directory (with `references/recipes.md`) installs in one step either way. Also listed on [ClawHub](https://clawhub.ai/dennisrongo/databar-mcp) — OpenClaw users: `openclaw skills install @dennisrongo/databar-mcp`. If you'd rather pin a copy: clone the repo into your skills tree.

### Claude / Cursor / other MCP clients

This is a standard SKILL.md-format skill. Point your client's skill loader at this repo, or copy `SKILL.md` + `references/` into your skills directory. The MCP server config for Claude/Cursor is in the [Databar MCP docs](https://docs.databar.ai/mcp-server).

## What the skill does

- **Discovery first**: `search_enrichments` → `get_enrichment_details` → exact params and `price_credits` before any spend
- **Waterfalls**: multi-provider email/person lookups that stop at first hit, optional built-in verification
- **Tables as pipelines**: attach enrichments as result columns, `run_empty` strategy to skip already-filled rows, scheduled sources, CRM exporters
- **Cost discipline**: balance check before/after, price-the-chain rule, no blind bulk runs
- **Verified pitfalls**: async task polling, position-aligned bulk joins, permanent deletions, BYOK auth modes, cache vs fresh pricing

## Example prompts

- "Check my Databar balance and find me the cheapest email finder for this list of 50 domains"
- "Build a table of Sacramento dentists from Google Maps, then find verified emails for the owners"
- "Which companies hiring data entry clerks also run Zapier? Give me contacts"
- "What keywords did [competitor] lose rankings for last month, and what are they buying on PPC?"
- "Pull the last 100 tweets from these 5 AI influencers and cluster what gets engagement"
- "One-page dossier on [company] before my meeting: stack, news, LinkedIn activity, social stats"
- "Which companies near me are hiring DevOps engineers? Find the hiring manager's verified email"
- "How many credits would it cost to enrich these 200 domains with company data?"

## Disclaimer

Enrichment IDs and prices in `references/recipes.md` were verified August 2026 and will drift — the skill itself re-verifies via `search_enrichments` on every use, which is the point. Data-provider terms and privacy laws (CAN-SPAM, GDPR) apply to how you use contact data; that's on you.

## License

MIT
