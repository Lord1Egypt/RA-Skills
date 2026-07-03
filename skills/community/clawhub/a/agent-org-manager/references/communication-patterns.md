# Communication Patterns — 深度协议

Not "how to send a message." How to design a communication system that survives failure.

## The Three Failure Modes

Every inter-agent communication failure falls into one of three buckets. If you understand these, you understand 90% of outages:

### Failure 1: Delivery Never Happened
The sender thinks it sent. The receiver never got it. Cause: tool failure, session crash, rate limit, or auth expiry.

**Detection**: Receiver-side timeout. If Agent B expects a handoff from Agent A at 08:00 and doesn't see it by 08:15, alarm.

**Recovery**: Resend on channel 2 (shared file) or channel 3 (status flag). Never retry on the same channel that failed — if it was a tool-level failure, it will fail again.

### Failure 2: Delivery Happened But Wasn't Consumed
The message landed. The receiver never read it. Cause: cron didn't fire, agent session died, or the reader logic has a bug.

**Detection**: Stale file check. Files older than expected_interval * 2 are stale. Flag.

**Recovery**: Inspector re-notifies the receiver via a different channel. If receiver is dead (session gone), DataCenter respawns it.

### Failure 3: Delivery Consumed But Misunderstood
The message was read. The action taken was wrong. Cause: ambiguous instructions, context mismatch, or the agent hallucinated.

**Detection**: Output verification — does the receiver's subsequent output make sense given the message?

**Recovery**: CEO clarifies. But only once — if the same misunderstanding happens twice, the communication protocol is broken, not the agent.

## Channel Selection Logic

Not every message needs all three channels. The protocol is:

```
Priority 0 (KILL_SWITCH, compliance violation)  → All 3 channels simultaneously
Priority 1 (Decision needed, deadline today)     → sessions_send + shared file
Priority 2 (FYI, no action needed)               → shared file only
Priority 3 (Nice to know, archival)              → shared file, no alert
```

The cost of using all 3 channels is near zero. The cost of using 1 channel and missing a critical message is infinite. Err on the side of redundancy for anything that matters.

## Flag File Protocol

Status flags are binary signals: "I'm done with X" or "I'm waiting for Y."

```markdown
# File: company/shared/flags/brand_published.flag
status: done
timestamp: 2026-06-26T15:52:00+08:00
next_expected: 2026-06-27T15:52:00+08:00
verified_by: inspector
```

A flag without a `next_expected` timestamp is a dead flag — it signals completion but not continuity. Every recurring task's flag must carry the next expected time.

### Stale Flag Recovery

If `next_expected` has passed and the flag hasn't updated:
1. Inspector detects staleness (routine check)
2. Inspector queries the owning department: "Status on {flag_name}?"
3. If no response within 1 hour → escalate to CEO with context

## Broadcast Protocol

When a decision affects 3+ departments:

1. Write `company/shared/broadcast/BC_{YYYYMMDD}_{HHMM}.md`
2. Set `company/shared/flags/broadcast_pending.flag`
3. Each department's next cron cycle checks for `broadcast_pending.flag`
4. Department reads the broadcast file, acts, and writes acknowledgment to its message box
5. When all departments have acknowledged, clear the pending flag

Broadcast without acknowledgment tracking is just shouting into the void.

## Communication Audit Trail

Every message, every flag transition, every broadcast acknowledgment is a file. This means:
- You can reconstruct exactly what happened during an outage
- You can identify which department is the bottleneck in any workflow
- You can prove to yourself (and anyone else) that your system is working — or not

A company with no audit trail isn't a company. It's a chat log.
