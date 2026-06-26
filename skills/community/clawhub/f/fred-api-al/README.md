# FRED Skill

This folder is the **agent skill** for FRED (Federal Reserve Economic Data). It is the *knowledge* an AI agent needs to use the FRED MCP server correctly — when to use it, how to pick series and units, how to cite, and how to handle errors.

---

## What this skill is

A set of Markdown instructions and references the agent loads into context. It does **not** make API calls itself. It teaches the agent to use the tools provided by the **`fred-mcp` server** (in `../mcp/`).

The central file is **[SKILL.md](SKILL.md)** — the operating manual. Everything else supports it.

---

## MCP vs. Skill

| | **MCP server** (`../mcp/`) | **This skill** |
|---|---|---|
| Nature | Runnable program (Node/TypeScript) | Documentation + procedures |
| Provides | The 6 callable tools over stdio | Know-how to use them well |
| Calls FRED? | Yes | No |
| Loaded where | MCP client config | Agent context |

Pair them: the **server** lets the agent act; the **skill** makes it act correctly (right series, right units, always cited, never inventing values).

---

## Folder map

```
skill/
├── SKILL.md                          # FEATURED — the operating manual (read first)
├── README.md                         # this file
├── reference/
│   ├── endpoints.md                  # the 6 tools + generic pattern
│   ├── series-and-units.md           # popular series IDs + units/frequency enums
│   ├── response-fields.md            # observation/series fields, "." = missing, vintages, citing
│   ├── common-errors.md              # 400 / 429 / empty — cause + reaction
│   └── best-practices.md             # discovery, units, citation, caching, freshness, integrity, security
├── recipes/
│   ├── fetch-indicator.md            # get a single indicator's latest value
│   ├── year-over-year-change.md      # YoY % change (pc1)
│   └── compare-series.md             # compare two series over time
├── prompts/
│   ├── series-discovery.md           # reusable prompt to find the right series_id
│   └── citation-generation.md        # reusable prompt to produce a correct citation
└── tests/
    ├── skill-evaluation.md           # eval checklist + scenarios
    └── failure-cases.md              # bad behaviors + corrected versions
```

---

## Pairing with fred-mcp

1. Install and configure the **`fred-mcp`** server (see `../mcp/README.md` and `../mcp/docs/01-installation.md`).
2. Make this skill available to the agent.
3. The agent reads `SKILL.md`, then uses the server's tools following these procedures.

---

## Updating

- When FRED changes endpoints/params, update `reference/endpoints.md` and `reference/series-and-units.md`, then the recipes.
- Keep citation rules in `SKILL.md` (Section 10) and `prompts/citation-generation.md` consistent.
- Re-run the checks in `tests/skill-evaluation.md` after any change.

> Verification needed: cross-check against <https://fred.stlouisfed.org/docs/api/fred/>.
