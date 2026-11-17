## Description:

Audits and hardens API credential handling for environment variables, credential separation, rotation planning, least privilege, and auditability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kowl64](https://clawhub.ai/user/kowl64)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when integrating services or preparing deployments that need safer API credential handling. It helps produce credential maps, rotation runbooks, least-privilege checklists, audit logging plans, and placeholder-only environment templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may accidentally provide real API keys, tokens, or private keys while requesting help.

Mitigation: Provide only redacted snippets, placeholder values, or variable names, and review generated templates before use.

Risk: Generated credential templates or rotation plans may not match an organization's operational requirements.

Mitigation: Review the generated documentation against the deployment environment, secret manager, owners, and rotation cadence before adopting it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kowl64/skills/api-credentials-hygiene)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with structured checklists, runbooks, credential maps, and placeholder-only environment templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not handle actual secrets; users should provide redacted snippets or variable names only.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
