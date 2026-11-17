## Description:

Audit dbt (data build tool) projects for model quality, test coverage, documentation completeness, performance, and adherence to best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analytics engineers, and data teams use this skill to review dbt projects for model quality, naming, ref/source usage, test coverage, documentation, materialization strategy, SQL quality, governance, and performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read dbt profile configuration that contains credentials, tokens, hosts, private key paths, or other sensitive connection details.

Mitigation: Use redacted profile data or confirm before use that the agent will not print or summarize sensitive profile fields.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown audit report with inline shell commands and remediation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a health score, category scores, prioritized findings, per-model details, and remediation examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
