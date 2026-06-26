---
name: ambiguous
description: Control an Ambiguous Workspace — tasks, docs, wiki, drive, calendar, CRM, mail, chat, and more — via the `ambiguous` CLI. Use for creating/reading/updating workspace data, running authenticated API calls, and discovering every available operation at runtime.
homepage: https://ambi.cc
metadata:
  openclaw:
    emoji: "🧭"
    requires:
      bins: [node, npx]
---

# Ambiguous Workspace CLI

Use `npx ambiguous` to act on an Ambiguous Workspace account. The CLI is a dynamic shell over the workspace's OpenAPI spec — every operation the API exposes is reachable as a subcommand, and `--help` at any level is authoritative.

## Authenticate

**First time?** Bootstrap an agent + workspace + human owner in one call. The API key is stored at `~/.ambi/config.json` automatically.

```bash
npx ambiguous auth signup --name "Research Bot" --human-email phil@example.com
# ✓ Workspace created, agent provisioned, API key saved
# → Verification email sent to phil@example.com
```

The human accountable for the agent receives a verification email. The agent is usable immediately; some workspace features (invites, billing, provisioning more agents) unlock after the human verifies.

**Already have an API key?** Paste it once:

```bash
npx ambiguous auth login --token ak_xxxxxxxxxxxx
npx ambiguous auth status        # confirm
```

## Discover what's available

Always start here when you don't already know the command — the help output is generated from the live API spec, so it reflects exactly what the server supports:

```bash
npx ambiguous --help                    # top-level groups (tasks, wiki, docs, drive, …)
npx ambiguous tasks --help              # subcommands in a group
npx ambiguous tasks create --help       # flags + positional args for one command
```

Flags map 1:1 to request fields. A field named `assignee_id` in the API becomes `--assignee-id`. Enum fields show their valid values in help text.

## Output modes

- Piped stdout or `--json`: JSON only, suitable for `| jq`
- Interactive TTY: tables for list endpoints, key/value records for single objects
- `-q` / `--quiet`: suppress non-essential output

```bash
npx ambiguous tasks list --json | jq '.data[] | {id, title, status}'
npx ambiguous tasks get <id> --json
```

## Common operations

```bash
# Tasks
npx ambiguous tasks list --status todo --priority high
npx ambiguous tasks create "Review Q1 plan" --priority high --assignee-id <user-id>
npx ambiguous tasks update <id> --status done
npx ambiguous tasks delete <id> -y        # `-y` skips confirmation

# Docs
npx ambiguous docs list
npx ambiguous docs get <id>

# Wiki
npx ambiguous wiki spaces list
npx ambiguous wiki pages list --space <space-id>

# Mail
npx ambiguous mail inbox
npx ambiguous mail send --to user@example.com --subject "Hi" --body "..."

# Calendar
npx ambiguous calendar events list --from 2026-05-01 --to 2026-05-31

# Drive
npx ambiguous drive list
```

The full catalog lives under `--help` — don't guess command names.

## Setting fields

Three equivalent ways to pass input, in precedence order (last wins):

1. Positional arg (only for fields named in `x-cli.positional`, e.g. `title` on `tasks create`)
2. Named flag — `--priority high`
3. Generic field flag — `-f priority=high` (repeatable, supports nested keys via dot notation, auto-coerces booleans/numbers)
4. Piped JSON on stdin — `echo '{"priority":"high"}' | npx ambiguous tasks create "Title"`

```bash
# Equivalent:
npx ambiguous tasks create "Ship" --priority high --assignee-id u_123
npx ambiguous tasks create "Ship" -f priority=high -f assignee_id=u_123
echo '{"priority":"high","assignee_id":"u_123"}' | npx ambiguous tasks create "Ship"
```

## Errors and exit codes

- `0` — success
- `1` — general error
- `2` — auth error (401 / 403, or not logged in)

In JSON mode, errors are structured:

```json
{"ok": false, "error": "Task not found", "statusCode": 404}
```

In TTY mode, errors print a red `Error:` line and a yellow `Hint:` line when actionable.

## Config and cache

- Auth + API URL: `~/.ambi/config.json`
- OpenAPI spec cache: `~/.ambi/spec.json`

## Notes

- Every command requires auth except `auth` and `config`. Unauthenticated calls return exit code `2` with a "Run `npx ambiguous auth login`" hint.
- Help output reflects the live API — new server commands appear without a CLI upgrade.
