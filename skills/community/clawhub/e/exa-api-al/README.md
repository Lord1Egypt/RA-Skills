# Exa Web Search Skill

This repository contains an **agent skill** for Exa (exa.ai) — neural web search,
content retrieval, similarity discovery, and citation-grounded answering.

It is **instructional knowledge**, not runnable software. It teaches an AI agent
WHEN and HOW to use Exa effectively: choosing operations, planning queries,
evaluating and citing sources, handling errors, and controlling cost.

---

## MCP server vs. skill — the key distinction

| | MCP server (`exa-mcp`) | This skill (`exa-web-search-skill`) |
|---|---|---|
| **What it is** | Executable infrastructure | Instructional knowledge (Markdown + one JSON manifest) |
| **What it provides** | Callable tools (`exa_search`, `exa_get_contents`, `exa_find_similar`, `exa_answer`) | Guidance on *when/how* to use those tools well |
| **Runs code?** | Yes — makes HTTP calls to `https://api.exa.ai`, holds the API key | No — it is documentation the agent reads |
| **Holds `EXA_API_KEY`?** | Yes | No (never) |
| **Analogy** | The hands | The playbook |

The two are complementary. The MCP server (or any HTTP client) makes Exa
*reachable*; this skill makes the agent *use it well*. The agent calls the
server's tools while following this skill's rules.

---

## Folder map

```
exa-skill/
├── SKILL.md          # Authoritative behavior: when/how to use Exa (read first)
├── README.md         # This file
├── CLAUDE.md         # Instructions for an agent maintaining this skill
├── skill.json        # Machine-readable manifest
├── reference/        # Concise API reference for the agent
│   ├── endpoints.md          # Each endpoint: purpose, params, response, cost
│   ├── parameters.md         # All parameters across endpoints
│   ├── response-fields.md    # Every response field and how to use it
│   ├── common-errors.md      # Error shapes, causes, correct reactions
│   ├── best-practices.md     # Distilled checklist
│   └── safety-and-security.md# Key safety, untrusted content, injection
├── examples/         # (optional) worked end-to-end agent workflows
├── recipes/          # (optional) reusable task patterns
├── prompts/          # (optional) prompt fragments the agent can reuse
└── tests/            # (optional) checks that docs stay consistent
```

`SKILL.md` is the entrypoint and the single source of truth. The `reference/`
files elaborate but must never contradict it. The `examples/`, `recipes/`,
`prompts/`, and `tests/` folders are optional homes for additional, consistently
formatted material.

---

## How an agent / host loads this skill

1. The host reads `skill.json` to discover the skill (name, version,
   `entrypoint: SKILL.md`, required env vars, operations, expected tools).
2. The host ensures `EXA_API_KEY` is available to the tool layer (the MCP server
   or HTTP client) — **not** to the skill text.
3. The agent reads `SKILL.md` (and `reference/` as needed) and follows its rules
   while invoking the Exa tools.
4. When the agent must call Exa, it uses the expected tools — typically
   `exa_search`, `exa_get_contents`, `exa_find_similar`, `exa_answer`.

---

## How it pairs with the exa-mcp server

- Install/configure the `exa-mcp` server so the agent has the Exa tools.
- Provide `EXA_API_KEY` to that server's environment.
- Load this skill so the agent knows how to drive those tools responsibly.
- The skill references tool names matching the server's tools; if your server
  names them differently, update `expected_tools` in `skill.json` and the tool
  references in `SKILL.md` §6.

If no MCP server is present, the same guidance applies to direct HTTP calls
against `https://api.exa.ai` with the `x-api-key` header.

---

## Keeping it updated

- Update `SKILL.md` first when Exa changes; then sync the `reference/` files.
- Bump `version` in `skill.json` on meaningful changes.
- Verify uncertain claims against https://docs.exa.ai and remove the
  `> Verification needed:` markers once confirmed.
- Re-check the `research` (beta) endpoint before relying on it.
- See `CLAUDE.md` for detailed maintenance rules.
