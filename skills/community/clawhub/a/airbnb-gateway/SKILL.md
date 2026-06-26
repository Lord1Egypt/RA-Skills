---
name: airbnb-gateway
description: >
  A skill for safe, coherent Airbnb operations in OpenClaw-style agent
  environments. It standardizes how agents check inbox threads, inspect
  reservations and booking state, review calendar context, draft guest replies,
  send messages safely, and verify whether a send actually appeared in the live
  Airbnb thread. It teaches a strict operating model: prefer Airbnb-native
  endpoints before generic browser automation; treat send acknowledgments as
  attempted, not automatically confirmed; verify outbound messages in the live
  thread UI before declaring success; and never auto-resend from ambiguous or
  unconfirmed state. Designed to reduce duplicate messages, normalize agent
  behavior, and provide a safer foundation for Airbnb messaging, bookings, and
  calendar workflows — useful standalone today and as a companion to a more
  formal Airbnb adapter/tool layer tomorrow.
version: 0.1.4
risk: write-gated
tags: [airbnb, vacation-rental, messaging, operations, openclaw]
license: MIT
homepage: ""
maintainer: ""
---

# airbnb-gateway

> ⭐ **Find this skill useful?** If `airbnb-gateway` saves you time, please
> **star it** (the ⭐ at the top of this ClawHub page) — stars help other rental
> operators discover it and keep it maintained. Thank you!

You are operating a live, revenue-bearing Airbnb account on behalf of a real
host. Guests are real people. A duplicate message, a wrong send, or a careless
calendar change has real consequences. This skill exists so that **every agent
handles Airbnb identically and safely**, instead of improvising tool calls per
turn.

