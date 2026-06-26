---
name: Clay
description: Search, manage, and organize your contact network via the Clay CLI.
homepage: https://clay.earth
metadata:
  {
    "openclaw":
      {
        "emoji": "🕸️",
        "os": ["darwin", "linux"],
        "requires": { "bins": ["clay"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@clayhq/clay-cli",
              "bins": ["clay"],
              "label": "Install clay (npm)",
            },
          ],
      },
  }
---

# Clay

Use `clay` to search, create, update, and manage your personal contact network from the command line.

## Requirements

- A Clay account ([clay.earth](https://clay.earth))
- Authenticate before using any commands: `clay login`

## Authentication

Log in (opens browser for OAuth):

```bash
clay login
```

Check authentication status:

```bash
clay status
```

Log out:

```bash
clay logout
```

Credentials are stored in `~/.config/clay.json`.

## Output Formats

All data commands support `--format` to control output:

- `json` (default) — Pretty-printed JSON
- `csv` — Comma-separated values
- `tsv` — Tab-separated values

```bash
clay contacts:search --name "Alice" --format csv
clay emails:recent --format tsv
```

## Contacts

Get a contact by ID:

```bash
clay contact --contact-id 12345
```

Search contacts:

```bash
clay contacts:search --name "Jane Smith"
clay contacts:search --work-history-company "Acme" --work-history-active true
clay contacts:search --education-history-school "MIT"
clay contacts:search --location-latitude 37.7749 --location-longitude -122.4194 --location-distance 50
clay contacts:search --last-email-date-gte "2025-01-01" --sort-field "last_email_date" --sort-direction "desc"
clay contacts:search --group-ids "starred" --limit 10
clay contacts:search --keywords "investor" --include-fields "name,email,title"
```

Create a contact:

```bash
clay contacts:create --first-name "Jane" --last-name "Doe" --email "jane@example.com"
clay contacts:create --first-name "Bob" --title "CEO" --organization "Acme Inc" --birthday "1990-05-15"
```

Update a contact:

```bash
clay contacts:update --contact-id 12345 --title "CTO" --organization "NewCo"
clay contacts:update --contact-id 12345 --email "new@example.com" --phone "+1234567890"
```

Archive / restore contacts:

```bash
clay contacts:archive --contact-ids 12345
clay contacts:restore --contact-ids 12345
```

Merge duplicate contacts:

```bash
clay contacts:merge --contact-ids 12345 --contact-ids 67890
```

## Notes

List notes in a date range:

```bash
clay notes --start "2025-01-01" --end "2025-12-31"
clay notes --contact-ids 12345
```

Create a note on a contact:

```bash
clay notes:create --contact-id 12345 --content "Met at the conference, very interested in partnerships."
clay notes:create --contact-id 12345 --content "Follow up next week" --reminder-date "2026-03-01T09:00:00Z"
```

Notes support contact references in content: `[contact:123:John Doe]`.

## Groups

List all groups:

```bash
clay groups
clay groups --limit 50
```

Create a group:

```bash
clay groups:create --title "Investors"
```

Update a group (rename, add/remove members):

```bash
clay groups:update --group-id 42 --title "Angel Investors"
clay groups:update --group-id 42 --add-contact-ids 12345 --add-contact-ids 67890
clay groups:update --group-id 42 --remove-contact-ids 11111
```

## Events

List events in a date range:

```bash
clay events --start "2025-01-01" --end "2025-03-01"
clay events --contact-ids 12345
```

List upcoming events:

```bash
clay events:upcoming
clay events:upcoming --limit 20 --page 2
```

## Emails

List emails in a date range:

```bash
clay emails --start "2025-01-01" --end "2025-02-01"
clay emails --contact-ids 12345
```

List recent emails:

```bash
clay emails:recent
clay emails:recent --limit 25 --contact-ids 12345
```

## Reminders

List recent reminders:

```bash
clay reminders:recent
clay reminders:recent --limit 5
```

List upcoming reminders:

```bash
clay reminders:upcoming
clay reminders:upcoming --limit 20 --page 2
```

## Search Options Reference

The `contacts:search` command supports filters for:

- **Name**: `--name`
- **Work**: `--work-history-company`, `--work-history-position`, `--work-history-active`
- **Education**: `--education-history-school`, `--education-history-degree`, `--education-history-active`
- **Location**: `--location-latitude`, `--location-longitude`, `--location-distance`
- **Age**: `--age-gte`, `--age-lte`
- **Birthday**: `--upcoming-birthday-gte/lte`, `--previous-birthday-gte/lte`
- **Contact info**: `--information-type` (filter by type of info available)
- **Interaction dates**: `--first-email-date-gte/lte`, `--last-email-date-gte/lte`, `--first-event-date-gte/lte`, `--last-event-date-gte/lte`, `--first-text-message-date-gte/lte`, `--last-text-message-date-gte/lte`, `--first-interaction-date-gte/lte`, `--last-interaction-date-gte/lte`
- **Interaction counts**: `--email-count-gte/lte`, `--event-count-gte/lte`, `--text-message-count-gte/lte`
- **Notes**: `--note-content`, `--note-date-gte/lte`
- **Groups**: `--group-ids` (group ID or `"starred"`)
- **Integration**: `--integration`
- **Sorting**: `--sort-field`, `--sort-direction`
- **Pagination**: `--limit`, `--exclude-contact-ids`
- **Fields**: `--include-fields` (select which fields to return)
