---
name: feishu-task-management
description: Manage Feishu tasks through a local Python toolkit that always has app credentials and can optionally act as a user for task APIs when OAuth user tokens are available. Use when Codex needs to create, inspect, update, complete, reopen, delete, or change task members in Feishu Task, especially when member names must be resolved through a locally synced member table and alias mapping instead of ad hoc contact lookups.
---

# Feishu Task Management

## Overview

Use this skill to operate Feishu Task through the companion toolkit in `feishu-task-management/toolkit/`. Keep the core workflow in this file: decide the command, resolve members locally, and apply the write-safety rules without loading extra references unless the request falls into an edge case.

## Core Workflow

1. Confirm the request is about Feishu task management through the local toolkit.
2. Before the first API-backed operation, make sure the toolkit is configured. If not, use:
   `python3 feishu-task-management/toolkit/scripts/feishu_config.py guide`
3. Treat app credentials as mandatory base config. Prefer the configured `user_access_token` for task APIs when available, but keep contact and member-sync operations on app auth.
4. If the operation involves people, use the local member table through the toolkit. Do not perform ad hoc contact lookups.
5. Choose the narrowest task command available instead of composing generic HTTP requests.
6. For destructive or state-changing operations, inspect the current task first when practical.
7. Stop if member resolution is ambiguous or missing.

## Command Routing

### Member Table Maintenance

- Sync the authorized contact scope:
  `python3 feishu-task-management/toolkit/scripts/feishu_members.py sync`
- Inspect sync state:
  `python3 feishu-task-management/toolkit/scripts/feishu_members.py stats`
- Test a member lookup:
  `python3 feishu-task-management/toolkit/scripts/feishu_members.py resolve --query "张三"`
- Validate manual aliases:
  `python3 feishu-task-management/toolkit/scripts/feishu_members.py validate-aliases`

### Toolkit Configuration

- Show configuration guidance:
  `python3 feishu-task-management/toolkit/scripts/feishu_config.py guide`
- Write a local runtime config:
  `python3 feishu-task-management/toolkit/scripts/feishu_config.py set --app-id ... --app-secret ...`
- Extend the config with existing user OAuth tokens:
  `python3 feishu-task-management/toolkit/scripts/feishu_config.py set --app-id ... --app-secret ... --user-access-token ...`
- Inspect effective config:
  `python3 feishu-task-management/toolkit/scripts/feishu_config.py show`
- Validate current config:
  `python3 feishu-task-management/toolkit/scripts/feishu_config.py validate`

### Read Operations

- Get one task:
  `python3 feishu-task-management/toolkit/scripts/feishu_task.py get --task-guid ...`
- List tasks:
  `python3 feishu-task-management/toolkit/scripts/feishu_task.py list`

### Write Operations

- Create a task:
  `python3 feishu-task-management/toolkit/scripts/feishu_task.py create --summary ...`
- Update core fields:
  `python3 feishu-task-management/toolkit/scripts/feishu_task.py update --task-guid ...`
- Complete a task:
  `python3 feishu-task-management/toolkit/scripts/feishu_task.py complete --task-guid ...`
- Reopen a task:
  `python3 feishu-task-management/toolkit/scripts/feishu_task.py reopen --task-guid ...`
- Add members:
  `python3 feishu-task-management/toolkit/scripts/feishu_task.py add-members --task-guid ... --member ...`
- Remove members:
  `python3 feishu-task-management/toolkit/scripts/feishu_task.py remove-members --task-guid ... --member ...`
- Delete a task:
  `python3 feishu-task-management/toolkit/scripts/feishu_task.py delete --task-guid ... --yes`

## Member Resolution

Use local resolution only, in this order:

1. Explicit identifiers: `open_id`, `user_id`, `email`, `mobile`
2. Manual alias mapping from `feishu-task-management/toolkit/data/member_aliases.json`
3. Exact canonical matches on `name`, `en_name`, `nickname`, and email
4. Limited fuzzy matching

Apply these safety rules:

- Zero matches: stop and report that the member table or aliases need updating.
- One match: proceed.
- Multiple matches: stop and return the candidate list.

If the authorized scope only yields identifier fields without profile fields, natural-language matching depends on manual aliases. This does not change when task APIs later use a user token.

## Write Safety Rules

- Use the toolkit instead of constructing raw HTTP requests in the skill body.
- Prefer dedicated commands over generic update payloads when a command exists.
- Use dedicated completion commands instead of editing `completed_at` directly.
- Treat `origin` as create-only.
- Clear `start` and `due` explicitly instead of relying on omission.
- Require explicit confirmation before deletion.

## Supported v1 Scope

- Create task
- Get task
- List tasks
- Update summary, description, start, and due
- Delete task
- Complete task
- Reopen task
- Add members
- Remove members

The following are intentionally out of scope for v1:

- reminders
- tasklists
- dependencies
- repeat rules
- custom complete
- attachments

## Conditional References

Load extra context only when the request falls off the main path:

- Read [member-sync-troubleshooting.md](references/member-sync-troubleshooting.md) only when member sync, alias validation, or authorized-scope coverage is the problem.
- Read [task-edge-cases.md](references/task-edge-cases.md) only when handling time-field clearing, `origin`, completion semantics, or deferred task features.
- Read [permission-errors.md](references/permission-errors.md) only when a task operation fails with permission-related behavior such as `1470403`.
- Read [api-alignment.md](references/api-alignment.md) only when changing toolkit payloads or aligning CLI defaults to newer Feishu API samples.
