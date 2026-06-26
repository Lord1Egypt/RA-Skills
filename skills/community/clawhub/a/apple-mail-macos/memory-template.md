# Memory Template - Apple Mail (MacOS)

Create `~/apple-mail-macos/memory.md` with this structure:

```markdown
# Apple Mail (MacOS) Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Context
- Providers connected in Mail.app
- Preferred command path and fallback path
- Preferred mailbox names and search windows

## Safety Defaults
- Dry-run before writes: yes/no
- Confirmation required for send: yes/no
- Confirmation required for delete: yes/no
- Confirmation required for bulk actions: yes/no
- Reply-all second confirmation: yes/no

## Command Reliability
- Working command path and last verification date
- Permission prompts seen and outcomes
- Fallback behavior that succeeded

## Provider Notes
- Gmail behavior notes
- Outlook behavior notes
- iCloud behavior notes
- Other provider caveats

## Recent High-Risk Operations
- operation_id, action, outcome, verification status

## Notes
- Repeated user preferences inferred from behavior
- Known failure modes and stable recovery steps

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still evolving | Keep learning while operating |
| `complete` | Defaults are stable | Operate with known preferences |
| `paused` | User wants minimal setup | Avoid extra discovery questions |
| `never_ask` | User asked to stop setup prompts | Use only explicit instructions |

## Rules

- Keep notes in natural language and avoid exposing internal config jargon to users.
- Update `last` whenever provider scope, command path, or safety defaults change.
- Record high-risk confirmations as safety evidence.
- Never delete historical notes without explicit user instruction.
