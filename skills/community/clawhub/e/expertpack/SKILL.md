---
name: expertpack
description: "Work with ExpertPacks — structured knowledge packs for AI agents. Obsidian-compatible: every pack is a valid Obsidian vault with Dataview support. Use when: (1) Loading/consuming an ExpertPack as agent context, (2) Creating or hydrating a new ExpertPack from scratch, (3) Configuring RAG for a pack, (4) Opening or authoring a pack in Obsidian. Triggers on: 'expertpack', 'expert pack', 'esoteric knowledge', 'knowledge pack', 'pack hydration', 'obsidian vault', 'obsidian pack'. For CLI tools (ep-validate, ep-doctor, ep-graph-export, ep-strip-frontmatter) install expertpack-cli. For EK ratio measurement and quality evals install expertpack-eval. For exporting an OpenClaw agent as an ExpertPack install expertpack-export. For converting an existing Obsidian Vault into an ExpertPack install obsidian-to-expertpack. For serving any ExpertPack as an MCP endpoint (expertise-as-a-service), see EP MCP at github.com/brianhearn/ep-mcp."
metadata:
  openclaw:
    homepage: https://expertpack.ai
---

# ExpertPack

Structured knowledge packs for AI agents. Maximize the knowledge your AI is missing.

**Learn more:** [expertpack.ai](https://expertpack.ai) · [GitHub](https://github.com/brianhearn/ExpertPack) · [Schema docs](https://expertpack.ai/#schemas) · [Obsidian compatible](https://expertpack.ai/#obsidian)

> **💎 Obsidian compatible:** Every ExpertPack is a valid Obsidian vault. Copy the `.obsidian/` folder from the ExpertPack repo `template/` directory into your pack root, open it in Obsidian, and install Dataview + Templater. You get live queries by content type, EK score, and tags; graph view; and full-text search. Standard relative Markdown links — packs render correctly on GitHub and in Obsidian simultaneously.

> **Companion skills:** This skill covers consumption and hydration guidance only. For CLI tooling (validate, doctor, graph export, frontmatter strip) use `expertpack-cli`. For EK measurement and quality evals use `expertpack-eval`. For exporting an OpenClaw agent's workspace as an ExpertPack use `expertpack-export`. For converting an existing Obsidian Vault into an agent-ready ExpertPack use `obsidian-to-expertpack`. For serving a pack as an MCP endpoint (expertise-as-a-service), see **[EP MCP](https://github.com/brianhearn/ep-mcp)** — a generic MCP server for any ExpertPack.

**Full schemas:** `/path/to/ExpertPack/schemas/` in the repo (core.md, person.md, product.md, process.md, composite.md, eval.md)

## Pack Location

Default directory: `~/expertpacks/`. Check there first, fall back to current workspace. Users can override by specifying a path.

## Actions

### 1. Load / Consume a Pack

1. Read `manifest.yaml` — identify type, version, context tiers
2. Read `overview.md` — understand what the pack covers
3. Load all Tier 1 (always) files into session context
4. For queries: search Tier 2 (searchable) files via RAG or `_index.md` navigation
5. Load Tier 3 (on-demand) only on explicit request (verbatim transcripts, training data)

To configure OpenClaw RAG, point `memorySearch.extraPaths` in `openclaw.json` at the pack directory. Files are authored at 400–800 tokens each — retrieval-ready by design.

For detailed platform integration (Cursor, Claude Code, custom APIs, direct context window): read `{skill_dir}/references/consumption.md`.

> **Volatile files:** If a pack uses `volatile/` files with a `source` URL, staleness is checked at session start and the agent alerts you. Refresh is always **user-initiated** — no automatic background network fetches occur.

### 2. Create / Hydrate a Pack

1. Determine pack type: person, product, process, or composite
2. Read `{skill_dir}/references/schemas.md` for structural requirements
3. Create root directory using the pack slug (kebab-case)
4. **Obsidian setup (optional):** Copy the `.obsidian/` folder from the `template/` directory in the public ExpertPack repo (github.com/brianhearn/ExpertPack) into the pack root — the user can do this manually to get Dataview + Templater pre-configured.
5. Create `manifest.yaml` and `overview.md` (both required)
6. Scaffold content directories per the type schema with `_index.md` in each
7. Populate content using EK-aware hydration:
   - Focus on esoteric knowledge — content the model cannot produce on its own
   - Full treatment for EK content; compressed scaffolding for general knowledge
   - Skip content with zero EK value
8. Add retrieval layers: `summaries/`, `propositions/`, `glossary.md`, lead summaries in content files
9. Add `sources/_coverage.md` documenting what was researched

For full hydration methodology and source prioritization: read `{skill_dir}/references/hydration.md`.

### 3. Configure RAG

Point OpenClaw RAG at the pack directory via `openclaw.json` (`memorySearch.extraPaths`). See `{skill_dir}/references/consumption.md` for the exact config. No external chunking tool needed — files are authored at 400–800 tokens by design.

### 4. Measure EK Ratio & Run Quality Evals

Install the companion skill `expertpack-eval` via clawhub — it handles all LLM API calls for blind probing and eval scoring.

### 5. Validate & Fix a Pack

Install the companion skill `expertpack-cli` via clawhub — it provides ep-validate, ep-doctor, ep-graph-export, and ep-strip-frontmatter with full command syntax and workflows.

### 6. Export an OpenClaw Agent as an ExpertPack

Install the companion skill `expertpack-export` via clawhub — it handles workspace scanning, distillation, and packaging.
