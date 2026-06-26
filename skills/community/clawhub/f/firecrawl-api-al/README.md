# Firecrawl Web Scraping Skill

This folder is an **agent skill**: instructional knowledge that teaches an AI agent how to use [Firecrawl](https://firecrawl.dev) (web scraping, crawling, mapping, and search) well — when to use it, how to drive each operation, how to cite sources, control cost, handle errors, and stay safe.

## Skill vs. MCP server (important distinction)

- An **MCP server** (e.g. `firecrawl-mcp`) is **executable infrastructure**. It exposes callable tools such as `firecrawl_scrape`, `firecrawl_crawl`, `firecrawl_map`, `firecrawl_search` that an agent invokes at runtime. It performs actions.
- **This skill is instructional knowledge.** It runs nothing. It is Markdown (plus one JSON manifest) that tells the agent WHEN to reach for Firecrawl and HOW to use it correctly — format choice, async crawl polling, citation, cost control, error handling, security.

The two are complementary: the MCP server provides the tools; this skill provides the judgment for using them. The skill assumes Firecrawl is reachable either through the `firecrawl-mcp` tools or through a direct HTTP client to `https://api.firecrawl.dev/v2` with `Authorization: Bearer <FIRECRAWL_API_KEY>`.

## Folder map

```
firecrawl-skill/
├── SKILL.md          # PRIMARY: the authoritative instructions (start here)
├── README.md         # This file
├── CLAUDE.md         # Instructions for an AI agent maintaining this skill
├── skill.json        # Machine-readable manifest
├── examples/         # Worked, end-to-end usage examples (optional)
├── recipes/          # Reusable task patterns (optional)
├── prompts/          # Reusable prompt snippets for agents (optional)
├── reference/        # Endpoint/parameter/response/error references
│   ├── endpoints.md
│   ├── parameters.md
│   ├── response-fields.md
│   ├── common-errors.md
│   ├── best-practices.md
│   └── safety-and-security.md
└── tests/            # Checks/fixtures validating the skill docs (optional)
```

`SKILL.md` is the entrypoint and the source of truth. Everything in `reference/` elaborates on it and must stay consistent with it.

## How an agent / host loads this skill

1. The host reads `skill.json` to discover the skill's name, description, required environment variables (`FIRECRAWL_API_KEY`), operations, tags, safety rules, and entrypoint.
2. The host loads `SKILL.md` (the `entrypoint`) into the agent's instructional context.
3. The agent consults `reference/` files as needed for endpoint, parameter, response, and error detail.
4. At runtime the agent calls the Firecrawl tools (via `firecrawl-mcp`) or HTTP, applying the judgment from this skill.

## How it pairs with firecrawl-mcp

- Install/configure `firecrawl-mcp` so the agent has the callable tools and set `FIRECRAWL_API_KEY` in that server's environment.
- Load this skill so the agent knows how to use those tools well.
- The skill's `expected_tools` (`firecrawl_scrape`, `firecrawl_search`, `firecrawl_map`, `firecrawl_crawl`) map to the MCP server's tools. If the tool names differ in your host, the workflows still apply — only the call surface changes.

## Keeping it updated

- Treat `SKILL.md` as authoritative; update it first, then reconcile `reference/`.
- When Firecrawl changes (new params, new formats, cost changes), update the affected reference file and re-check `SKILL.md`.
- Mark anything you have not verified with `> Verification needed: ...` and a link to https://docs.firecrawl.dev.
- See `CLAUDE.md` for the rules an AI maintainer must follow (no hallucinated behavior, cite official docs, keep ground-truth facts intact).
