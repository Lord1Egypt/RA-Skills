## Description:

Provides expense-categorization guidance and a basic transaction duplicate report for US small-business ledger review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US bookkeepers, small-business owners, and office managers can use it to review vendor descriptors and potential duplicate ledger rows. It provides categorization guidance, but does not assign categories or determine tax deductibility.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Duplicate flags can be incorrect.

Mitigation: Work from a copy of the data and manually verify each flagged pair before taking action.

Risk: The bundled tool does not perform the promised expense categorization, and the documented YAML quickstart is incompatible with its CSV reader.

Mitigation: Treat the tool as a duplicate-report helper only; provide CSV input and review categorization separately rather than relying on it to assign categories.

Risk: The optional Windows app is a separate download whose safety is not established by this assessment.

Mitigation: Assess that software independently before downloading or running it.

## Reference(s):

- [US expense categorization basics](references/expense-categorization.md)
- [Expense Categorizer on ClawHub](https://clawhub.ai/rapidworker1/skills/expense-categorizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown duplicate report and expense-review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report flags possible duplicates; it does not categorize transactions or modify the source ledger.]

## Skill Version(s):

1.0.7 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
