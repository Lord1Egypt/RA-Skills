---
name: Fastmail API
slug: fastmail-api
version: 1.0.0
homepage: https://clawic.com/skills/fastmail-api
description: Manage Fastmail mail, mailbox, identity, contact, and calendar workflows through JMAP API calls with safe batching and token hygiene.
changelog: Initial release with production-safe Fastmail JMAP API workflows for mail, mailbox, identity, and calendar automation.
metadata: {"clawdbot":{"emoji":"📬","requires":{"bins":["curl","jq"],"env":["FASTMAIL_API_TOKEN"]},"os":["linux","darwin","win32"]}}
---

# Fastmail API Operations

## Setup

On first use, read `setup.md` for account integration preferences, activation rules, and credential handling.

## When to Use

User needs to automate Fastmail through API calls: mailbox management, message search, draft/send flows, identity settings, contact operations, or calendar events. Agent handles capability discovery, safe request construction, and high-impact confirmation.

## Architecture

Memory lives in `~/fastmail-api/`. See `memory-template.md` for structure.

```text
~/fastmail-api/
├── memory.md         # Account context, IDs, and operating preferences
├── request-log.md    # High-impact API actions and outcomes
└── snapshots/        # Optional payload backups before bulk writes
```

## Quick Reference

Use these files when you need details beyond core operating rules.

| Topic | File |
|-------|------|
| Setup flow | `setup.md` |
| Memory template | `memory-template.md` |
| Session and method call patterns | `jmap-patterns.md` |
| Mailbox and message workflows | `mail-workflows.md` |
| Contacts and calendar operations | `calendar-contacts.md` |
| Error handling and recovery | `troubleshooting.md` |

## Requirements

- `curl`
- `jq`
- `FASTMAIL_API_TOKEN`
- Optional: `FASTMAIL_API_BASE` (defaults to `https://api.fastmail.com/jmap/api`)

Never commit bearer tokens to repository files, shell history, or shared logs.

## Data Storage

- `~/fastmail-api/memory.md` for account ID, preferred defaults, and workflow context
- `~/fastmail-api/request-log.md` for high-impact action history
- `~/fastmail-api/snapshots/` for payload backups before bulk updates

## Core Rules

### 1. Discover Session Capabilities Before First Write
- Call the Fastmail JMAP session endpoint first to confirm `apiUrl`, `primaryAccounts`, and capability support.
- Cache discovered account IDs in memory to avoid writing to the wrong account.

```bash
curl -sS https://api.fastmail.com/jmap/session \
  -H "Authorization: Bearer $FASTMAIL_API_TOKEN" | jq
```

### 2. Build Method Calls with Explicit Account Scope
- Include `using` capabilities and account-specific IDs in each method call set.
- Use deterministic `clientCallId` values so retries can be traced safely.

```bash
curl -sS "${FASTMAIL_API_BASE:-https://api.fastmail.com/jmap/api}" \
  -H "Authorization: Bearer $FASTMAIL_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "using": ["urn:ietf:params:jmap:mail", "urn:ietf:params:jmap:core"],
    "methodCalls": [
      ["Mailbox/get", {"accountId": "u123", "ids": null}, "c1"]
    ]
  }' | jq
```

### 3. Use Safe Pagination and Narrow Filters
- Do not run unbounded queries on large inboxes; always set limits and filters.
- Prefer `Email/query` plus `Email/get` windows over full mailbox dumps.

### 4. Confirm Destructive and Broad-Impact Actions
- Confirm before mailbox deletes, message moves affecting many threads, identity updates, or bulk calendar edits.
- For high-impact writes, record pre-change payloads in `~/fastmail-api/snapshots/`.

### 5. Treat Partial Failures as First-Class Results
- Inspect `notCreated`, `notUpdated`, and method-level errors after every write.
- Report partial success explicitly and propose rollback or retry paths.

### 6. Redact Sensitive Data in Outputs
- Never print raw authorization headers or full token strings in normal responses.
- Redact addresses and subject lines when logs are shared outside trusted contexts.

### 7. Verify Post-Write State with Follow-Up Reads
- After writes, run targeted read calls (`Mailbox/get`, `Email/get`, `Contact/get`, `CalendarEvent/get`) to confirm final state.
- Only close tasks after state verification succeeds.

## Safety Checklist

Before bulk updates, deletes, send flows, or identity changes:

1. Confirm target account ID and environment.
2. Capture a request snapshot for rollback context.
3. Confirm user intent for irreversible actions.
4. Execute smallest safe batch first.
5. Verify resulting state with read calls.

## Fastmail API Traps

- Skipping session discovery can send writes to an incorrect account ID.
- Missing capabilities in `using` causes method failures that look like auth issues.
- Bulk message moves without filters can reorganize entire mailboxes accidentally.
- Assuming all writes succeeded without checking `notUpdated` hides partial failure.
- Logging bearer tokens in debugging output creates credential exposure risk.

## External Endpoints

Only the official Fastmail JMAP endpoints below are used by this skill.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://api.fastmail.com/jmap/session` | Bearer token in Authorization header | Discover API URLs, capabilities, and account IDs |
| `https://api.fastmail.com/jmap/api` | JMAP method payloads for mail, mailbox, identity, contacts, and calendar operations | Execute read and write workflows |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Authenticated JMAP payloads for mailbox, message, contact, and calendar operations
- Message metadata required for requested queries and write actions

**Data that stays local:**
- Operational context in `~/fastmail-api/memory.md`
- High-impact action history in `~/fastmail-api/request-log.md`
- Optional payload snapshots in `~/fastmail-api/snapshots/`

**This skill does NOT:**
- Send undeclared API traffic
- Store bearer tokens in repository files
- Execute destructive writes without explicit confirmation

## Trust

By using this skill, mailbox and calendar operation data is sent to Fastmail infrastructure.
Only install if you trust Fastmail with this operational data.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `api` - Build robust HTTP request and response workflows for complex APIs
- `oauth` - Handle token lifecycle and secure delegated authorization flows
- `mail` - Plan high-quality email workflows, tone, and delivery structure
- `webhook` - Orchestrate event-driven integrations that react to API-side changes

## Feedback

- If useful: `clawhub star fastmail-api`
- Stay updated: `clawhub sync`
