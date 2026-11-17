## Description:

Read, query, update, and manage Feishu Bitable data through SQL-like CLI commands with URL parameter extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xjli360](https://clawhub.ai/user/xjli360)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect Feishu Bitable schemas, query records, aggregate table data, and perform controlled insert, update, or delete operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can directly change or delete live business data.

Mitigation: Scope the Feishu app to the minimum required tables and permissions, inspect schemas and records before writes, and avoid broad filter-based deletes unless intentionally bounded.

Risk: Feishu credentials and cached bearer tokens may be exposed on shared machines.

Mitigation: Protect FEISHU_APP_ID and FEISHU_APP_SECRET, review or disable the token cache on shared systems, and clear cached tokens when access is no longer needed.

Risk: A custom FEISHU_API_HOST could send requests or credentials to an untrusted endpoint.

Mitigation: Use the default Feishu API host or only set FEISHU_API_HOST to a trusted Feishu endpoint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xjli360/skills/feishu-bitable-database)
- [Feishu Open Platform](https://open.feishu.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read, create, update, or delete live Feishu Bitable records when executed with valid credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
