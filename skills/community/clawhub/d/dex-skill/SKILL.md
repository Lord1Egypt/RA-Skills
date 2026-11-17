---
name: dex-skill
description: >
  Manage your Dex personal CRM — search, filter, create, archive, and update contacts; log notes;
  manage follow-ups, tags, groups, and custom fields; search connected email; and read or manage
  connected calendars.
  Use this skill to: (1) Find, add, or update contacts, (2) Log meetings and notes,
  (3) Manage reminders and keep-in-touch cadence, (4) Organize tags, groups, and custom fields,
  (5) Merge or archive contacts, (6) Review relationships or prepare meetings,
  (7) Search correspondence, (8) Manage calendar events, (9) Categorize, audit, or clean a network,
  (10) Turn notetaker output or transcripts into notes and follow-ups,
  (11) Prepare multiple meetings or event follow-up, (12) Research a contact on the public web,
  (13) See what is coming up — upcoming birthdays, due reminders, and who to reach out to,
  (14) Authenticate via /dex-login,
  or handle another personal CRM task involving the user's professional network.
metadata:
  version: '2.4.2'
  openclaw:
    emoji: "\U0001F91D"
    homepage: https://getdex.com
    skillKey: 'dex-skill'
    requires:
      bins: ['dex']
    install:
      - id: 'npm'
        kind: 'node'
        package: '@getdex/cli'
        bins: ['dex']
        label: 'Install Dex CLI (npm)'
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

Triggered by `/dex-login` or on first use when not authenticated. Prefer MCP browser OAuth when available, then device code for an interactive CLI session, and API keys for CI or when the user explicitly chooses one.

**Do not trust `dex auth status` alone.** Status is green if any credential file exists. Verify with a real command such as `dex dex-list-tags`. A `401 unauthorized` after a "successful" login almost always means the CLI is still reading a stale token.

**Where credentials actually live:**

- `@getdex/cli` reads `~/.clihub/credentials.json` (`auth_type: bearer_token`, `token: dex_…`).
- Some docs and older agents only write `~/.dex/api-key`. That file is **not** what the CLI sends on MCP calls.
- After device-code or API-key setup, write **both** files, or the next `dex …` call will 401.

**Cloudflare:** every request to `mcp.getdex.com` must send `User-Agent: dex-cli`. Bare `curl` with no UA returns Cloudflare **1010** (`browser_signature_banned`). That is not an expired code and not a Dex 401.

Never ask the user to paste an API key into chat. Do not print, log, commit, or include it in tool arguments that will be shown back to the user. `dex auth --token <key>` puts the secret on the process argv — do not run that from an agent.

**Option 1 — API Key:**

