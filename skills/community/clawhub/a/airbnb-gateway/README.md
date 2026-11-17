# airbnb-gateway

A reusable OpenClaw / Codex-style **skill package** for safe, coherent,
end-to-end Airbnb host operations: inbox checks, thread reading, reservation
lookup, booking summaries, calendar inspection, draft replies, **verified**
message sending, and disciplined escalation.

> ⭐ **Find this useful?** If `airbnb-gateway` saves you time, please **star it on ClawHub** — stars help other operators discover it and keep it maintained. Thank you!

It does not add transport. It orchestrates whatever Airbnb tooling your
environment already has — first-class Airbnb endpoints, agent-browser, DevTools,
Playwright — behind one consistent operating model so multiple agents behave
identically and never duplicate a guest message.

## Why this exists

Two reliability lessons are baked into the design:

1. **Browser weirdness ≠ Airbnb down.** Auth is host-owned; prefer platform-aware
   endpoints before generic browser automation.
2. **`sent: true` ≠ delivered.** A send is only `confirmed` after re-reading the
   live thread and *seeing* the message. Endpoint success is just `attempted`,
   and an `unconfirmed` send is **never** auto-resent.

## Install / use

1. Drop `skills/airbnb-gateway/` into your skills library.
2. Edit **`references/airbnb-tool-priority.md`** — map the abstract tool roles to
   the real tool names in your deployment. This is the only required
   customization.
3. (Optional) Set your approval policy and wire a persistent send ledger.
4. Point your agents at the skill. They should speak only in the command verbs
   (`check_inbox`, `read_thread`, `send_reply`, …) and never call low-level
   Airbnb tools directly.

## What's portable vs. deployment-specific

| Portable (don't fork) | Deployment-specific (customize) |
|---|---|
| The Five Laws | role → tool name map |
| Send state machine | approval policy |
| Safety tiers (READ/WRITE/MUTATE) | persistent ledger wiring |
| Command vocabulary | example payload shapes |

## Layout

```
airbnb-gateway/
├── SKILL.md                              # the operating contract (start here)
├── README.md                             # this file
├── CHANGELOG.md
├── LICENSE
├── references/
│   ├── airbnb-tool-priority.md           # ← customize per deployment
│   ├── airbnb-message-state-machine.md   # universal
│   ├── airbnb-safety-rules.md            # universal
│   └── future-adapter-interface.md       # how to pair with a code adapter later
├── examples/
│   ├── check-inbox.md
│   ├── read-thread.md
│   ├── send-reply-with-verification.md   # the critical path
│   ├── reservation-lookup.md
│   └── calendar-inspection.md
└── state/
    └── send-log.schema.json              # append-only dedupe ledger schema
```

## Status

v0.2.x — read operations, verified single-send, and **approval-gated calendar
mutations** (block/open dates, nightly price) under an explicit per-operation
approval gate with mandatory fresh-load verification (tier MUTATE-CAL). Listing
edits, accept/decline, and refunds remain intentionally **out of scope** (tier
MUTATE-RESTRICTED — refuse + escalate).

## License

MIT. No private tokens, paths, or secrets are embedded — example tool names are
illustrative and must be mapped to your environment.
