---
name: aha-orch-xx
description: "Runtime-agnostic capability orchestration skill. Activates full delegation mode with capability discovery and task-driven orchestration. Use when maximizing runtime + enhancement layer capabilities. If you have a runtime-specific skill (aha-codex-omx / aha-opencode-omo), prefer that instead."
license: MIT-0
metadata:
  repository: https://github.com/its-How/aha-orch
  version: "1.0.0"
---

## What This Skill Activates

This skill is a runtime-neutral orchestration framework. It does not prescribe concrete tools, commands, or runtime implementations. Instead, it tells the agent how to detect the current execution context, discover all available capability surfaces, converge them into the lowest sufficient execution route, execute with transparency, and re-orchestrate when a capability gap appears.

Use this skill when no runtime-specific skill is available. If aha-codex-omx or aha-opencode-omo is present and matches the active runtime, prefer that instead.

## Do NOT Use This Skill For

- Tasks that are already covered by a runtime-specific skill (aha-codex-omx / aha-opencode-omo).
- Situations where the user explicitly wants a fixed, non-adaptive execution route.
- Bypassing confirmation-gated actions, permission limits, or safety boundaries.
- Claiming capability availability without evidence.

## Rollback / Deactivation

To deactivate this skill, stop applying the orchestration framework. If the runtime-specific skill is available, switch to it. If neither is appropriate, fall back to the runtime's default behavior. There is no persistent state to clean up.

## Reference

- Read `./references/capability-orchestration.md` before applying orchestration logic. It is the source of truth for runtime detection, capability discovery fields, orchestration, transparency, re-orchestration, out-of-session, and cost awareness.
- If aha-codex-omx or aha-opencode-omo is available and matches the active runtime, prefer that runtime-specific skill instead.

## Source & Upgrade

- **Repository**: https://github.com/its-How/aha-orch
- **Note**: This skill is part of the aha-orch multi-skill repository (contains aha-codex-omx, aha-opencode-omo, aha-orch-xx, aha-claudecode-omc).
- **Upgrade**: Run `git pull` in the aha-orch repo, or re-run `npx skills add its-how/aha-orch` to get the latest version.
- **Uninstall**: Delete the skill directory (e.g., `aha-orch-xx/`) from your skills path.
