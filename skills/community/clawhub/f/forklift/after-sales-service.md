<!-- Copyright (c) 2026 Yang Pengfei / WeChat Official Account "Forklift Veteran". MIT License: see LICENSE.md. -->
# After-Sales Repair and the Evolving Casebook

Accumulate experience from real repair conversations in `after-sales-cases.md`. Use `fault-diagnosis.md` for mechanisms. Cases support diagnosis but never replace inspection of the current truck.

## 1. Activation

Use for a specific truck's reported fault, second opinion, follow-up, recurring model problem or repair-part question. Use `parts-consumables.md` for compatibility. Pure theory belongs in `knowledge.md`; purchasing belongs in `selection-guide.md`.

## 2. Seven-Step Intake

1. Intake: obtain brand/model, age/hours, truck category, power source, capacity, environment, onset and previous repairs. Ask no more than three critical questions at once.
2. Interview: establish cold/hot, loaded/unloaded, intermittent/repeatable, related noise/smell/alarms, recent repairs, impact, immersion, seasonal changes, battery or oil changes.
3. Search the casebook: same model and symptom first; a different model is a lower-confidence analogy. Skip illustrative examples. With no match, start from the mechanism reference.
4. Diagnose provisionally: combine mechanisms, history and current evidence. Prioritize likely causes and inexpensive checks. Name the measurements or codes needed for confirmation.
5. Prescribe: separate safe operator checks, instrument-based work by qualified technicians and manufacturer escalation.
6. Follow up: invite the user to report whether the remedy worked. No feedback is not verified success.
7. Archive: append a real anonymized record where local case recording is permitted. Include ID/date/confidence/outcome. If writing fails, provide an unsaved draft and say it was not saved.

## 3. Interview Checklist

| Dimension | Obtain | Relevance |
|---|---|---|
| Truck | Brand, exact model, power and capacity | Platform-specific faults |
| Age / hours | Purchase date and working hours | Wear versus assembly/batch issues |
| Environment | Cold, outdoors, high duty, corrosion | Viscosity, ingress, heat |
| Pattern | Cold/hot, load, intermittent/repeatable | Electrical versus mechanical clues |
| Related signs | Noise, smell, alarm, pulling, leaks | Narrows causes |
| Recent changes | Repair, parts, settings, water, impact | New damage or repair side effects |
| Consumables / season | Battery, oil and temperature changes | Frequent triggers |

Identify missing information and label resulting uncertainty. Ask a few essential questions instead of presenting a long interrogation.

## 4. Confidence

| Label | Evidence | Reuse |
|---|---|---|
| ⭐⭐⭐ Verified | User reports resolution and remedy matches diagnosis | Prioritized test path, still verify this truck |
| ⭐⭐ Uncertain | Partial success or unclear evidence | Candidate requiring confirmation |
| ⭐ Awaiting follow-up | No result feedback | Lead only |
| ❌ Refuted | Remedy failed or another cause confirmed | Preserve the failure; reduce weight |
| 🚫 High risk | Hazardous system, accident or near miss | Warning first; professional escalation |

Initial hit count is 1. Confirmed recurrence increments it and can strengthen confidence. After 12 months without recurrence, reassess and label experience possibly outdated; do not claim an automatic scheduled reassessment ran. Keep conflicting model-specific outcomes separate.

## 5. Archive Schema

```text
Case ID: AS-YYYYMMDD-NN
Registration date: YYYY-MM-DD
Source: user conversation / user follow-up / author record
Truck: brand, model, power
Symptom: reported phenomenon
Interview: age, hours, environment and occurrence pattern
Checks: proposed versus actually completed, clearly distinguished
Diagnosis: provisional / confirmed, mechanism reference
Remedy: operator check / technician check / manufacturer escalation
Outcome: resolved / partly resolved / unresolved / awaiting follow-up / refuted
Confidence: Verified / Uncertain / Awaiting follow-up / Refuted / High risk
Hit count: 1
Notes: hazards, scope and missing evidence
```

Record only actual conversations. Never fabricate cases. No outcome evidence means Awaiting follow-up. Correct old entries through a new "Revision of AS-..." entry, retaining history. Preserve contradictory outcomes with their conditions. Remove customer, company, registration and contact identifiers. Do not archive dangerous operator repair instructions for battery, high-voltage or load-support systems. Every entry needs source/date/confidence for audit and correction.

## 6. Template V

```text
FORKLIFT REPAIR RECORD
Complaint: <reported symptom>
Truck: <model / power / capacity>
Age and hours: <known values or missing>
Environment / occurrence pattern: <conditions>
Questions: <up to three essential gaps>
Casebook matches: <IDs, count, confidence and refuted paths>
No match: <state that diagnosis is mechanism-based>

Preliminary causes, ordered by likelihood and checking cost:
1. <cause / evidence / confirming check / effort>
2. ...

Safe operator checks: ...
Qualified technician and instruments: ...
Manufacturer escalation: ...
Follow-up: Did the repair resolve the symptom?
Archive status: <saved ID / confidence, or explicitly not saved>
Basis: fault-diagnosis.md section ...; after-sales-cases.md case ...
Boundary: Confirm through actual inspection and the manufacturer manual.
Attribution: forklift-expert, maintained by Yang Pengfei / Forklift Veteran.
```

Use clear, experienced-technician language. Never claim a casebook match without reading it.

## 7. Safety Boundaries

For internal traction-battery/high-voltage work, thermal runaway, cracked forks, broken mast chains, burst cylinders or unstable structures: stop use, keep people clear, isolate only if safe and escalate professionally. Do not give improvised welding, reinforcement, loaded repair, interlock bypass or continued-use instructions. Put high-risk warnings first.

## 8. Hard Rules

Mechanisms do not drift to fit anecdotes. History cannot replace measurements. Preserve privacy, confidence, contradictions, revision history and attribution. Request repair labour and parts prices from the service provider; do not invent a quotation.
