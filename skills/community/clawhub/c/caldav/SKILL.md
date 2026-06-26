---
name: CalDAV
slug: caldav
version: 1.0.0
homepage: https://clawic.com/skills/caldav
description: Sync, inspect, and modify CalDAV calendars with vdirsyncer and khal using deterministic windows, verified writes, and recurrence-aware workflows.
changelog: Initial release with safer CalDAV operating rules for vdirsyncer and khal, including sync discipline, edit verification, and conflict-aware workflows.
metadata: {"clawdbot":{"emoji":"📅","requires":{"bins":["vdirsyncer","khal"]},"os":["linux","darwin"]}}
---

## When to Use

Use when the user needs to work with CalDAV calendars through a local `vdirsyncer` + `khal` stack, especially for iCloud, Fastmail, Nextcloud, DAViCal, Radicale, or other standards-based calendar servers.

This skill is for local-first querying, event creation, safe edits, troubleshooting stale sync state, and handling ambiguous matches without corrupting recurring events or overwriting the wrong calendar.

## Requirements

- `vdirsyncer` and `khal` must be installed and available in `PATH`.
- The CalDAV account and collection config must already exist outside this skill.
- A TTY is required for interactive `khal edit` workflows.

## Core Rules

### 1. Sync is part of every real operation

- Treat `vdirsyncer sync` as part of the workflow, not an optional cleanup step.
- Sync before reads when freshness matters, and sync again after confirmed writes so local and remote state converge.
- If collections are missing or a server path changed, use `vdirsyncer discover` before assuming the calendar is empty.
- Do not trust a stale `khal` result until sync and cache state have been checked.

### 2. Use bounded windows and explicit calendar scope

- Prefer day, 7-day, 14-day, or exact date range queries over open-ended searches.
- Narrow to a specific calendar whenever the user already knows the target calendar.
- Resolve ambiguous phrases such as "next Friday" or "this evening" into exact dates, times, and timezone assumptions before writing.
- Titles are not unique identifiers, so duplicate-event risk rises quickly when searching across every calendar at once.

### 3. Respect khal's editing limits

- `khal edit` is interactive and needs a TTY, so do not present it as a non-interactive batch primitive.
- `khal` has only rudimentary recurrence editing and cannot edit event timezones directly, so complex recurring or timezone-sensitive events need extra caution.
- For fragile recurring series, DST-sensitive events, or uncertain matches, prefer inspect-first and recreate-only-with-approval over aggressive in-place edits.
- If the user wants bulk recurring surgery, stop and explain the risk before touching anything.

### 4. Verify every write with a read-back pass

- Before changing an event, read the target window first so the agent sees the exact current state.
- After create, update, or delete, run a read-back check in the same bounded window and report the returned title, time, and calendar.
- Use title plus date/time plus calendar, or UID when available, to confirm the right event changed.
- If verification is ambiguous or inconsistent, stop and surface the conflict instead of claiming success.

### 5. Treat local vdir state and conflict policy as real data

- `vdirsyncer` is synchronizing real local `.ics` state, not just acting as a remote viewer.
- The configured `conflict_resolution` policy can overwrite one side, so do not assume an "a wins" or "b wins" setup is harmless.
- Manual filesystem edits, cache resets, or storage path changes should be deliberate and reversible.
- Deleting `khal`'s cache database is a troubleshooting move for stale cache behavior, not a default fix for every mismatch.

### 6. Protect connection details, URLs, and certificates

- Confirm the CalDAV base URL and collection path before debugging deeper issues.
- Certificate and TLS errors are blockers; stop and fix the trust chain before continuing.
- Keep private connection details and sync config out of summaries unless the user explicitly asks for them.

### 7. Finish with operational clarity

- Every answer should end with the exact calendar scope, time window, action taken or proposed, and whether another sync is needed.
- If blocked, name the real blocker precisely: missing `vdirsyncer`, missing `khal`, missing TTY, undiscovered collections, login failure, or ambiguous event match.
- If the safest action is read-only, say so directly instead of improvising a write path.

## Common Traps

- Querying without syncing first -> stale answers and wrong scheduling decisions.
- Editing by title only -> the wrong duplicate event gets changed or deleted.
- Treating recurring events like normal one-offs -> series corruption or DST drift.
- Searching every calendar by default -> noisy matches and accidental writes to the wrong calendar.
- Using a one-sided `conflict_resolution` policy blindly -> local or remote data loss.
- Deleting `khal.db` too early -> symptoms disappear briefly while the real sync bug remains.
- Assuming any WebDAV-looking URL is a valid CalDAV calendar collection -> discovery and auth failures.
- Reporting success before read-back verification -> hidden mismatch between local cache and remote server.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `calendar-planner` - Plan weeks, repair conflicts, and turn calendar state into defended scheduling decisions.
- `schedule` - Handle general scheduling requests when the user needs timing help beyond raw CalDAV operations.
- `fastmail-api` - Use provider-specific Fastmail mail and calendar APIs when CalDAV is not enough.
- `remind` - Turn calendar deadlines and follow-ups into reminder workflows.

## Feedback

- If useful: `clawhub star caldav`
- Stay updated: `clawhub sync`
