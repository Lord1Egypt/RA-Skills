## Description:

Alibaba Cloud PolarDB Database AI Assistant for PolarDB MySQL and PostgreSQL cluster management, instance inspection, performance diagnostics, parameter explanation and change assessment, SQL and log analysis, backup, security audit, HA/DR, event analysis, and other PolarDB operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database administrators, and operations engineers use this skill to ask PolarDB-specific operational questions and receive diagnostic guidance grounded in Alibaba Cloud DAS and YaoChi Agent responses. It is scoped to PolarDB MySQL and PostgreSQL inspection, troubleshooting, security review, backup checks, parameter analysis, version risk review, and related O&M workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends database operations queries, session identifiers, and diagnostic context to Alibaba Cloud services.

Mitigation: Avoid including secrets or raw customer data in prompts, and treat queries and session IDs as data disclosed to Alibaba Cloud.

Risk: The skill depends on Aliyun CLI and DAS plugin installation or updates, including mutable plugin behavior.

Mitigation: Review installers and plugin versions before use, avoid broad automatic plugin updates where possible, and verify the Aliyun CLI and DAS plugin source and version.

Risk: Broad cloud permissions could expose more PolarDB and DAS data than needed.

Mitigation: Use a test or least-privileged RAM identity, prefer temporary or OAuth credentials, and grant only the RAM actions required for the intended workflow.

Risk: Operational recommendations for parameter changes, failover, recovery, or security settings can affect database availability or data integrity.

Mitigation: Require explicit user confirmation, explain operational risk, and verify recovery point, consistency, and business impact before any change path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-polardb-ai-assistant)
- [Aliyun CLI installation guide](references/cli-installation-guide.md)
- [Related APIs](references/related-apis.md)
- [RAM policies](references/ram-policies.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Alibaba Cloud RAM authorization documentation](https://help.aliyun.com/document_detail/116146.html)
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and evidence-driven diagnostic text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include streamed response text, a session ID for multi-turn diagnostics, structured error details, and remediation guidance.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
