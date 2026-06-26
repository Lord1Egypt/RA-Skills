---
name: alert-triage
description: Normalize noisy notifications into a simple triage model: send now, batch later, ignore, suppress as duplicate, or escalate. Use when the user wants to reduce alert fatigue, deduplicate alerts, route notifications by severity or audience, define quiet hours, create digest policies, decide what deserves paging, or design an OpenClaw-first alert policy without binding to a specific sender or monitoring vendor.
---

# Alert Triage

Use this skill to turn a stream of alerts into a clear policy and response model.

## Core principle

Do not start with channels or tools. Start with the decision.

For each alert, decide:
1. Is it actionable?
2. Is it urgent?
3. Is it trustworthy?
4. Is it new information?
5. Who actually needs it?
6. Should it be immediate, batched, suppressed, ignored, or escalated?

## Output model

Classify each alert into one of these outcomes:
- **send-now**
- **batch-later**
- **ignore**
- **suppress-as-duplicate**
- **escalate**

When helpful, also assign:
- severity: `critical | high | medium | low | info`
- confidence: `high | medium | low`
- audience: `operator | owner | team | system`
- timing: `immediate | next-digest | business-hours | maintenance-window`

## Workflow

### 1. Normalize the signal

Convert the raw notification into a compact event record:
- source type
- event summary
- likely impact
- affected system or workflow
- first seen time
- repeat count if known
- current evidence

If the source is noisy or ambiguous, rewrite it into one sentence before classifying it.

### 2. Check actionability

Ask:
- Can someone do something useful now?
- Does delay make the outcome materially worse?
- Is there a clear owner or audience?

If not actionable, prefer `ignore` or `batch-later`.

### 3. Score urgency

Urgency increases when:
- revenue, uptime, data safety, or customer experience is at risk
- the problem is time-sensitive or irreversible
- the signal indicates active degradation, not just a threshold crossing
- the event affects many users or critical workflows

Urgency decreases when:
- the event is informational only
- the issue is self-healing or reversible
- the metric fluctuation is within normal variance
- the event is outside service relevance or ownership

### 4. Check trust and evidence

Before escalating, check whether the alert is:
- from a trustworthy source
- supported by more than one signal
- already acknowledged elsewhere
- likely a false positive or transient blip

Low-trust alerts should usually not page people unless impact is potentially severe.

### 5. Deduplicate and suppress

Treat an alert as a duplicate when it repeats the same underlying issue within the same suppression window.

Use a suppression key based on the smallest stable combination that identifies the problem, for example:
- source
- affected component
- error family
- environment
- severity bucket

Suppress duplicates when the new event adds no meaningful information.

Do **not** suppress when the event shows:
- a severity increase
- wider blast radius
- longer duration than expected
- a new affected component
- failure of a previous recovery attempt

### 6. Route by audience

Route based on who can act, not who might be interested.

Default pattern:
- `critical` and actionable, immediate owner plus escalation path
- `high`, owner or operating team quickly
- `medium`, working queue or next digest unless time-sensitive
- `low` and `info`, digest or ignore

### 7. Apply timing policy

Use timing rules such as:
- immediate if impact is active and delay is costly
- next digest if useful but not urgent
- business hours if action can safely wait
- maintenance window if the alert is expected during change work

Quiet hours should reduce noise, but not hide critical actionable events.

### 8. Produce final policy output

Return a concise table or bullet list with:
- normalized alert
- severity
- final outcome
- audience
- timing
- rationale
- suppression key or digest bucket when relevant

## Recommended output template

```markdown
## Alert triage result

| Alert | Severity | Outcome | Audience | Timing | Reason |
|------|----------|---------|----------|--------|--------|
| [normalized alert] | high | send-now | operator | immediate | customer-facing outage with clear action |
| [normalized alert] | low | batch-later | owner | next-digest | useful trend, no urgent action |
| [normalized alert] | medium | suppress-as-duplicate | system | current window | same root issue, no new information |
```

## Decision heuristics

Prefer **send-now** when all are true:
- actionable
- time-sensitive
- trusted enough
- meaningful impact

Prefer **batch-later** when:
- action exists, but delay is acceptable
- the alert is useful as pattern context
- the event is better understood in aggregate

Prefer **ignore** when:
- no action is needed
- the event is vanity noise
- the source is too weak without corroboration

Prefer **suppress-as-duplicate** when:
- it is the same incident inside the suppression window
- nothing important changed

Prefer **escalate** when:
- severity increased
- the response owner did not act in time
- business impact crossed a threshold
- the event exceeded duration or repetition limits

## Privacy and portability rules

Keep outputs reusable and marketplace-safe.

Do not include:
- personal phone numbers
- private email addresses
- real user names
- internal channel IDs
- device nicknames
- company secrets
- private endpoints or tokens

Use abstract placeholders instead:
- `primary-on-call`
- `ops-channel`
- `business-owner`
- `customer-alerts`
- `critical-systems`

## References

Read these when needed:
- `references/policies.md` for reusable policy patterns
- `references/examples.md` for worked examples
