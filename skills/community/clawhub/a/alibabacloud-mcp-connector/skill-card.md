## Description:

Operate and manage Alibaba Cloud resources through local commands, Python batch scripts, Terraform orchestration, API discovery, and official documentation retrieval without requiring MCP client configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operators, and engineers use this skill to inspect, operate, automate, and provision Alibaba Cloud resources while following documented confirmation, credential, observability, API discovery, and cost-review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad Alibaba Cloud operations, including changes that may create, modify, delete, or incur costs.

Mitigation: Use a least-privilege RAM identity and require explicit confirmation before any create, update, delete, Terraform apply, Terraform destroy, or paid operation.

Risk: Setup may involve remote installer commands and dependency execution.

Mitigation: Review installer commands before running them and install only when the publisher and dependency chain are trusted.

Risk: Cloud credentials could be exposed or over-privileged if handled casually.

Mitigation: Avoid primary-account credentials, never paste secrets into the agent conversation, and rely on the documented credential flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-mcp-connector)
- [Publisher profile](https://clawhub.ai/user/sdk-team)
- [Verified invocation examples](references/examples.md)
- [RAM permissions](references/ram-policies.md)
- [Tool reference](references/tool-reference.md)
- [Reliable workflow for querying an unfamiliar product](references/unfamiliar-product-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, JSON, Python, and Terraform snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API responses, task status summaries, cost review notes, and resource-change plans depending on the requested Alibaba Cloud operation.]

## Skill Version(s):

1.0.0 (source: server release evidence and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
