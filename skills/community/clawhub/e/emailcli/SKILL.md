---
name: emailcli
description: Use the emailcli CLI to read, search, send, and manage emails. Use whenever the user wants to interact with their email inbox, send emails, search for messages, or manage email organization. Commands like "check my inbox", "send an email", "search for X", "delete spam", "mark as read" should always use this skill. The skill handles the full workflow: composing correct commands, parsing JSON output, handling errors, and presenting results clearly.
---

# emailcli Skill

Use this skill whenever you need to interact with the user's email using the `mail-cli` command-line client.

## Quick Reference

```bash
# Installation (if needed)
npm install -g @laffy1309/emailcli

# Commands
mail-cli list [--folder FOLDER] [--limit N] [--account EMAIL:PROVIDER]
mail-cli read <message-id> [--thread] [--download [dir]]
mail-cli search "<query>" [--account EMAIL:PROVIDER]
mail-cli send --to <addr> --subject "<subj>" --body "<text>" [--cc <addr>] [--bcc <addr>] [--attach <file>] [--save-draft] [--draft <id>]
mail-cli reply <message-id> --to <addr> [--cc <addr>]
mail-cli mark <message-id> --read|--unread
mail-cli mark --ids 1,2,3 --read|--unread  # Batch
mail-cli move <message-id> --folder "<folder>"
mail-cli move --ids 1,2,3 --folder "<folder>"  # Batch
mail-cli delete <message-id>
mail-cli delete --ids 1,2,3  # Batch
mail-cli folders [--account EMAIL:PROVIDER]
mail-cli status
mail-cli drafts --list|--delete <id>
mail-cli account list|add --provider gmail|outlook|remove --account EMAIL:PROVIDER|--all
```

## Account Format

All accounts use `email:provider` format:
- Gmail: `me@gmail.com:gmail`
- Outlook: `me@outlook.com:outlook`

When multiple accounts exist, use `--account EMAIL:PROVIDER` to specify which one.
If no account is specified, the CLI uses `default:gmail` internally.

## JSON Output

All commands return JSON. Parse output programmatically:

**Success:**
```json
{"ok": true}
{"id": "abc123", "from": "sender@example.com", "subject": "Hello", "date": "2024-01-01T00:00:00Z"}
[{"id": "1", "from": "a@example.com"}, {"id": "2", "from": "b@example.com"}]
{"id": "...", "saved": true}   // --save-draft output
{"removed": ["a@g.com:gmail", "b@outlook.com:outlook"]}  // account remove --all
```

**Error:**
```json
{"error": {"code": "NO_ACCOUNTS", "message": "No accounts configured. Run 'mail-cli account add --provider gmail' first."}}
{"error": {"code": "DRAFT_NOT_FOUND", "message": "Draft with ID 'xxx' not found"}}
{"error": {"code": "MISSING_FLAG", "message": "Either --account <id> or --all is required"}}
```

**Batch partial failure:**
```json
{"ok": true, "failed": [{"id": "2", "error": {"code": "NOT_FOUND", "message": "Email not found"}}]}
```

## Command Patterns

### Listing Emails
```bash
# Default: 20 most recent inbox emails
mail-cli list

# Specific folder (Gmail uses brackets)
mail-cli list --folder "[Gmail]/Sent"

# Limit results
mail-cli list --limit 50

# Specific account
mail-cli list --account me@gmail.com:gmail
```

### Reading Email
```bash
# Single email by ID (get ID from list output)
mail-cli read abc123

# Full thread
mail-cli read thread-456 --thread

# Read and download attachments to current directory
mail-cli read abc123 --download

# Read and download attachments to specific directory
mail-cli read abc123 --download ./attachments
```

### Searching
```bash
# Gmail search syntax
mail-cli search "from:foo subject:bar has:attachment"

# Outlook KQL syntax
mail-cli search "from:foo subject:bar"
```

### Sending Email
```bash
# Basic send
mail-cli send --to recipient@example.com --subject "Hello" --body "Message"

# With CC/BCC
mail-cli send --to recipient@example.com --cc other@example.com --bcc hidden@example.com --subject "Hello" --body "Message"

# From file
mail-cli send --to recipient@example.com --subject "Hello" --body-file-path message.txt

# With attachment
mail-cli send --to recipient@example.com --subject "Hello" --body "Message" --attach file.pdf

# Save as draft (don't send)
mail-cli send --to recipient@example.com --subject "Hello" --body "Message" --save-draft

# Load and send existing draft
mail-cli send --draft draft-id-123 --subject "Updated Subject"
```

