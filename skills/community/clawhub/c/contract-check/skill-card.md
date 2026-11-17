## Description:

Contract Check helps businesses configure company-specific contract review rules, check PDF, Word, or text contracts against commercial redlines, and produce a structured risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chartgen-ai](https://clawhub.ai/user/chartgen-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Legal, procurement, sales, and business operations teams use this skill to set company-specific contract review thresholds and screen commercial contracts for veto conditions, warnings, missing required terms, and suggested revisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for shell command execution even though its declared permissions only cover file access.

Mitigation: Review the shell use before installation in restricted environments; the publisher should replace the exec check with a native file read or existence check.

Risk: The skill stores company contract redlines locally.

Mitigation: Use the skill only when local storage of those redlines is acceptable for the target environment.

## Reference(s):

- [商业底线配置问答模板](references/config-questions.md)
- [合同审核关键词速查表](references/keywords.md)
- [商务合同审核红线标准](references/redlines.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance, Shell commands]

**Output Format:** [Markdown contract review report with structured sections and JSON configuration during initialization]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local contract-review configuration file under the agent workspace.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
