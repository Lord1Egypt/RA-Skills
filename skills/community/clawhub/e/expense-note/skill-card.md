## Description:

A simple daily expense recording and statistics tool for managing personal finances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangjinghua0127](https://clawhub.ai/user/yangjinghua0127)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to record everyday expenses with simple Chinese commands, review recent records, view category and monthly totals, and export local JSON reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal financial records in local JSON files under its data directory.

Mitigation: Users should review local data handling expectations, back up expenses.json before relying on it, and avoid sharing the data directory unintentionally.

Risk: Malformed amounts or unusual category names may lead to incorrect expense records because validation is limited.

Mitigation: Users should review entered amounts and category names before relying on reports or summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangjinghua0127/skills/expense-note)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Console text and local JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes expense records to data/expenses.json and exports dated report JSON files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
