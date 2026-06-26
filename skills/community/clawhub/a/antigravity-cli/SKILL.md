---
name: antigravity-cli
description: Use this skill when the user wants to run, configure, troubleshoot, or explain Google Antigravity CLI (`agy`), including one-shot prompts, interactive TUI sessions, conversation resume, artifact review, plugin management, slash commands, keybindings, sandbox/permissions, settings files, or migration from Gemini CLI.
metadata:
  openclaw:
    emoji: 🪂
    requires:
      bins: [agy]
---

# Antigravity CLI

Use this skill for Google Antigravity CLI, whose binary is `agy`. Do not call it `antigravity` in commands.

## Default workflow

1. Determine whether the user needs non-interactive automation, interactive TUI help, configuration, artifact review, plugin work, or migration.
2. Prefer `agy --print` for scriptable one-shot tasks and `agy` / `agy --prompt-interactive` for live TUI workflows.
3. Check the local binary before giving command-specific guidance when possible:
   ```bash
   agy --help
   agy version
   ```
4. For risky work, keep sandboxing and permission prompts enabled. Do not suggest `--dangerously-skip-permissions` unless the user explicitly wants that risk and the workspace is trusted.
5. When changing settings, prefer the TUI `/config`, `/permissions`, `/model`, `/keybindings`, or `/mcp` commands. Edit JSON files directly only when the TUI path is unavailable or the user asks for file-level changes.

## References

Load only the relevant reference:

- `references/cli-usage.md`: one-shot mode, conversation resume, common flags, subcommands, plugins, and install/update basics.
- `references/overview-workflows.md`: CLI vs Antigravity 2.0 positioning, integration model, and best-practice workflow patterns.
- `references/tui.md`: interactive TUI, slash commands, keybindings, prompt composition, and interaction tips.
- `references/artifacts.md`: artifact review workflow, approvals/rejections, media drawer, and safe review defaults.
- `references/security-permissions.md`: sandbox, fine-grained permissions, approval presets, and risky-command guidance.
- `references/config-platform.md`: settings paths, plugins, MCP config, skills paths, auth, SSH, Antigravity 2.0 integration, and migration notes.

## Gotchas

- `--prompt` is an alias for `--print`; it does not keep the session interactive.
- Model selection is normally handled inside the TUI with `/model`, not by inventing a model flag.
- `agy --continue` resumes the most recent conversation; use `agy --conversation <id>` for a specific session.
- Plugin management is under `agy plugin ...`; local Agent Skills live separately in skill paths.
- Artifact review is interactive; for headless automation, design prompts to ask for patch summaries or command output instead of relying on the review panel.
