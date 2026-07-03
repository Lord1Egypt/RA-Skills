<p align="center">
  <h1 align="center">⚙️ Agent Harness Engineer Skill</h1>
  <p align="center">
    <strong>Production-grade AI Agent Construction Blueprint</strong>
    <br />
    A <a href="https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills">Skill</a> that guides AI coding tools to build enterprise-ready Agent systems — not just demos.
  </p>
</p>

<p align="center">
  <a href="https://github.com/nicepkg/agent-harness-engineer/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="License" /></a>
  <a href="https://github.com/nicepkg/agent-harness-engineer/stargazers"><img src="https://img.shields.io/github/stars/nicepkg/agent-harness-engineer?style=flat&color=yellow" alt="Stars" /></a>
  <a href="README_ZH.md"><img src="https://img.shields.io/badge/中文文档-简体中文-red.svg" alt="Chinese Doc" /></a>
</p>

---

## Why Agent Harness Engineer?

Most "Build an Agent" tutorials give you a 50-line Python script that calls an LLM in a loop. That's a demo, not a production system.

**Agent Harness Engineer** is different. It's a comprehensive **7-phase construction blueprint** that AI coding tools follow to generate structurally complete, secure, extensible Agent systems — complete with permission models, context compression pipelines, multi-agent coordination, sandbox isolation, and production monitoring.

> *"Information that the Agent cannot access in its context does not exist."* — Harness Engineering Principle

---

## Quick Start

This is a **Skill** consumed by AI coding assistants (Claude Code, etc.). Simply include it in your project and ask your AI coding tool:

```
"Build me an Agent"
```

The AI will automatically load this Skill and guide you through a structured 7-phase build process — from scaffolding to production deployment.

### One-Click Setup

```bash
git clone https://github.com/nicepkg/agent-harness-engineer.git
# Place the SKILL.md in your project's skills directory
```

When triggered, the Skill will:
1. Confirm your requirements (tech stack, LLM provider, scale, use case)
2. Execute each phase sequentially with checklist verification
3. Generate a complete, production-ready Agent project from battle-tested templates

---

## Core Framework: Harness Engineering

<p align="center">
  <b>Three Pillars of Production Agent Systems</b>
</p>

| Pillar | Principle | Implementation |
|--------|-----------|----------------|
| **Context Engineering** | Information accessibility is everything | 4-level compression pipeline, lazy-loaded tools, on-demand memory |
| **Architectural Constraints** | Mechanical enforcement beats suggestions | 5 permission modes × 7 rule hierarchies, schema validation, sandbox isolation |
| **Entropy Management** | Code degrades without regular maintenance | Documentation audits, constraint violation scanning, coverage gates |

---

## 7-Phase Construction Blueprint

```
Phase 1  ●──○ Project Init       ▸ Scaffolding, config, directory structure
Phase 2  ●──○ LLM Abstraction    ▸ Provider-agnostic client (Anthropic, OpenAI, Azure, Local)
Phase 3  ●──○ Tool System        ▸ Registry, schema validation, concurrency safety
Phase 4  ●──○ Agent Core Loop    ▸ 7 continue-sites, immutable state, error recovery
Phase 5  ●──○ Context Management ▸ 4-level compression, memory system, auto-dreaming
Phase 6  ●──○ Permissions        ▸ 6-layer defense-in-depth, sandbox, audit logging
Phase 7  ●──○ Production         ▸ Testing, monitoring, logging, deployment docs
```

Each phase includes: **Theory → Practice Steps → Checklist → Common Pitfalls**

---

## Architecture in 30 Seconds

```
┌─────────────────────────────────────────────────────────┐
│                      HARNESS                            │
│                (Stateless Orchestrator)                  │
│                                                         │
│   while (running) {                                     │
│     step = yield from Session.next()                    │
│     result = Sandbox.execute(step)                      │
│     Session.commit(result)                              │
│   }                                                     │
└──────────┬──────────────────────────┬───────────────────┘
           │                          │
    ┌──────▼──────┐           ┌──────▼──────┐
    │   SESSION   │           │   SANDBOX   │
    │ Append-only │           │  Isolated   │
    │  Event Log  │           │  Execution  │
    │ Immutable & │           │  Env (fs,   │
    │ Replayable  │           │  net, proc) │
    └─────────────┘           └─────────────┘
```

**Session** — Immutable append-only event log (like database WAL). The single source of truth.  
**Harness** — Stateless orchestration loop. Crash-tolerant, can restart from any point.  
**Sandbox** — Isolated execution environment. Blast radius containment.

---

## Features

<table>
<tr>
<td width="50%">

