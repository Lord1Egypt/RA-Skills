---
name: create-opc-wiki
description: Scaffold a personal LLM wiki (Karpathy pattern) — multi-agent, MCP-ready, with SEO/GEO publish target. Compiles knowledge into a persistent wiki instead of re-deriving from raw docs on every query. One paste from any agent (OpenClaw, Claude Code, Codex, Cursor, Hermes) installs it.
---

# create-opc-wiki

Scaffold a personal LLM wiki on the [Karpathy pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) in 30 seconds. Multi-agent native, MCP server built-in, SEO/GEO-optimized publish target.

## What this skill does

Run the scaffolder against any folder and you get a complete personal-knowledge-base vault:

- `agent-rules/main.md` — single source of truth, synced to **9 agent file formats** (CLAUDE.md, AGENTS.md, .cursor/rules/main.mdc, .cursorrules, .github/copilot-instructions.md, .trae/rules.md, **.openclaw/rules.md**, .hermes/agent.md)
- Three reusable skills: `/wiki-ingest`, `/wiki-query`, `/wiki-lint`
- Five source recipes: arXiv paper, X thread, YouTube transcript, RSS article, podcast transcript
- Privacy-tagged frontmatter: `public | private | secret`
- An MCP server with three tools (`wiki_query`, `wiki_list`, `wiki_read`) and a hard privacy gate (`privacy: secret` pages **never** leave the box)
- Optional Astro static site target with sitemap.xml, llms.txt, robots.txt, RSS feed, OpenGraph + JSON-LD per page

## How to invoke

The skill wraps the published npm package `create-opc-wiki@latest`. From any agent that can run a shell command:

```bash
npx -y create-opc-wiki@latest <path> --yes --agents=openclaw,claude,codex,cursor
```

Common one-liners:

| Agent | Command |
|---|---|
| OpenClaw | `npx -y create-opc-wiki@latest ~/wiki --yes --agents=openclaw,claude` |
| Claude Code | `npx -y create-opc-wiki@latest ~/wiki --yes --agents=claude` |
| Codex CLI | `npx -y create-opc-wiki@latest ~/wiki --yes --agents=codex` |
| Cursor | `npx -y create-opc-wiki@latest ~/wiki --yes --agents=cursor` |
| All of them | `npx -y create-opc-wiki@latest ~/wiki --yes --agents=openclaw,claude,codex,cursor,hermes,vscode,trae` |

Add `--no-mcp`, `--no-site`, `--no-recipes`, or `--no-git` to skip those layers. `--json` emits machine-readable result on stdout.

## How to use the generated vault

1. **Open the folder in Obsidian** (it's a valid Obsidian vault) — and/or
2. **Open the folder in your AI agent** (it reads `CLAUDE.md` / `AGENTS.md` / `.openclaw/rules.md` / etc.)
3. From inside the agent, use the three skills:
   - `/wiki-ingest <url-or-file>` — drop a new source, agent files it into `raw/` and synthesizes wiki pages
   - `/wiki-query <question>` — natural-language query across compiled wiki
   - `/wiki-lint` — health-check (contradictions, stale `speculative` claims, orphan pages)

The MCP server in `mcp/server.mjs` exposes the wiki to any MCP client (Claude Desktop, Cursor, Codex). Run `npm install && npm start` from the `mcp/` directory.

## Why a wiki and not just RAG

Most LLM-on-files setups re-derive answers from raw docs at every query. There's no accumulation. Quoting [Karpathy's gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):

> The LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources. The wiki keeps getting richer with every source you add and every question you ask.

This skill operationalizes exactly that, with concrete choices for ontology, agent rules, MCP, and publishing.

## Privacy & security

- `privacy: secret` pages **never** returned by the MCP server (enforced at `mcp/server.mjs:38`)
- `privacy: public` is the **only** level that publishes (enforced at `site/build.mjs:53`)
- Default frontmatter privacy is `private` — nothing publishes by accident
- The scaffolder runs once, locally, and exits — no telemetry, no network calls during scaffolding except the optional `npm` install you trigger yourself

## Links

- **npm**: <https://www.npmjs.com/package/create-opc-wiki>
- **GitHub**: <https://github.com/MackDing/create-opc-wiki>
- **Inspiration**: <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>
- **Stability scope**: see `STABILITY.md` in the repo for the semver-stable surface
- **Per-agent install recipes**: see `docs/INSTALL-FOR-AGENTS.md` in the repo

## License

MIT. Inspired by Andrej Karpathy's "LLM Wiki" gist; implementation choices are this project's. Full attribution in `INSPIRATION.md`.
