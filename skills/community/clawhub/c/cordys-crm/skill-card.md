## Description:

CordysCRM helps agents support Cordys CRM lead-to-cash workflows with cross-module relationship tracing, funnel analysis, Customer 360 views, role-aware guidance, and CLI command mapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fit2-zhao](https://clawhub.ai/user/fit2-zhao)

### License/Terms of Use:

MIT-0

## Use Case:

CRM users and business teams use this skill to query and update Cordys CRM records, inspect lead-to-cash pipelines, review approvals, and receive role-aware summaries and next-step guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses high-impact CRM credentials and write authority.

Mitigation: Install only in trusted deployment environments and restrict CRM credentials to least privilege before use.

Risk: Raw API and environment-file loading paths can expand access beyond normal guided workflows.

Mitigation: Disable or harden raw API access and .env loading unless the deployment has reviewed and accepted those paths.

Risk: Approval actions and other CRM writes can affect business records.

Mitigation: Use non-administrator credentials for initial deployment and require confirmation for write and approval actions.

## Reference(s):

- [CordysCRM ClawHub release](https://clawhub.ai/fit2-zhao/skills/cordys-crm)
- [CORDYS CRM API reference](references/crm-api.md)
- [CLI semantic specification](core/cli-spec.md)
- [Write operation engine](core/write-engine.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with CRM summaries, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include L2C relationship views, CRM risk reminders, proposed write actions, approval actions, and configuration guidance.]

## Skill Version(s):

1.2.1 (source: server release metadata and registry.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
