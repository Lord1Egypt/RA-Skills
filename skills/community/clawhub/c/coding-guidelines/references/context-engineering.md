# Context Engineering for Coding

## The Attention Budget Model

Think of context as a finite attention budget. Every token costs attention to process. The model has to form n² pairwise relationships between all tokens — so doubling context more than doubles the complexity.

**Key insight:** Context size has diminishing returns. After a point, more context *hurts* performance (context rot).

## Context Components & Their Costs

| Component | Always loaded? | Cost | Optimization |
|---|---|---|---|
| System prompt / rules | Yes | High | Keep under 500 lines. Core conventions only. |
| Tool definitions | Yes | Medium-High | Only enable tools the task needs |
| File contents | No | Variable | Read targeted files, not whole directories |
| Conversation history | Yes (grows) | Linear | Compact/summarize completed work |
| External data (MCP, APIs) | No | Variable | Load on demand, not by default |

## Context Sizing Rules

### For simple tasks (1-2 files, clear intent)
- System prompt: project conventions only
- Files: the specific files being changed + direct dependencies
- History: fresh session or compacted

### For medium tasks (3-5 files, some ambiguity)
- System prompt: project conventions + relevant domain rules
- Files: changed files + their tests + shared utilities
- History: keep plan + decisions, compact exploration

### For complex tasks (5+ files, architectural changes)
- System prompt: full project context
- Files: changed files + all direct dependencies + tests
- Consider splitting into subagents per module
- History: plan.md as persistent artifact, aggressive compaction

## Compaction Strategies

1. **Summarize completed phases** — "Phase 1 complete: auth middleware added to routes/auth.ts, tests passing"
2. **Drop intermediate exploration** — once you've found the right approach, forget the dead ends
3. **Use files as external memory** — write plans/decisions to files instead of keeping in conversation
4. **Fresh sessions for fresh tasks** — don't carry one task's context into an unrelated task

## AI-Friendly Codebase Design

Code that serves as good context for AI agents:

- **Clear module boundaries** — agent can understand one file without reading 10 others
- **Descriptive naming** — `authenticateUser()` not `auth()`
- **Type definitions** — TypeScript/JSDoc types help the agent understand data shapes
- **Consistent patterns** — if auth uses middleware, don't do auth differently in one module
- **Good comments on non-obvious logic** — explain *why*, not *what*
- **Test files alongside source** — tests show expected behavior as context

## The Context Refresh Pattern

When a session gets long (>70% of context window):

1. Write a summary of current state to a plan file
2. Start a fresh session
3. Load: system prompt + plan file + relevant files
4. Continue from the summary

This is more effective than trying to compact a massive conversation history.
