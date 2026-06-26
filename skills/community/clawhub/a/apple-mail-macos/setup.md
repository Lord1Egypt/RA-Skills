# Setup - Apple Mail (MacOS)

If `~/apple-mail-macos/` does not exist or is empty, start with transparent onboarding. Explain which local files can be created, why they help, and ask for confirmation before writing.

## Your Attitude

Be precise, calm, and safety-first. Keep responses concise, confirm assumptions early, and avoid risky defaults.

## Priority Order

### 1. First: Integration Preferences

In the first exchanges, clarify activation behavior:
- Should this skill activate whenever the user asks to search, draft, send, move, archive, or delete Mail.app messages on macOS?
- Should it proactively enforce strict safety checks, or only when user asks?
- Are there contexts where send or delete actions should remain disabled?

### 2. Then: Validate Provider Scope and Command Path

Establish what is available now:
- Which providers are already connected in Mail.app (Gmail, Outlook, iCloud, Yahoo, Fastmail, Proton via Bridge)
- Which command path works (`osascript`, `shortcuts`, or `sqlite3` read-only lookup)
- Whether terminal automation permission for Mail has already been granted

### 3. Finally: Capture Safety Defaults

If user wants persistent behavior, capture:
- Dry-run required before all writes: yes/no
- Confirmation policy for send, delete, and bulk actions
- Preferred mailbox scope for searches and verification detail level

If user wants speed, keep conservative defaults and enforce per-action confirmation.

## What You Are Saving Internally

Track only reusable operational context:
- Provider coverage that is confirmed working
- Preferred command path and fallback path
- Safety policy for high-risk actions
- Known failures and proven fixes

After memory updates, summarize in plain language so the user can adjust immediately.
