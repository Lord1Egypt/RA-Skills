# Problem discovery rules and access control

## Problem statement formula

```text
Under [Trigger/Scenario], [Target Character] needs to complete [Task/Result], but currently causes [Observable Impact] due to [Confirmed Obstacle].
We have confirmed this issue with [Evidence]; [Key Assumptions] have yet to be tested.
```

It is forbidden to write "requires an agent, requires automation, and requires a knowledge base" into the question itself.

## Dismantling of current workflow

At least cover: trigger → input → manual judgment → system action → handover → result → exception/rework.

Document each step: execution role, tools/data, time taken, waits, errors, control points, and observable evidence. Only use Mermaid for complex processes.

## Stakeholder Map

| Role | Questions that must be answered |
|---|---|
| Actual users | How work happens, where it takes the most effort, and when automation is unacceptable |
| Business leader | Business results, priorities, resources and stopping conditions |
| Technical/Data Lead | Systems, Integration, Data Quality, Permissions, and Operational Constraints |
| Security/Legal/Compliance | Unacceptable Risks and Approval Pathways |
| Procurement/Finance | Budget, Procurement Cycle and Proof of Value |
| Affected but not users | Downstream impacts, fairness, trust and appeal paths |

## POC candidate scoring

Score 0–2 points for each item:

| Dimensions | 0 points | 1 point | 2 points |
|---|---|---|---|
| Problem evidence | Opinion only | Multiple descriptions | Behavioral/data cross-validation |
| Business importance | No clear impact | Directional impact | Quantified or confirmed by the owner |
| Workflow Boundary | Undescriptable | Partially Clear | Triggered to Result Complete |
| Data/system reachable | Unknown/unavailable | Mock or sample available | Real path is basically available |
| Customer investment | No owner | Contact person | Business, technology and user commitment |
| Time box verifiable | The scope is too large | Can be split | Verifiable in a short period of closed loop |

- 10–12: Recommended entry into POC contract;
- 7–9: Make a decision after completing key evidence;
- 0–6: Continue discovery or stop investing.

Scores are discussion tools only; a 0 for Security, Compliance, or Customer Commitment should not be used to get past the gate.

## Common anti-patterns

- Only interview managers and do not observe real users;
- Ask "can you use it" instead of how it has been done in the past;
- Directly list the functions proposed by customers as requirements;
- Only record pain points, not why existing alternatives exist;
- Only look for evidence that supports the plan and do not actively look for counter-evidence;
- Assume that automation must be valuable when you see high time consumption, ignoring the cost of errors, review and trust.
