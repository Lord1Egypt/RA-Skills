---
name: Codex
slug: codex
version: 1.0.0
homepage: https://clawic.com/skills/codex
description: Use Codex safely for repo-aware coding with explicit approvals, sandbox choices, MCP boundaries, and PR-ready verification workflows.
changelog: Initial release with repo-safe execution, approval and sandbox guidance, MCP and cloud guardrails, and review-ready handoff workflows.
metadata: {"clawdbot":{"emoji":"🧭","requires":{"bins":["codex"],"bins.optional":["git","rg"],"env.optional":["OPENAI_API_KEY"],"config":["~/codex/","~/.codex/config.toml"]},"os":["linux","darwin","win32"],"configPaths":["~/codex/","~/.codex/config.toml"]}}
---

## When to Use

User wants to use Codex as a real coding agent instead of a generic chat assistant: inspect a repo, make bounded edits, run review mode, resume work, use MCP safely, or hand work off with clear verification evidence.

Use this skill when the hard part is not "write code" but "make Codex behave safely and predictably" across CLI, `exec`, `review`, `resume`, MCP, app-server, cloud tasks, or local OSS-provider workflows.

## Architecture

Memory lives in `~/codex/`. If `~/codex/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/codex/
|-- memory.md          # Durable activation boundaries and operating defaults
|-- repo-profiles.md   # Per-repo conventions, test surface, and blast-radius notes
|-- safety.md          # Sandbox, approval, and trust defaults
|-- mcp-notes.md       # Approved MCP servers, scopes, and rejection reasons
`-- incidents.md       # Stuck sessions, failed commands, and recovery patterns
```

## Quick Reference

Load only the smallest file needed for the current blocker.

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Install, login, and first-run checks | `install-and-auth.md` |
| Repo execution and `codex exec` workflows | `repo-execution.md` |
| Approval modes and sandbox choices | `approvals-and-sandbox.md` |
| MCP, app-server, cloud, and local-provider guardrails | `mcp-and-cloud.md` |
| Review mode and handoff patterns | `review-and-handoffs.md` |
| Recovery playbooks for auth, stuck sessions, and wrong-scope work | `troubleshooting.md` |

## Requirements

- `codex` binary installed and working on the target machine.
- Active authentication through `codex login` or an explicit `OPENAI_API_KEY` flow when that mode is chosen.
- `git` available when the task involves repository inspection, diff review, or commit-ready workflows.
- Explicit user approval before dangerous sandbox bypass, remote MCP usage, Codex Cloud apply, production commands, or any operation with irreversible side effects.
- Treat model names, features, and app-server behavior as live product surface: verify with `codex --help`, subcommand help, or official docs instead of hardcoding stale assumptions.

## Operating Coverage

This skill treats Codex as an operational coding surface, not as generic AI advice. It covers:
- interactive Codex CLI usage with explicit working-directory and safety choices
- non-interactive `codex exec` and `codex review` workflows
- `resume`, `fork`, and handoff-friendly session recovery
- sandbox and approval policy selection by blast radius
- MCP server trust decisions and local-versus-remote tool boundaries
- Codex app-server and cloud task usage only when their extra trust and review requirements are explicit
- local OSS-provider routing via `--oss` and `--local-provider` when the user intentionally wants local execution

## Data Storage

Keep only durable Codex operating context in `~/codex/`:
- which repos or workspaces are approved for Codex use
- default sandbox and approval posture per task type
- preferred execution surfaces: interactive CLI, `exec`, `review`, cloud, or local OSS provider
- approved MCP servers and what each one is allowed to touch
- recurring recovery notes for wrong directory, dirty worktree, stalled commands, or broken auth

## Core Rules

### 1. Preflight the Task Before Codex Acts
- Lock five facts first: target repo, current directory, dirty worktree state, required permissions, and expected verification.
- If any of those are unclear, pause and resolve them before running Codex with write capability.
- "Start coding" is never the first step in an unfamiliar repo.

### 2. Choose the Operating Mode Explicitly
- Use interactive Codex for exploratory repo work, `codex exec` for bounded non-interactive execution, and `codex review` for review-first tasks.
- If resuming or branching prior work, prefer `resume` or `fork` over re-describing the entire context from scratch.
- Treat cloud, app-server, and MCP-assisted runs as separate modes with separate risk.

### 3. Match Sandbox and Approval to Blast Radius
- Read-only fits inspection, planning, and low-trust exploration.
- Workspace-write fits normal local coding in the approved repo.
- Full access or dangerous bypass is a special-case mode that needs explicit user intent and an external sandbox story.
- Do not normalize high-trust modes for convenience.

### 4. Read the Repo Before Editing It
- Inspect tree shape, git status, entrypoints, conventions, and test surface before proposing edits.
- When the worktree is already dirty, separate user changes from agent changes and avoid destructive cleanup.
- Codex should adapt to the repo, not force the repo into a generic workflow.

### 5. Keep Changes Reviewable and Scoped
- Favor minimal diffs, targeted commands, and explicit file ownership.
- Avoid unrelated cleanup, speculative refactors, or "while here" edits unless requested.
- If a command or edit expands scope, stop and surface that expansion immediately.

### 6. Treat Auth, MCP, and Cloud as Trust Boundaries
- A tool being available does not mean it is approved.
- Review each MCP server for scope, data access, and side effects before enabling it.
- Use existing login sessions when possible; never scrape secrets from local files without clear user intent.
- Inspect cloud diffs before applying them locally.

### 7. Verify Outcomes and Leave a Handoff Trail
- A successful Codex run ends with checks, not with code edits alone.
- Report what changed, what was verified, what failed, and what remains risky.
- For interrupted or long-running work, leave a crisp checkpoint that another operator can resume without guesswork.

## Codex Traps

- Running Codex in the wrong directory -> edits land in the wrong repo or outside intended scope.
- Treating `workspace-write` as harmless -> it still writes real files and can widen a diff quickly.
- Using `--dangerously-bypass-approvals-and-sandbox` for routine work -> convenience becomes unreviewable risk.
- Enabling MCP servers because they are available -> hidden data reach and side effects expand silently.
- Applying cloud output without reviewing the diff -> local repo changes become opaque.
- Letting Codex work through a dirty tree without clarifying ownership -> review noise and accidental overwrite risk.
- Re-running vague prompts after interruption -> duplicated work and inconsistent verification.

## External Endpoints

Only these external categories are allowed unless the user explicitly approves more:

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://api.openai.com | prompts, selected repository context, tool results, and execution metadata needed for Codex runs | Codex model execution, cloud tasks, login-linked agent work |
| https://developers.openai.com/* | doc queries only | Verify current Codex product behavior and configuration details |
| https://{user-approved-mcp-host} | request payloads required by the specific MCP server | Optional user-approved tool access beyond the local machine |

No other data is sent externally unless the user explicitly approves additional MCP servers, Git remotes, or service endpoints.

## Security & Privacy

Data that leaves your machine:
- prompts and the repo context selected for Codex runs against OpenAI services
- optional MCP payloads only for user-approved MCP servers
- optional cloud task payloads and diffs when Codex Cloud is intentionally used

Data that stays local:
- `~/.codex/config.toml` and the user's local Codex session/config state
- durable operating notes under `~/codex/`
- local diffs, verification output, and repo metadata unless the user explicitly pushes or uploads them

This skill does NOT:
- assume dangerous bypass is acceptable by default
- enable remote MCP or cloud apply silently
- scrape tokens from arbitrary files to "help" auth succeed
- hide sandbox or approval choices from the user
- claim that CLI, app-server, cloud, and local `--oss` flows have identical risk

## Trust

By using this skill, Codex work may send prompts and selected repository context to OpenAI, plus any optional user-approved MCP endpoints.
Only install if you trust those services with that data.

## Scope

This skill ONLY:
- helps operate Codex safely and effectively in real coding environments
- structures repo work into explicit execution, review, and handoff modes
- keeps durable memory for approved repos, safety posture, and recurring recovery patterns

This skill NEVER:
- treat every available Codex feature as automatically approved
- recommend destructive git cleanup as a default fix
- blur the line between local-only, cloud, and MCP-assisted execution
- modify its own skill files

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `agentic-engineering` - Strengthen the human workflow around parallel coding agents and blast-radius thinking.
- `coding` - Improve implementation quality once Codex is operating inside the right repo boundaries.
- `git` - Handle branches, diffs, and non-destructive repository recovery safely.
- `api` - Reuse structured API and request-debugging patterns when Codex integrates with services.
- `workflow` - Turn recurring Codex tasks into repeatable, reviewable execution paths.

## Feedback

- If useful: `clawhub star codex`
- Stay updated: `clawhub sync`
