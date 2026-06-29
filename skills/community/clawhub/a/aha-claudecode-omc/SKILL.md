---
name: aha-claudecode-omc
description: "Claude Code+OMC optimized capability orchestration skill. Use this when in Claude Code with OMC (oh-my-claudecode) installed. Activates full delegation mode with OMC-specific capability discovery and task-driven orchestration."
license: MIT-0
compatibility: "Claude Code with OMC installed"
metadata:
  repository: https://github.com/its-How/aha-orch
  version: "1.0.0"
---

# aha-claudecode-omc

## What This Mode Activates

Full-delegation capability orchestration for [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) with [oh-my-claudecode (OMC)](https://github.com/Yeachan-Heo/oh-my-claudecode) installed. This skill enables the agent to autonomously discover, select, combine, and reselect available capability surfaces (native runtime, enhancement layer, skill, MCP, command, subagent, worktree) to build the lowest-sufficient execution route for each task unit.

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
2. **OMC orchestration modes**: Team Mode, Autopilot, Ultrawork, Ralph, Pipeline — verify which are available in the current OMC installation
3. **Agent categories**: planning, execution, review, diagnosis, discovery, writing, visual — discover exact available agents from OMC runtime/docs during use; do not hardcode all 32+ agent names
4. **Secondary scan**: check for configured MCPs, available commands, validators, and native subagent surfaces
5. **Permission envelope**: determine read-only vs write, external-write, network, approval policy, and destructive-action limits

See `./references/capability-orchestration.md` for the 7-field discovery schema.

If discovery fails, transparently tell the user, fall back to built-in reference knowledge, mark it as possibly outdated, and invite the user to provide current capability information. Do not overclaim actual availability.

## Do NOT Use This Mode For

- Trivial single-file edits or quick Q&A where native Claude Code is sufficient
- Tasks that require explicit human confirmation at every step
- Read-only exploration (use Claude Code native Explore agent instead)
- When the user says "don't delegate" or explicitly asks for direct execution
- Environments where OMC is not installed and cannot be installed

## Rollback / Deactivation

- **Soft**: Stop invoking OMC-specific capabilities and re-orchestrate to native Claude Code execution. No persistent state is maintained by this skill.
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
