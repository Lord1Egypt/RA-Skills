---
name: agent-repo-router
description: "Repo-aware router skill for AI coding CLIs: map tasks to the right repository, project skill or agent, and native CLI backend across OpenClaw, Claude Code, OpenCode, Codex, Cursor, and Hermes. This ClawHub package is an install notice; follow the official repository documentation for the runtime skill."
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

This ClawHub package is an install notice, not the AgentRepoRouter runtime skill body. AgentRepoRouter is configured at installation time, so use the official repository's installation documentation and review the current source before making any local agent-host changes.

Official repository: https://github.com/wufei-png/AgentRepoRouter

The native setup selects an English or Chinese runtime skill, creates the local repository mapping file, records selected agent hosts and execution CLIs, and links the router skill into the selected agent host directories.

After installation, use the installed router skill and edit the generated repository mapping file printed by the installer.
