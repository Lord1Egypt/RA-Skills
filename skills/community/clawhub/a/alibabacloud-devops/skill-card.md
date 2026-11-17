## Description:

Automates Alibaba Cloud Yunxiao DevOps tasks across CI/CD pipelines, code repositories, merge requests, work items, sprints, test cases, artifacts, and application release workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to translate natural-language requests into Alibaba Cloud Yunxiao CLI, MCP, or mcporter operations for CI/CD, code management, project collaboration, testing, artifact management, and application delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run installers or download runtime tooling such as CLI installers and npm packages.

Mitigation: Use a controlled environment and approve the exact installer or package command before execution.

Risk: The skill can perform live CI/CD, repository, membership, artifact, and release mutations.

Mitigation: Confirm the organization, project, repository, pipeline, application, environment, deletion, and release targets before any write action.

Risk: Over-broad Yunxiao personal access tokens can expand the impact of accidental or unauthorized operations.

Mitigation: Use a least-privilege personal access token, avoid passing tokens on the command line, and store tokens in environment variables or approved secret handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-devops)
- [Yunxiao documentation portal](https://help.aliyun.com/product/150040.html)
- [Yunxiao OpenAPI documentation](https://help.aliyun.com/zh/yunxiao/developer-reference/)
- [Yunxiao personal access token guide](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)
- [alibabacloud-devops-mcp-server](https://www.npmjs.com/package/alibabacloud-devops-mcp-server)
- [Product reference](references/product-reference.md)
- [Tool catalog](references/tool-catalog.md)
- [Token scopes](references/token-scopes.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce live DevOps operation plans and command sequences that require explicit user confirmation before mutation.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
