---
name: aha-codex-omx
description: "Codex+OMX orchestration: keep this session as decision maker/integrator; for non-trivial work prefer bounded native subagents with runtime-resolved OMX roles for search, reading, research, testing, review, and mutually exclusive writes. Preserve confirmation gates and the lowest-sufficient route."
license: MIT-0
metadata:
  compatibility: "Codex with OMX installed"
  repository: https://github.com/its-How/aha-orch
  version: "1.1.0"
---

# aha-codex-omx

## What This Mode Activates

Agent-facing, brain-led capability orchestration for [Codex CLI](https://github.com/openai/codex) with [oh-my-codex (OMX)](https://github.com/Yeachan-Heo/oh-my-codex) installed. This skill enables the agent to discover, select, combine, and reselect available capability surfaces (native runtime, enhancement layer, skill, MCP, command, subagent, worktree) to build the lowest-sufficient task-lifecycle capability route for the task.

For non-trivial work, keep the current Codex session as the decision maker and final integrator: own the goal, constraints, decomposition, permission checks, integration, acceptance, verification, and final answer. Run a delegation-first scan before equivalent inline work. Prefer bounded Codex native subagents and available OMX lanes when they provide better evidence or context economy; do not delegate merely to create fan-out.

## Pre-Check

Run detection at three levels. Do not collapse a partial failure into a full fallback — only re-orchestrate the specific surface that is unavailable.

1. **L1 Binary installed**: Verify OMX binary is installed: `omx --version`
2. **L2 CLI surface available**: Verify core OMX CLI commands work: `omx list`, `omx exec --help`. If L2 passes, the agent may use OMX skill enumeration, exec delegation, and sparkshell throughout the session.
3. **L3 Interactive bridge available**: Verify tmux-attached interactive bridge if the task needs `omx question` or team/question orchestration. Check whether a tmux session is attached. If L3 fails, skip `omx question` and team bridge features, but continue using L2 CLI surfaces.
4. Confirm runtime family: Codex (not [OpenCode](https://github.com/sst/opencode), not [oh-my-openagent (OMO)](https://github.com/code-yeongyu/oh-my-openagent))
5. **Wrong-runtime guard**: If you are in OpenCode with OMO, use `aha-opencode-omo` instead. This skill is for Codex+OMX only.
6. **Fallback rule**: If L1 fails (OMX binary not installed), proceed with native Codex capabilities and state the limitation transparently. If L1 passes but L2 or L3 fail, do not fall back to native Codex — only skip the specific unavailable OMX surface and continue using available OMX CLI surfaces.

## Capability Discovery

Run discovery on every orchestration pass. Capability surfaces change across sessions, projects, versions, and permission modes.

1. **Primary tools**: detect native subagent roles plus `omx list` and only the OMX feature surfaces needed for this task. Do not treat a binary or one feature as proof that all roles, models, or interactive bridges are available.
2. **Delegation-first scan**: mandatory for non-trivial work before equivalent inline work; identify bounded units suitable for OMX/native subagents, background lanes, review lanes, or QA lanes; delegate suitable units, but keep urgent blockers, tightly coupled integration, secret/session boundaries, and write-conflict risks in the primary session; if no unit is delegated, state the concrete reason when it affects collaboration shape or evidence
3. **Secondary scan**: check for configured MCPs, available commands, validators, and native subagent surfaces
4. **Permission envelope**: determine read-only vs write, external-write, network, approval policy, and destructive-action limits

### Codex Delegation Map

Resolve these roles from the current runtime before dispatch; use the closest available role or keep the documented exception inline. Do not hardcode model names: the runtime resolves the model for the selected role.

| Unit | Preferred role / lane |
|---|---|
| Repository search, file mapping, focused reading | native `explore` |
| Official/version-sensitive research | native `researcher` |
| Diagnosis | native `debugger` |
| Tests and regression strategy | native `test-engineer` or `verifier` |
| Review / acceptance cross-check | native `code-reviewer`, `verifier`, or `architect` |
| Bounded write | one native `executor` with a declared disjoint `write_set` |

OMX team, review, QA, or persistent modes are optional feature-level lanes; detect the specific feature before use. The primary session remains the only final integrator. Refer to the shared v1.1 delegation contract for return evidence, direct-work exceptions, and tool-composition limits.

See `./references/capability-orchestration.md` for the 7-field discovery schema.

If discovery fails, transparently disclose, fall back to built-in reference knowledge, mark it as possibly outdated, and request current capability information only when needed. Do not overclaim actual availability.

## Do NOT Use This Mode For

- Trivial single-step edits or read-only Q&A where native Codex is sufficient
- Tasks that require explicit operator confirmation at every step
- Cases where delegation would expose secrets/session material, create unbounded write conflicts, or add coordination cost without improving outcome evidence
- Environments where OMX is not installed and cannot be installed

## Rollback / Deactivation

To deactivate: stop using OMX-specific capabilities and re-orchestrate to native Codex. No persistent state is maintained by this skill. Partial deactivation is valid: if only the interactive bridge is unavailable, deactivate bridge features only and keep using OMX CLI surfaces.

## Reference

- Read `./references/capability-orchestration.md` before applying orchestration logic. It is the source of truth for orchestration steps, transparency, re-orchestration, out-of-session, cost awareness, and the 7-field discovery schema.

## Source & Upgrade

- **Repository**: https://github.com/its-How/aha-orch
- **Note**: This skill is part of the aha-orch multi-skill repository (contains aha-codex-omx, aha-opencode-omo, aha-orch-xx, aha-claudecode-omc).
- **Upgrade**: Run `git pull` in the aha-orch repo, or re-run `npx skills add its-how/aha-orch` to get the latest version.
- **Uninstall**: Delete the skill directory (e.g., `aha-codex-omx/`) from your skills path.