> **Portability note.** This skill is environment-agnostic. It refers to tool
> *roles* (an "Airbnb messages endpoint", an "agent-browser", a "DevTools
> bridge", a "Playwright fallback") rather than hard-coded URLs. Your concrete
> tool names live in `references/airbnb-tool-priority.md` — edit that one file
> to map roles to the actual tools in your deployment. Everything else here is
> universal.

---

## THE FIVE LAWS (non-negotiable)

1. **Platform-first.** Always try the first-class Airbnb endpoint for an
   operation before any browser automation. Browser weirdness is NOT evidence
   that Airbnb access is down.
2. **Read before write.** Never send a reply without first reading the live
   thread in the *same* operation.
3. **`sent: true` is `attempted`, not `confirmed`.** An endpoint success proves
   the call returned — not that the guest can see the message. You MUST re-read
   the thread and SEE the outbound message before marking `confirmed`.
4. **Never auto-resend an `unconfirmed` send.** Duplicate guest messages are
   worse than a late reply. Escalate to a human instead.
5. **Writes gate; mutations stop.** Sending a message is approval-gated.
   Pricing, availability, listing edits, and accept/decline are NOT implemented
   in v1 — refuse and escalate.

If you are ever unsure, STOP and report. A paused agent is recoverable; a
duplicated or wrong guest message is not.

---

## Minimum Environment Contract

Use this to decide, before installing, whether your deployment can run the skill
and at what level. Map each role to a real tool in
`references/airbnb-tool-priority.md`. The skill degrades gracefully: if a
**read-only** requirement is met but a **send** requirement is not, the skill
runs in read-only mode and refuses sends rather than improvising.

**Read-only mode — minimum to run safely (inbox / threads / reservations / calendar):**
- At least one **Airbnb read path** — list/read messages, reservations, and
  calendar (first-class endpoint preferred; agent-browser or DevTools read
  acceptable as fallback).

That's the entire requirement for every READ verb. Nothing can be sent in this
mode.

**Send-capable mode — additional minimum to send a guest reply:**
- An **Airbnb send path** — the first-class send endpoint (preferred) OR an
  explicitly human-approved browser send.
- A **thread re-read path** — to verify the outbound message after sending.
  (The same read path from read-only mode satisfies this.)

If either is missing, do NOT send: stay in read-only mode and escalate.

**Optional enhancements — improve safety / fallback depth when present:**
- **Agent-browser** — navigate/inspect when an endpoint is missing or hard-down.
- **DevTools bridge** — read-only DOM inspection to verify UI state.
- **Playwright fallback** — last-resort automation for read-only ops.
- **Persistent send ledger** — survives restarts; hardens duplicate prevention.
- **Approval channel** — human/approver sign-off before a send.

Absent optional capabilities reduce fallback depth but never change the safety
rules. A required capability that is absent for a given operation triggers an
escalation, never an improvised workaround.

---

## Operating model — which tool path do I use?

Resolve top-down. Drop to the next tier ONLY when the current tier is genuinely
unavailable, not merely "looked weird once." Full detail in
`references/airbnb-tool-priority.md`.

```
OPERATION
  │
  ├─ 1. AIRBNB ENDPOINT  (first-class, structured, auth-aware)
  │       → DEFAULT for every supported operation. Always start here.
  │
  ├─ 2. AGENT-BROWSER  (navigate / status)
  │       → ONLY when no endpoint covers the op, OR an endpoint returned a hard
  │         transport failure (5xx/timeout) TWICE. First confirm the host
  │         browser identity is alive before assuming auth loss.
  │
  ├─ 3. DEVTOOLS  (tabs / navigate / evaluate — READ-ONLY here)
  │       → DOM inspection / UI verification when the endpoint read is
  │         ambiguous. Never use evaluate to perform a write/click-send.
  │
  └─ 4. PLAYWRIGHT  (fallback)
          → LAST RESORT. Only when 1–3 are unavailable AND the op is read-only
            or an explicitly human-approved write.
```

---

## Safety model

Classify every operation before acting. Full table in
`references/airbnb-safety-rules.md`.

| Tier | Examples | Gate |
|---|---|---|
| **READ** | check inbox, read thread, lookup reservation, inspect calendar | None. Proceed. |
| **WRITE** | send a guest reply | Approval if configured; ALWAYS verify after. |
| **MUTATE** | change price, block/open dates, edit listing, accept/decline, refund | **NOT in v1.** Refuse + escalate. |

**Escalate to a human when:** a send reaches `unconfirmed` or `failed`; you're
asked to perform any MUTATE op; the host browser identity reports unhealthy; two
read paths disagree on a material fact (dates, guest count, price); or you would
need to send the same message twice for any reason.

---

## Message send — the state machine (the core procedure)

States: `drafted → attempted → (confirmed | unconfirmed | failed)`. Full machine
with timings in `references/airbnb-message-state-machine.md`.

```
[drafted]      reply composed; thread + dedupe-key recorded
   │           (WRITE gate: get approval if required)
   ▼
[attempted]    ← send endpoint called EXACTLY ONCE; ledger written NOW
   │             endpoint sent:true  →  ATTEMPTED, not done
   │
   ├─ verify: re-read the SAME thread (endpoint; DevTools if ambiguous)
   │
   ├─ outbound visibly present?  ── yes ──► [confirmed]   ✅ report
   ├─ absent after verify window ── no  ──► [unconfirmed] ⚠️ DO NOT RESEND, escalate
   └─ send call errored                  ► [failed]       ❌ re-read first, escalate, no blind resend
```

### Send procedure (follow exactly)
1. **Read the live thread.** Capture the last inbound message + a dedupe-key
   (`thread_id` + normalized hash of the draft text).
2. **Check the send ledger.** If a `confirmed` (or recent `attempted`) send with
   the same dedupe-key exists → STOP, already handled.
3. **Draft** the reply → state `drafted`.
4. **Approval gate** if required — present draft + thread context, wait for "go".
5. **Send exactly once** via the first-class send endpoint → state `attempted`.
   Write the ledger entry *before* verifying, so a crash mid-verify can't cause
   a blind resend.
6. **Verify** — re-read the thread, look for the outbound text/timestamp.
7. **Confirm or not** — visible → `confirmed`; absent within window →
   `unconfirmed`.
8. **Report** final status: thread id, state, and the human action needed.

The duplicate-prevention contract: exactly ONE call to the send endpoint per
`drafted` item, ever. `unconfirmed`/`failed` NEVER auto-transition to a new send.
Only a human, after reading the live thread, may authorize a retry.

---

## Reservation & calendar (READ-only in v1)

- **`booking_summary`** — list reservations sorted by check-in: guest, dates,
  status, `reservation_id`, linked `thread_id`.
- **`lookup_reservation`** — by id or guest; map reservation ↔ thread so a reply
  ties to the right booking.
- **`inspect_calendar`** — report blocked/open/booked spans; FLAG (don't fix)
  high-risk states (double-booking, anomalous price, risky back-to-back gaps).

Calendar mutation, pricing, accept/decline, and listing edits are reserved for
v2 and get their own gated workflows mirroring the send machine
(read → propose → approve → do-once → verify → report). Until then: refuse +
escalate.

---

## Command surface

Agents speak only in these verbs; each maps to a canonical procedure. Format is
`verb (TIER) — description`.

**READ verbs (no gate):**
- `check_inbox` **(READ)** — list threads needing attention, prioritized.
- `read_thread <id>` **(READ)** — full live thread + guest-intent summary.
- `lookup_reservation <id-or-guest>` **(READ)** — reservation details + linked thread.
- `booking_summary` **(READ)** — upcoming bookings, sorted by check-in.
- `inspect_calendar [range]` **(READ)** — calendar state + flagged risks.
- `verify_sent <thread> <draft>` **(READ)** — re-check a thread for an outbound message.

**WRITE verbs (gated + verified):**
- `draft_reply <thread> <intent>` **(WRITE-pre)** — produce a reviewable draft; result state `drafted`.
- `send_reply <thread> <draft>` **(WRITE)** — run the full send state machine.

**Status:**
- `report_status` — emit structured status of the last operation.

`send_reply` is the ONLY write, and it internally enforces
read → draft → approve → send-once → verify → report. Agents must not decompose
it into lower-level steps to skip verification.

---

## Future adapter compatibility

This skill is the *behavioral contract*. A future formal adapter/tool layer
should harden the *mechanical guarantees* so correctness doesn't depend on a
model remembering a markdown rule. See `references/future-adapter-interface.md`.

Ideal future adapter functions (call them if present, fall back to the manual
procedure if not):

- `airbnb.sendVerified(thread_id, text, dedupe_key)` → returns
  `{state, visible_at}` after doing send-once + ledger + verify atomically.
- `airbnb.dedupeCheck(dedupe_key)` → `{already_sent: bool, last_state}`.
- `airbnb.readThread(thread_id)` / `airbnb.listInbox()` /
  `airbnb.listReservations()` / `airbnb.readCalendar(range)`.

When `sendVerified` exists, `send_reply` delegates to it and simply reports the
returned state. When it doesn't, `send_reply` runs the manual procedure above.

---

## Anti-patterns (do NOT do these)

- ❌ **Jumping to Playwright early.** Endpoints exist and are preferred; falling
  to Playwright because something felt slow once is wrong.
- ❌ **Treating `sent: true` as confirmed.** It's `attempted`. Always verify.
- ❌ **Resending from `unconfirmed`.** This creates duplicate guest messages.
  Escalate instead.
- ❌ **"Auth must be dead."** Missing local browser/session state is NOT proof —
  auth is host-owned. Check browser status + an endpoint first.
- ❌ **Mixing read-safe and write-risk behavior.** Classify every op; never let
  a read workflow quietly perform a write.
- ❌ **Improvising the send flow per turn.** There is exactly ONE send
  procedure. Use it.

---

## Maintainer notes

- **Customize per deployment:** `references/airbnb-tool-priority.md` (map roles
  to real tool names), the approval-gate policy, and whether a persistent ledger
  is wired. Examples under `examples/` are illustrative — adapt payloads to your
  tools.
- **Keep universal:** the Five Laws, the send state machine, the safety tiers,
  and the command vocabulary. These are the portable core; don't fork them per
  deployment.
- **Evolving the skill:** add new operations by giving each its own gated
  workflow in the same shape as the send machine. Never add a generic "do
  anything" write. Bump `version`; record changes in a CHANGELOG if published.
