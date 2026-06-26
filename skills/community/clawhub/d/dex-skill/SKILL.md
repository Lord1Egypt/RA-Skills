---
name: dex-skill
description: >
  Manage your Dex personal CRM — search, create, and update contacts, log interaction notes,
  set follow-up reminders, organize contacts with tags and groups, and manage custom fields.
  Use this skill when the user wants to: (1) Find or look up a contact, (2) Add or edit contact details,
  (3) Log a meeting, call, or interaction note, (4) Set a reminder or follow-up task,
  (5) Organize contacts into groups or apply tags, (6) Track custom data with custom fields,
  (7) Merge duplicate contacts, (8) Review their relationship history or prepare for a meeting,
  (9) Authenticate with Dex via /dex-login,
  or any other personal CRM task involving their professional network.
metadata:
  version: "2.0.2"
  openclaw:
    emoji: "\U0001F91D"
    homepage: https://getdex.com
    skillKey: "dex-skill"
    requires:
      bins: ["dex"]
    install:
      - id: "npm"
        kind: "node"
        package: "@getdex/cli"
        bins: ["dex"]
        label: "Install Dex CLI (npm)"
---

# Dex Personal CRM

Dex is a personal CRM that helps users maintain and nurture their professional relationships. It tracks contacts, interaction history, reminders, and organizational structures (groups, tags, custom fields).

## Setup — Detect Access Method

Check which access method is available, in this order:

1. **MCP tools available?** If `dex_search_contacts` and other `dex_*` tools are in the tool list, use MCP tools directly. This is the preferred method — skip CLI setup entirely.
2. **CLI installed?** Check if `dex` command exists (run `which dex` or `dex auth status`). If authenticated, use CLI commands.
3. **Neither?** Guide the user through setup.

### First-Time Setup

**Path A — Platform supports MCP (Claude Desktop, Cursor, VS Code, Gemini CLI, etc.):**

If the user already has the Dex MCP server configured, or their platform can add MCP servers:

```bash
npx -y add-mcp https://mcp.getdex.com/mcp -y
```

This auto-detects installed AI clients and configures the Dex MCP server for all of them. User authenticates via browser on first MCP connection.

**Path B — Install CLI:**

```bash
npm install -g @getdex/cli
```

Works with npm, pnpm, and yarn. No postinstall scripts — the binary is bundled in a platform-specific package.

**Keeping the CLI up to date:**

The CLI auto-generates commands from the MCP server's tool schemas at build time. When tools are added or updated on the server, users need to update the CLI to get the new commands. If a user reports a missing command or parameter, suggest updating:

```bash
npm install -g @getdex/cli@latest
```

**Path C — No Node.js:**

Direct the user to follow the setup guide at **https://getdex.com/docs/ai/mcp-server** — it has client-specific instructions for Claude Desktop, Claude Code, Cursor, VS Code, and other MCP-capable clients.

### Authentication

Triggered by `/dex-login` or on first use when not authenticated. Ask the user which method they prefer:

