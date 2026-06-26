---
name: alab-experiment-worker
description: Use when operating inside one ALab experiment worktree with that worktree token context to inspect status, edit candidate source, run evaluations, submit final results, and read visible experiment evidence without project admin or root privileges.
---

# ALab Experiment Worker

## Overview

Use this skill for the experiment worktree layer of ALab. It improves one candidate source tree, reads visible evidence available to that worktree token, runs evaluation from the worktree token context for standard projects, and submits the final result when the project mode allows it.

## Layer Boundaries

- This skill is not the project-coordination layer and not the root-administration layer.
- It must not use project admin keys, root keys, catalog commands, cache commands, project configuration mutation, credential management, audit commands, or lifecycle removal commands.
- If project-level or root authority is required, stop that branch and report the needed operation to a project-level or root-admin session instead of requesting a higher-privilege key.

## Operating Rules

- Trust only the current worktree context and its `.alab/token`.
- Do not accept root keys, project admin keys, or tokens for other worktrees or inspection checkouts. If a launcher provides an explicit token, verify that it belongs to the current worktree context before using it.
- Do not read, print, copy, commit, or rewrite raw tokens or keys.
- Do not edit `.alab/`, ALab home state, cache directories, shared run directories, hidden evaluator assets, secret files, or project control files.
- Edit only task-relevant source files inside the experiment worktree.
- Keep source editing and CLI state separate. The experiment worktree is the only editable source surface; any added ALab home, uv cache, pycache, or shared directory is for `alab run`/`submit` state only and must not be inspected, patched, copied, or committed.
- Keep changes reviewable: prefer focused iterations, deterministic checks, and concise run messages.
- If the launcher provides `ALAB_CMD_PREFIX`, use that launcher-provided command prefix for ALab calls; otherwise use `alab`.
- Check `git status --short` before important runs or submit when Git is available, and keep generated/untracked files intentional.
- Use `alab help` before unfamiliar commands; commands outside the worktree token surface must be treated as unavailable.
- If ALab returns `COMMAND_UNAVAILABLE`, stop that branch and report the missing capability instead of trying to bypass it.

## Working Flow

Do not treat this as a fixed checklist. First understand the current worktree task, local instructions, existing candidate, and ALab context. When useful, inspect visible prior experiments, runs, artifacts, logs, annotations, or inspection checkouts for reference and inspiration.

Iterate on the candidate with focused edits and cheap local checks. In standard evaluation projects, run `alab run --message "<brief reason>"` when the candidate is ready. In free evaluation projects where ALab points directly to submit, or `alab run` returns `COMMAND_UNAVAILABLE` because no evaluator exists, skip run evidence and prepare a direct submit instead.

Use visible evidence to diagnose weak or failed results and keep improving while there is a plausible path forward. Record durable context with annotations when it would help later workers, especially decision rationale, failed approaches, remaining risks, and next-step context. Archive and remove annotations that are no longer needed, no longer valid, or likely to mislead later workers.

Submit only with a supporting passed run in standard evaluation mode, or with documented direct-submit behavior in free evaluation mode. If no supporting passed run exists in standard mode, do not submit; report the best evidence and blocker.

## Capabilities

This is a capability guide, not a required sequence. Use the capabilities that fit the task:

- Inspect current context with `alab status` and `alab help`.
- Leave ALab-home feedback with `alab feedback` when you notice a tooling suggestion, question, or bug that should not be mixed into experiment submission feedback.
- Read task files and project instructions that are present in the worktree.
- Inspect visible historical experiments with `alab observe experiments ...` and related visible runs, artifacts, logs, and annotations. Use this evidence to find promising approaches, avoid repeated failures, and understand prior best or final commits. Visibility is still enforced by ALab; do not try to access hidden or unavailable items.
- When a visible historical experiment looks relevant, create an inspection checkout with `alab exp checkout <exp_id> --path <dir> --commit best|final|latest`, record the rendered inspection commit, read its task-relevant files, and compare them with the current worktree before copying anything. Use normal Git comparison tools where helpful, for example `git diff --stat <inspection_commit>..HEAD`, `git diff <inspection_commit> -- <path>`, or `git diff --no-index <inspection_checkout>/<source_path> <current_worktree>/<source_path>` for a direct file/subtree comparison. Copy only task-relevant source files or snippets into the current experiment worktree when they are genuinely useful; never copy `.alab/`, raw tokens, hidden assets, secret files, ALab home/cache files, or project control files.
- Change task-relevant source files in the worktree and keep the changes understandable for later workers.
- Add or list tags on the current experiment when tags are useful evidence for later project-level sessions or workers; tags do not grant visibility.
- Keep runner outputs machine-parseable. If the task writes a reward file, put only the configured numeric metrics in that reward file; put case details, traces, or explanations in separate visible artifacts/logs when allowed.
- Run local cheap checks when they exist, then run `alab run --message "<brief reason>"` for standard evaluation projects. For free evaluation projects, do not force a run; direct submit is expected.
- Diagnose failed or weak runs using visible stdout/stderr previews, warning codes, artifacts, logs, metrics, and annotations.
- When the intended changes are complete and the current worktree has the required support for its mode, submit the result with a factual message, summary, feedback, and refs.

## Submit Guidance

- Submit only after a passed run for the current candidate in standard evaluation mode. In free evaluation mode, direct submit is allowed and the final run id will render as `none`.
- Treat submit refs as provenance links for later review and optimization, not as decoration.
- Actively add `--ref <exp_id>` for visible experiments that informed the strategy, source changes, comparison baseline, failure avoidance, or continuation path.
- Use `--ref none` only when the result does not depend on or intentionally reference any prior experiment.
- Do not invent refs, cite inaccessible experiment ids, or cite a visible experiment only because it exists.
- Keep `--message` short. Put the substantive record in `--summary`/`--summary-file` and `--feedback`/`--feedback-file`: what changed, which passed run supports it or why free evaluation has no run, key metrics when present, which refs mattered, and remaining risks.
- If no submit is performed, clearly state the blocking reason and the best run evidence available.

## Skill Files

- `SKILL.md`: Canonical experiment-worktree boundaries, operating rules, workflow, and submit guidance.
- `SKILL_cn.md`: Synchronized Chinese version of this file.
- `references/commands.md`: Detailed worker command surface, observe patterns, inspection checkout rules, evaluation, and submit reference; read before unfamiliar ALab commands or run/submit flows.
- `references/commands_cn.md`: Synchronized Chinese version of the command reference.
- `agents/openai.yaml`: UI metadata and default prompt; update when invocation guidance changes.
