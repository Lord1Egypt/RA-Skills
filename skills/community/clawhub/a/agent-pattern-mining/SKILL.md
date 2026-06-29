---
name: agent-pattern-mining
description: Study another AI agent, coding CLI, or assistant codebase and extract transferable patterns into concrete local improvements. Use when asked to learn from Claude Code, Codex, Gemini CLI, Cursor, or any agent framework/repo; when benchmarking agent UX/architecture; or when turning observed features into OpenClaw skills, workflow upgrades, AGENTS.md updates, or implementation plans.
---

# Agent Pattern Mining

Mine reusable agent patterns from real codebases and turn them into concrete upgrades instead of vague inspiration.

## Workflow

1. Scope the source repo and the upgrade target.
   - Clarify whether the goal is analysis only, a new skill, workflow changes, implementation work, or all of them.
   - Prefer targeted reading over exhaustive reading.

2. Map the architecture quickly.
   - Inspect entrypoints, command/tool registries, memory/context code, planning/tasking, permissions, plugin/extensibility, remote/background execution, and observability.
   - Ignore vendor-specific infrastructure unless it carries a transferable pattern.

3. Build a transfer matrix.
   - For each promising pattern, capture:
     - source feature
     - user benefit
     - portability/risk
     - nearest OpenClaw equivalent
     - concrete local action

4. Classify findings.
   - **Adopt now**: can be captured as a skill, workspace rule, reference note, or small implementation.
   - **Prototype later**: good idea, but needs tool/runtime changes.
   - **Do not copy**: tightly vendor-locked, high-complexity, or low-value for the local setup.

5. Apply improvements in this order.
   - Create or improve a skill when the pattern is reusable.
   - Update `AGENTS.md` for stable workflow changes.
   - Update `TOOLS.md` for environment-specific operational notes.
   - Update daily memory or `MEMORY.md` for durable lessons.
   - Propose config/runtime changes only when the user explicitly asks for them.

6. Report the result concretely.
   - Summarize what the source system does well.
   - List what was adopted locally.
   - List what still requires deeper implementation work.
   - Name the exact files created or changed.

## What to Look For

Prioritize patterns that reduce operator burden or improve agent reliability:

- explicit planning modes
- visible task tracking
- context budget awareness
- selective memory recall
- permission boundaries and review gates
- multi-agent orchestration
- deferred tool discovery
- plugin/skill hot reload
- change/diff observability
- session recovery and history search

Deprioritize patterns that are mostly infrastructure-specific:

- first-party SaaS integrations
- internal telemetry wiring
- organization-specific policy systems
- vendor-only remote services without a local analogue

## Output Shape

Use this structure when delivering results:

1. **Architecture sweep** — the subsystems reviewed
2. **Best transferable ideas** — ranked by impact
3. **Concrete local upgrades** — skill/doc/workflow changes already made
4. **Gaps left open** — good ideas not yet implemented
5. **Files changed** — exact paths

## References

- Read `references/claude-code-patterns.md` when the source is Claude Code or when the user wants proven patterns from agentic coding CLIs.

## Guardrails

- Do not claim an upgrade happened unless a file, workflow, or configuration actually changed.
- Prefer lean skills: keep `SKILL.md` procedural and move detailed analysis to `references/`.
- When the repo is large, read representative files first, then deepen only where the pattern is promising.
- If the user asks for self-upgrade, translate findings into persistent artifacts, not just commentary.
