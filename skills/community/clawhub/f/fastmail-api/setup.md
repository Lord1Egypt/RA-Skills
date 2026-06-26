# Setup — Fastmail API

Read this silently when `~/fastmail-api/` does not exist or is empty. Start naturally without mentioning setup files.

## Your Attitude

Be exact and calm. Email and calendar automation can affect real communication, so safety and verification come first.

## Priority Order

### Integration Preferences First

Within the first exchanges, clarify activation behavior:
- "Should I jump in whenever you mention Fastmail, JMAP, inbox automation, or mailbox cleanup?"
- "Do you want proactive safety checks before send, move, delete, and identity changes?"
- "Any actions where you want mandatory confirmation every time?"

Save activation preferences in the user's main memory.

### Access and Scope Next

Collect execution context:
- Whether a Fastmail API token already exists
- Preferred scope (mail only, or mail plus contacts and calendar)
- Primary account ID and critical mailboxes
- Preferred default environment and retry behavior

If credentials are incomplete, help the user complete token setup before write actions.

### Operational Baseline Then

Ask what they do most often:
- Inbox triage and mailbox structure changes
- Draft and send automation
- Contact sync and deduplication
- Calendar event creation or updates

Use this baseline to prioritize method templates and safeguards.

## What You're Saving (internally)

In `~/fastmail-api/memory.md`:
- Activation preferences and confirmation policy
- Known account IDs, mailbox IDs, identity IDs, and common targets
- Preferred operation scope and risk boundaries
- Recent failures and reliable recovery patterns

In `~/fastmail-api/request-log.md`:
- Timestamped high-impact operations
- Request intent and result summary
- Rollback notes when partial failures occur
