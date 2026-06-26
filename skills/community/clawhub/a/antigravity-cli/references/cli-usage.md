# CLI Usage

## Quick start

- Headless one-shot: `agy --print "Answer this question..."`
- Short one-shot alias: `agy -p "Review this git diff and draft a conventional commit message"`
- Headless alias: `agy --prompt "Prompt..."`
- Continue last session: `agy --continue` or `agy -c`
- Resume by ID: `agy --conversation <id>`
- Start TUI with initial prompt: `agy --prompt-interactive "Summarize this codebase"` or `agy -i`
- Pipe stdin into an interactive prompt: `cat notes.md | agy --prompt-interactive "Analyze"`

## Common flags

| Flag | Alias | Purpose |
| --- | --- | --- |
| `--print <prompt>` | `-p` | Run a single prompt non-interactively and print the response |
| `--prompt <prompt>` | | Alias for `--print` |
| `--print-timeout` | | Timeout for print mode, default `5m0s` |
| `--continue` | `-c` | Continue the most recent conversation |
| `--conversation <id>` | | Resume a specific conversation by ID |
| `--prompt-interactive` | `-i` | Run an initial prompt interactively and keep the session alive |
| `--sandbox` | | Run with terminal sandbox restrictions enabled |
| `--dangerously-skip-permissions` | | Auto-approve all tool requests without prompting |
| `--add-dir <path>` | | Add a workspace directory; repeatable |
| `--log-file <path>` | | Override log file location |

## Subcommands

- `agy install`: configure environment paths and shell settings.
  - `--skip-aliases`: skip shell profile alias purging.
  - `--skip-path`: skip shell profile PATH appending.
- `agy plugin`: manage plugins.
  - `agy plugin list`: list installed plugins.
  - `agy plugin install <target>`: install a plugin, including `plugin@marketplace` targets.
  - `agy plugin uninstall <name>`: remove a plugin.
  - `agy plugin import [source]`: import plugins from Gemini or Claude.
  - `agy plugin enable <name>` / `agy plugin disable <name>`: toggle a plugin.
  - `agy plugin validate [path]`: validate a plugin directory.
  - `agy plugin link <marketplace> <target>`: link to a marketplace.
- `agy update`: update CLI to the latest version.
- `agy changelog`: show changelog and release notes.

## Installation and updates

Use the official Antigravity CLI installation documentation for OS-specific setup, authentication, and enterprise parameters.

Mac/Linux:

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://antigravity.google/cli/install.ps1 | iex
```

Windows CMD:

```cmd
curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd
```

- Installation and auth: https://antigravity.google/docs/cli-install
- CLI overview: https://antigravity.google/docs/cli-overview
- Getting started: https://antigravity.google/docs/cli-getting-started
- Tutorial: https://antigravity.google/docs/cli-tutorial

Use `agy update` for normal CLI updates after installation.

## Command selection

- Use `agy --print` for CI-like or scriptable tasks where stdout is enough.
- Use `agy --prompt-interactive` when the user wants a live session seeded with context.
- Use `agy --continue` only when "latest conversation" is acceptable.
- Use `agy --conversation <id>` when reproducibility matters.
- Add `--add-dir` when a task spans multiple workspace roots.
- For automation or hooks, combine `agy -p` with explicit local verification commands in the prompt.
