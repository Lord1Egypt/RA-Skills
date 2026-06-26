---
name: alab-skills
description: Use as the top-level guide for ALab agent-facing role skills. It explains how to install the ALab CLI package, the root/project/experiment skill hierarchy, when to use each subskill, and how the three role skills differ without loading every command reference.
---

# ALab Skills

## Install ALab

ALab installs as the `alab-cli` Python package and exposes the `alab` console command.

Install it from PyPI:

```sh
python -m pip install alab-cli
alab help
```

## Overview

ALab is a local agent-first experiment workbench. It separates root home administration, project coordination, and experiment worktree work so agents can collaborate without sharing unnecessary credentials or mutating the wrong layer.

Use this top-level skill when you need to understand the ALab role-skill system before choosing a specific subskill. For actual operations, load the narrowest matching subskill and its command reference only when needed.

## Skill Hierarchy

- `alab-global-admin`: Root layer. Use for ALab home bootstrap, root credential rotation, project admin key creation/revocation, project initialization, SkyDiscover catalog lifecycle, global cache/backup pruning, root dashboard, and root/global audit inspection. It should hand project coordination to `alab-project-controller` and worktree work to `alab-experiment-worker`.
- `alab-project-controller`: Project layer. Use with one project admin key to create and coordinate experiments, manage project-scoped config/source/validation/lifecycle state, observe evidence, compare runs, and launch experiment worker sessions or subagents. It must not perform root administration or do experiment work in the current session unless the user explicitly asks.
- `alab-experiment-worker`: Experiment worktree layer. Use inside one experiment worktree with that worktree token context to inspect visible evidence, edit candidate source, run evaluation, annotate useful context, and submit final results. It must not accept project admin/root keys or perform project/root operations.

## Selection Rules

- Start with the user's requested authority and current path context. Root key implies `alab-global-admin`; project admin key implies `alab-project-controller`; experiment worktree token context implies `alab-experiment-worker`.
- Prefer the least-privileged subskill that can complete the task.
- When creating or continuing experiment work, create the project/experiment at the higher layer first, then hand worktree changes to a separate session/thread or subagent using the matching lower-layer skill and only the matching credential/token context.
- User instructions override the delegation preference, but not credential hygiene or ALab command authorization.

## Shared Principles

- Keep credentials layer-specific: root keys stay with root-admin sessions, project admin keys stay with project-level sessions for the matching project, and worktree or inspection tokens stay with sessions working in that exact worktree or checkout.
- Provide the matching subskill/instructions to delegated sessions or subagents.
- Keep raw keys and tokens out of prompts, tracked files, logs, screenshots, reports, shared non-secret directories, and copied source files.
- Treat command references as detailed operational material. Do not load every command reference unless the task requires it.

## Files

- `SKILL.md`: This top-level ALab skill guide and subskill router.
- `SKILL_cn.md`: Synchronized Chinese version of this file.
- `agents/openai.yaml`: UI metadata and default prompt for this top-level skill.
- `alab-global-admin/`: Root-layer subskill, including its `SKILL.md`, `SKILL_cn.md`, `agents/openai.yaml`, and `references/commands*.md`.
- `alab-project-controller/`: Project-layer subskill, including its `SKILL.md`, `SKILL_cn.md`, `agents/openai.yaml`, and `references/commands*.md`.
- `alab-experiment-worker/`: Experiment-worktree subskill, including its `SKILL.md`, `SKILL_cn.md`, `agents/openai.yaml`, and `references/commands*.md`.
