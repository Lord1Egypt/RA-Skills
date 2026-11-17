---
name: folk-cli
description: Use folkctl to inspect and update folk.app CRM data through its REST API. Covers people, companies, groups, members, custom fields, deals, custom objects, users, notes, tasks, interactions, legacy reminders, webhooks, and official MCP setup.
version: 0.2.2
license: MIT-0
metadata: {"openclaw":{"requires":{"env":["FOLK_API_KEY"],"bins":["node","folkctl"]},"install":[{"kind":"node","package":"github:j-edel/folkctl#4a9c2af28427432beee018561f5f43e3ecfc2645","bins":["folkctl"]}],"primaryEnv":"FOLK_API_KEY","envVars":[{"name":"FOLK_API_KEY","required":true,"description":"folk API key used as an Authorization Bearer token."},{"name":"FOLK_API_VERSION","required":false,"description":"Optional folk API version date for X-API-Version."},{"name":"FOLK_API_BASE_URL","required":false,"description":"Optional API base URL override. Defaults to https://api.folk.app."}],"emoji":"👥","homepage":"https://github.com/j-edel/folkctl"}}
---

# folk CLI skill

Use this skill when the user wants to work with folk.app CRM data through the first-party folk API and does not want a third-party connector.

## Tooling

The CLI command is `folkctl`. It is designed for OpenClaw-style agent use:

- `--json` for machine-readable output
- `--dry-run` before mutations when you need to preview requests
- `--all` to follow pagination
- `--no-input` to fail instead of prompting
- `--yes` or `--force` only when the user has explicitly confirmed deletion

Never print, log, or include `FOLK_API_KEY` in responses. Prefer environment variables over stored config in automated environments.

## First checks

Run these before doing unfamiliar work:

```bash
folkctl --version
folkctl api ls
folkctl api docs people.list
folkctl people --help
```

When a command is missing or the schema is unclear, use the generic escape hatch:

```bash
folkctl api request GET /v1/users/me --json
folkctl api request POST /v1/people --data '{"firstName":"Ada"}' --dry-run --json
```

## Authentication

For OpenClaw, expect `FOLK_API_KEY` to be set in the environment:

```bash
export FOLK_API_KEY="fk_live_..."
folkctl auth status
```

For local setup:

```bash
printf '%s' "$FOLK_API_KEY" | folkctl auth login --token-stdin
```

## Common tasks

### List or search people

```bash
folkctl people list --limit 20 --json
folkctl people search "Ada Lovelace" --json
folkctl people list --filter fullName:like:Ada --json
```

### Create a person

Preview first:

```bash
folkctl people create \
  --first-name Ada \
  --last-name Lovelace \
  --email ada@example.com \
  --group-id grp_123 \
  --dry-run --json
```

Then run without `--dry-run` once confirmed.

### Create or update companies

```bash
folkctl companies create --name "Acme Inc" --url https://acme.example --group-id grp_123 --dry-run --json
folkctl companies update com_123 --name "Acme Corporation" --dry-run --json
```

### Discover groups and custom fields

```bash
folkctl groups list --json
folkctl groups fields grp_123 person --json
folkctl groups fields grp_123 company --json
folkctl groups fields grp_123 Deals --json
folkctl groups members list grp_123 --json
folkctl groups fields get grp_123 person "Status" --json
folkctl groups create --name "Partners" --visibility private --dry-run --json
folkctl groups members add grp_123 usr_123 --role reader --dry-run --json
folkctl groups fields create grp_123 person --name "Region" --type textField --dry-run --json
```

Use `groups fields update` with raw JSON for `addOptions`, `updateOptions`, and `removeOptions`. Removing options also removes their associated contact data and requires the same confirmation as deletion. Names containing spaces must be quoted.

### Deals

folk deals are addressed under a group and an object type, usually the name of the deal object field, for example `Deals`.

```bash
folkctl deals list --group-id grp_123 --object-type Deals --json
folkctl deals create --group-id grp_123 --object-type Deals --name "Project Alpha" --company-id com_123 --person-id per_123 --custom Status=Active --dry-run --json
folkctl objects list --group-id grp_123 --object-type Projects --json
folkctl objects create --group-id grp_123 --object-type Projects --name "Website launch" --dry-run --json
```

