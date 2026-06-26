---
name: agentmeet
description: Agent-to-agent meeting coordination over email. Read Google Calendar, generate available slots, send protocol-formatted emails. Recipients click a time slot to reply — no server, no account, pure p2p over email.
homepage: https://github.com/agentmeet/agentmeet
metadata: {"clawdbot":{"emoji":"📅","os":["darwin","linux"],"requires":{"bins":["bun"]},"install":[{"id":"bun","kind":"shell","command":"cd ~/Dropbox/Dev/agentmeet && bun install","label":"Install agentmeet dependencies via Bun"}]}}
---

# AgentMeet — Agent-to-Agent Meeting Coordination

An open protocol for AI agents to coordinate meetings over email.
No server. No domain. No account. Pure p2p.

## How It Works

1. Agent reads user's Google Calendar -> generates available slots
2. Agent sends an HTML email where each time slot is a clickable mailto: link
3. Recipient clicks a slot -> opens pre-filled reply with machine-readable payload
4. Sender's agent detects the reply -> creates calendar events for both parties

Every invite email also includes an "Add AgentMeet" link for viral adoption.

## Setup

```bash
cd ~/Dropbox/Dev/agentmeet && npm install
```

Requires Google Calendar and Gmail access (OAuth or MCP).

## Usage

### Send a meeting invite

```bash
bun run -e '
import { buildInvite } from "~/Dropbox/Dev/agentmeet/src/invite";
import { writeFileSync } from "fs";

const result = await buildInvite({
  from: { name: "YOUR_NAME", email: "YOUR_EMAIL" },
  to: "RECIPIENT_EMAIL",
  meeting: {
    title: "Meeting Title",
    duration_minutes: 30,
    notes: "Optional description",
  },
  slots: [
    { start: "2026-03-25T10:00:00+08:00", end: "2026-03-25T10:30:00+08:00" },
  ],
});

// result.subject = email subject line
// result.html = email body (HTML with embedded protocol payload)
// Send via Gmail API or any email service
'
```

### Parse an incoming agentmeet email

```typescript
import { parseAgentMeetEmail, isAgentMeetSubject } from "agentmeet";

// Check subject line
if (isAgentMeetSubject(emailSubject)) {
  const payload = parseAgentMeetEmail(emailHtmlBody);
  if (payload) {
    console.log(payload.type);           // INVITE | COUNTER | SELECT | CONFIRM
    console.log(payload.request_id);     // am_xxx
    console.log(payload.selected_slots); // for SELECT type
  }
}
```

### Generate available slots from calendar

```typescript
import { getBusyPeriods, generateAvailableSlots, DEFAULT_PREFERENCES } from "agentmeet";

const busy = await getBusyPeriods(oauth2Client, startISO, endISO);
const slots = generateAvailableSlots(busy, startDate, endDate, 30, DEFAULT_PREFERENCES);
```

## Protocol

Four message types, embedded as HTML comments in email body:

| Type | Direction | Purpose |
|------|-----------|---------|
| INVITE | A -> B | Sender's available slots |
| COUNTER | B -> A | Recipient's alternative slots |
| SELECT | B -> A | Recipient picks one or more slots |
| CONFIRM | A -> B | Calendar events created |

Detection: subject starts with `[AgentMeet]`, body contains `<!-- agentmeet/v1`.

Payload format:
```html
<!-- agentmeet/v1
{
  "protocol": "agentmeet",
  "version": "0.1",
  "type": "SELECT",
  "request_id": "am_abc123",
  "selected_slots": [{ "start": "ISO8601", "end": "ISO8601" }]
}
-->
```

## Multi-Party Scheduling

Send INVITE to multiple recipients. Each responds with their available slots.
The initiating agent finds the intersection and proposes the best overlap.

## Email Format

Each slot in the invite email is a mailto: link. Clicking it opens a pre-filled
reply email with the SELECT payload. For group scheduling, a separate
"I'm available for all of these" link lets recipients select multiple slots
and delete the ones that don't work.

## Configuration

Default preferences (override per-invite):

```yaml
working_hours:
  start: "09:00"
  end: "18:00"
  timezone: "Asia/Taipei"
buffer_minutes: 15
max_slots_to_share: 5
blocked_days: ["saturday", "sunday"]
```

## Source

Protocol spec: `PROTOCOL.md`
Implementation: `src/` (TypeScript)
License: Apache-2.0
