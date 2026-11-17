# Problem discovery input guide

## Acceptable materials

| Input | Extractable information | Common deviations | Recommended actions |
|---|---|---|---|
| Customer interviews/recordings | Tasks, behaviors, emotions, alternatives, decision language | Interviewees cater to, talk in generalities | Ask about the most recent instance and verifiable material |
| Frontline observation/following | Actual steps, manual detours, system switching, waiting and rework | Too few observation samples | Mark dates, roles and scenes to look for evidence of recurrence |
| Ticket/chat/emails | High-frequency issues, urgency, handover breakpoints | The reporter is not the same as the user | Return to the original task and business consequences |
| Process/SOP | Specified processes, responsibilities and control points | Documented processes are not equal to real processes | Compare "prescribed practices" and "actual practices" |
| Business indicators | Frequency, handling time, cost, quality, risk | Changes in indicator definition or metric definition | Recording formula, time period, data owner |
| Existing solutions/competing products | Current capabilities and constraints | Easy to infer problems from solutions | Only used to understand alternatives, not as evidence of requirements |
| Sales narrative | Business background, key people, urgency | Second-hand information distortion | Mark as lead, schedule direct user verification |

## Minimum information model

```markdown
- Who: people who actually complete the task, people who approve the results, people who are affected by the results
- When: trigger conditions, frequency, peak and cut-off time
- What to do: end-to-end steps from trigger to result
- What to use: systems, data, documents, human judgment and handover
- Where failure occurs: waiting, double entry, errors, rework, risks or invisible states
- Impact: time, cost, revenue, quality, experience or compliance consequences
- What now: alternatives, artificial cover and reasons not to change
- How to prove: original words, observations, samples, ticket, logs, indicators or confirmation from the owner
```

## What to ask first when the input is insufficient?

Ask only the questions that will most change your decision, in order of priority:

1. "When did this last happen? Please walk me through the steps."
2. “Who does it, who approves it, and who bears the consequences if something goes wrong?”
3. "How to solve it now? Is the time taken, frequency, errors or rework documented?"
4. “What data, permissions, regulations, or system limitations cannot be changed?”
5. “What will happen if it is not resolved in three months?”

## Level of evidence

| Level | Evidence | Usage |
|---|---|---|
| E0 | Speculation, sales paraphrase, unsourced conclusion | Can only generate hypotheses to be verified |
| E1 | A single user’s opinion or recollection | Can guide interviews, but not enough to establish a project |
| E2 | Multiple users' consistent descriptions, single observations, or examples | Can formulate candidate questions |
| E3 | Repeated observation, ticket/log/business data support | Can support POC contract |
| E4 | Multi-source cross-validation and Owner confirmation | Freezable issues and baselines |

Levels of evidence are not statistical significance. High-risk projects still require professional research, safety, legal or compliance verification.