### Replying
```bash
mail-cli reply <message-id> --to sender@example.com
mail-cli reply <message-id> --to sender@example.com --cc other@example.com
```

### Marking
```bash
# Single
mail-cli mark abc123 --read
mail-cli mark abc123 --unread

# Batch - comma-separated IDs (no spaces)
mail-cli mark --ids 1,2,3 --read
```

### Moving
```bash
# Single
mail-cli move abc123 --folder "[Gmail]/Trash"

# Batch
mail-cli move --ids 1,2,3 --folder "[Gmail]/Archive"
```

### Deleting
```bash
# Single (moves to trash)
mail-cli delete abc123

# Batch
mail-cli delete --ids 1,2,3
```

### Folder Operations
```bash
# List all folders
mail-cli folders

# Mailbox status (message counts)
mail-cli status
```

### Drafts
```bash
# List all saved drafts
mail-cli drafts --list

# Delete a draft by ID
mail-cli drafts --delete draft-id-123
```

### Account Management
```bash
# Add account
mail-cli account add --provider gmail
mail-cli account add --provider outlook

# List accounts
mail-cli account list

# Remove specific account
mail-cli account remove --account me@gmail.com:gmail

# Remove ALL accounts
mail-cli account remove --all
```

## Workflows

### Check Inbox
1. Run `mail-cli list` to get recent emails
2. Parse JSON output - each email has `id`, `from`, `subject`, `date`
3. Present summary to user
4. User can request specific email by ID

### Send Email
1. Collect: recipient, subject, body (and optionally CC, attachments)
2. Compose command with proper escaping
3. Execute and check for `{"ok": true}` or error
4. Report success or error message

### Save Draft
1. Compose the email without sending
2. Use `--save-draft` instead of sending
3. The output `{"id": "...", "saved": true}` contains the draft ID for later use

### Load and Edit Draft
1. List drafts with `mail-cli drafts --list`
2. Load a draft with `mail-cli send --draft <id>`
3. Override any fields with command-line flags (CLI takes precedence over draft data)
4. Draft is automatically deleted after successful send

### Search and Act
1. Run `mail-cli search` with appropriate query syntax
2. Present results
3. User can then mark, move, delete by ID

### Batch Operations
1. Get list of IDs (from list or search results)
2. Use `--ids 1,2,3` format (comma-separated, no spaces)
3. Check response for `failed` array to identify partial failures

### Download Attachments
1. When reading an email, add `--download` or `--download <dir>`
2. Attachments are saved to the specified directory (or current directory)
3. Output includes `downloads` array with filename, path, and size for each attachment

## Error Handling

If you receive an error response:
1. Extract `error.code` and `error.message`
2. Present the issue clearly to the user
3. Suggest remediation if applicable:
   - `NO_ACCOUNTS`: Run `mail-cli account add --provider gmail|outlook`
   - `NOT_FOUND`: The message ID doesn't exist or was already deleted
   - `INVALID_CREDENTIALS`: Re-authenticate with `mail-cli account remove` then `mail-cli account add`
   - `DRAFT_NOT_FOUND`: The draft ID doesn't exist or was already sent/deleted
   - `MISSING_FLAG`: Required flag missing (e.g., `--account` or `--all` for `account remove`)
   - `CONFLICTING_FLAGS`: Cannot use both `--account` and `--all` together

## Important Notes

- Always use JSON output parsing - the CLI only outputs JSON
- Gmail folders use brackets: `[Gmail]/Sent`, `[Gmail]/Trash`, `[Gmail]/Archive`
- Message IDs from list/search are strings, preserve them exactly
- Batch IDs must be comma-separated with no spaces: `--ids 1,2,3`
- Reply requires both the message ID and `--to` with the recipient address
- Without `--account`, commands default to using the first available account
- Drafts are stored locally and persist across sessions
- `--save-draft` and `--draft` are mutually exclusive in the same command
