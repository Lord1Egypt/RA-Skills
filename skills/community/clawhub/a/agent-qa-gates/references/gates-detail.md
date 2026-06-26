# Gate Detail Reference

Full checklists for each gate tier. Load this file when you need the complete criteria.

---

## Gate 0: Verify & Commit

Before reporting any change as "done":

- ✅ Did the **mechanism** change, or just the **text**?
- ✅ Can you **observe** the new behavior? (test output, verify config loaded, check logs)
- ✅ File exists and is non-empty
- ✅ No placeholder text — grep for `TODO`, `PLACEHOLDER`, `TBD`, `Lorem ipsum`
- ✅ Correct file path and format
- ✅ If config/schedule change: all required fields verified after creation

**Rule:** Text changes ≠ behavior changes. "Done" means tested and working.

---

## Gate 1: Human-Facing

Briefings, summaries, task updates, dashboards.

- ✅ Gate 0 checks pass
- ✅ Key finding or recommendation in the first 2 lines
- ✅ No paragraph exceeds 3 lines
- ✅ No sentence that could be deleted without losing information
- ✅ Structured — headers, bullets, or clear flow (not walls of text)
- ✅ Facts verified against source — no hallucinated stats
- ✅ Channel length check enforced for delivery surface

### Common Channel Limits

| Surface | Limit | Action if over |
|---------|-------|---------------|
| Telegram | 4,096 chars | Split into multiple messages |
| Discord | 2,000 chars | Split or summarize |
| Slack | 40,000 chars | Rarely an issue |
| Email | No hard limit | Keep under 500 words preferred |
| SMS | 160 chars | Extreme compression |

---

## Gate 2: External

### Email
- ✅ Gate 1 checks pass
- ✅ BCC or CC rules applied per org policy
- ✅ Sent-folder dedup check before sending (no duplicate sends in last 24h)
- ✅ Recipient-appropriate tone
- ✅ No internal context leaked (agent names, memory files, system details)
- ✅ Session-channel alignment (don't cross-send between messaging platforms)

### Public Content (social media, articles, blog posts)
- ✅ Matches the human's voice profile
- ✅ No internal context leaked
- ✅ Links verified (not broken, not expired)
- ✅ Proofread for typos, grammar, formatting artifacts

### Client / External Materials
- ✅ No private data unless explicitly requested
- ✅ Professional tone appropriate to audience
- ✅ All references and links verified
- ✅ No secrets or tokens anywhere in output

---

## Gate 3: Code & Technical

- ✅ Gate 0 checks pass
- ✅ Builds without errors
- ✅ No hardcoded secrets, API keys, or tokens
- ✅ No debug logging left in production code
- ✅ Error handling present (not just happy path)
- ✅ Tests exist and pass (for non-trivial logic)
- ✅ Responsive verified (if UI work)
- ✅ Follows existing codebase patterns
- ✅ Committed with descriptive message

---

## Protocol Gates

### Heartbeat / Periodic Output
- ✅ Binary: alert text ONLY or status-OK ONLY. Never both. Never mixed.
- ✅ No conversational framing ("here's what I found...")
- ✅ Every data point verified by tool call in current session
- ✅ No stale data carried forward from previous cycle
- ✅ Duplicate alerts suppressed (only re-alert on state change)
- **Severity:** Treat format violations as 🔴 BLOCK

### Post-Compaction / Context Reset
- ✅ Do not trust pre-reset "facts" — verify from files and tools
- ✅ Rerun pending checks from scratch with fresh tool calls
- ✅ If a periodic check is due: zero carryover

### Scheduled Job Changes
- ✅ Explicit timeout set
- ✅ Explicit model/configuration set
- ✅ Schedule verified after creation
- ✅ Output fits destination channel limits
- ✅ Pre-flight checklist questions answered:
  1. What business outcome does this protect?
  2. Why can't this be done in a periodic check instead?
  3. What happens if it times out?
  4. How will success be verified?

### Sub-Agent Review
- ✅ Output matches brief's success criteria
- ✅ No unresolved uncertainty flags (`[UNCERTAIN]`, `[TODO]`, etc.)
- ✅ Reasoning is sound (check the "why", not just the conclusion)
- ✅ 2-3 critical paths spot-checked
- ✅ Passes the relevant gate (1, 2, or 3)

### Isolated Agent / Cron Output (real-world data)
For any scheduled job or sub-agent that reports external data (bookings, email, health, finance, calendar, API responses) **without going through an orchestrator review step first**:

- ✅ Agent made a verifiable live tool call — the raw API response or CLI output is present or referenced
- ✅ No proper nouns (names, places, amounts, IDs) that cannot be traced to a tool result
- ✅ If the tool call failed: output is `DATA_UNAVAILABLE — [reason]`, not plausible-sounding fabricated data
- ✅ No dates, statuses, or metrics that weren't returned by the live call
- ✅ The cron/agent prompt includes the Real-World Data Verification Rule (see battle-tested-agent Pattern 2a)

**Severity:** Fabricated real-world data is 🔴 BLOCK. Treat as equivalent to hallucinated metrics in a human-facing briefing.

**Real incident:** A Lodgify cron fabricated three guest names, arrival/departure dates, and cancellation statuses. None existed. Delivered directly to the operator. (2026-03-27)

**Prevention:** Inject this into every external-data cron prompt:
```
If the API call fails or returns empty: output ONLY "DATA_UNAVAILABLE — [reason]".
NEVER invent names, numbers, dates, or statuses. Silence > fabrication.
```

### Delegated Work Acceptance Gate
For any non-trivial delegated task (build, config change, audit, migration, or external deliverable), do not accept completion until all checks pass:

- ✅ Expected artifact exists
- ✅ Artifact matches the brief
- ✅ Exact commands run are listed
- ✅ Verification was actually performed, with results
- ✅ Output is non-empty and specific
- ✅ Known gaps / next actions are named explicitly

**Severity:** Empty or artifact-free "success" = 🔴 BLOCK. Treat as a failed delivery claim, not a soft warning.

**Valid dispositions:**
- `Done` — acceptance checks pass
- `Revision Needed` — artifact exists but brief mismatch / weak verification / missing detail
- `Blocked` — real dependency prevents completion or verification
- `Failed` — no usable artifact or unrecoverable execution failure
- `Stale` — accepted run exists but work has gone quiet beyond freshness thresholds

### Silent Worker / Stale Task Gate
For delegated work that appears to be running:

- ✅ Accepted spawn exists before describing the task as running
- ✅ Start signal appears within 10 minutes after accepted spawn, or the task is marked `Stale`
- ✅ Materially new output appears within 30 minutes on active work, unless the task explicitly allows a longer quiet window
- ✅ `Stale` work is investigated, re-briefed, killed+respawned, or escalated — never left as indefinite `In Progress`

**Severity:** Misreporting silent work as active progress = 🟡 FIX at minimum; repeated cases should be promoted to a hard protocol gate.

---

## Post-Ship Failure Protocol

When something ships and fails:

1. **Contain** — delete/retract if possible
2. **Notify** — tell the human immediately
3. **Log** — record with root cause analysis
4. **Prevent** — add or tighten the relevant gate

### Failure Log Format

```
[YYYY-MM-DD] QA FAIL: <agent> delivered <what> that failed Gate <N>.
Issue: <what was wrong>
Root cause: <spec too vague / hallucination / format wrong / etc.>
Fix: <what changed>
```

---

## Gate Evolution Rules

- Same failure class 2+ times → add a gate item
- Gate hasn't caught anything in 60 days → prune it
- New delivery surface added → add its channel limits
- New agent type → verify existing gates cover its output patterns
