# GitHub Copilot CLI docs summary (from docs.github.com)

Reviewed pages:
- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-copilot-cli
- https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli
- https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli

## Confirmed points

- Copilot CLI is GitHub's coding agent for the terminal.
- It can write code, debug, refactor, review, and interact with GitHub.com (PRs, issues, Actions).
- Install command: `npm install -g @github/copilot` (also via brew, winget, or install script).
- Run command: `copilot` (interactive) or `copilot -p "<prompt>"` (programmatic).
- First run requires sign-in (GitHub account with active Copilot subscription).
- Auth via `/login` slash command, or set `COPILOT_GITHUB_TOKEN` / `GH_TOKEN` / `GITHUB_TOKEN`.
- Tool approval system: `--allow-all-tools`, `--allow-tool 'shell(git)'`, `--deny-tool 'shell(rm)'`.
- Plan mode via Shift+Tab for structured implementation planning.
- Session resume with `copilot --resume` or `copilot --continue`.
- Supports MCP servers, custom agents, skills, hooks, and Copilot Memory.
- Auto-compaction when context approaches 95% token limit.
- Default model: Claude Sonnet 4.5 (changeable via `/model`).

## Operational implication for OpenClaw

When OpenClaw invokes Copilot CLI:
1. set `workdir` to target repo,
2. keep `pty:true`,
3. choose foreground/background mode per task length,
4. use `--allow-tool` for scoped permissions or `--allow-all-tools` for full autonomy,
5. stream/check logs for verifiable completion.
