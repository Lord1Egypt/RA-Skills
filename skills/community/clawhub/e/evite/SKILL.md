---
name: evite
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

**Write (asks you to confirm first):** `evite_rsvp`, `evite_send_message`, `evite_broadcast`, `evite_create_event`, `evite_update_event`, `evite_add_guest`, `evite_update_guest`, `evite_remove_guest`, `evite_send`, `evite_cancel_event`, `evite_reinstate_event`, `evite_duplicate_event`.

Every write tool **asks the user to confirm before it sends anything**: a confirmation prompt where the client supports one (unless the server sets `MCP_CONFIRM_ELICITATION=off`); otherwise the first call makes no write (at most a read-only lookup, e.g. `evite_update_guest` reads the draft guest list to build its preview) and returns a preview of exactly what would be sent plus a `confirmToken` (see `MCP_CONFIRM_MODE`). Show the user that preview and get their approval in chat, then call the same tool again with the same arguments plus `confirmToken`. The token is single-use and bound to those exact arguments — change anything and it is refused (`DRAFT_CHANGED`) with a fresh preview and token. The authoring flow is `evite_create_event` → `evite_add_guest` → `evite_send`.

## In context groups

On a host that groups MCPs by context (mcp-host's context groups), this server is in the **family** group. Every tool except `evite_healthcheck` carries a `_meta.mint` hint.

- **Canonical read:** `evite_list_events` answers the group's **what's on** question. With `view: "brief"` it returns one line per upcoming event — `title — <ISO start or "no date"> — <status>`, where the status is Evite's event status plus your part in it (`hosting`, `rsvp yes|no|maybe`, `no reply`) — inside the untrusted-data envelope as `data` (event titles are written by each host). A `-- none` line means no events; `-- more` means the page came back full. An event whose own title starts with `-- ` or `\` is shown with one leading `\`, so it never reads as a note; each line is cut to 120 characters, title first.
- **No subject and no range:** Evite has no listable subjects (children, properties) and its event list takes no date range, so the canonical read declares neither. Nothing here answers *what's new* or *what's due*; the other reads are `lookup` hints and the writes are `change`/`send` hints.
- **Compound ask:** "what's on this weekend — any parties, and anything due at school?" — the family group answers the party half from `evite_list_events`, and the school group the rest.
- **Browser bridge:** when the session comes from the fetchproxy tier (a signed-in evite.com tab) rather than email/password, the group answers "needs your browser open" while that browser is not connected.
