# Memory Type Taxonomy

Full reference for typed memory entries with examples and decision rules.

---

## Format

```
[TYPE] YYYY-MM-DD: <content>
```

All entries in MEMORY.md and decisions.md should be typed. Daily notes may be untyped for speed but should be typed when promoted to long-term memory.

---

## Types

### DECISION
A choice that was made and should not be revisited without cause.

```
[DECISION] 2026-01-15: Use Codex for new feature development, Claude Code for debugging
[DECISION] 2026-02-01: Switched to HIFO cost basis method for crypto tax reporting
[DECISION] 2026-02-20: Discord is primary channel for client work going forward
```

**Retention:** High. Decisions compound — reversing one without knowing it existed causes drift.

---

### PREFERENCE
How the human or system likes things done. Behavioral calibration.

```
[PREFERENCE] 2025-11-03: Irfan prefers bullet lists over markdown tables in Discord
[PREFERENCE] 2025-12-10: No headers in WhatsApp — use **bold** or CAPS instead
[PREFERENCE] 2026-01-05: Brevity is law — no fluffy openers or filler phrases
```

**Retention:** High. Preferences are durable and frequently referenced.

---

### FACT
A stable truth about the world, system, infrastructure, or domain.

```
[FACT] 2026-01-10: BlueBubbles webhook URL changes on every restart
[FACT] 2026-02-05: Twitter free tier is write-only — no read access without $100/mo plan
[FACT] 2026-03-01: 1099-DA is required for covered crypto transactions from 2025 onward
```

**Retention:** Medium-high. Review periodically — facts can become stale.

---

### ENTITY
A person, company, product, or service that needs context attached.

```
[ENTITY] 2025-11-20: DataForSEO — keyword/SERP API, credentials in 1Password "DataForSEO Prod"
[ENTITY] 2026-01-08: Khalid — second agent, handles social/client outreach, khalid@ workspace
[ENTITY] 2026-02-14: PrecisionLedger — Irfan's accounting firm, primary client for all work
```

**Retention:** High. Entity knowledge is hard to reconstruct and frequently referenced.

---

### EPISODE
A significant event — what happened, what the outcome was, why it matters.

```
[EPISODE] 2026-01-22: Deployed ClawdTalk voice skill. First outbound call succeeded.
  Irfan tested greeting — approved. WebSocket PID management via connect.sh.
[EPISODE] 2026-02-10: Gateway restart without BB restart caused all iMessage
  webhooks to fail for 3 hours. Identified bug in plugin registry. Added restart script.
```

**Retention:** Medium. Keep for 30-90 days; compress to LESSON or DECISION if pattern emerges.

---

### LESSON
Something that went wrong (or nearly wrong) and the specific fix.

```
[LESSON] 2026-01-20: Never run `openclaw gateway stop` from inside a session.
  It kills the host process. Use `openclaw gateway restart` only.
[LESSON] 2026-02-08: Cron jobs that send messages need bestEffort:true or they fail silently
  when the channel is offline. Always set this for notification crons.
[LESSON] 2026-03-01: Mental notes don't survive session restarts. Always write to file.
```

**Retention:** High. Lessons are expensive to re-learn.

---

### AGENT_IDENTITY
Self-knowledge about the agent — who it is, what it's becoming, how it's evolved.

```
[AGENT_IDENTITY] 2025-11-01: I am Sam Ledger, operational intelligence for PrecisionLedger.
  Primary persona is a senior finance professional, not a chatbot.
[AGENT_IDENTITY] 2026-01-15: I don't optimize old processes — I reimagine the approach.
  The Fosbury Flop principle.
```

**Retention:** Permanent. Identity is foundational.

---

## Priority Order for Compression

When compressing daily notes to MEMORY.md, prioritize in this order:

1. **LESSON** — Most valuable. Re-learning is expensive.
2. **DECISION** — Prevents drift and re-litigation.
3. **ENTITY** — Context that's hard to reconstruct.
4. **PREFERENCE** — Calibrates ongoing behavior.
5. **AGENT_IDENTITY** — Rarely added, always kept.
6. **FACT** — Keep if non-obvious or infrastructure-specific.
7. **EPISODE** — Only keep if it led to a LESSON or DECISION.

---

## Anti-patterns

| Avoid | Better |
|---|---|
| Untyped entries in MEMORY.md | Always add [TYPE] tag |
| "TODO" or task lists in MEMORY.md | Use a task manager or daily note |
| Duplicating what's in USER.md | MEMORY.md is for evolved knowledge, not baseline profile |
| Giant paragraph episodes | Keep to 2-4 lines; details in daily note |
| Stale FACTs left in place | Review quarterly; add `[STALE]` prefix when uncertain |
