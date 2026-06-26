---
name: bigin
description: |
  Zoho Bigin CRM CLI. Search deals, contacts, accounts. Add notes, move deal stages.
  Use when user asks about CRM, deals, pipeline status, or needs to update Bigin records.
  Triggers on: Bigin, CRM, Deal, Pipeline, Contact, Account, Note.
metadata:
  author: heinz
  version: "2.0"
---

# Bigin CRM Skill

CLI: `bash scripts/bigin.sh <command> [args...]`
Map: `bigin-map.json` (auto-generated, refresh with `bigin.sh map`)

## Prerequisites

Required on host: `curl`, `jq`, `python3` (for map generation and stage validation).
Credentials: `~/.bigin-oauth.json` (or set `BIGIN_CREDS_FILE`). See README.md for OAuth setup.

## Guardrails

- **Read-only by default.** All read commands work without flags.
- **Write ops** require: `BIGIN_WRITE=1 bash scripts/bigin.sh <write-command> ...`
- **Delete ops** require: `BIGIN_WRITE=1 BIGIN_CONFIRM=1 bash scripts/bigin.sh delete ...`
- **NEVER** write/update/delete without explicit user approval.

## Key Concepts

### Bigin != Zoho CRM
- "Deals" are called **Pipelines** (module API name: `Pipelines`)
- "Companies" are called **Accounts**
- Sub_Pipeline = the pipeline category (e.g., "Sales", "Support")
- Stage = the deal stage within a pipeline
- Sub_Pipeline is **NOT criteria-searchable** — use `word` search instead

### Module Names
| UI Name | API Name |
|---------|----------|
| Deals/Pipelines | Pipelines |
| Companies | Accounts |
| Contacts | Contacts |
| Products | Products |
| Tasks | Tasks |

> **Tip:** Run `bash scripts/bigin.sh map` to discover your org's layouts, stages, sub-pipelines, and field definitions.

## Commands

### Read Operations (no flags needed)

```bash
# Search deals by keyword (company name, deal name, etc.)
bash scripts/bigin.sh deals "Acme Corp"

# Search deals by stage
bash scripts/bigin.sh deals --stage "Qualified"

# List all deals (paginated)
bash scripts/bigin.sh deals --limit 50

# Get single deal
bash scripts/bigin.sh deal <deal_id>

# Search contacts
bash scripts/bigin.sh contacts "Smith"

# Search accounts (companies)
bash scripts/bigin.sh accounts "Google"

# Get single record
bash scripts/bigin.sh get Accounts <account_id>
bash scripts/bigin.sh get Contacts <contact_id>

# List notes for a record
bash scripts/bigin.sh notes Accounts <account_id>
bash scripts/bigin.sh notes Pipelines <deal_id>

# List products
bash scripts/bigin.sh products              # all products
bash scripts/bigin.sh products <deal_id>    # products on a deal

# Metadata
bash scripts/bigin.sh modules               # list all modules
bash scripts/bigin.sh fields Pipelines      # list fields for module
bash scripts/bigin.sh map                   # regenerate bigin-map.json
```

### Write Operations (require BIGIN_WRITE=1)

```bash
# Add note to record
BIGIN_WRITE=1 bash scripts/bigin.sh note Accounts <id> "Title" "Note content here"
BIGIN_WRITE=1 bash scripts/bigin.sh note Pipelines <deal_id> "Title" "Note content"

# Move deal to new stage
BIGIN_WRITE=1 bash scripts/bigin.sh move <deal_id> "Qualified"

# Update record fields
BIGIN_WRITE=1 bash scripts/bigin.sh update Pipelines <deal_id> '{"Amount":15000}'

# Create record
BIGIN_WRITE=1 bash scripts/bigin.sh create Contacts '{"First_Name":"Jane","Last_Name":"Doe","Email":"jane@example.com"}'
```

### Raw API (escape hatch)

```bash
bash scripts/bigin.sh raw GET "/Pipelines?fields=Deal_Name,Stage&per_page=10"
BIGIN_WRITE=1 bash scripts/bigin.sh raw PUT "/Pipelines/<id>" '{"data":[{"Stage":"Won"}]}'
```

## Important: fields Parameter

Bigin v2 GET endpoints **require** explicit `fields` parameter. The CLI handles this automatically with sensible defaults per module. Override with `--fields` flag.

## Search Behavior

- `deals <keyword>` — word search across all searchable deal fields
- `deals --stage "Stage Name"` — criteria search on Stage field
- `contacts <keyword>` — word search (name, email, etc.)
- `accounts <keyword>` — word search (company name, etc.)
- `search <module> <field> <value>` — exact criteria search on specific field

## Token Management

Tokens auto-refresh (1h lifetime). If token errors occur, the CLI auto-refreshes and retries.

## Error Handling

- 429/5xx: Auto-retry with exponential backoff (3 attempts)
- OAUTH_SCOPE_MISMATCH: Endpoint needs a scope we don't have
- REQUIRED_PARAM_MISSING: Usually means `fields` parameter needed
- INVALID_QUERY: Field not searchable via criteria — use word search instead

## Date Formats

Bigin expects dates in **YYYY-MM-DD** format (e.g. `2026-03-15`). DateTime fields use ISO 8601: `2026-03-15T14:30:00+01:00`.

When creating or updating records with date fields, always format as `YYYY-MM-DD`. Do NOT use `DD.MM.YYYY`, `March 15, 2026` or other locale formats.

## Pagination

The CLI returns one page of results (default: 50, max: 200 via `--limit`). Check the `info.more_records` field in the response. If `true`, more records are available.

## Anti-Patterns

- Don't search Sub_Pipeline via criteria (not searchable), use word search
- Don't use `Pipeline_Name` field, it's `Deal_Name`
- Don't forget `BIGIN_WRITE=1` for any mutation
- Don't hardcode Stage/Pipeline IDs, use `bigin-map.json` or stage names
- Don't use COQL, Bigin v2 doesn't support it (no scope exists)
- Don't pass dates as `DD.MM.YYYY` or locale strings, always `YYYY-MM-DD`
- Don't pass already-wrapped arrays to create/update (CLI wraps in `{data:[...]}` automatically)
