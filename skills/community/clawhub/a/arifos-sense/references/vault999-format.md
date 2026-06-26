# VAULT999 — Immutable Audit Ledger Format

VAULT999 is the append-only audit ledger for arifOS consequential decisions.

## Purpose
- Every `HOLD`, `VOID`, or significant decision gets logged
- Provides continuity across sessions
- Creates a traceable accountability chain

## File Location
`~/.openclaw/workspace/memory/vault999.md`

## Entry Format

```
## VAULT999 Entry
**Timestamp:** YYYY-MM-DD HH:MM UTC
**Session:** <session-id or label>
**Verdict:** [SEAL|CAUTION|HOLD|VOID]
**Floor(s) checked:** [floor names]
**Reason:** [concise explanation of the decision logic]
**Action taken:** [what was done / what was deferred]
**Arif authorized:** [YES / PENDING / VOID-NO-AUTH]
**Notes:** [optional follow-up context]
---
```

## Rules
1. **Append only** — never edit existing entries
2. **Timestamp in UTC** — use ISO-8601 format
3. **One entry per consequential decision**
4. **Include session context** — helps trace across sessions
5. **Mark pending vs resolved** — HOLD entries should be updated when resolved

## Example Entry

```
## VAULT999 Entry
**Timestamp:** 2026-04-13 14:30 UTC
**Session:** telegram-main-20260413
**Verdict:** HOLD
**Floor(s) checked:** Kedaulatan (Sovereign), Kebijaksanaan (Wisdom)
**Reason:** External API write could not be fully reversed. Arif's explicit approval required.
**Action taken:** Paused. Awaiting /approve or direct authorization.
**Arif authorized:** PENDING
**Notes:** Action: delete 3 old memory files from /root/.openclaw/workspace/memory/
---
```

## Triage Log Format (for quick session logging)

For faster logging during sessions, also maintain `memory/vault999-triage.md`:

```
HH:MM UTC | VERDICT | short reason | action
```
This is scan-readable for quick context on recent decisions.
