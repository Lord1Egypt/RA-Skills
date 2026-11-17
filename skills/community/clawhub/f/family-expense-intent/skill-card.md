## Description:

Family finance management skill for tracking household expenses, income, savings goals, subscriptions, budgets, spending insights, trends, and product price comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaichao87](https://clawhub.ai/user/wuhaichao87)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to record and review household financial activity, including expenses, income, budgets, goals, subscriptions, reports, and savings guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive household spending, income, subscription, goal, and family-member details are stored as local plaintext JSON files.

Mitigation: Use only on trusted local systems, limit recorded personal details, and review or delete ~/.openclaw/skills-data/family-expense-intent/ when the records are no longer needed.

Risk: Broad activation wording could cause finance data to be recorded unintentionally.

Mitigation: Invoke the skill deliberately for finance tracking and review generated records for accidental entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuhaichao87/skills/family-expense-intent)
- [ClawHub publisher profile](https://clawhub.ai/user/wuhaichao87)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python CLI commands; CLI output is plain text and JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists household finance records as local plaintext JSON files under ~/.openclaw/skills-data/family-expense-intent/.]

## Skill Version(s):

4.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
