---
name: aha-orch-xx
description: "Runtime-neutral orchestration: keep this session as decision maker/integrator; for non-trivial work prefer bounded available agents for search, reading, research, testing, review, and mutually exclusive writes. Preserve confirmation gates and the lowest-sufficient route; prefer a matching runtime adapter when available."
license: MIT-0
metadata:
  repository: https://github.com/its-How/aha-orch
  version: "1.1.0"
---

## What This Skill Activates

This skill is an agent-facing runtime-neutral orchestration framework for the consuming AI agent. It does not prescribe concrete tools, commands, or runtime implementations. Keep the current session as decision maker and final integrator, detect the current runtime context, then prefer bounded available agents for separable search, reading, research, tests, review, and single-writer units when they improve evidence. Converge to the lowest sufficient route and re-orchestrate on a capability gap.

Use this skill when no runtime-specific skill is available. If aha-codex-omx, aha-opencode-omo, or aha-claudecode-omc is present and matches the active runtime, prefer that instead.

## Do NOT Use This Skill For

- Tasks that are already covered by a runtime-specific skill (aha-codex-omx / aha-opencode-omo / aha-claudecode-omc).
- Situations where the instruction explicitly requests a fixed, non-adaptive capability route.
- Bypassing confirmation-gated actions, permission limits, or safety boundaries.
- Claiming capability availability without evidence.
- Delegating trivial tasks or unbounded work where delegation would add coordination cost without improving outcome evidence.

## Runtime-neutral Delegation Map

Detect available agent capabilities first, then use the closest capability for exploration/read-only context, research, diagnosis, testing, review, or one bounded writer. Do not invent role or model names. The shared v1.1 delegation contract defines the unit matrix, `write_set` rule, direct-work exceptions, and tool-composition boundary.

## Rollback / Deactivation

To deactivate this skill, stop applying the orchestration framework. If the runtime-specific skill is available, switch to it. If neither is appropriate, fall back to the runtime's default behavior. There is no persistent state to clean up.

## Reference

- Read `./references/capability-orchestration.md` before applying orchestration logic. It is the source of truth for runtime detection, capability discovery fields, orchestration, transparency, re-orchestration, out-of-session, and cost awareness.
- If aha-codex-omx, aha-opencode-omo, or aha-claudecode-omc is available and matches the active runtime, prefer that runtime-specific skill instead.

## Source & Upgrade

- **Repository**: https://github.com/its-How/aha-orch
- **Note**: This skill is part of the aha-orch multi-skill repository (contains aha-codex-omx, aha-opencode-omo, aha-orch-xx, aha-claudecode-omc).
- **Upgrade**: Run `git pull` in the aha-orch repo, or re-run `npx skills add its-how/aha-orch` to get the latest version.
- **Uninstall**: Delete the skill directory (e.g., `aha-orch-xx/`) from your skills path.
