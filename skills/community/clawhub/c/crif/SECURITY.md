# Security & Permissions

## Overview

**CRIF (Crypto Research Interactive Framework)** is a prompt engineering framework for crypto market research with AI assistance. It is written entirely in Markdown — zero code, zero binaries.

---

## What is CRIF?

CRIF is **not a software application**. It is a collection of Markdown files that instruct AI assistants how to conduct structured crypto research.

```
references/
├── core/                # Orchestrator, config, state templates
├── agents/*.md          # AI persona definitions
├── workflows/*/         # Research methodologies
│   ├── workflow.md      # Workflow config + agent assignment
│   ├── objectives.md    # What to research
│   └── template.md      # How to format output
├── components/*.md      # Execution protocols
└── guides/*.md          # Methodology references
```

**How it works:**
1. User requests crypto research
2. AI reads Markdown files to understand persona and methodology
3. AI conducts research following structured instructions
4. AI generates formatted research outputs to local workspace

---

## Required Permissions

### 1. File System — READ

**Scope:**
```
references/core/*.md
references/agents/*.md
references/workflows/**/*.md
references/components/*.md
references/guides/*.md
```

**Purpose:** AI reads instruction files to understand how to conduct research. This is the core functionality.

### 2. File System — WRITE

**Scope:**
```
workspaces/{project-id}/.orchestrator
workspaces/{project-id}/outputs/**/*.md
workspaces/{project-id}/outputs/**/.scratch
```

**Purpose:** Save research outputs and manage session state. All writes are confined to the `workspaces/` directory.

### 3. Network — WebSearch / WebFetch

**Purpose:** Search for and fetch current crypto market data, news, documentation, and public blockchain data.

**Why needed:** Crypto research requires access to current market data and primary sources.

### 4. Network — MCP Servers (Optional)

**Scope:** Only if user explicitly configures MCP servers in `.mcp.json` or `~/.claude.json`.

**Purpose:** Real-time structured data from CoinGecko, CoinMarketCap, DeFiLlama, Dune, Exa.

**Important:**
- MCP servers are **optional** — CRIF works fully without them
- User **manually configures** each server and provides their own API keys
- CRIF framework files do **not** contain any API keys or credentials
- MCP config details are in `references/core/mcp-servers.md` for reference only — the actual config lives in the user's `.mcp.json`, outside the framework

---

## What CRIF Does NOT Do

- **No data exfiltration** — All outputs saved locally in `workspaces/`
- **No system modifications** — Does not modify system files or install processes
- **No remote control** — No C2 servers, no backdoors, all instructions from local files
- **No credential harvesting** — Does not collect API keys, passwords, or credentials
- **No obfuscation** — All files are plain text Markdown, fully readable

---

## Transparency

### All Instructions Are Readable

Every instruction in CRIF is plain text Markdown:

```
references/agents/market-analyst.md       ← AI persona definition
references/workflows/*/objectives.md      ← Research objectives
references/components/workflow-execution.md ← Execution protocol
references/guides/research-methodology.md  ← Research principles
```

Anyone can read every instruction, understand what AI will do, modify behavior, and verify no malicious content.

### Data Flow

```
User request
  ↓
AI reads LOCAL Markdown files
  ↓
AI conducts research (WebSearch/WebFetch/MCP — PUBLIC data)
  ↓
AI generates report
  ↓
Output saved to workspaces/ (LOCAL)
```

No step involves unauthorized data access, hidden network connections, or system modifications.

---

## Security Best Practices

### For Users

1. **Review framework files** — All instructions are readable Markdown
2. **Monitor workspaces/** — All outputs saved here; review and delete when done
3. **MCP API keys** — Store in `.mcp.json` (local config), never in framework files. Add `.mcp.json` to `.gitignore` if sharing your project
4. **Understand permissions** — File read/write for workspace management, network for research

### For Platform Reviewers

1. **This is a prompt engineering framework** — AI instructions are the framework's purpose, not prompt injection
2. **Network access is for research** — WebSearch/WebFetch/MCP used for public data gathering only
3. **File operations are legitimate** — Workspace management, similar to any productivity tool
4. **Verify by inspection** — All plain text Markdown, no binaries, no obfuscation

---

## File Manifest

```
crif/
├── SKILL.md                              # Entry point for AI
├── README.md                             # Documentation for humans
├── LICENSE.md                            # MIT License
├── SECURITY.md                           # This file
├── references/
│   ├── core/
│   │   ├── orchestrator.md               # Orchestration lifecycle
│   │   ├── core-config.md                # User settings, workflow registry, MCP registry
│   │   ├── orchestrator-state-template.md # Session state template
│   │   ├── scratch-template.md           # Per-workflow state template
│   │   └── mcp-servers.md               # MCP server installation reference
│   ├── agents/
│   │   ├── market-analyst.md             # Market intelligence persona
│   │   ├── project-analyst.md            # Project fundamentals persona
│   │   ├── technology-analyst.md         # Technical analysis persona
│   │   ├── content-creator.md            # Content creation persona
│   │   ├── qa-specialist.md              # Quality assurance persona
│   │   └── image-creator.md              # Image prompt persona
│   ├── workflows/                        # 19 research workflows
│   ├── components/                       # 7 execution protocols
│   └── guides/                           # 7 methodology references
└── workspaces/                           # User research outputs (runtime)
```

**Total code:** 0 lines (all natural language Markdown)
**Binary files:** 0
**Network endpoints:** None hardcoded. MCP servers optionally configured by user.
**Data storage:** All local. No cloud, no databases, no telemetry.

---

**Framework Version:** 0.1.1
**Created by:** [Kudo](https://x.com/kudodefi)
