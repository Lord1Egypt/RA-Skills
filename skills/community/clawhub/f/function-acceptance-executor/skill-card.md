## Description:

Function Acceptance Executor helps agents execute functional acceptance checklists item by item, report pass, conditional pass, or fail outcomes, and record defect details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and product teams use this skill to validate functional requirements against an acceptance checklist, capture observed results, and summarize pass rates and defects for release decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Acceptance testing may require system URLs, accounts, environment details, or test data.

Mitigation: Use staging or sandbox environments, least-privilege test accounts, and sanitized test data.

Risk: Sensitive credentials, API keys, production secrets, or real customer data could be exposed if included in chat inputs.

Mitigation: Keep secrets and real customer data out of agent prompts and provide only redacted or synthetic values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/function-acceptance-executor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown acceptance reports with summary tables and defect records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces item-level acceptance outcomes, defect severity labels, defect details, and aggregate pass-rate summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
