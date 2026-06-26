# Strategy Patterns — Quick Reference

## Argument Types (Ranked by Strength)

For construction contracts (all forms):

| Rank | Type | Strength | When to use |
|------|------|----------|-------------|
| 1 | Textual Interpretation | Strongest | Always start here. Win on the text and you need nothing else. |
| 2 | Factual Distinction | Strong | Text is broad but facts are extraordinary. Pairs with Rank 1. |
| 3 | Concede-then-Distinguish | Moderate-Strong | Risk allocation rebuttals. Concede ordinary, distinguish this case. |
| 4 | Implied Terms / Prevention Principle | Weakest | Last resort. Courts reluctant to imply terms over express clauses. |

**Rule:** Build from the clause wording first. If textual interpretation wins, stop. Don't reach for implied terms when the text supports you.

## Disclosure Control Levels

| Level | Use for | Examples |
|-------|---------|----------|
| **State Precisely** | Documented facts, letter refs, clause numbers | "Disposal facility closed [date] (ref. Contractor's letter [XXX])" |
| **Keep General** | Zones, quantities, operational details | "multiple designated zones" (not Zone A, Zone B) |
| **Defer** | Delay analysis, cost breakdown, programme | "will be provided in the Notified Claim Report" |

**Rule:** Be specific on legal arguments, general on operational facts, defer quantification.

## Response Architecture Patterns

### 1. Standard Authority Query Response
1. Acknowledge the Authority's position
2. Pivot to Contractor's primary contractual reliance
3. State primary argument (textual interpretation)
4. Reserve fallback clause(s) without elaborating
5. Close cooperatively

### 2. Risk Allocation Rebuttal (Concede-then-Distinguish)
1. Concede the ordinary application of the risk clause
2. Distinguish the extraordinary facts of THIS case
3. Provide factual support (before/after)
4. State legal conclusion (clause covers X, this is Y)
5. Show mitigation evidence (good faith)
6. Close cooperatively

### 3. Chronology / Details Response
1. State known facts with exact dates and references
2. Flag items still being compiled
3. Commit to supplementing in the Claim Report
4. Reserve right to provide further details

### 4. Cost Claim Response (Pre-Quantification)
1. Identify contractual basis for cost recovery (e.g., Cl. 63.1)
2. List heads of claim without quantifying
3. State disruption is ongoing / costs being assessed
4. Commit to detailed breakdown in the Claim Report
5. Reserve right to supplement

### 5. Reservation of Rights Closing
- Interim / without prejudice basis
- Reserve all rights, remedies, claims, entitlements
- Under the Contract, at law, or otherwise
- **Always use this. Every substantive response.**

## Scope Control Rules

| Rule | Description | Anti-pattern |
|------|-------------|-------------|
| Limit to letter | Reply only to what was asked | Volunteering a mitigation proposal narrative when the Employer only asked about the initial notice |
| Preserve future claims | "reserves its position" + "without prejudice" | Making absolute statements that limit future claims |
| Keep details general | Don't name zones/quantities early | Naming "Zone A, Zone B" when boundaries might shift |

## Risk Assessment Checklist

### Counter-Arguments
- What will the Authority argue?
- Which clauses might they cite?
- Any provisions that explicitly allocate this risk to us?
- Can they argue we failed to mitigate?

### Weak Points
- Notice timing vulnerable?
- Gaps in contemporaneous records?
- Inconsistencies in prior correspondence?
- Relying on verbal communications without written record?

### Timing Risks
- Response deadline?
- Disruption still ongoing?
- Parallel claims that interact?
- Could delay in responding trigger time-bar?

### Disclosure Risks
- Volunteering anything not asked about?
- Any statement usable against us later?
- Prematurely quantifying?
- Naming specifics we might need to change?

## Common Anti-Patterns

| ❌ Don't | ✅ Do instead |
|----------|--------------|
| Cite wrong clause (e.g. EOT clause for other contractors' acts when the delay is caused by the Employer) | Verify clause text against actual contract |
| Lead with "the clause doesn't apply" | Concede ordinary application, then distinguish |
| Volunteer topics not yet raised | Limit scope to the letter being replied to |
| Name specific zones/quantities early | Keep general: "multiple designated zones" |
| Reach for implied terms first | Start with textual interpretation |
| Hedge documented dates | Use exact dates for formal letters |
| Quantify costs before records are complete | List heads of claim, defer numbers |
