---
name: aha-opencode-omo
description: "OpenCode+OMO orchestration: keep this session as decision maker/integrator; for non-trivial work prefer bounded available agents for search, reading, research, testing, review, and mutually exclusive writes. Preserve confirmation gates and the lowest-sufficient route."
license: MIT-0
metadata:
  compatibility: "OpenCode with OMO installed"
  repository: https://github.com/its-How/aha-orch
  version: "1.1.0"
---

# aha-opencode-omo

## What This Mode Activates

Agent-facing, brain-led capability orchestration for [OpenCode](https://github.com/sst/opencode) with [oh-my-openagent (OMO)](https://github.com/code-yeongyu/oh-my-openagent) installed. This skill enables the agent to discover, select, combine, and reselect available capability surfaces (native runtime, enhancement layer, skill, MCP, command, subagent, worktree) to build the lowest-sufficient task-lifecycle capability route for the task.

For non-trivial work, keep the current OpenCode session as the decision maker and final integrator: own goal, constraints, decomposition, permission checks, integration, acceptance, verification, and final answer. Resolve available agents at runtime and prefer bounded lanes for separable units when they improve evidence; do not delegate merely to create fan-out.

## Pre-Check

Run detection at multiple levels. Do not collapse a partial failure into a full fallback — only re-orchestrate the specific surface that is unavailable.

1. **L1 OMO installed**: Verify OMO is installed and its agent surface is parseable: `opencode agent list`
2. **L2 Agent surfaces available**: Verify that specific OMO agents (e.g., primary and subagent entries) are listed and not empty. If L2 passes, the agent may use OMO agent delegation throughout the session.
3. **L3 Feature surfaces available**: If the task needs a specific OMO feature (e.g., background tasks, specific agent categories), verify that feature is available. If L3 fails for a feature, skip that feature but continue using available OMO agent surfaces.
4. Confirm runtime family: OpenCode (not [Codex CLI](https://github.com/openai/codex), not [oh-my-codex (OMX)](https://github.com/Yeachan-Heo/oh-my-codex))
5. **Wrong-runtime guard**: If you are in Codex with OMX, use `aha-codex-omx` instead. This skill is for OpenCode+OMO only.
6. **Fallback rule**: If L1 fails (OMO not installed), proceed with native OpenCode capabilities and state the limitation transparently. If L1 passes but L2 or L3 fail, do not fall back to native OpenCode — only skip the specific unavailable OMO surface and continue using available OMO agent surfaces.

## Capability Discovery

Run discovery on every orchestration pass. Capability surfaces change across sessions, projects, versions, and permission modes.

1. **Primary tool**: `opencode agent list` to enumerate available agents and enhancement layers
2. **Delegation-first scan**: mandatory for non-trivial work before equivalent inline work; identify bounded units suitable for OMO/native subagents, background lanes, review lanes, or QA lanes; delegate suitable units, but keep urgent blockers, tightly coupled integration, secret/session boundaries, and write-conflict risks in the primary session; if no unit is delegated, state the concrete reason when it affects collaboration shape or evidence
3. **Secondary scan**: use `librarian` to query installed skills, MCPs, commands, validators, and native subagent surfaces
4. **Permission envelope**: determine read-only vs write, external-write, network, approval policy, and destructive-action limits

Use the closest available OMO/native agent capability for exploration, research, diagnosis, testing, review, or a single bounded writer; do not promise role names that discovery did not expose. The shared v1.1 delegation contract defines the unit matrix, `write_set` rule, direct-work exceptions, and tool-composition boundary.

See `./references/capability-orchestration.md` for the 7-field discovery schema.

If discovery fails, transparently disclose, fall back to built-in reference knowledge, mark it as possibly outdated, and request current capability information only when needed. Do not overclaim actual availability.

## Do NOT Use This Mode For

- Trivial single-step edits or read-only Q&A where native OpenCode is sufficient
- Tasks that require explicit operator confirmation at every step
- Cases where delegation would expose secrets/session material, create unbounded write conflicts, or add coordination cost without improving outcome evidence
- Environments where OMO is not installed and cannot be installed

## Rollback / Deactivation

To deactivate: stop using OMO-specific capabilities and re-orchestrate to native OpenCode. No persistent state is maintained by this skill. Partial deactivation is valid: if only a specific OMO feature is unavailable, deactivate that feature only and keep using available OMO agent surfaces.

## Reference

- Read `./references/capability-orchestration.md` before applying orchestration logic. It is the source of truth for orchestration steps, transparency, re-orchestration, out-of-session, cost awareness, and the 7-field discovery schema.

## Source & Upgrade

- **Repository**: https://github.com/its-How/aha-orch
- **Note**: This skill is part of the aha-orch multi-skill repository (contains aha-codex-omx, aha-opencode-omo, aha-orch-xx, aha-claudecode-omc).
- **Upgrade**: Run `git pull` in the aha-orch repo, or re-run `npx skills add its-how/aha-orch` to get the latest version.
- **Uninstall**: Delete the skill directory (e.g., `aha-opencode-omo/`) from your skills path.
