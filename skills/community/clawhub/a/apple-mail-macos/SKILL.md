---
name: Apple Mail (MacOS)
slug: apple-mail-macos
version: 1.0.0
homepage: https://clawic.com/skills/apple-mail-macos
description: Use local CLI to manage Gmail, Outlook, iCloud, Yahoo, Fastmail, and other mail accounts synced in Apple Mail on macOS, without APIs or OAuth.
changelog: Initial release with deterministic Apple Mail command paths, provider-aware operations, and safety gates for send and delete actions.
metadata: {"clawdbot":{"emoji":"✉️","requires":{"bins":[],"anyBins":["osascript","shortcuts","sqlite3"],"config":["~/apple-mail-macos/"]},"os":["darwin"],"configPaths":["~/apple-mail-macos/"]}}
---

## Setup

On first use, follow `setup.md` to define provider scope, command path preferences, and safety defaults before any write action.

## When to Use

User wants to control Apple Mail from CLI while keeping account sync managed by Mail.app.
Agent handles read, search, triage, draft, send, move, archive, and delete workflows across accounts already connected in Apple Mail.

## Requirements

- macOS with Mail.app account access enabled for terminal automation.
- At least one working command path: `osascript`, `shortcuts`, or `sqlite3` read-only for indexed lookup.
- Provider accounts already connected in Mail.app (Gmail, Outlook, iCloud, Yahoo, Fastmail, and Proton via Bridge if used).
- Explicit confirmation before sending, deleting, or bulk actions.

## Architecture

Memory lives in `~/apple-mail-macos/`. See `memory-template.md` for structure.

```text
~/apple-mail-macos/
├── memory.md               # Status, provider map, safety defaults
├── command-paths.md        # Working command path and fallback notes
├── provider-coverage.md    # Provider-specific behavior and caveats
├── safety-log.md           # Send/delete confirmations and rollback notes
└── operation-log.md        # Operation IDs, verification evidence, outcomes
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup and first-run behavior | `setup.md` |
| Memory structure | `memory-template.md` |
| Command hierarchy and probes | `command-paths.md` |
| Provider behavior matrix | `provider-coverage.md` |
| Safety checklist before writes | `safety-checklist.md` |
| Deterministic operation patterns | `operation-patterns.md` |
| Failure handling and recovery | `troubleshooting.md` |

## Data Storage

All skill files are stored in `~/apple-mail-macos/`.
Before creating or changing local files, describe the planned write and ask for confirmation.

## Core Rules

### 1. Treat Mail.app as the Unified Account Layer
- Assume provider sync is already configured in Apple Mail and operate on that local unified mailbox layer.
- Do not request direct provider OAuth inside this skill unless user explicitly asks for setup help.

### 2. Detect Command Path Before Every Operation
- Probe command paths in strict order: `osascript`, then `shortcuts`, then `sqlite3` for read-only indexed lookup.
- If no safe path is available, stop and report the exact blocker instead of guessing.

### 3. Default to Dry-Run for Write Intents
- For compose, reply, move, archive, and delete workflows, first produce a dry-run preview with impacted messages and fields.
- Do not execute live changes until user confirms the dry-run summary.

### 4. Enforce High-Risk Confirmation Gates
- Require explicit confirmation for send, delete, bulk move, bulk archive, forwarding, and reply-all expansions.
- If external recipients are added or recipient count changes, require a second confirmation.

### 5. Use Operation IDs and Idempotency
- Generate a unique operation ID for every write workflow and include it in local operation logs.
- Before send, verify there is no prior successful send with the same operation context.

### 6. Read First, Write Once, Verify Immediately
- Resolve message identity with at least two fields (message ID plus sender or date) before any write action.
- After every write, run read-back verification and report final mailbox state.

### 7. Keep Exposure Minimal and Local-First
- Use only required fields for the requested task and avoid broad mailbox exports by default.
- Never send message bodies or attachments to undeclared external endpoints.

## Common Traps

- Sending from draft without final recipient review -> wrong recipient incidents.
- Matching threads by subject only -> replies sent in the wrong conversation.
- Bulk archive or delete without dry-run count -> accidental data loss.
- Assuming provider folder names are identical -> move failures or misplaced messages.
- Skipping read-back verification -> false success reports.

## Security & Privacy

**Data that stays local:**
- Operational context and defaults in `~/apple-mail-macos/`.
- Message metadata needed to execute the requested task.

**Data that may leave your machine:**
- Email content only when user confirms a send, reply, or forward through already configured provider accounts.

**This skill does NOT:**
- Send mail without explicit user confirmation.
- Execute destructive mailbox actions without dry-run and confirmation gates.
- Request undeclared API keys or call undeclared third-party APIs.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `macos` - macOS command workflows and system automation patterns.
- `mail` - cross-platform mailbox handling patterns and protocol references.
- `events` - event extraction and action-item framing from communications.
- `schedule` - scheduling workflows linked to message-driven tasks.
- `productivity` - execution and prioritization frameworks for daily work.

## Feedback

- If useful: `clawhub star apple-mail-macos`
- Stay updated: `clawhub sync`
