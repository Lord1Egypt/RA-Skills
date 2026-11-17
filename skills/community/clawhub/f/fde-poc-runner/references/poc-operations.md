# POC Operation Manual

## role

| Role | Responsibilities |
|---|---|
| POC owner | Freeze the scope, preside over the operation, and protect the integrity of the evidence |
|Business confirmer |Judges whether the work results are useful and makes continue/stop decisions |
| User Representative | Complete real tasks and provide feedback on usability and trust |
| Technical on-call | Handling environment, integration, permissions and failures |
| Assessment Leader | Manage datasets, scoring, deviations and reporting |
| Security/Compliance | Monitor high-risk actions, events, and stop conditions |

## Single round running process

1. Confirm the frozen version and environment health;
2. Explain the scenario, data boundaries and user tasks without prompting expected answers;
3. Run and record the complete trajectory, tools and manual intervention;
4. Collect the original results first, and then discuss the interpretation;
5. Score according to predetermined standards and save scoring reasons and disagreements;
6. Record problems and do not secretly fix them and then run again in the same round;
7. Complete the summary of this round and decide whether to start a new version round.

## Problem triage

| Type | Example | Postback Phase |
|---|---|---|
| Problem/Goal Wrong | Users don’t actually need it, success criteria are meaningless | 1–2 |
| Specification error | Missing rules, exceptions, permissions, or acceptances | 3 |
| Architecture/data errors | Integration failures, data quality, environment drift | 4 |
| Skill behavior errors | Tool selection, prompts, guardrails, upgrade failures | 5 |
| Run design errors | Unrepresentative data, inconsistent scoring, sample contamination | 6 |
| Adoption/Value Issues | Users are reluctant to use, results have not changed the business | 7 |

## Severity

- S0: Security, privacy, compliance, or irreversible impact; stop and escalate immediately;
- S1: The core scenario cannot be completed or the data is damaged; stop the current round;
- S2: Important quality/experience issues; record and decide whether to open a new round;
- S3: Minor issues that do not affect the core conclusion; enter the to-do list.

## Prohibited practices

- Temporarily lowering the threshold for passage;
- Delete failure tracks or only display selected cases;
- Treat model scores directly as business value;
- Merge the new version results with the old version;
- Replace real users with the skilled operations of demonstrators;
- Infinite iteration without making decisions after the POC expires.
