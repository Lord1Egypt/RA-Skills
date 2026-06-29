---
name: aha-codex-omx
description: "Codex+OMX optimized capability orchestration skill. Use this when in Codex with OMX installed. Activates full delegation mode with OMX-specific capability discovery and task-driven orchestration."
license: MIT-0
compatibility: "Codex with OMX installed"
metadata:
  repository: https://github.com/its-How/aha-orch
  version: "1.0.0"
---

# aha-codex-omx

## What This Mode Activates

Full-delegation capability orchestration for [Codex CLI](https://github.com/openai/codex) with [oh-my-codex (OMX)](https://github.com/Yeachan-Heo/oh-my-codex) installed. This skill enables the agent to autonomously discover, select, combine, and reselect available capability surfaces (native runtime, enhancement layer, skill, MCP, command, subagent, worktree) to build the lowest-sufficient execution route for each task unit.

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

1. **Primary tools**: `omx list` to enumerate installed skills and enhancement layers; `explore` for codebase exploration; `autoresearch` for iterative research
2. **Secondary scan**: check for configured MCPs, available commands, validators, and native subagent surfaces
3. **Permission envelope**: determine read-only vs write, external-write, network, approval policy, and destructive-action limits

See `./references/capability-orchestration.md` for the 7-field discovery schema.

If discovery fails, transparently tell the user, fall back to built-in reference knowledge, mark it as possibly outdated, and invite the user to provide current capability information. Do not overclaim actual availability.

## Do NOT Use This Mode For

- Trivial single-step edits or read-only Q&A where native Codex is sufficient
- Tasks that require explicit human confirmation at every step
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
