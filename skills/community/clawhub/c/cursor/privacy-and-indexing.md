# Privacy And Indexing - Cursor

Use this file when the user cares about where code goes, what indexing really means, or whether ignore files provide enough protection.

## Core Reality

Cursor features can send prompts and code context to Cursor services.
That remains true even when the user supplies their own model provider key for some flows.
Do not describe Cursor as local-only unless the exact workflow truly is.

## Indexing

Codebase indexing improves retrieval, but it is also a data-flow decision.
Treat indexing as a separate approval question for privacy-sensitive repos.

## Ignore Files

### `.cursorignore`
Use it to reduce what Cursor should index or reference.
It helps, but it is not a perfect barrier.
Do not assume it blocks every possible tool path or terminal action.

### `.cursorindexingignore`
Use it when the goal is narrower indexing control specifically.
Do not confuse "not indexed" with "impossible to reach."

## Important Boundary

Ignore controls do not guarantee protection against everything an agent can reach through terminal commands or MCP tool calls.
If a file must never be exposed, solve that at the repo, filesystem, or integration boundary, not only with Cursor ignore settings.

## Practical Policy

- for sensitive repos, ask whether indexing is acceptable before enabling rich context features
- keep secrets and production credentials out of repo paths the agent can touch
- treat Background Agents, Bugbot, GitHub integration, and MCP as additional privacy layers to review separately
