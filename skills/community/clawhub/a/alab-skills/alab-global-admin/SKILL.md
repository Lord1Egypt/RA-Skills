---
name: alab-global-admin
description: Use when administering an ALab home with root authority, including home bootstrap, root and project-admin credential management, project initialization and handoff, SkyDiscover catalog management, global cache or backup pruning, and root-level audit/dashboard inspection. Do not use for routine project coordination or experiment work.
---

# ALab Global Admin

## Overview

Use this skill for the root layer of ALab. It owns ALab home setup, root credential rotation, project admin key creation or revocation, project initialization, SkyDiscover catalog lifecycle, cache and backup pruning, global audit inspection, and the root-only local read-only dashboard.

## Layer Boundaries

- This skill is not the project-coordination layer and not the experiment-work layer.
- Use root authority only for root-scoped administration or for project operations that explicitly require root authority.
- After creating a project, issuing a project admin key, or creating a bootstrap experiment, hand follow-up project work to a separate session/thread or subagent using `alab-project-controller`.
- Hand experiment worktree edits to a separate session/thread or subagent in that experiment worktree using `alab-experiment-worker`.
- If a separate session is unavailable, use a subagent or worker process with equivalent project/worktree/token isolation. User instructions override this preference.

## Credential Rules

- Treat the root key as a one-time-rendered local secret.
- Prefer `--key-stdin` for root commands; avoid inline key arguments in logs.
- Do not store raw root/admin keys in tracked files, prompts, commits, screenshots, reports, or command transcripts.
- Store generated project admin keys only in ignored local secret files, such as an example-local `.run/secrets/` directory, or a user-approved secure location.
- When delegating, pass only the credential needed for that task and scope. Root keys stay only with root-admin sessions. Project admin keys go only to project-level sessions for that project. Experiment worktree or inspection tokens go only to sessions working in that exact worktree or checkout.
- Use ignored secret files, private environment variables, or secure stdin rather than prompt text for credential delivery.
- Provide the matching ALab skill/instructions to delegated sessions or subagents: `alab-project-controller` for project-level work and `alab-experiment-worker` for experiment worktree work.
- If a root key is lost, ALab cannot recover it; do not try to bypass credential recovery by editing local state.

## Capabilities

This is a capability guide, not a required sequence. Use the capabilities that fit the administrative objective:

- Bootstrap an ALab home with `alab auth init` only when no home exists, and inspect home health with `alab config show` or `alab config validate`.
- Use `alab feedback` for local ALab/tooling suggestions, questions, or bug reports that should be retained under the home; use root-only `alab feedback list|show|archive` to triage those entries.
- Use `alab dashboard` when a root user needs browser-based read-only inspection of the local home. Treat the dashboard as local-only; do not share the token URL or use it for mutation workflows.
- Manage root credentials deliberately. Rotate root only with explicit intent, and treat replacement keys as one-time-rendered secrets.
- Create, list, and revoke project admin keys. Revoke only after identifying the key id, project scope, and expected impact.
- Initialize projects from local, Git, empty, Harbor, or SkyDiscover sources using config files. Capture the generated project admin key exactly once, store it only in an ignored secret location, and hand it off securely to the project layer, never to an experiment worker.
- When project initialization fails during baseline validation, preserve the redacted logs and distinguish environment/capability failures from reward-contract failures such as non-numeric reward metrics.
- Manage SkyDiscover catalog lifecycle with exact commit pinning, no-network `show`, active-reference blockers, and explicit remove confirmation.
- Maintain global non-authoritative state with cache, trash, and backup prune commands.
- Inspect global or project audit events to verify sensitive lifecycle events, credential changes, catalog changes, cleanup, and project initialization.
- Use dry-run where available before destructive removal, and keep lower-layer work delegated unless the user explicitly instructs otherwise.

## Skill Files

- `SKILL.md`: Canonical root-layer boundaries, credential rules, and workflow guidance.
- `SKILL_cn.md`: Synchronized Chinese version of this file.
- `references/commands.md`: Detailed root command surface, project initialization, catalog, cleanup, and handoff reference; read before root-only actions or destructive maintenance.
- `references/commands_cn.md`: Synchronized Chinese version of the command reference.
- `agents/openai.yaml`: UI metadata and default prompt; update when invocation guidance changes.
