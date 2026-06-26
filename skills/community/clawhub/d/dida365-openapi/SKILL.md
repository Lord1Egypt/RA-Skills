---
name: dida365-openapi
description: 基于滴答清单（Dida365）官方 OpenAPI 和 OAuth2 的任务管理 Skill，直连 dida365.com，不经过任何第三方服务，你的数据只在本地和滴答清单服务器之间传输。零第三方依赖，纯 Python 标准库实现。完整覆盖项目与任务的增删改查、完成、移动、筛选，支持标签、提醒、重复规则等丰富功能，并内置输入验证和灰色区域防护，确保每次 API 调用都安全可靠。详细文档与同类 Skill 对比见 GitHub：https://github.com/workingcoder/dida365-openapi 。Use when the agent needs to manage Dida365 tasks, projects, tags, reminders, or repeat rules through the official OpenAPI.
metadata:
  openclaw:
    requires:
      bins:
        - python
      env:
        - DIDA365_CLIENT_ID
        - DIDA365_CLIENT_SECRET
---

# Dida365 OpenAPI

## Overview

Use this skill to call the documented Dida365 OpenAPI surface through the bundled Python CLI.
Prefer `python scripts/dida365.py ...` over ad hoc `curl` because the bundled CLI already handles OAuth, config loading, exact project-name resolution, structured errors, and every documented endpoint.
Use Python 3.9 or newer.

The skill's default support surface is the documented API plus stable tested extensions that behaved consistently in real app/API round-trips:

- task `kind` writes for `TEXT` and `NOTE`
- task `tags` writes

## Boundaries

This skill intentionally stays on the official Dida365 OpenAPI surface.
It does not use browser-cookie private APIs.

That means the following are explicit non-goals here:

- standalone tag catalog / CRUD operations outside task create or update writes
- project folder / group operations
- full-account sync from private endpoints
- private batch task/project operations
- achievement or productivity-stat calculations from private data

If a user asks for those, state that they are outside the official API-backed scope of this skill.

## Quick Start

1. Persist app config once:
   - `python scripts/dida365.py auth setup --client-id ... --client-secret ... --redirect-uri ...`
2. Preferred OAuth path:
   - `python scripts/dida365.py auth login-local --client-id ... --client-secret ...`
   - Open the URL printed to stderr and finish the browser flow.
3. Verify the connection:
   - `python scripts/dida365.py project data --project-id inbox`
4. Read or write data:
   - `python scripts/dida365.py project list`
   - `python scripts/dida365.py task create --project-id inbox --title "Example"`
   - `python scripts/dida365.py task completed --start-date ... --end-date ...` to query completed tasks across all projects

Manual `authorize-url` / `exchange-code` flows remain supported; see `references/auth-and-config.md` when the localhost callback flow is not suitable.

## Command Rules

- Use `auth` for OAuth helpers, token cache inspection, and token cleanup.
- Use `project` for project CRUD and project data reads.
- Use `task` for task CRUD, complete, move, completed-task queries, and filter queries.
- Use `project data --project-id inbox` for inbox reads. Do not use `project get --project-id inbox`.
- Use `--project-name` only when the user gave a human-readable project name. Resolution is exact match only.
- Use `--json-file` or `--json` when the payload contains arrays or nested objects such as `items`, `reminders`, bulk move operations, or advanced filter bodies.
- Treat first-class flags as the final override layer. `--json-file` loads a base payload, `--json` overrides it, and scalar flags override both.
- After write operations such as `task create`, `task update`, and `task complete`, prefer a read-back step when the stored result matters. Use `task get` to verify fields like `reminders`, `repeatFlag`, `tags`, and `kind`.
- Stable task `kind` writes are `TEXT` and `NOTE`. Use checklist `items` instead of direct `CHECKLIST` kind writes.
- `task filter --tag-json` uses any-match / OR semantics in real testing, not all-match semantics.
- Unfiltered `task filter` responses are capped at 200 rows for this endpoint on the tested account. Narrow the query window or add filters when completeness matters.
- Use the enum values, date format, confirmed reminder patterns, and confirmed recurrence patterns from `references/api-reference.md`. Do not invent undocumented values.
- The CLI blocks known gray-area reminder and recurrence values. If a pattern is not listed as confirmed in `references/api-reference.md`, do not assume it is safe.
- Expect JSON on stdout for every command. Commands that allow successful empty responses normalize them to `{"ok": true}`.
- Expect structured JSON errors on stderr for validation failures and non-2xx API responses.

## Auth And Config

- Config precedence is CLI flags, then environment variables, then local files in `${XDG_CONFIG_HOME:-~/.config}/dida365-openapi/`.
- `auth exchange-code` and `auth login-local` persist config and token state; `auth setup` persists config without performing OAuth.
- See `references/auth-and-config.md` for environment variables, local file locations, and localhost callback details.

## Command Selection

- Need the raw authorization link: use `auth authorize-url`.
- Already have an OAuth `code`: use `auth exchange-code`.
- Want the CLI to wait for the browser callback: use `auth login-local`.
- Need to inspect current config or token state: use `auth status`.
- Need to remove only the cached token: use `auth clear-token`.
- Need inbox tasks or columns: use `project data --project-id inbox`.
- Need one project by id or exact name: use `project get`.
- Need tasks under a project plus columns: use `project data`.
- Need today's tasks: use `task filter` with the local-day `startDate` / `endDate` window.
- Need a weekly completion review: use `task completed` with a weekly date range and omit `--project-id` for an account-wide view.
- Need an exact documented create/update payload: prefer `--json-file`.
- Need a single move operation quickly: use `task move --from-project-id ... --to-project-id ... --task-id ...`.
- Need multiple move operations: use `task move --json '[{...}, {...}]'`.
- Need completed tasks across all projects: omit `--project-id` from `task completed`.

## References

- Read [references/auth-and-config.md](references/auth-and-config.md) for OAuth flow details, config precedence, token cache rules, and local callback behavior.
- Read [references/api-reference.md](references/api-reference.md) for endpoint coverage, field names, request-body quirks, documented schema notes, and confirmed `repeatFlag` patterns.
- Read [references/examples.md](references/examples.md) for command examples covering common read/write flows.
