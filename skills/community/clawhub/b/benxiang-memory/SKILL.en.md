---
name: benxiang-memory
description: Shadow Memory — continuously commit chat history into world state; new sessions recover in seconds. MCP server (stdio, zero dependencies): project state persists in a .origin package. The AI stops "remembering" things — it requests a projection when work starts and commits a semantic transaction when work concludes. Transactions pass deterministic gates before anything is written, so state cannot rot from model misremembering; every field can answer "why is this value what it is". Use when new sessions lose context, multi-agent collaboration drifts, or project progress needs persistence and accountability. (中文版见 SKILL.md)
version: 1.1.1
slug: benxiang-memory
license: Apache-2.0
displayName: Shadow Memory — Project State Persistence
summary: Commits chat history into world state; new sessions recover in seconds. MCP server; transactions pass deterministic gates before commit.
metadata:
  openclaw:
    runtime: node >= 18
    tags: [memory, mcp, state, persistence, agent]
---

# Benxiang Memory · Shadow Memory (MCP Server)

> Chat history is a disposable operating window; project world state persists in a
> Benxiang (.origin) package.
> The AI stops "remembering" things — it requests a projection when work starts and
> commits a semantic transaction when work concludes.

## Why

The real problem with context explosion isn't the window being too small — it's
**chat history being treated as project state**. The longer you talk, the closer you
get to a full memory; compression summaries keep distorting; starting a new session
throws all progress away.

This tool separates the two: what you can afford to lose (conversation) and what you
cannot (world state) are stored apart. Every state change passes a deterministic gate,
so state cannot slowly rot from the model misremembering; every field can answer
"why is this value what it is", so when accounts don't reconcile you can trace who
mangled it, at which step.

## Install

```bash
# The Benxiang protocol repo
git clone https://github.com/dongsheng123132/2origin.git
cd 2origin

# Verify
npm run test:e2e        # 25 assertions (spawns a real subprocess over stdio JSON-RPC)
```

## Usage

```bash
# Create a package (empty — every decision must enter via a transaction, so it carries provenance)
node adapters/memory/init.mjs ./my-project.origin my-project "My Project"

# Wire it into Claude Code
claude mcp add benxiang -- node /absolute/path/adapters/memory/mcp-server.mjs /absolute/path/my-project.origin

# Or via environment variable
ORIGIN_PKG=<package-path> node adapters/memory/mcp-server.mjs
```

## The five tools

| Tool | When to use |
|---|---|
| `origin_state` | Session start, or whenever you're unsure where things stand. Returns a projection of persisted state, not chat history |
| `origin_commit` | Commit after every concluded piece of work. On failure: zero bytes written, plus a reason you can rewrite against |
| `origin_why` | Before reporting a number, or whenever you have a question about a current value. Returns the full change chain with who did what |
| `origin_history` | "What changed recently" / "who touched this area" |
| `origin_diagnose` | Constraint violations, dangling references, double ledgers, model memory-drift rate |

## The five object types

`decision:` decisions · `task:` to-dos · `risk:` risks · `fact:` verified facts · `module:` workspaces

Chat logs themselves, fleeting thoughts, and inconclusive discussions are deliberately
not accepted — those belong to the operating window and are discarded after use.

## Six machine-checkable constraints

- decision status only takes legal values
- task status only takes legal values
- risk status only takes legal values
- **Every decision must state its rationale** — three months later, no one can say why
  an undocumented decision was made
- Every task must have an owner
- Every fact must carry an evidence citation (facts and inferences stay separated)

## New objects must be explicitly declared

```json
{ "creates": [{ "id": "decision:mvp", "type": "decision" }],
  "state_changes": [{ "object": "decision:mvp", "field": "status", "to": "decided" }] }
```

Writing to an undeclared object is rejected on the spot — if a one-letter ID typo
could silently conjure a new object, that ghost object would forever escape every
constraint.

## Verification

```bash
npm run test:e2e     # spawns a real subprocess over stdio JSON-RPC and walks a full round, 25 assertions
```

`e2e.mjs` prints every request and response verbatim — anyone can run it and compare,
including "an illegal commit is rejected with zero bytes written" and "after two
agents change the same field in turn, `why` surfaces both changes".

## Related

- Benxiang protocol (benxiang-protocol): the persistent object representation layer.
- OriginWriter (origin-writer): the same mechanism applied to fiction — world-state
  persistence for long-form novels.

---
