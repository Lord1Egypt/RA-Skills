---
name: checkly-members
description: List and manage Checkly account members and pending invites with npx checkly members. Use when auditing account access, filtering members by role/status, updating a member role, or removing a member. Triggers on checkly members, account members, list members, update member role, delete member, pending invites.
---

# checkly members

List account members and pending invites, and safely update or remove existing members.

## Quick start

```bash
# List members and pending invites
npx checkly members

# Search by name or email and emit JSON for automation
npx checkly members --search alice --output json

# Filter access by role/status
npx checkly members --role read_only --status active

# Preview a role change before executing it
npx checkly members update alice@example.com --email --role read_run --dry-run

# Remove a member after previewing the action
npx checkly members delete user_123 --id --dry-run
npx checkly members delete user_123 --id --force
```

## Command reference

```text
checkly members [-s <value>] [--type <value>] [--role <value>] [--status <value>] [-l <value>] [--next-id <value>] [--hide-id] [-o table|json|md]
```

### List flags

| Flag | Description |
|------|-------------|
| `--search`, `-s` | Search members and invites by name or email. |
| `--type` | Filter by item type: `member` or `invite`. |
| `--role` | Filter by role: `owner`, `admin`, `read_write`, `read_run`, `read_only`. |
| `--status` | Filter by status: `active`, `pending`, `expired`. |
| `--limit`, `-l` | Return 1-100 items and enable cursor pagination. |
| `--next-id` | Cursor for the next page; requires `--limit`. |
| `--hide-id` | Hide member and invite IDs in table output. |
| `--output`, `-o` | Output format: `table`, `json`, or `md`. |

## Updating member roles

Use `members update` for role changes. Prefer `--dry-run` first and use `--email` or `--id` to remove ambiguity.

```bash
# Preview a role change
npx checkly members update alice@example.com --email --role read_write --dry-run

# Apply non-interactively after reviewing the preview
npx checkly members update alice@example.com --email --role read_write --force

# Use an ID when emails are ambiguous or unavailable
npx checkly members update user_123 --id --role read_only --force --output json
```

```text
checkly members update MEMBER --role <admin|read_write|read_run|read_only> [--email | --id] [--force] [--dry-run] [-o table|json|md]
```

Owners are account-critical; verify current access with `npx checkly members --role owner` before making ownership/admin changes.

## Deleting members

Deleting members changes account access. Always list and dry-run first; do not use `--force` until the target identity is confirmed.

```bash
# Find the member
npx checkly members --search alice --output table

# Preview deletion
npx checkly members delete alice@example.com --email --dry-run

# Execute only after explicit confirmation/review
npx checkly members delete alice@example.com --email --force
```

```text
checkly members delete MEMBER [--email | --id] [--force] [--dry-run]
```

## Automation patterns

```bash
# Export active admins for audit evidence
npx checkly members --role admin --status active --output json > checkly-admins.json

# Page through members deterministically
npx checkly members --limit 100 --output json
npx checkly members --limit 100 --next-id "$NEXT_ID" --output json
```

## Safety checklist

- Treat role updates and deletes as account-access changes.
- Prefer JSON output for scripts and table/Markdown output for human review.
- Use `--dry-run` on `update` and `delete` before applying changes.
- Use `--email` or `--id` explicitly so automation does not rely on CLI inference.
- Do not print or commit API keys; authenticate with `CHECKLY_API_KEY` and `CHECKLY_ACCOUNT_ID` or `npx checkly login`.