**Option 1 — API Key:**
1. User generates a key at [Dex Settings > Integrations](https://getdex.com/appv3/settings/api) (requires Professional plan)
2. For CLI: `dex auth --token dex_your_key_here`
3. Key is saved to `~/.dex/api-key` (chmod 600)

**Option 2 — Device Code Flow (works on remote/headless machines):**

Drive this flow directly via HTTP — no browser needed on the machine:

1. Request a device code:
   ```bash
   curl -s -X POST https://mcp.getdex.com/device/code -H "Content-Type: application/json"
   ```
   Response: `{ "device_code": "...", "user_code": "ABCD-EFGH", "verification_uri": "https://...", "expires_in": 600, "interval": 5 }`

2. Show the user the `user_code` and `verification_uri`. They open the URL on any device with a browser, log in to Dex, and enter the code.

3. Poll for approval every 5 seconds:
   ```bash
   curl -s -X POST https://mcp.getdex.com/device/token \
     -H "Content-Type: application/json" \
     -d '{"device_code": "<device_code>"}'
   ```
   - `{"error": "authorization_pending"}` → keep polling
   - `{"api_key": "dex_..."}` → done, save the key

4. Save the API key:
   ```bash
   mkdir -p ~/.dex && echo "<api_key>" > ~/.dex/api-key && chmod 600 ~/.dex/api-key
   ```
   For CLI: `dex auth --token <api_key>`

For CI/automation with no human present, use the API key method with `DEX_API_KEY` environment variable.

## Data Model

```
Contact
├── Emails, Phone Numbers, Social Profiles
├── Company, Job Title, Birthday, Website
├── Description (rich text notes about the person)
├── Tags (flat labels: "Investor", "College Friend")
├── Groups (collections with emoji + description: "🏢 Acme Team")
├── Custom Fields (user-defined: input, dropdown, datepicker)
├── Notes/Timeline (interaction log: meetings, calls, coffees)
├── Reminders (follow-up tasks with optional recurrence)
└── Starred / Archived status
```

## Using Tools

### MCP Mode

Call `dex_*` tools directly. All tools accept and return JSON.

### CLI Mode

Use the `dex` command. CLIHub generates subcommands from MCP tool names (replacing `_` with `-`):

```bash
dex dex-search-contacts --query "John"
dex dex-list-contacts --limit 100
dex dex-create-contact --first-name "Jane" --last-name "Doe"
dex dex-list-tags
dex dex-create-reminder --text "Follow up" --due-at-date "2026-03-15"
```

Use `--output json` for machine-readable output, `--output text` (default) for human-readable.

Run `dex --help` for all commands, or `dex <command> --help` for command-specific help.

See **[CLI Command Reference](references/cli-commands.md)** for the full mapping table of all 38 tools to CLI commands.

## Core Workflows

### 1. Find a Contact

```
search → get details (with notes if needed)
```

- Search by name, email, company, or any keyword
- Use empty query to browse recent contacts (sorted by last interaction)
- Use `dex_list_contacts` for bulk iteration (up to 500 per page, cursor-paginated)
- Include `include_notes: true` when user needs interaction history

### 2. Add a New Contact

```
create contact → (optionally) add to groups → apply tags → set reminder
```

- Create with whatever info is available (no fields are strictly required)
- Immediately organize: add relevant tags and groups
- Set a follow-up reminder if the user just met this person

**Bulk import (CSV, spreadsheet, list):**
```
batch create contacts → add to group → create note for all
```

- Use `dex_create_contact` with the `contacts` array (up to 100 per call) for batch creation
- Use the returned contact IDs to add them all to a group with `dex_add_contacts_to_group`
- Use `dex_create_note` with `contact_ids` to log a shared note across all imported contacts

### 3. Log an Interaction

```
(optional) list note types → create note on contact timeline
```

- Discover note types first with `dex_list_note_types` to pick the right one (Meeting, Call, Coffee, Note, etc.)
- Set `event_time` to when the interaction happened, not when logging it
- Keep notes concise but capture key details, action items, and personal context
- Use `contact_ids` (plural) to link a single note to multiple contacts (e.g. a group meeting)

### 4. Set a Reminder

```
create reminder → (link to contact if applicable)
```

- Always require `due_at_date` (ISO format: "2026-03-15")
- Use `text` for the reminder description — there is no separate title field
- Recurrence options: `weekly`, `biweekly`, `monthly`, `quarterly`, `biannually`, `yearly`

### 5. Organize Contacts

**Tags** — flat labels for cross-cutting categories:
```
create tag → add to contacts (bulk)
```

**Groups** — named collections with emoji and description:
```
create group → add contacts (bulk)
```

Best practice: Use tags for attributes ("Investor", "Engineer", "Met at Conference X") and groups for relationship clusters ("Startup Advisors", "Book Club", "Acme Corp Team").

### 6. Manage Custom Fields

```
list fields → create field definition → batch set values on contacts
```

- Three field types: `input` (free text), `autocomplete` (dropdown with options), `datepicker`
- Use `dex_set_custom_field_values` to set values on multiple contacts at once
- For autocomplete fields, provide `categories` array with the allowed options

### 7. Meeting Prep

When a user says "I have a meeting with X":

1. Search for the contact
2. Get full details with `include_notes: true`
3. Check recent reminders for pending items
4. Summarize: last interaction, key notes, pending follow-ups, shared context
5. See [CRM Workflows](references/crm-workflows.md) for detailed meeting prep guidance

### 8. Merge Duplicates

```
search for potential duplicates → confirm with user → merge
```

- First ID in each group becomes the primary — all other data merges into it
- Always confirm with the user before merging (destructive operation)
- Can merge multiple groups in a single call

## Important Patterns

### Pagination

List operations use cursor-based pagination:
- `dex_list_contacts`: default 100 per page, max 500
- `dex_search_contacts`: default 50 per page, max 200
- Other list tools: default 10 per page
- Check `has_more` in response
- Pass `next_cursor` from previous response to get next page
- Iterate until `has_more: false` to get all results

### Destructive Operations

Always confirm with the user before:
- Deleting contacts (`dex_delete_contacts`)
- Merging contacts (`dex_merge_contacts`)
- Deleting tags, groups, notes, reminders, or custom fields

### Response Truncation

Responses are capped at 25,000 characters. If truncated, the response preserves pagination metadata (`next_cursor`, `has_more`) so you can fetch the next page. Use smaller `limit` values if responses are being truncated.

### Date Formats

- All dates: ISO 8601 strings (e.g., `"2026-03-15"`, `"2026-03-15T14:30:00Z"`)
- Birthdays: `YYYY-MM-DD`
- Reminder due dates: `YYYY-MM-DD`

## Detailed References

- **[Tool Reference](references/tools-reference.md)** — Complete parameter documentation for every tool, with examples
- **[CLI Command Reference](references/cli-commands.md)** — Full MCP tool → CLI command mapping table (only needed for CLI mode)
- **[CRM Workflows](references/crm-workflows.md)** — Relationship management best practices, follow-up cadences, and strategies for being an effective CRM assistant
