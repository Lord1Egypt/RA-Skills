---
name: alab-project-controller
description: Use when managing one existing ALab project with a project admin key to create and coordinate experiments, validate and adjust project configuration, manage project-scoped source or lifecycle state, observe project evidence, and launch experiment worker sessions or subagents without exposing admin credentials.
---

# ALab Project Controller

## Overview

Use this skill for the project layer of ALab. It coordinates one existing project with a project admin key: create experiments, launch experiment worker sessions or subagents, observe project-visible evidence, compare best runs, and manage project-scoped configuration, source, validation, annotation, token, and lifecycle state.

## Layer Boundaries

- This skill is not the root-administration layer and not the experiment-work layer.
- It must not initialize ALab homes, rotate root credentials, manage SkyDiscover catalogs, prune global caches/backups, or create/revoke project admin keys.
- After creating an experiment, hand worktree changes to a separate session/thread or subagent in that experiment worktree using `alab-experiment-worker`.
- If follow-up project-level coordination needs its own execution context, use a separate session/thread or subagent with the project admin key and this skill.
- If a separate session is unavailable, use a subagent or worker process with equivalent project/worktree/token isolation. User instructions override this preference.

## Credential Rules

- Accept the project admin key only from a private environment variable or secure stdin.
- Prefer `--key-stdin` for ALab admin commands; avoid inline key arguments in commands that may be logged.
- Never print, commit, write to prompts, or pass the project admin key to experiment worker sessions/subagents.
- When delegating, provide only the credential needed for the delegated task. Project-level coordination may receive the project admin key through a private environment variable, ignored secret file, or secure stdin. Experiment work must use only that experiment's worktree token context.
- The project admin key is for project-level commands such as experiment creation, config/source/lifecycle maintenance, observe, report, and audit. It must not be inherited by experiment worker sessions.
- Experiment worker sessions should not receive root/admin keys or unrelated ambient tokens. Prefer the token file already written in the worktree; if a token must be supplied explicitly, provide only the token for that exact worktree or inspection checkout through a private channel.
- Provide `alab-experiment-worker` skill/instructions to any delegated experiment worker session/thread or subagent.
- When launching a worker, target the experiment worktree and clear admin/root credentials plus unrelated ambient tokens. Use the command reference for environment and path requirements.

## Capabilities

This is a capability guide, not a required sequence. Use the capabilities that fit the project objective:

- Inspect project state with `alab project show`, `alab project config show`, `alab status`, and project-scoped audit or observe commands.
- Use `alab feedback` for ALab/tooling suggestions, questions, or bug reports that should be stored with the local home rather than inside project annotations.
- Create new experiments from the project default source, explicit sources, or visible predecessor experiments when continuation is useful, then delegate worktree changes from that worktree.
- Coordinate experiment lineage by recording experiment ids, worktree paths, source refs, tags, from-experiment choices, and selected commits such as `best`, `final`, or `latest`.
- Launch experiment worker sessions or subagents in experiment worktrees with `alab-experiment-worker` skill/instructions and without project admin or root credentials. Provide task instructions and non-secret helper variables only; let workers use their worktree tokens for `alab run` and `alab submit`.
- When a project uses free evaluation (`runner.type = "none"` and `reward.type = "none"`), tell experiment worker sessions/subagents to submit directly without `alab run`; final run id will be `none` and the result will not appear in best reward ranking.
- Observe project-visible evidence across experiments, runs, artifacts, logs, and annotations. Prefer reward, parse status, warning codes, metrics, best/final commits, and submitted refs over free-form worker claims.
- Treat reward parse failures as contract failures first. For file or Harbor rewards, check that reward JSON contains only finite numeric metrics and move detailed diagnostics to artifacts or hidden/visible logs as appropriate.
- Manage project-scoped configuration, environment variables, secrets, validation, sources, tags, and lifecycle state only when they are part of the requested project objective.
- Use dry-run remove commands before destructive lifecycle actions, and record blockers or cleanup consequences before using force/confirm.
- Produce project-level summaries that state what was created or changed, which experiments and runs matter, what credentials were deliberately withheld from experiment workers, and what follow-up remains.

## Skill Files

- `SKILL.md`: Canonical project-layer boundaries, credential rules, and coordination workflow.
- `SKILL_cn.md`: Synchronized Chinese version of this file.
- `references/commands.md`: Detailed project command surface, experiment creation, worker launch, observe, and lifecycle reference; read before project-scoped admin commands or worker handoff.
- `references/commands_cn.md`: Synchronized Chinese version of the command reference.
- `agents/openai.yaml`: UI metadata and default prompt; update when invocation guidance changes.
