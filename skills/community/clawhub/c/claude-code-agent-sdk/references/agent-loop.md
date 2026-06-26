# How the Agent Loop Works

## Loop Cycle

Each agent session follows the same cycle:
1. **Receive prompt** — SDK produces `SystemMessage` (subtype="init")
2. **Evaluate and respond** — Claude produces `AssistantMessage` (text + tool calls)
3. **Execute tools** — SDK runs requested tools and collects results
4. **Repeat** — Steps 2-3 loop (each full cycle is a turn)
5. **Return result** — Final `AssistantMessage` + `ResultMessage` (includes cost, token usage, session ID)

## Message Types

| Type | Description |
|------|-------------|
| `SystemMessage` | Session lifecycle events (init, compact_boundary) |
| `AssistantMessage` | Claude response (text and tool call blocks) |
| `UserMessage` | Tool execution results |
| `StreamEvent` | Raw API stream events (only with partial messages enabled) |
| `ResultMessage` | Loop end marker. subtypes: success/error_max_turns/error_max_budget_usd/error_during_execution |

**TypeScript additional types:** SDKCompactBoundaryMessage, hook events, tool progress, rate limits, etc.

## Tool Execution

**Built-in tool categories:**
- File operations: Read, Edit, Write
- Search: Glob, Grep
- Execution: Bash
- Web: WebSearch, WebFetch
- Orchestration: Agent, Skill, AskUserQuestion, TodoWrite

**Permission controls:** `allowed_tools` (auto-approve), `disallowed_tools` (block), `permission_mode` (mode control).

**Parallel execution:** Read-only tools can run concurrently, state-modifying tools run sequentially.

## Loop Controls

| Option | Controls | Default |
|--------|----------|---------|
| `max_turns`/`maxTurns` | Maximum tool usage round trips | Unlimited |
| `max_budget_usd`/`maxBudgetUsd` | Maximum cost before stopping | Unlimited |

**Effort levels:**
| Level | Behavior | Best for |
|-------|----------|----------|
| `low` | Minimal reasoning, fast responses | File finding, directory listing |
| `medium` | Balanced reasoning | Routine edits |
| `high` | Thorough analysis | Refactoring, debugging |
| `xhigh` | Extended reasoning depth | Coding and agent tasks |
| `max` | Maximum reasoning depth | Complex multi-step problems |

## Context Window

Context does not reset between turns. Consumption sources: system prompt, CLAUDE.md, tool definitions, conversation history, skill descriptions. Large tool outputs consume significant context.

**Auto-compaction:** Automatically summarizes old history when approaching limits. Triggers `compact_boundary` message.

**Strategies to stay efficient:** Use sub-agents to isolate context, selectively load tools, use low effort for simple tasks.

## Handling Results

`ResultMessage.subtype`:
- `success` — Normal completion
- `error_max_turns` — Turn limit reached
- `error_max_budget_usd` — Budget limit reached
- `error_during_execution` — Interrupted by error

`stop_reason` field: `end_turn`, `max_tokens`, `refusal`.