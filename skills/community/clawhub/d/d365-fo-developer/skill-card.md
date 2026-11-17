## Description:

Comprehensive D365 Finance & Operations development assistant covering X++, customizations, integrations, data entities, DMF, security, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for D365 Finance & Operations development guidance, including X++ customizations, data entities, integrations, security, build and deployment workflows, and AX-to-D365 migration tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Data-changing examples such as DELETE requests and DMF imports could affect real D365 F&O environments if used without review.

Mitigation: Review generated steps before execution and test data-changing operations in non-production environments first.

Risk: Integration workflows may involve credentials, bearer tokens, or SAS URLs.

Mitigation: Use least-privilege credentials, avoid exposing secrets in prompts or logs, and protect temporary package URLs.

## Reference(s):

- [D365 F&O Integrations](references/integrations.md)
- [D365 F&O Security](references/security.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline X++, HTTP, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no tool execution or persistence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
