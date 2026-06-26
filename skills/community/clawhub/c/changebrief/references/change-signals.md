# Change Signals

Use these heuristics when deciding whether a delta deserves to be highlighted.

## 1. Important Addition

Treat a new statement as high value when it changes:
- customer demand
- revenue, cost, conversion, or growth
- risk, compliance, or security
- launch timing or roadmaps
- scope, owner, or prioritization

## 2. Changed Claim

Treat two statements as the same topic with a changed claim when:
- they discuss the same object, product, feature, audience, or workstream
- but the numbers, timing, direction, or recommendation changed

Typical examples:
- `4 月底上线` -> `5 月中旬上线`
- `不需要法务审批` -> `需要先完成法务审批`
- `主要问题是步骤太多` -> `主要问题是价值表达不清`

## 3. Stale Conclusion

Mark an older statement as stale when:
- it was a conclusion, default, assumption, or plan
- and the new snapshot weakens or contradicts it

Good labels:
- old conclusion no longer safe
- underlying condition changed
- should be rewritten before it is repeated

## 4. Conflict Needing A Call

Escalate to a decision when the new delta implies:
- a changed time line
- a new blocker
- a new customer requirement
- a scope tradeoff
- unclear owner or priority

The goal is not to prove logical inconsistency.
The goal is to say: this change now creates management pressure and needs a call.

## 5. Top Priority Changes

Rank higher when a change affects:
- legal, compliance, or security risk
- customer commitments
- launch timing
- a previous executive conclusion
- what the team should do this week
