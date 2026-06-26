---
name: acpx
description: Multi-agent collaboration and task delegation via the Agent Client Protocol (ACP) using acpx. Form agent teams from Claude Code, Codex, OpenCode, Gemini, Cursor, Copilot, and other ACP-compatible agents. Run parallel workstreams, switch agent modes, orchestrate deliberation and consensus, or delegate coding tasks to another agent. Triggers include "delegate to Claude", "use Claude Code", "ask Claude to", "parallel agents", "acpx", "ACP", "agent delegation", "form a team", "council", "multi-agent", "debate", "consensus", "code review team", "security audit", "have Claude/Codex/Gemini review/implement/fix", or any request involving multiple AI agents collaborating.
---

# acpx — Multi-Agent Collaboration via ACP

Form teams of AI coding agents, run deliberations, build consensus, and delegate work — all through the Agent Client Protocol.

## Prerequisites

```bash
npm i -g acpx@latest
```

Install the target agents you want to use (e.g., `npm i -g @anthropic-ai/claude-code`).

## Quick Start: Single Agent

```bash
# One-shot (no session state)
acpx claude exec "fix the failing tests"

# Persistent multi-turn session
acpx claude sessions new --name worker
acpx claude -s worker "analyze the auth module"
acpx claude -s worker "now refactor it based on your analysis"
```

## Quick Start: Multi-Agent Council

The fastest way to get multiple opinions on a task:

```bash
# 1. Assemble team (create named sessions for each agent)
acpx claude sessions new --name claude-r && acpx codex sessions new --name codex-r && acpx gemini sessions new --name gemini-r

# 2. Round 1: fan-out the same question to all agents in parallel
acpx --format quiet claude -s claude-r "Review src/auth.ts for security vulnerabilities. Be specific." > /tmp/r1-claude.txt &
acpx --format quiet codex -s codex-r "Review src/auth.ts for security vulnerabilities. Be specific." > /tmp/r1-codex.txt &
acpx --format quiet gemini -s gemini-r "Review src/auth.ts for security vulnerabilities. Be specific." > /tmp/r1-gemini.txt &
wait

# 3. Round 2: each agent sees all responses and revises
acpx --format quiet claude -s claude-r "Other reviewers said:\n[Codex]: $(cat /tmp/r1-codex.txt)\n[Gemini]: $(cat /tmp/r1-gemini.txt)\n\nRevise your assessment." > /tmp/r2-claude.txt &
acpx --format quiet codex -s codex-r "Other reviewers said:\n[Claude]: $(cat /tmp/r1-claude.txt)\n[Gemini]: $(cat /tmp/r1-gemini.txt)\n\nRevise your assessment." > /tmp/r2-codex.txt &
acpx --format quiet gemini -s gemini-r "Other reviewers said:\n[Claude]: $(cat /tmp/r1-claude.txt)\n[Codex]: $(cat /tmp/r1-codex.txt)\n\nRevise your assessment." > /tmp/r2-gemini.txt &
wait

# 4. Synthesize (the orchestrator agent does this)
echo "=== Final Reviews ===\n\n[Claude]: $(cat /tmp/r2-claude.txt)\n\n[Codex]: $(cat /tmp/r2-codex.txt)\n\n[Gemini]: $(cat /tmp/r2-gemini.txt)"
```

## Council Protocol

The standard multi-agent collaboration pipeline:

```
ASSEMBLE → BRIEF → DELIBERATE → CONVERGE → EXECUTE → REVIEW → DELIVER
 组建团队   分发问题   交叉讨论    形成共识    分工执行   交叉审查   交付成果
```

### Step-by-Step

**1. ASSEMBLE** — Create named sessions for each agent:

```bash
acpx claude sessions new --name council-claude
acpx codex sessions new --name council-codex
acpx opencode sessions new --name council-opencode
```

**2. BRIEF** — Send each agent the task with a role prefix:

```bash
acpx --format quiet claude -s council-claude "[ROLE: Architect] Design a caching layer for our API. Consider: invalidation strategy, TTL, cache-aside vs write-through." > /tmp/r1-claude.txt
acpx --format quiet codex -s council-codex "[ROLE: Performance Expert] Design a caching layer for our API. Consider: invalidation strategy, TTL, cache-aside vs write-through." > /tmp/r1-codex.txt
```

**3. DELIBERATE** — Each agent reviews all other responses and revises:

```bash
ALL_RESPONSES=$(echo "[Claude]: $(cat /tmp/r1-claude.txt)\n\n[Codex]: $(cat /tmp/r1-codex.txt)")
acpx --format quiet claude -s council-claude "Other architects said:\n$ALL_RESPONSES\n\nRevise your design. Address any concerns raised." > /tmp/r2-claude.txt
acpx --format quiet codex -s council-codex "Other architects said:\n$ALL_RESPONSES\n\nRevise your design. Address any concerns raised." > /tmp/r2-codex.txt
```

**4. CONVERGE** — Orchestrator synthesizes a consensus plan.

**5. EXECUTE** — Delegate implementation to agents in parallel:

```bash
acpx --approve-all claude -s exec-claude "Implement the caching layer based on this design: $(cat /tmp/consensus.txt)" &
acpx --approve-all codex -s exec-codex "Write tests for the caching layer: $(cat /tmp/consensus.txt)" &
wait
```

