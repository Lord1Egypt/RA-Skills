## Description:

Alibaba Cloud Yunxiao DevOps MCP Server skill that helps agents work with code repositories, projects, pipelines, application delivery, artifacts, and test management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangbowen521](https://clawhub.ai/user/huangbowen521)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps teams use this skill to inspect and operate Alibaba Cloud Yunxiao resources, including repositories, merge requests, work items, pipelines, deployments, packages, and tests, through MCP tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes broad DevOps mutation authority, including write, delete, pipeline, deployment, ownership, and variable-management actions.

Mitigation: Require explicit user confirmation and rollback planning for production-impacting actions, and use short-lived least-privilege Yunxiao tokens.

Risk: Runtime package execution is described with unpinned mcporter and alibabacloud-devops-mcp-server packages.

Mitigation: Use reviewed and pinned versions of mcporter and alibabacloud-devops-mcp-server before installation or invocation.

Risk: Token examples may encourage direct entry of real access tokens in commands.

Mitigation: Prefer a secret manager or protected environment injection instead of pasting real tokens directly into command lines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangbowen521/skills/alibaba-devops)
- [Alibaba Cloud Yunxiao documentation](https://help.aliyun.com/product/153China)
- [Alibaba Cloud Yunxiao API documentation](https://help.aliyun.com/document_detail/China)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and MCP tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command examples, environment variable guidance, and tool-selection guidance for Alibaba Cloud Yunxiao DevOps operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
