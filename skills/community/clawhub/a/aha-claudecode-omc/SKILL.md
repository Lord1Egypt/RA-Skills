---
name: aha-claudecode-omc
description: "Claude Code+OMC orchestration: keep this session as decision maker/integrator; for non-trivial work prefer bounded available agents for search, reading, research, testing, review, and mutually exclusive writes. Preserve confirmation gates and the lowest-sufficient route."
license: MIT-0
metadata:
  compatibility: "Claude Code with OMC installed"
  repository: https://github.com/its-How/aha-orch
  version: "1.1.0"
---

# aha-claudecode-omc

## What This Mode Activates

Agent-facing, brain-led capability orchestration for [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) with [oh-my-claudecode (OMC)](https://github.com/Yeachan-Heo/oh-my-claudecode) installed. This skill enables the agent to discover, select, combine, and reselect available capability surfaces (native runtime, enhancement layer, skill, MCP, command, subagent, worktree) to build the lowest-sufficient task-lifecycle capability route for the task.

For non-trivial work, keep the current Claude Code session as the decision maker and final integrator: own goal, constraints, decomposition, permission checks, integration, acceptance, verification, and final answer. Resolve available agents at runtime and prefer bounded lanes for separable units when they improve evidence; do not delegate merely to create fan-out.

OMC provides a rich agent surface: 32+ specialized agents, Team Mode, Autopilot, Ultrawork, Ralph, and Pipeline orchestration. This skill activates per-task agent matching — the agent selects the OMC capability surface that best fits the task unit rather than defaulting to a fixed agent.

## Pre-Check

Run detection at three levels. Do not collapse a partial failure into a full fallback — only re-orchestrate the specific surface that is unavailable.

1. **L1 OMC installed**: Verify OMC is installed. Check `claude plugin list` for `oh-my-claudecode`. Fallback: inspect `~/.claude/plugins/` directory for OMC. Fallback: check if OMC agents are available via `@mention` in Claude Code.
2. **L2 Agent surfaces available**: Verify that OMC agents are listed and not empty. If L2 passes, the agent may use OMC agent delegation throughout the session.
3. **L3 Feature surfaces available**: If the task needs a specific OMC feature (e.g., Team Mode, Autopilot, Ultrawork, Ralph, Pipeline), verify that feature is available. If L3 fails for a feature, skip that feature but continue using available OMC agent surfaces.
4. Confirm runtime family: Claude Code (not [Codex CLI](https://github.com/openai/codex), not [OpenCode](https://github.com/sst/opencode), not [oh-my-codex (OMX)](https://github.com/Yeachan-Heo/oh-my-codex), not [oh-my-openagent (OMO)](https://github.com/code-yeongyu/oh-my-openagent))
5. **Wrong-runtime guard**: If you are in Codex with OMX, use `aha-codex-omx` instead. If you are in OpenCode with OMO, use `aha-opencode-omo` instead. This skill is for Claude Code+OMC only.
6. **Fallback rule**: If L1 fails (OMC not installed), proceed with native Claude Code capabilities and state the limitation transparently. If L1 passes but L2 or L3 fail, do not fall back to native Claude Code — only skip the specific unavailable OMC surface and continue using available OMC agent surfaces.
7. **Install reference**: If OMC is not installed, see the Reference section below for the install command. This skill does not install OMC.

## Capability Discovery

Run discovery on every orchestration pass. Capability surfaces change across sessions, projects, versions, and permission modes.

1. **Primary tools**: Use Claude Code native Task tool and `@mention` to discover available OMC agents; check OMC runtime docs for the exact agent list
2. **Delegation-first scan**: mandatory for non-trivial work before equivalent inline work; identify bounded units suitable for OMC/native agents, Team Mode, Ultrawork, review lanes, or QA lanes; delegate suitable units, but keep urgent blockers, tightly coupled integration, secret/session boundaries, and write-conflict risks in the primary session; if no unit is delegated, state the concrete reason when it affects collaboration shape or evidence
3. **OMC orchestration modes**: Team Mode, Autopilot, Ultrawork, Ralph, Pipeline — verify which are available in the current OMC installation
4. **Agent categories**: planning, implementation, review, diagnosis, discovery, writing, visual — discover exact available agents from OMC runtime/docs during use; do not hardcode all 32+ agent names
5. **Secondary scan**: check for configured MCPs, available commands, validators, and native subagent surfaces
6. **Permission envelope**: determine read-only vs write, external-write, network, approval policy, and destructive-action limits

Use the closest available OMC/native agent capability for exploration, research, diagnosis, testing, review, or a single bounded writer; do not promise role names that discovery did not expose. The shared v1.1 delegation contract defines the unit matrix, `write_set` rule, direct-work exceptions, and tool-composition boundary.

See `./references/capability-orchestration.md` for the 7-field discovery schema.

If discovery fails, transparently disclose, fall back to built-in reference knowledge, mark it as possibly outdated, and request current capability information only when needed. Do not overclaim actual availability.

## Do NOT Use This Mode For

- Trivial single-file edits or quick Q&A where native Claude Code is sufficient
- Tasks that require explicit operator confirmation at every step
- Cases where delegation would expose secrets/session material, create unbounded write conflicts, or add coordination cost without improving outcome evidence
- Read-only exploration (use Claude Code native Explore agent instead)
- When the instruction says "don't delegate" or explicitly asks for direct work
- Environments where OMC is not installed and cannot be installed

## Rollback / Deactivation

- **Soft**: Stop invoking OMC-specific capabilities and re-orchestrate to native Claude Code capability route. No persistent state is maintained by this skill.
- **Hard**: Remove the skill directory from your skills path (e.g., `~/.claude/skills/aha-claudecode-omc/`).
- **Partial**: If only a specific OMC feature is unavailable, deactivate that feature only and keep using available OMC agent surfaces.

## Reference

- [OMC repository](https://github.com/Yeachan-Heo/oh-my-claudecode)
- OMC install command: `claude plugin marketplace add Yeachan-Heo/oh-my-claudecode` (verify against official repo before use)
- [Claude Code subagents documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- Read `./references/capability-orchestration.md` before applying orchestration logic. It is the source of truth for orchestration steps, transparency, re-orchestration, out-of-session, cost awareness, and the 7-field discovery schema.

## Source & Upgrade

- **Repository**: https://github.com/its-How/aha-orch
- **Note**: This skill is part of the aha-orch multi-skill repository (contains aha-orch-xx, aha-codex-omx, aha-opencode-omo, aha-claudecode-omc).
- **Upgrade**: Run `git pull` in the aha-orch repo, or re-run `npx skills add its-how/aha-orch` to get the latest version.
- **Uninstall**: Delete the skill directory (e.g., `aha-claudecode-omc/`) from your skills path.
