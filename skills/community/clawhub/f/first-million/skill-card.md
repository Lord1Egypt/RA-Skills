## Description:

Journey to First Million helps users record income and expenses, set and check budgets, analyze spending, and track progress toward a savings goal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiguopengs](https://clawhub.ai/user/cuiguopengs)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a personal finance companion to log transactions, manage budgets, review spending patterns, and estimate progress toward a first-million savings target.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual finance entries and notes are stored as local plaintext JSON files.

Mitigation: Use the skill from a private user account, avoid entering secrets or account numbers, tighten file permissions when needed, and delete ~/.openclaw/workspace/first-million/ when the data should no longer be retained.

Risk: Reports, budget status, and savings projections depend on manually entered data and simple calculations.

Mitigation: Review transaction entries and budget settings before relying on summaries, and treat progress estimates as planning guidance rather than financial advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cuiguopengs/skills/first-million)
- [Budget Guide](references/budget-guide.md)
- [Spending Categories](references/categories.md)
- [Finance Tips](references/finance-tips.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text responses with local script command invocations and finance summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists ledger and budget data as local JSON files under ~/.openclaw/workspace/first-million/.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
