## Description:

编排完整API开发生命周期：设计、规格生成、脚手架、测试、文档与版本部署。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API teams use this skill to plan API designs, generate OpenAPI-style specifications, scaffold endpoints, create tests and documentation, and prepare versioning or migration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill discloses command execution access, so generated commands, dependency installs, deployments, or external service calls could affect local or production environments.

Mitigation: Review each command, install, deployment, and external service call before allowing it, especially when secrets or production systems are involved.

Risk: The skill can read project files while helping with API development, which may expose credentials, tokens, or sensitive implementation details in prompts or outputs.

Mitigation: Limit use to appropriate workspaces and review generated outputs to ensure secrets and sensitive data are not included.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/api-dev-tool-free)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code blocks, JSON, YAML, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API design recommendations, OpenAPI specifications, endpoint scaffolding, tests, documentation, versioning plans, and commands that should be reviewed before execution.]

## Skill Version(s):

1.0.4 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
