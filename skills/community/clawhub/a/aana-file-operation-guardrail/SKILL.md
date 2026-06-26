# AANA File Operation Guardrail Skill

Use this skill when an OpenClaw-style agent may delete, move, rename, overwrite, publish, upload, export, transform, or bulk-edit user files.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

File operations should be scoped, reversible when possible, explicitly authorized, and limited to the files the user actually intended.

The agent should separate:

- files explicitly named by the user,
- files discovered by a reviewed search or listing,
- files that are candidates but not yet approved,
- files outside the intended workspace or target folder,
- files that need backup, preview, dry-run, or human approval,
- files that must not be touched.

## When To Use

Use this skill before:

- deleting files or folders,
- moving, renaming, or reorganizing files,
- overwriting existing content,
- bulk-editing many files,
- publishing, uploading, exporting, or sharing files,
- running cleanup operations,
- changing generated artifacts that may replace user work,
- applying scripts or formatters across broad paths,
- modifying files outside the current project workspace.

## File Risk Classes

Treat these as higher risk:

- user-authored source files, papers, notes, decks, spreadsheets, images, videos, and documents,
- credentials, config, environment, account, billing, payment, legal, health, or personal files,
- files outside the current workspace,
- large directories, globbed paths, recursive operations, and bulk edits,
- published assets, release artifacts, website files, package outputs, and shared folders,
- operations that are difficult to undo or verify.

## AANA File Safety Loop

1. Identify the intended operation: delete, move, rename, overwrite, publish, upload, export, or bulk edit.
2. Identify the target set: list exact paths or describe the approved folder boundary.
3. Check scope: confirm the target paths are inside the intended workspace or explicitly named destination.
4. Check necessity: remove unrelated files from the target set.
5. Check reversibility: prefer dry-run, preview, diff, backup, copy, trash, or staged change before irreversible action.
6. Check authorization: require explicit user approval for destructive, recursive, cross-folder, publish, upload, or broad operations.
7. Check evidence: do not infer that a file is safe to delete or overwrite without verifying path, ownership, and purpose.
8. Choose action: accept, revise, ask, defer, refuse, or route to human review.

## Required Pre-Flight Checks

Before a risky file operation, verify:

- the operation type,
- the exact target path or bounded target folder,
- whether recursion, globbing, or bulk edits are involved,
- whether files are generated or user-authored,
- whether a backup, diff, or dry-run is available,
- whether the operation crosses project, account, cloud, or shared-folder boundaries,
- whether the result will be published, uploaded, or shared.

## Approval Rules

Ask for explicit user approval before:

- deleting files or directories,
- overwriting non-generated files,
- moving files out of the current workspace,
- applying recursive or glob-based changes,
- publishing or uploading files,
- modifying personal, legal, health, financial, credential, or account files,
- changing more files than the user named,
- acting when path resolution or ownership is unclear.

Approval should name the operation and target scope, for example:

```text
I am about to delete 12 generated files under build/cache/. No user-authored files are included. Proceed?
```

## Safer Alternatives

Prefer:

- preview or dry-run before action,
- diff before overwrite,
- copy before move,
- trash or archive before permanent delete,
- narrow path lists before broad globs,
- generated-output folders before source folders,
- explicit allowlists before recursive edits,
- separate commit or checkpoint before large changes.

## Do Not

- Delete or overwrite files because they appear unused without evidence.
- Expand the target scope beyond the user request.
- Follow broad paths such as a home directory, drive root, cloud root, or repository root unless clearly intended and approved.
- Publish, upload, or share private files without explicit approval.
- Store file contents or paths in memory without permission.
- Treat hidden files, configs, credentials, or dotfiles as safe by default.
- Continue after discovering unexpected files in the target set.

## Review Payload

When using a configured AANA checker, send only a minimal review payload:

- `task_summary`
- `operation_type`
- `target_scope`
- `target_count`
- `risk_classes`
- `authorization_status`
- `reversibility_status`
- `scope_status`
- `recommended_action`

Do not include raw file contents, secrets, private records, or full directory dumps when a path summary is enough.

## Decision Rule

- If scope is narrow, authorized, necessary, and reversible, accept.
- If the operation is useful but target scope is too broad, revise to a narrower allowlist.
- If authorization, path ownership, or expected impact is unclear, ask.
- If the operation needs a dry-run, diff, backup, verified tool, or human review, defer.
- If the request would destroy, expose, or overwrite unrelated user files, refuse and explain briefly.
- If a checker is unavailable or untrusted, use manual file-safety review.

## Output Pattern

For file-sensitive actions, prefer:

```text
File operation review:
- Operation: ...
- Target scope: ...
- Risk: ...
- Safeguard: dry-run / diff / backup / explicit approval / not needed
- Decision: accept / revise / ask / defer / refuse
```

Do not include this review block unless useful to the user or needed before taking action.