**6. REVIEW** — Cross-review implementations:

```bash
acpx --format quiet codex -s council-codex "Review Claude's implementation for bugs and edge cases:\n$(cat /tmp/impl-claude.txt)"
acpx --format quiet claude -s council-claude "Review Codex's tests for coverage gaps:\n$(cat /tmp/tests-codex.txt)"
```

### Quick Council Commands

```bash
# Assemble a 3-agent team in one line
acpx claude sessions new --name t1 && acpx codex sessions new --name t2 && acpx gemini sessions new --name t3

# Fire-and-forget fan-out (don't wait)
acpx --no-wait --format quiet claude -s t1 "task..." > /tmp/r1-t1.txt

# Collect all Round 1 results
cat /tmp/r1-*.txt

# Cleanup after deliberation
acpx claude sessions close t1 && acpx codex sessions close t2 && acpx gemini sessions close t3
```

### Team Presets

Pre-configured role assignments for common scenarios. See `references/roles.md` for full definitions.

| Preset | Agents | Best For |
|---|---|---|
| `code_review` | maintainer, perf, testing, security, dx | PR reviews, quality gates |
| `security_audit` | security, skeptic, architect, dx, testing | Security-sensitive changes |
| `architecture_review` | architect, perf, skeptic, maintainer, testing | Design decisions, tech debt |
| `devil_advocate` | skeptic, skeptic, architect, maintainer | Go/no-go decisions, proposals |
| `balanced` | neutral × N | General tasks, no specialization |
| `build_deploy` | architect, testing, maintainer | Feature implementation |

## Supported Agents

| Agent | Command | Install |
|---|---|---|
| Claude Code | `acpx claude` | `npm i -g @anthropic-ai/claude-code` |
| Codex | `acpx codex` | `npm i -g @openai/codex` |
| OpenCode | `acpx opencode` | `npm i -g opencode-ai` |
| Gemini CLI | `acpx gemini` | `npm i -g @anthropic-ai/gemini-cli` |
| Cursor | `acpx cursor` | Cursor app |
| GitHub Copilot | `acpx copilot` | `npm i -g @githubnext/github-copilot-cli` |
| Pi | `acpx pi` | github.com/mariozechner/pi |
| Qwen Code | `acpx qwen` | `npm i -g @qwen/qwen-code` |

## Agent Mode Switching

Set working modes (Claude Code example; other agents may vary):

| Mode | Behavior | Use When |
|---|---|---|
| `plan` | Plan only, no execution | Architecture, analysis |
| `default` | Ask before changes | Standard work |
| `acceptEdits` | Auto-accept edits | Trusted refactoring |
| `dontAsk` | Auto-accept everything | Batch tasks |
| `bypassPermissions` | Skip all checks | CI/automation |

```bash
acpx claude -s worker set-mode plan
acpx claude -s worker set model opus      # or sonnet
```

## Session Management

```bash
acpx claude sessions new --name worker    # create named session
acpx claude sessions ensure               # create if missing
acpx claude sessions list                 # list all
acpx claude sessions show                 # inspect current
acpx claude -s worker sessions history    # recent turns
acpx claude -s worker status              # pid, uptime
acpx claude sessions close worker         # soft-close (keeps history)
```

## Output & Permissions

```bash
# Output formats
acpx --format quiet claude exec "task"    # final text only
acpx --format json claude exec "task"     # NDJSON stream

# Permissions
acpx --approve-all claude -s w "task"     # auto-approve all
acpx --approve-reads claude -s w "task"   # auto-approve reads
acpx --deny-all claude -s w "task"        # analysis only

# Lifecycle
acpx --cwd ~/repo claude "task"           # set working directory
acpx --timeout 300 claude "task"          # set timeout (seconds)
acpx --no-wait claude -s w "task"         # fire-and-forget
acpx claude -s w cancel                   # cancel in-flight prompt
```

## Bidirectional Communication

Any agent can call any other agent through acpx:

```bash
# From OpenCode → Claude Code
acpx claude -s worker "review src/auth.ts"

# From Claude Code → OpenCode
acpx opencode -s helper "analyze test results"

# From any → Codex → Gemini (chain)
acpx codex -s coder "implement X" && acpx gemini -s reviewer "review: $(cat result.txt)"
```

## Reference Files

- **`references/roles.md`** — All 8 role definitions (security, architect, skeptic, perf, testing, maintainer, dx, neutral) with prompt prefixes for Round 1 and Round 2, plus team presets with agent-to-role mappings.
- **`references/protocols.md`** — 7 collaboration patterns (fan-out, deliberation, role council, adversarial debate, sequential pipeline, DOVA hybrid, DCI structured) with acpx command examples, decision matrix, and cost estimates.

## Gotchas

- **Mode not settable at creation**: Use `set-mode` after `sessions new`
- **session/update warnings**: Claude Code adapter may emit `Invalid params` — harmless
- **Dead session recovery**: acpx auto-detects and reconnects, replaying mode settings
- **No direct agent-to-agent messaging**: All communication goes through the orchestrator
- **`--format quiet` is essential for piping**: Returns only final text, no tool calls or thinking
- **2 rounds is optimal**: Research shows diminishing returns beyond 2 deliberation rounds
- **Session resume preserves context**: Use the same `-s name` across rounds for continuity
