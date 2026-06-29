---
name: folk-cli
description: Use the folkctl CLI to inspect and update folk.app CRM data without third-party connectors. Covers people, companies, groups, deals, users, notes, reminders, interactions, and webhooks.
version: 0.1.0
license: MIT-0
metadata: {"openclaw":{"requires":{"env":["FOLK_API_KEY"],"bins":["node","folkctl"]},"install":[{"kind":"node","package":"folkctl","bins":["folkctl"]}],"primaryEnv":"FOLK_API_KEY","envVars":[{"name":"FOLK_API_KEY","required":true,"description":"folk API key used as an Authorization Bearer token."},{"name":"FOLK_API_VERSION","required":false,"description":"Optional folk API version date for X-API-Version."},{"name":"FOLK_API_BASE_URL","required":false,"description":"Optional API base URL override. Defaults to https://api.folk.app."}],"emoji":"👥","homepage":"https://github.com/j-edel/folkctl"}}
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
```

### Deals

folk deals are addressed under a group and an object type, usually the name of the deal object field, for example `Deals`.

```bash
folkctl deals list --group-id grp_123 --object-type Deals --json
folkctl deals create --group-id grp_123 --object-type Deals --name "Project Alpha" --company-id com_123 --person-id per_123 --custom Status=Active --dry-run --json
```

### Notes, reminders, and interactions

```bash
folkctl notes create --entity-id per_123 --content "Met at SaaStr. Follow up next week." --visibility private --dry-run --json
folkctl reminders create --entity-id per_123 --name "Follow up" --visibility private --recurrence-rule "DTSTART;TZID=Europe/Paris:20250717T090000\nRRULE:FREQ=WEEKLY;INTERVAL=1" --dry-run --json
folkctl interactions create --entity-id per_123 --date-time 2025-07-17T09:00:00.000Z --title "Coffee" --content "Discussed the new project." --type ☕️ --dry-run --json
```

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

If `folkctl` is missing, install it from npm (or from GitHub as a fallback):

```bash
npm install -g folkctl
# or: npm install -g github:j-edel/folkctl
```
