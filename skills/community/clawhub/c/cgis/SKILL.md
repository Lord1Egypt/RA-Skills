---
name: cgis
description: Use when a question is about how code connects rather than what a single file says — finding every caller of a symbol, judging whether a rename or signature change is safe, tracing an execution path, mapping an unfamiliar module, or checking architectural drift. Reach for it before grepping across files or reading whole modules for context.
---

# CGIS — query the graph instead of guessing

Reading files to answer a structural question is the slow, lossy path: it burns context and still leaves you inferring connections. CGIS holds a deterministic graph of the codebase — every function, method, class and the resolved edges between them — and answers those questions exactly.

## When to reach for it

| Question | Tool | Instead of |
| :--- | :--- | :--- |
| "What calls this?" | `cgis_analyze_impact` | grepping the name and hoping |
| "Is this rename safe?" | `cgis_analyze_impact` | reading every plausible caller |
| "What does this end up calling?" | `cgis_trace_flow` | following imports by hand |
| "How is this class laid out?" | `cgis_get_structure` | reading the whole file |
| "Give me context on this symbol" | `cgis_context` | pasting several files |
| "Where is the symbol named X?" | `cgis_find_symbol` | a broad grep |
| "What's coupled or god-classed?" | `cgis_metrics` | intuition |
| "Did this change drift the architecture?" | `cgis_drift` | nothing — there is no manual equivalent |
| "Does every handler reach its authz guard?" | `cgis_audit_reachability` | auditing routes one by one |

A subgraph at depth 2 costs a few hundred tokens. The equivalent in file chunks costs thousands and is less precise.

## First run in a repository

The graph lives in `graph.db` in the project root, and every tool resolves that path relative to the working directory. If a tool answers `Database not found`, the graph has not been built yet:

```
cgis_ingest(project_path="./src")
```

Point it at the source root, not the repository root — ingesting `node_modules` or a virtualenv wastes time and pollutes the graph. `/cgis:ingest` does this for you and picks the right path.

Re-run `cgis_ingest` after any substantial change; it is incremental by default and skips unchanged files. A stale graph is worse than no graph, because it answers confidently and wrongly.

## Reading the answers honestly

CGIS classifies each edge as **internal**, **stdlib**, **external**, or **unresolved**. Unresolved edges are not bugs — they are calls on objects whose type is decided at runtime (`response.json`, `logger.info`, an injected client). No static analyser resolves those without executing the code.

This matters when you act on the output: **an empty impact result means "no static callers found", not "safe to delete."** A symbol reached only through dynamic dispatch, a registry, or a framework decorator will not appear. Check `cgis_validate` if the unresolved share looks high for the area you are touching, and say so rather than asserting safety you cannot see.

## Coverage

Extractors exist for **Python** (`.py`) and **TypeScript** (`.ts`, `.tsx`). Vue, Astro, Go, Rust and everything else are invisible to the graph — in a mixed repository, fall back to reading files for those parts and say which parts of the answer the graph could not cover.

## Not covered here

Guardian, the graph-aware LLM reviewer, is a CI tool rather than an interactive one — it reviews pull requests where no agent is present. Inside a Claude Code session you are already the reviewer, and you now have the graph. See [Guardian in the README](https://github.com/zaebee/codegraph-brain#-guardian-graph-aware-code-review) to wire it into CI.