1. User generates a key at [Dex Settings > Integrations](https://getdex.com/appv3/settings/api) (requires Professional plan)
2. Ask the user to save it in their own terminal, or write both files below from a local script that never prints the value
3. Destinations: `~/.dex/api-key` (chmod 600) **and** `~/.clihub/credentials.json` (chmod 600)

**Option 2 — Device Code Flow (works on remote/headless machines):**

Drive this flow directly via HTTP — no browser needed on the machine. Always send `User-Agent: dex-cli`.

1. Request a device code:

   ```bash
   curl -s -X POST https://mcp.getdex.com/device/code \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -H "User-Agent: dex-cli"
   ```

   Response: `{ "device_code": "...", "user_code": "ABCD-EFGH", "verification_uri": "https://...", "expires_in": 600, "interval": 5 }`

2. Show the user the `user_code` and `verification_uri`. They open the URL on any device with a browser, log in to Dex, and enter the code.

3. Poll for approval every 5 seconds without logging the successful response:

   ```bash
   curl -s -X POST https://mcp.getdex.com/device/token \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -H "User-Agent: dex-cli" \
     -d '{"device_code": "<device_code>"}'
   ```

   - HTTP 200 + `{"error": "authorization_pending"}` → keep polling (this is **not** success)
   - HTTP 429 + `{"error": "slow_down"}` → wait longer than `interval`
   - HTTP 400 + `{"error": "expired_token"}` → request a new device code
   - HTTP 403 Cloudflare 1010 → add `User-Agent: dex-cli` and start over
   - HTTP 200 + `api_key` → stop polling. Do not print the body.

4. Save the key to **both** locations without printing it:

   ```bash
   install -d -m 700 ~/.dex ~/.clihub
   umask 077
   ```

   - `~/.dex/api-key` — raw `dex_…` bytes, mode `600`, no trailing commentary
   - `~/.clihub/credentials.json` — mode `600`, this schema (CLI source of truth):

   ```json
   {
     "version": 2,
     "servers": {
       "https://mcp.getdex.com/mcp": {
         "type": "bearer",
         "auth_type": "bearer_token",
         "token": "<api_key>"
       }
     }
   }
   ```

   If the execution surface cannot keep the successful `/device/token` response out of chat or tool logs, stop and ask the user to finish in their own terminal.

5. Verify with `dex dex-list-tags` (or another read). If that 401s, `~/.clihub/credentials.json` was not updated.

There is no `dex auth login` subcommand in current `@getdex/cli` (1.0.x) even if some READMEs mention it. Use this HTTP device flow.

For CI/automation with no human present, use the API key method with `DEX_API_KEY` environment variable **and** the credentials file above.

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

See **[CLI Command Reference](references/cli-commands.md)** for the full mapping table of all 53 tools to CLI commands.

## Core Workflows

### 1. Find a Contact

```
choose search/filter/list → get details (with notes if needed)
```

- Use `dex_search_contacts` for keywords or real geographic proximity with `near` and optional `radius_km`
- When using `near`, keep `query` for an additional non-location filter; do not repeat the place in both fields
- Use `dex_filter_contacts` for structured AND filters such as tags, groups, company, profile presence, dates, archived state, and custom fields
- Use `dex_list_contacts` for unfiltered bulk iteration (up to 500 per page, cursor-paginated)
- Use an empty search query to browse a single batch of contacts sorted by most recent interaction
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

### 4. Manage Follow-Ups

```
set cadence or create reminder → complete/snooze when due
```

- Use `dex_update_contact.keep_in_touch` for relationship cadence; use a reminder for a specific task
- Always require `due_at_date` (ISO format: "2026-03-15")
- Use `text` for the reminder description — there is no separate title field
- Recurrence options: `weekly`, `biweekly`, `monthly`, `quarterly`, `biannually`, `yearly`
- Use `dex_complete_keep_in_touch` without `snooze_days` after a real interaction; use `snooze_days` to defer without recording a touch

**"What's coming up?"** — for any question about the near future ("whose birthday is next week?", "who should I reach out to this week?", "what do I have coming up?"), call `dex_list_upcoming_reminders_and_birthdays` rather than stitching several lists together. One call returns birthdays, open reminders and keep-in-touch contacts for a window (default 7 days, `days: 30` for a month).

- It reports `turning_age` ONLY when the birth year is known. A birthday with no year returns neither `birthday_year` nor `turning_age` — say the date, never a guessed age
- Its `keep_in_touch` list DOES include people already overdue (`is_overdue: true`); its `reminders` list does NOT include overdue reminders — get those from `dex_list_reminders` with `is_overdue: true`
- On a wide window, check `reminders_truncated` / `keep_in_touch_truncated` before telling the user that is everything

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
4. Optionally search relevant email correspondence and fetch the calendar event when the user asks for live context
5. Check `dex_get_contact_research` for a stored web research note; offer `dex_research_contacts` (paid, slow) when there is none and the user wants public background
6. Summarize: last interaction, key notes, pending follow-ups, shared context, attendees, recent correspondence, and cited web findings
7. See [CRM Workflows](references/crm-workflows.md) for detailed meeting prep guidance

### 8. Manage Calendar Events

- Use `dex_list_calendar_events` for a time window or plain-text event search across all connected Google/Microsoft accounts
- Reuse an event's returned `email` as `account_email` for get/update/delete
- For get/create/update/delete, also pass `account_provider` when the same address is connected to both providers
- For timed events, provide both `start_datetime` and `end_datetime` with explicit offsets; include an IANA `timezone`
- For all-day events, provide `start_date`; `end_date` is exclusive and defaults to the next day
- Confirm before creation when attendees may receive invitations
- On update, `attendees` replaces the whole list; fetch the event first and include everyone who should remain
- A recurring series ID updates the whole series; state that scope before confirmation
- For calendar create/update, generate `idempotency_key` before the first attempt and reuse it with identical arguments only to retry that operation within 24 hours. Every new edit or intended new event needs a new key. Without one, update executes again; create deduplicates identical content for 24 hours, so use a new key when recreating a deleted event or intentionally creating another identical event. This does NOT generalise: `dex_create_contact`, `dex_create_group`, `dex_create_tag` and `dex_create_custom_field` carry a fresh key per call, so a retry of those duplicates. `dex_create_note` and `dex_create_reminder` are safe to retry only when you pass your own `idempotency_key` — reuse the SAME key and the same arguments, within the server's 24-hour window, and the original row comes back instead of a duplicate. **`dex_create_note` additionally requires an explicit `event_time` whenever `idempotency_key` is present** (it is rejected otherwise), because a defaulted "now" would differ on every attempt and defeat the replay. Set `event_time` yourself when you intend to retry.

An update cannot move an event between connected accounts. To transfer one, fetch the original, confirm creating a replacement on the target account, then separately confirm deleting the original. Preserve the full attendee list and details, and warn that organizer identity, RSVP state, conferencing data, and provider notifications may change.

If a calendar list returns `warnings`, describe the results as incomplete; do not infer availability from the missing accounts. If all calendars fail, report the error rather than saying there are no meetings.

If a calendar write fails for missing provider scope, direct the user to **Settings → Sync & Integrations → Grant calendar access** for that account.

### 9. Search Correspondence

- Use `dex_search_emails` for live, read-only search across all connected Google/Microsoft mailboxes
- To list recent mail, omit `query`; use `folder: 'inbox'` for received mail. Follow `next_cursor` while keeping the same folder and date bounds
- Use plain keywords such as a name, company, domain, or topic; provider operators such as `from:` and `to:` are neutralized
- Set `after` and `before` for precise date ranges; otherwise the search covers roughly the last six months
- Results contain metadata, snippets, and provider links, not full bodies
- Dex cannot send email; do not imply that this tool drafts or sends messages

### 10. Research a Contact on the Web

- `dex_get_contact_research` reads the stored note for up to 10 contacts at no cost — check it first
- `dex_research_contacts` runs Dex Research for up to 5 contacts per call: a paid web search + page extraction + LLM summary that takes a minute or more per contact. Confirm with the user before running it on more than a couple of contacts
- Notes under 30 days old are served from cache; pass `force: true` only when the user explicitly wants a fresh run
- A fresh run replaces the stored research note and its finding statuses. Preserving existing contact fields does not preserve the previous research note; explain that replacement before forcing a rerun
- Quote findings with their citations (`[[n]]` markers resolve into `sources`) and mention `identity_confidence` when it is not `high`
- A run fills empty `linkedin` / `website` fields itself **only from high-confidence findings**, reported in `applied`; it never overwrites an existing value. A lower-confidence `linkedin`/`website` finding comes back `pending`, exactly like every email and phone finding — check each row's `status` rather than assuming a field was filled. Anything `pending` needs the user's confirmation, then `dex_update_contact` to apply it
- `in_progress` means another request is already researching that contact: read it back later instead of running again

### 11. Archive, Delete, or Merge

Prefer reversible cleanup:

1. Use `dex_archive_contacts` for contacts the user may want later
2. Find archived contacts with `dex_filter_contacts` and `archived_only: true`
3. Restore them with `dex_archive_contacts` and `archived: false`

For duplicates:

```
search for potential duplicates → confirm with user → merge
```

- Dex chooses the oldest record in each group as the survivor, regardless of input order
- Read `mergedContactIds` from the response to learn which ID survived
- Always confirm with the user before merging (destructive operation)
- Can merge multiple groups in a single call

### 12. Handle Outcome-Oriented Requests

For multi-contact or multi-step requests, follow this reusable contract:

```
define scope → inspect current state → preview proposed outcome → confirm writes → execute → verify
```

- Treat requests to analyze, recommend, audit, or prepare as read-only unless the user also asks for changes
- When the user says “all,” paginate the complete relevant dataset and state whether the scope includes active contacts, archived contacts, or both
- Reuse existing tags, groups, custom fields, contacts, and recent notes before creating anything
- Separate high-confidence actions from ambiguous records that need review
- Present exact additions, updates, removals, archives, merges, notes, and reminders before bulk writes
- Verify changed records with fresh reads and report successes, skips, and failures

Load [CRM Workflows](references/crm-workflows.md) for detailed playbooks when the user asks to:

- Categorize or reorganize their whole network
- Turn a notetaker summary or transcript into notes, contact updates, and reminders
- Audit or clean up CRM data
- Import and follow up with people from an event or roster
- Review relationship health or plan outreach
- Prepare a day or week of meetings
- Build a target contact list from several criteria

## Important Patterns

### Privacy and Data Minimization

- Retrieve only the fields and history needed for the request; leave `include_notes` and `include_contacts` off unless relationship context is necessary
- Treat contact methods, notes, email snippets, attendee lists, and provider links as private relationship data
- Summarize relevant context instead of repeating unnecessary personal details
- Never share or transmit Dex data to another service without an explicit user request
- Do not claim access to full email bodies when `dex_search_emails` returns only metadata and snippets
- Present web research as cited public information, not as facts Dex verified; surface `identity_confidence` when the note may describe a different person

### Pagination

Only responses with `has_more` and `next_cursor` use cursor pagination:

- `dex_list_contacts`: default 100 per page, max 500
- `dex_filter_contacts`: default 50 per page, max 200
- Tag, group-contact, note, and reminder lists: default 10 per page
- Check `has_more` in response
- Pass `next_cursor` as `cursor` while preserving the original filters, sort order, and optional includes
- Iterate until `has_more: false` to get all results

`dex_search_emails` listings (without `query`) also paginate, with default 25 and maximum 100 messages per page. Searches with `query` are a single page and reject `cursor`.

`dex_search_contacts` and `dex_list_calendar_events` return a bounded single batch, not a cursor. Narrow the query or date range when necessary.

### Destructive Operations

Respect MCP host confirmations. In CLI mode, explicitly summarize the target and consequence before any operation that deletes, overwrites, removes relationships, archives, completes cadence state, changes external calendar state, or may send invitations.

High-risk examples:

- Contact deletion, merge, and bulk archive
- Any update that overwrites saved fields or replaces a collection
- Removing tags or group memberships
- Completing/snoozing keep-in-touch state
- Deleting groups, tags, notes, reminders, or custom fields
- Setting custom field values in bulk
- Creating, updating, or deleting calendar events
- Running paid web research (`dex_research_contacts`) on more than a couple of contacts, or with `force: true`

Before a destructive call, resolve names to current IDs, read the current record when overwriting a collection, show the intended delta, and never guess ambiguous targets.

For contact cleanup, do not define “stale” from inactivity alone. Review open reminders and active relationship signals, present exact archive/retain lists, and require approval before archiving or changing cadence. Date filters exclude contacts with no recorded interaction, so review those separately when they matter.

### Response Truncation

Responses are capped at 25,000 characters. Cursor-based tools preserve `next_cursor` and `has_more`; continue with a smaller page. For single-batch search, calendar, and email tools, reduce `limit` or narrow the query/date range.

### Date Formats

- All dates: ISO 8601 strings (e.g., `"2026-03-15"`, `"2026-03-15T14:30:00Z"`)
- Birthdays: `YYYY-MM-DD` when the year is known, or `--MM-DD` when only the month and day are. Dex stores the year in a separate column, so a birthday that reads back as `--MM-DD` means the year was never recorded — do not substitute the current year, and do not report one.
- Reminder due dates: `YYYY-MM-DD`
- Calendar timed events: ISO 8601 with an explicit UTC offset plus an IANA timezone
- Calendar all-day `end_date`: exclusive

## Detailed References

- **[Tool Reference](references/tools-reference.md)** — Complete parameter documentation for every tool, with examples
- **[CLI Command Reference](references/cli-commands.md)** — Full MCP tool → CLI command mapping table (only needed for CLI mode)
- **[CRM Workflows](references/crm-workflows.md)** — Relationship management best practices, follow-up cadences, and strategies for being an effective CRM assistant
