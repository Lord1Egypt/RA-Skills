---
name: evite-mcp
description: This skill should be used when the user asks about Evite events or invitations. Triggers on phrases like "check Evite", "my Evite events", "who RSVP'd", "Evite guest list", "RSVP to the party", "message my Evite guests", "create an Evite invite", or any request involving event invitations, guest lists, RSVPs, or party/event hosting on evite.com.
---

# evite-mcp

MCP server for [Evite](https://www.evite.com) — read and act on your events as both **guest** (invitations received) and **host** (events you created): list events, view guest lists & RSVP tallies, RSVP, message guests, and create/edit events.

- **npm:** [npmjs.com/package/evite-mcp](https://www.npmjs.com/package/evite-mcp)
- **Source:** [github.com/chrischall/evite-mcp](https://github.com/chrischall/evite-mcp)

## Setup

### Option A — Claude Code (direct MCP)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "evite": {
      "command": "npx",
      "args": ["-y", "evite-mcp"],
      "env": {
        "EVITE_EMAIL": "you@example.com",
        "EVITE_PASSWORD": "yourpassword"
      }
    }
  }
}
```

### Option B — global install

```bash
npm install -g evite-mcp
```

## Auth

The server resolves a session in priority order (see the README for details):

1. **`EVITE_EMAIL` + `EVITE_PASSWORD`** — headless email/password login (preferred).
2. **`EVITE_SESSION_COOKIE`** — a raw `cookie:` header copied from a signed-in evite.com tab.
3. **Fetchproxy bootstrap** — lifts session cookies from a signed-in evite.com browser tab. Opt out with `EVITE_DISABLE_FETCHPROXY=1`.

## Tools

**Read (6 + healthcheck):** `evite_list_events`, `evite_get_event`, `evite_list_guests`, `evite_rsvp_summary`, `evite_list_messages`, `evite_list_templates`, `evite_healthcheck`.

**Write (confirm-gated):** `evite_rsvp`, `evite_send_message`, `evite_broadcast`, `evite_create_event`, `evite_update_event`, `evite_add_guest`, `evite_update_guest`, `evite_remove_guest`, `evite_send`, `evite_cancel_event`, `evite_reinstate_event`, `evite_duplicate_event`.

Every write tool takes `confirm: boolean`. **Without `confirm: true` it makes no network call and returns a dry-run preview** of exactly what would be sent — the safe default. The authoring flow is `evite_create_event` → `evite_add_guest` → `evite_send`.
