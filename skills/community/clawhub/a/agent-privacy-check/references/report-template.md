# Report Template

Use this outline for the final user-facing report. Replace every placeholder
with evidence or an explicit Unknown. Write in the user's language and explain
the first technical term in plain language.

~~~markdown
# Agent Privacy Check

Overall risk: <Low | Medium | High | Critical>
Confidence: <High | Medium | Low>
Scope: <agent, project or Skill, and inspected boundary>

## 一句话结论 / Plain-language conclusion

<Say what matters, what is proven, and whether the user should pause use.>
Evidence basis: <evidence row IDs or explicit Unknown>

## Agent 能看到什么 / What the agent can see

| Data class or path | Operation | Evidence | What this means |
| --- | --- | --- | --- |
| <classified source> | <read/write/...> | <Observed/Available/Not found/Unknown> | <plain-language explanation> |

## 数据能发到哪里 / Where data can leave

| Destination or service | Sink class and recipient control | Mechanism | Possible payload | Evidence | Approval and retention |
| --- | --- | --- | --- | --- | --- |
| <provider, webhook, browser, ...> | <trusted / third-party / agent-controlled / attacker-controlled> | <request/upload/...> | <data class> | <label> | <known or Unknown> |

## 三项危险组合 / Three-part combination

| Secret Source | External Sink | Untrusted Content | Connection | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| <source> | <sink and class> | <content> | <how influence could flow> | <Confirmed/Likely/Not demonstrated/Unknown> | <row IDs or Unknown> |

Actual transmission: <Observed / Not found / Unknown>
Capability: <Available / Not found / Unknown>

## 最坏后果 / Worst credible consequence

<Tie the consequence to the specific source, sink, and action. State whether
the audit observed an incident.>
Evidence basis: <row IDs or explicit Unknown>

## 怎么整改 / What to fix first

| Priority | Action | Why this is next | Evidence or trigger | Verification |
| --- | --- | --- | --- | --- |
| P0 | <Containment or credential-owner action if needed> | <impact> | <row IDs or Unknown> | <safe read-back> |
| P1 | <Least-privilege, isolation, or egress change> | <impact> | <row IDs or Unknown> | <permission or policy evidence> |
| P2 | <Untrusted-content, approval, pinning, or monitoring change> | <impact> | <row IDs or Unknown> | <post-change audit> |

## Evidence and unknowns

- Inspected: <paths, configs, tool metadata, logs>
- Not inspected: <excluded or unavailable boundary>
- Observed actions: <events, or None observed>
- Unverified assumptions: <provider retention, runtime enforcement, ...>
- Claim references: <which evidence rows support the conclusion and worst case>

This is a scoped, read-only privacy review, not proof that every future run is
safe.
~~~
