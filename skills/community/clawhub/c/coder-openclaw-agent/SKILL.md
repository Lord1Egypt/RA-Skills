---
name: "Coder for OpenClaw"
description: "Install and wire a coding-focused OpenClaw sub-agent for background code execution, test-driven edits, bug fixing, small project scaffolding, and small-to-medium data-analysis tasks."
version: "0.1.3"
metadata:
  openclaw:
    homepage: "https://github.com/MilleniumGenAI/coder-openclaw-agent"
    requires:
      bins:
        - openclaw
        - docker
        - git
      config:
        - openclaw.json
        - openai-codex provider profile configured in OpenClaw
---

# Coder for OpenClaw

## What this skill is
This is an integration skill for installing and wiring the `coder` OpenClaw sub-agent from the public repository:

- [coder-openclaw-agent](https://github.com/MilleniumGenAI/coder-openclaw-agent)

The repository contains:
- the `workspace-coder` prompt pack;
- the `coder-sandbox:latest` Docker image definition;
- the `coder` agent config template;
- the Main -> Coder orchestration contract.

This skill is intended for OpenClaw users who want a strong background coding and data-analysis sub-agent without building the orchestration from scratch.

## What it can do
- code execution and verification inside the OpenClaw sandbox;
- bug fixing and test-driven edits;
- small project scaffolding;
- small-to-medium data-analysis tasks;
- HTML, PDF, spreadsheet, and office-style document processing;
- honest blocked-state reporting through `PARTIAL` or `FAILURE`.

## Requirements
- OpenClaw `2026.3.x` or later
- Docker available on the host
- an authenticated `openai-codex` provider profile

## Install
1. Clone the repository:
   - `git clone https://github.com/MilleniumGenAI/coder-openclaw-agent.git`
2. Copy `openclaw/workspace-coder/` into your OpenClaw base directory, or point your agent config at that path directly.
3. Build the sandbox image from the repository root:
   - `docker build -f docker/coder-sandbox.dockerfile -t coder-sandbox:latest .`
4. Register the agent in `openclaw.json` using:
   - `openclaw/agent-config.template.json`
5. If your main agent delegates coding tasks, align it with:
   - `openclaw/main-coder-prompt.md`

## Validate
Run these checks before using the agent in real work:

```bash
openclaw models status --agent coder --probe --probe-provider openai-codex --json
openclaw sandbox explain --agent coder
```

Then run a first smoke task:

```bash
openclaw agent --agent coder --json --message "Return strictly valid JSON matching coder SOUL schema. GOAL: create /tmp/coder/smoke/main.py that prints hello. INPUTS: none. CONSTRAINTS: work only in /tmp/coder/smoke; use python3 and Linux/bash commands only; use PARTIAL if blocked. SUCCESS CRITERIA: python3 /tmp/coder/smoke/main.py prints hello. DELIVERABLES: codeblocks and sandbox_log."
```

## Core references
- Root README: [README.md](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/README.md)
- Agent config template: [openclaw/agent-config.template.json](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/openclaw/agent-config.template.json)
- Main -> Coder orchestration guide: [openclaw/main-coder-prompt.md](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/openclaw/main-coder-prompt.md)
- Runtime inventory: [docker/RUNTIME.md](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/docker/RUNTIME.md)
- Known limits: [docs/known-limits.md](https://github.com/MilleniumGenAI/coder-openclaw-agent/blob/main/docs/known-limits.md)

## Notes
- This is an OpenClaw-only v1 package.
- ClawHub publishes skills under platform-wide MIT-0 terms.
- The runtime source of truth is `openclaw/workspace-coder/SOUL.md`.
- Default working area inside the sandbox is `/tmp/coder/<task_name>/`.
- The expected output contract is strict JSON with `SUCCESS | PARTIAL | FAILURE`.