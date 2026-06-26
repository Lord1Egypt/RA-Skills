# Policy patterns for alert-triage

## 1. Severity model

### Critical
Use when there is active business, safety, revenue, or major uptime impact and immediate action is justified.

### High
Use when there is material degradation, rising risk, or likely near-term impact that should be handled quickly.

### Medium
Use when the issue is real and actionable, but safe to queue or batch unless it persists.

### Low
Use when the event is mildly useful, low-risk, or operationally routine.

### Info
Use when the event is mainly informational and should usually go to digest or be ignored.

## 2. Outcome policy

### send-now
Use for urgent, trusted, actionable alerts.

### batch-later
Use for non-urgent but decision-useful signals.

### ignore
Use for vanity metrics, low-signal noise, and non-actionable events.

### suppress-as-duplicate
Use when repeated events add no meaningful new information.

### escalate
Use when ownership failed, impact widened, or duration exceeded policy.

## 3. Suppression windows

Typical starting ranges:
- transient infra noise: 5 to 15 minutes
- repeated app errors: 15 to 60 minutes
- recurring business workflow failures: 30 to 120 minutes
- digest-only info events: one digest bucket per period

Tune windows based on how often new information actually appears.

## 4. Digest policy patterns

### Hourly digest
Use for operational updates that matter during the day but do not justify interruptions.

### Morning digest
Use for overnight low-priority events, trends, and summary metrics.

### End-of-day digest
Use for leadership or owner summaries focused on decisions, not raw noise.

A good digest should group by:
- system or workflow
- repeated root cause
- trend direction
- action needed

## 5. Routing policy patterns

### Operator-first routing
Best for incidents where a technical responder can act directly.

### Owner-first routing
Best for business workflow alerts, approvals, or commercial impact.

### Team digest routing
Best for shared situational awareness without interrupting anyone.

### Silent system routing
Best for machine-only acknowledgement, counters, or incident correlation.

## 6. Quiet hours policy

Quiet hours should suppress low-value interruptions, not hide urgent failures.

Suggested rule set:
- critical plus actionable bypasses quiet hours
- high severity may wait until business hours unless customer-facing
- medium, low, and info default to digest during quiet hours

## 7. Escalation policy

Escalate only on explicit conditions, for example:
- no acknowledgement within defined time
- repeated failure beyond retry budget
- severity rises from medium to high or high to critical
- customer impact crosses threshold
- issue duration exceeds tolerated window

## 8. Anti-fatigue rules

- Prefer one good alert over ten noisy ones
- Aggregate repeated failures into one evolving incident
- Suppress vanity thresholds with no action path
- Review false positives and downgrade or remove them
- Route to the smallest audience that can act
