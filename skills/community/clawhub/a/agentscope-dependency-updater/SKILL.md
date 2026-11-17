---
name: agentscope-dependency-updater
description: Inspect an AgentScope project's dependencies and suggest safe updates for agentscope and related packages. Use this whenever the user wants to keep their AgentScope project current or review upgrade impact before bumping versions.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env:
        - PIP_INDEX_URL
      bins:
        - python3
        - pip
    primaryEnv: PIP_INDEX_URL
    envVars:
      - name: PIP_INDEX_URL
        required: false
        description: Optional Python package index URL, useful in air-gapped or internal environments.
    emoji: "\U0001F4E6"
    homepage: https://github.com/agentscope-ai/agentscope
---

# AgentScope Dependency Updater

This skill inspects `pyproject.toml` and current installed packages, then reports upgrade candidates and potential compatibility notes for AgentScope-based projects.

## What this skill does

- Reads `pyproject.toml` dependencies
- Compares against the latest available PyPI versions when possible
- Flags major version bumps for manual review
- Reports AgentScope-related extras and optional dependencies

## Usage

Run the updater script from this skill folder:

```bash
python3 scripts/check_deps.py --project /path/to/project
```

Output is a markdown report with current versions, latest versions, and recommended actions.

## Safety

- This skill never modifies files automatically.
- It only reports; version bumps must be applied manually.
- Network access is best-effort; if PyPI is unreachable, it reports installed versions only.
