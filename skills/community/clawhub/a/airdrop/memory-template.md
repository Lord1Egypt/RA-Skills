# Memory Template - AirDrop

Create `~/airdrop/memory.md` with this structure:

```markdown
# AirDrop Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | paused | never_ask

## Context
- Default activation moments for nearby local file transfer
- Preferred mode: direct AppKit launcher or Shortcut fallback
- Confirmation strictness for sensitive files
- Whether temporary staging files are acceptable

## Notes
- Reliable file-packaging patterns that worked before
- Known local shortcut names used for AirDrop fallback
- Device classes commonly targeted: iPhone, iPad, Mac

---
Updated: YYYY-MM-DD
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning | Capture stable sharing preferences gradually |
| `complete` | Enough context exists | Use remembered defaults without extra setup |
| `paused` | User wants minimal setup | Avoid more preference questions unless needed |
| `never_ask` | User does not want persistence | Keep everything session-only |

## Key Principles

- Save behavior patterns, not file contents.
- Do not store recipient names or device identifiers unless the user explicitly asks.
- Keep memory focused on activation and safety defaults.
- If the user declines persistence, do not create or update `~/airdrop/`.