`objects` exposes the same API for any custom object type. Discover the exact group and object type names before creating or updating records.

### Notes and interaction history

```bash
folkctl notes create --entity-id per_123 --content "Met at SaaStr. Follow up next week." --visibility private --dry-run --json
folkctl notes search "contract renewal" --created-after 2026-08-01T00:00:00Z --all --json
folkctl interactions past --entity-id per_123 --all --json
folkctl interactions upcoming --entity-id per_123 --json
folkctl interactions get lit_123 --entity-id per_123 --json
folkctl interactions create --entity-id per_123 --date-time 2026-09-06T09:00:00.000Z --title "Coffee" --content "Discussed the new project." --activity-type coffee --dry-run --json
folkctl interactions update lit_123 --entity-id per_123 --content "Updated notes." --dry-run --json
```

Interaction history and editing are in open beta. Reads need the linked entity ID; update needs it in the body (`--entity-id` constructs it). Only manually logged interactions can be updated or deleted. Imported email, calendar, and WhatsApp content may be hidden by workspace privacy rules; missing content is not evidence that an interaction never occurred.

### Tasks and follow-ups

```bash
folkctl tasks list --only-assigned-to-me --empty completedAt --all --json
folkctl tasks list --entity-id per_123 --filter dueAt:lt:2026-09-30 --json
folkctl tasks create --entity-id per_123 --title "Follow up" --due-at 2026-09-08 --due-time 09:00 --is-public=false --dry-run --json
folkctl tasks update tsk_123 --due-at 2026-09-10 --description "Review the proposal." --dry-run --json
folkctl tasks done tsk_123 --completed-at 2026-09-08T14:00:00Z --dry-run --json
folkctl tasks todo tsk_123 --dry-run --json
```

Use real user-supplied dates and identifiers. `dueAt` is a date, `dueTime` is an optional `HH:mm` time, and `recurrenceFrequency` is weekday, weekly, biweekly, monthly, quarterly, yearly, or null. Tasks default to public in the API; set `--is-public=false` when a private task is intended. Completion is a deliberate POST action; do not send `completedAt` through `tasks update` or mark work complete merely because its due date has passed.

Task `--entity-id` uses `filter[entity][in]`; task text search is not supported. Existing `reminders` commands remain available but are deprecated and are not automatically migrated. Folk's sunset documentation differs between February 11 and 13, 2027; migrate before the earlier date and consult the live endpoint's `Sunset` header and [migration guide](https://developer.folk.app/migrations/reminders-to-tasks).

### Official MCP setup

```bash
folkctl mcp info --json
folkctl mcp config codex
folkctl mcp config cursor
```

These commands print offline setup snippets for `https://mcp.folk.app/mcp`. Merge them with existing client configuration and authenticate through the client's OAuth flow. The REST API key is separate from MCP authentication. `folkctl` does not execute MCP tools or run an MCP server. For current tools and schemas, use [Folk's MCP reference](https://developer.folk.app/mcp/tools).

### Webhooks

```bash
folkctl webhooks list --json
folkctl webhooks create --name "My app" --target-url https://example.com/webhook --event person.created --dry-run --json
```

## Safety rules

Before create/update/delete commands, prefer `--dry-run --json` and summarize the exact resource, method, path, and body for the user.

For deletes, do not pass `--yes` or `--force` unless the user explicitly asks to delete the exact record. If the user has not confirmed, run a dry-run or ask for confirmation.

If the API returns 401/403, tell the user to verify or rotate `FOLK_API_KEY`. Do not ask them to paste secrets into chat.

## Installation hint

Skill 0.2.2 targets CLI 0.2.1. If `folkctl` is missing, install the immutable CLI source used in [v0.2.1](https://github.com/j-edel/folkctl/releases/tag/v0.2.1), including the task boolean validation fix:

```bash
npm install -g --ignore-scripts github:j-edel/folkctl#4a9c2af28427432beee018561f5f43e3ecfc2645
folkctl --version
```

The expected CLI version is `0.2.1`. The commit pin fixes the installed source even if the default branch or release tag changes. Its CLI source and package metadata match the release tag; the tag also includes this updated companion skill. This release has no runtime dependencies or installation lifecycle scripts. Complete installation and check the version before making `FOLK_API_KEY` available to the CLI.
