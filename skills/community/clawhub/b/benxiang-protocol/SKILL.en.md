---
name: benxiang-protocol
description: Benxiang (本象) — a persistent object representation layer for AI work. Chat history is a disposable operating window; project world state persists in a .origin package: objects + relations + state + constraints + provenance. The AI stops "remembering" things — it requests a projection when work starts and commits a semantic transaction when work concludes. Transactions pass deterministic gates before anything is written; every field can answer "why is this value what it is". Use when new sessions lose context, multi-agent collaboration drifts, or project state needs persistence / accountability / replay. (中文版见 SKILL.md)
version: 1.1.1
slug: benxiang-protocol
license: Apache-2.0
displayName: Benxiang Protocol — AI State Layer
summary: A persistent object representation layer: semantic transactions + deterministic gates + evidence chains. State you can query, verify, and trace.
metadata:
  openclaw:
    runtime: node >= 18
    tags: [protocol, state, provenance, transaction, agent, mcp]
---

# Benxiang Protocol · Origin IR + Semantic Transactions + Evidence Chains

**Chat history is a disposable operating window; project world state persists in a
.origin package.**

The AI stops "remembering" things — it requests a projection when work starts and
commits a semantic transaction when work concludes. Transactions pass deterministic
gates before anything is written, so state cannot slowly rot from the model
misremembering; every field can answer "why is this value what it is", so when
accounts don't reconcile you can trace who mangled it, at which step.

> Positioning: Benxiang is an intermediate representation for AI work — the LLVM IR
> of the AI era. The AI doesn't rebuild the world; it submits semantic edits to it.

## Install

```bash
git clone https://github.com/dongsheng123132/2origin.git
cd 2origin
npm run verify    # 96 self-test assertions + 25 MCP end-to-end + mutation check 19/19
```

Zero dependencies: the core runtime (compiler/) imports no third-party packages,
so it can be audited standalone.

## Usage

```bash
# 1. Create a package (empty — every decision must enter via a transaction, so it carries provenance)
node adapters/memory/init.mjs my-project.origin my-project "My Project"

# 2. First thing in any new session: recover the project's world state
node compiler/cli.mjs status my-project.origin

# 3. After every concluded piece of work, commit a semantic transaction
#    (decisions / tasks / risks / facts / workspaces — see the object model below)
node compiler/cli.mjs commit my-project.origin tx.json --by agent-a

# 4. Doubt a value? Ask why
node compiler/cli.mjs why my-project.origin decision:mvp.status

# 5. Package health check: constraint violations, dangling references, model memory-drift rate
node compiler/cli.mjs diagnose my-project.origin && echo healthy
```

Transaction file shape (tx.json):

```json
{
  "transaction_id": "tx-20260807-001",
  "operation": "decide",
  "creates": [{ "id": "decision:mvp", "type": "decision" }],
  "state_changes": [
    { "object": "decision:mvp", "field": "status", "from": "proposed", "to": "decided", "op": "set" },
    { "object": "decision:mvp", "field": "value", "to": "Build Shadow Memory first", "op": "set" }
  ],
  "assertions": ["no-ghost-objects", "every-decision-has-rationale"]
}
```

## The five object types

| Prefix | Object | What it holds |
|---|---|---|
| `decision:` | Decision | What was decided and why (rationale mandatory) |
| `task:` | To-do | What to do, who owns it (owner mandatory) |
| `risk:` | Risk | Risk, severity, mitigation (state must be legal) |
| `fact:` | Verified fact | Facts (evidence citation mandatory; facts and inferences separated) |
| `module:` | Workspace | The boundary of a module or domain |

## Six machine-checkable constraints

All expressed as wildcard objects (`decision:*`), so new objects are covered
automatically — nobody has to remember to add rules:

- decision status only takes legal values
- task status only takes legal values
- risk status only takes legal values
- **Every decision must state its rationale** — three months later, no one can say
  why an undocumented decision was made
- Every task must have an owner
- Every fact must carry an evidence citation (facts and inferences stay separated)

## Why state doesn't rot

1. **Original text and facts are the source** — summaries are rebuildable projections
   with no authority to overwrite the source
2. **Every change passes a gate** — structure / references / snapshot isolation checked
   item by item; on failure, zero bytes written
3. **Inference and fact stay separated** — `status: inference` + confidence + evidence citation
4. **Every state has provenance** — `valid_from` event + `evidence` reference; errors
   can be traced back to the original text
5. **New objects must be explicitly declared** — a one-letter ID typo cannot silently
   conjure an unconstrained ghost object

## MCP integration (recommended)

```bash
node adapters/memory/mcp-server.mjs my-project.origin
# or
ORIGIN_PKG=my-project.origin node adapters/memory/mcp-server.mjs
```

Five tools: `origin_state` (recover projection in a new session) / `origin_commit`
(commit a transaction) / `origin_why` (ask why a value is what it is) /
`origin_history` (who touched this) / `origin_diagnose` (package health check).

## Verification

```bash
npm run verify
```

Full verification chain: core self-tests + five dialect self-tests
(cad/law/office/xlsx/story) + MCP end-to-end (e2e) + conformance vectors +
mutation check.

`compiler/mutation-check.mjs` deliberately breaks protocol promises to see whether
the self-tests catch them — rerun after every core change.

## Related

- OriginWriter (origin-writer skill): the million-word novel engine — transactional
  long-form writing; the Story dialect of this protocol.
- Shadow Memory (benxiang-memory skill): MCP-server project-state persistence, out of the box.
- Action Kernel (影核): the unified action layer — what the AI wants done, and who executes it.
- Redline (叠象): the state, diff, evidence and version layer — what changed, whether it is right,
  and whether it can be proven.

---