### 🔒 Production Security
- **6-layer defense-in-depth** security model
- Permission modes: `allow` / `deny` / `ask`
- Pre/post tool-use hooks for auditing
- Sandbox isolation (filesystem, network, process)
- Hardcoded deny rules for dangerous commands

</td>
<td width="50%">

### 🧠 Advanced Context Management
- **4-level compression pipeline**
  - Snip → Microcompact → Context-Collapse → Autocompact
- Multi-category memory system (short/long-term)
- Automatic dream/consolidation mechanism
- Lazy tool loading to conserve context window

</td>
</tr>
<tr>
<td width="50%">

### 🔧 Multi-Provider LLM Support
- Provider-agnostic `LLMClient` interface
- Anthropic, OpenAI, Azure, Local (Ollama/vLLM)
- Factory pattern for zero-code switching
- Streaming (async generator) architecture

</td>
<td width="50%">

### 🤖 Multi-Agent & MCP
- Coordinator & Swarm patterns
- Model Context Protocol integration
- 6 transport mechanisms (stdio, HTTP, SSE, WS, gRPC, local)
- Sub-agent context isolation with summary-only returns

</td>
</tr>
</table>

---

## Project Templates

Ready-to-use scaffolds with full source code:

```
templates/project-scaffold/
├── python/                    # Python Agent scaffold
│   ├── src/
│   │   ├── agent/             # Core loop, session, context, memory
│   │   ├── llm/               # Client abstraction, factory, providers
│   │   ├── tools/             # Registry, file tools, network tools
│   │   ├── permissions/       # Models, hooks, sandbox
│   │   └── utils/             # Logging, error handling
│   ├── config/                # YAML settings, agent roles, hooks
│   ├── skills/                # Custom skill templates
│   └── tests/                 # Unit & integration tests
│
└── nodejs/                    # Node.js Agent scaffold
    ├── src/                   # Same structure as Python
    ├── config/
    ├── skills/
    └── tests/
```

### Python Stack
`anthropic` · `openai` · `httpx` · `pydantic` · `pyyaml` · `beautifulsoup4` · `pytest`

### Node.js Stack
`@anthropic-ai/sdk` · `openai` · `axios` · `cheerio` · `js-yaml` · `jest`

---

## 10 Design Philosophies

1. **Async Generator Streaming** — yield intermediate events, don't just return results
2. **Continue-Sites for Recovery** — `while(true)` + 7 recovery points from any error
3. **Compile-Time Feature Gating** — dead code elimination at build time
4. **Cache-Prefix Stability** — built-in tools as stable prefix, MCP tools don't invalidate cache
5. **Defense-in-Depth** — 6-layer superposition makes bypass probability decay exponentially
6. **Data-Driven Extensibility** — `settings.json` + `agents/*.md` + `skills/*.md` + hooks
7. **Context as Scarce Resource** — lazy loading, on-demand memory, 4-level compression
8. **Hierarchical Config Override** — CLI > Flag > Policy > Managed > Local > Project > User
9. **Isolated Sub-Agent Contexts** — blank message list, summary-only return
10. **Reversibility-First** — Edit via string replacement, not file overwrite

---

## When to Use

This Skill auto-triggers on keywords like:

> "Build an agent" · "Create an AI assistant" · "Design an agent system" · "Agent optimization" · "Agent scaffolding" · "Agent project template" · "Agent framework" · "Multi-agent" · "Agent upgrade"

### Use Cases

| Scale | Description | Example |
|-------|-------------|---------|
| **Small** | Personal assistant | Coding helper, note organizer |
| **Medium** | Team tooling | Code review bot, CI/CD assistant |
| **Large** | Enterprise platform | Customer support swarm, ops automation fleet |

---

## Roadmap

- [x] 7-phase construction blueprint (v2)
- [x] Python & Node.js project scaffolds
- [x] Multi-agent coordination patterns
- [x] MCP protocol integration
- [x] 6-layer defense-in-depth security
- [x] 4-level context compression pipeline
- [ ] Go language scaffold
- [ ] Evaluation benchmark suite
- [ ] Visual architecture diagrams
- [ ] Real-world case studies

---

## Contributing

Contributions are welcome! Here's how you can help:

- Add scaffolds for new languages (Go, Rust, TypeScript-native)
- Improve reference documentation
- Add evaluation test cases
- Share real-world case studies of agents built with this Skill

Please read the [contributing guide](CONTRIBUTING.md) before submitting a PR.

---

## License

This project is licensed under the Apache License 2.0 — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <sub>Built with ❤️ by the Agent Engineering Community</sub>
  <br />
  <sub>If this project helps you, please ⭐ star it on GitHub!</sub>
</p>
