## Description:

AWS CDK MCP Server是一个提供AWS Cloud Development Kit (CDK)最佳实践、基础设施即代码模式和CDK Nag安全合规性的工具，适用于开发者在构建AWS应用程序时获取指导和建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to request AWS CDK guidance, CDK Nag rule explanations, AWS Solutions Constructs discovery, GenAI CDK construct search, Lambda layer documentation sources, and selected CDK-related code analysis or schema generation support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes CDK and code-related inputs through a third-party API.

Mitigation: Avoid using it with private repositories or sensitive infrastructure code unless the publisher narrows the scope and validates the API endpoint.

Risk: The skill stores the XiaoBenYang API key in a plaintext .env file in the working directory.

Mitigation: Use a dedicated key, keep the workspace access-controlled, rotate or revoke the key after use, and prefer secure secret storage before production use.

Risk: The release security summary notes mismatched gaokao template remnants.

Mitigation: Review the installed files before deployment and confirm the publisher removes unrelated template remnants or explains their presence.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cainingnk/skills/awslabs-cdk)
- [XiaoBenYang API Key Site](https://xiaobenyang.com)
- [XiaoBenYang MCP Endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown summaries with JSON-derived tool results and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied XiaoBenYang API key; responses may include raw data returned by the third-party API.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
