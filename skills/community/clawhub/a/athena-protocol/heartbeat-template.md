# Athena Protocol — Heartbeat Template
# Add relevant sections to your HEARTBEAT.md

## What Heartbeats Are For

Heartbeats are your AI's proactive check-in system. Instead of waiting to be asked,
your AI periodically checks if anything needs attention.

This template gives you a starting structure. Customize it for your life.

---

## Minimal Heartbeat Template

Paste into your HEARTBEAT.md:

---

```markdown
# HEARTBEAT.md

## On Every Heartbeat

Check in this order:
1. Any urgent tasks or pending follow-ups?
2. Anything time-sensitive in the next 2 hours?
3. Any recent errors or failures to address?

If nothing needs attention: reply HEARTBEAT_OK.
If something needs attention: describe it clearly, don't bury the lead.
```

---

## Full Heartbeat Template (with optional modules)

---

```markdown
# HEARTBEAT.md

## Core Check (every heartbeat)

- Pending tasks or blockers?
- Upcoming events in the next 2 hours?
- Anything that needs to go out (email, post, message) waiting for approval?

## Periodic Checks (rotate, 2-3x per day)

- **Email** — any urgent unread messages?
- **Calendar** — any prep needed for upcoming events?
- **Active projects** — any blockers or things to flag?

## Quiet Hours

Do not interrupt between 23:00–08:00 unless urgent.
Urgent = time-sensitive, irreversible, or the human explicitly asked for a wake.

## Proactive Work (do without asking)

- Read and organize memory files
- Update MEMORY.md if it's been more than 3 days
- Check git status on active projects
- Nothing that sends, publishes, or modifies external state
```

---

## Heartbeat State Tracking

Track what you've already checked to avoid redundant checks:

Create `memory/heartbeat-state.json`:

```json
{
  "lastChecks": {
    "email": null,
    "calendar": null,
    "projects": null
  }
}
```

Update after each check. Don't re-check something you checked less than 30 minutes ago.
