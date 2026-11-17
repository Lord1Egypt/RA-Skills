# codex-thread-repair

> Safely diagnose and repair a single Codex Desktop conversation whose recent turns are hidden by a damaged rollout sequence.

## Features

- Select one local Codex task by its visible title or exact thread ID.
- Detect the narrowly defined ordinal-regression and stale-turn corruption pattern.
- Create a targeted backup, preserve message bodies, and install the repaired rollout atomically.
- Refuse ambiguous or unfamiliar damage, verify both Codex databases, and support guarded rollback.

## Quick Start

```bash
# Install from the multi-skill GitHub repository
npx -y skills add Songhonglei/better-agent-skills -s codex-thread-repair

# Or install with ClawHub
clawhub install codex-thread-repair

# Or clone and copy manually
git clone https://github.com/Songhonglei/better-agent-skills.git
cp -R better-agent-skills/skills/codex-thread-repair ~/.codex/skills/
```

## Usage

Ask your agent:

```text
Use $codex-thread-repair to diagnose and repair "My missing Codex task".
```

The agent diagnoses while Codex is open. If the corruption pattern is supported, it prepares a `.command` launcher. Quit Codex with Cmd+Q, run that launcher once, and let it reopen Codex after verification.

For the complete workflow, safety rules, CLI commands, and exit codes, see [SKILL.md](./SKILL.md).

## Install in your AI agent

| Agent | Install |
|---|---|
| OpenClaw | `clawhub install codex-thread-repair` |
| Codex | `npx -y skills add Songhonglei/better-agent-skills -s codex-thread-repair` |
| Claude Code | Manual: copy to `~/.claude/skills/` |
| Cursor | Manual: copy to `.cursor/skills/` |

## Requirements

- macOS
- Codex Desktop installed as `/Applications/ChatGPT.app`
- Python 3.10+
- Local access to the Codex state directory (normally `~/.codex`)

No third-party Python package or network access is required for repair operations.

## Safety model

Automatic mutation is limited to one validated corruption signature. Before replacement, the tool backs up the selected rollout and consistent SQLite snapshots outside the skill directory. It verifies normalized record hashes and restores the original rollout automatically if post-installation checks fail.

The selected rollout must resolve inside the chosen Codex home's `sessions/` directory; relative paths, symlink escapes, and database paths outside that boundary are refused.

## License

MIT (see [LICENSE](./LICENSE))

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)

## Part of better-agent-skills

This skill belongs to the **🗃️ Workspace & Session** collection in [better-agent-skills](https://github.com/Songhonglei/better-agent-skills).

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for the full version history.
