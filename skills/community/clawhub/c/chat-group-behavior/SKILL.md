---
name: chat-group-behavior
description: How to join, participate in, and leave group conversations on messaging platforms (WhatsApp, Signal, Telegram, etc.). Use when the owner tags the agent into a group chat, when the agent needs to open or close the participation gate, or as a reference for correct group chat behavior.
---

# Chat Group Behavior

This skill covers the full lifecycle of group chat participation: joining, behaving well while active, and leaving cleanly.

## Prerequisites

`channels.<platform>.groupPolicy`, `groupAllowFrom`, and `groups.*.requireMention` are set so that only the owner can wake you in any group by default. Trigger phrases are defined in `agents.list[main].groupChat.mentionPatterns`. This applies to WhatsApp, Signal, Telegram, and other supported platforms.

---

## Joining a Group

When the owner @mentions you in a group chat, follow these steps in order.

**Step 1 — Capture context**

From the inbound message metadata: platform (e.g. `whatsapp`, `signal`), group ID (the `chat_id` / `from` field), and duration (parse from the owner's message — default 30 minutes if unspecified).

**Step 2 — Open the gate**

Patch `channels.<platform>.groups.<group_id>.requireMention` to `false` in `openclaw.json`. The gateway file-watches the config and hot-reloads automatically — no restart needed.

**Step 2b — Open the sender filter**  ⚠️ Critical — easy to miss

`groupAllowFrom` controls not just *who can wake you* in a group, but also *which senders' messages are delivered to you* once active. If it's set to only the owner's number (the default), messages from other group members will be silently dropped even with `requireMention: false`.

Fix: patch `channels.<platform>.groupAllowFrom` to `["*"]` so all group members' messages are delivered.

This is safe because `groupPolicy: "allowlist"` still restricts *which groups* you are active in — opening the sender filter only affects groups you've explicitly joined.

Verify with `openclaw doctor` — config changes must pass schema validation.

**Step 3 — Signal before going quiet**

Before doing any work (research, lookups, etc.) triggered by a group message, send a brief acknowledgment first: *"On it, give me a moment 👁️"* — then go do the work. Silence looks like a crash.

**Step 4 — Introduce yourself**

Say hi, introduce yourself briefly if it's a new group. Participate like a human — use judgment about when to contribute. Do not respond to every message.

**Step 5 — Set a closing cron job**

Create a one-shot cron job (`kind: "at"`) for the parsed duration. When it fires: patch `requireMention` back to `true` for this group in `openclaw.json`, then send a brief goodbye. The gateway hot-reloads and the gate closes — no owner action needed.

**Step 6 — Confirm to owner**

Tell the owner the window is open and when it closes: _"Joined! I'll be here for 60 minutes — going quiet at 4:19 PM."_

---

## Behavior While Active

- **One response per message** — don't triple-tap with different reactions
- **Signal before working** — acknowledge first, deliver second (see Step 3)
- **Don't dominate** — respond when you add value; stay quiet for casual banter between humans
- **Be present, not performative** — contribute naturally, like a human participant

---

## Leaving a Group

**Timed close (automatic):**
When the closing cron fires: patch `requireMention: true` back for this group in `openclaw.json`, send a brief goodbye to the group. Gateway hot-reloads.

**Early close (owner request):**
Owner says `@<agent> that's enough` / `close` → patch `requireMention: true` immediately, cancel the cron, say goodbye.

**Extend (owner request):**
Owner says `@<agent> stay for another X mins` → cancel existing cron, set a new one.

---

## Troubleshooting

**Messages from group members not reaching me:**
Check `groupAllowFrom` — if it's restricted to the owner's number, non-owner messages are silently filtered. Set to `["*"]` (see Step 2b).

**"thinking/redacted_thinking blocks cannot be modified" errors:**
This happens when the session has reasoning tokens in its history and a subsequent API call tries to re-process them. Fix: clear the session transcript file (find it via `sessions.json` in the agent sessions directory). The session will restart clean on the next message.

---

## Notes

- Group ID is in inbound message metadata (`chat_id` / `from` field)
- Config changes hot-reload — no gateway restart or Docker restart needed
- When closing, set `requireMention: true` for the specific group entry (or remove it to fall back to the wildcard default)
- `groupAllowFrom: ["*"]` combined with `groupPolicy: "allowlist"` is the correct secure pattern — open sender filter, restricted group allowlist
