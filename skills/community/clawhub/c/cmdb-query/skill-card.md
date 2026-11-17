## Description:

Queries CMDB asset data by resource type, including hosts, applications, databases, and name-based filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbhasbc](https://clawhub.ai/user/jbhasbc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to look up internal CMDB assets, inspect resource models, and produce filtered query examples for operational inventory work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports exposed reusable CMDB credentials.

Mitigation: Rotate the credential, remove it from the skill, and require users to provide approved secrets through a managed secret store or environment-specific credential process.

Risk: The release evidence reports disabled TLS verification.

Mitigation: Require TLS verification with a trusted internal CA before using the skill against CMDB endpoints.

Risk: The release evidence reports that the skill can query sensitive internal asset models.

Mitigation: Restrict use to approved resource labels and safe output fields, and review query scope before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jbhasbc/skills/cmdb-query)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples are intended for authenticated CMDB queries and may require curl, jq, Python, and approved network access.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
