---
name: agent-repo-router
description: "Repo-aware router skill for AI coding CLIs: map tasks to the right repository, project skill or agent, and native CLI backend across OpenClaw, Claude Code, OpenCode, Codex, Cursor, and Hermes. This ClawHub package is an install notice; use the native curl installer for the runtime skill."
---

# AgentRepoRouter

AgentRepoRouter is repo-aware routing for AI coding CLIs as an installable skill for multiple agent hosts. It does not replace OpenClaw, Claude Code, OpenCode, Codex, Cursor, or Hermes; it helps a host choose the right repository, preserve each CLI's native conventions, and pass work to the selected native CLI backend.

AgentRepoRouter is useful when you want an agent host to:

- resolve the target repository from repo names, aliases, and task intent;
- use structured local repo metadata from `repo_mappings.json`;
- notice project-level skills and agents before falling back to global capabilities;
- choose execution CLIs in a predictable order while preserving native CLI invocation patterns;
- share one routing entry point across OpenClaw, Claude Code, OpenCode, Codex, and Hermes.

## Install

If you installed AgentRepoRouter through ClawHub, this package is only a ClawHub page and install notice. It is not the AgentRepoRouter runtime skill body.

Use the native installer from the README:

```bash
curl -fsSL https://raw.githubusercontent.com/wufei-png/AgentRepoRouter/main/scripts/install.sh | bash
```

The native installer is required because AgentRepoRouter is configured at install time. It installs the selected English or Chinese runtime skill, creates the local repository mapping file, records selected agent hosts and execution CLIs, and links the router skill into the selected agent host directories.

Do not use this ClawHub package as the active AgentRepoRouter skill. After running the curl installer, use the installed router skill and edit the generated repository mapping file printed by the installer.
