## Description:

Guides agents developing, deploying, and troubleshooting Tencent CloudBase applications across web, WeChat Mini Programs, and mobile platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binggg](https://clawhub.ai/user/binggg)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to plan, build, deploy, and troubleshoot CloudBase applications, including authentication, databases, cloud functions, storage, AI features, and WeChat integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud management and deployment steps can change live resources.

Mitigation: Limit the agent's cloud permissions and approve deployments or resource changes before execution.

Risk: Temporary credentials may be exposed in chat or logs.

Mitigation: Do not print temporary credentials; use approved secret-handling methods.

Risk: Role-policy changes and destructive cleanup can remove access, local files, or cloud resources.

Mitigation: Review IAM/CAM policy changes yourself and require explicit approval before destructive cleanup or cloud deletion.

## Reference(s):

- [CloudBase skill routing and development guidelines](artifact/SKILL.md)
- [CloudBase MCP setup](artifact/references/mcp-setup.md)
- [CloudBase deployment workflow](artifact/references/deployment-workflow.md)
- [CloudBase tooling fallback](artifact/references/tooling-fallback.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment steps and troubleshooting recommendations.]

## Skill Version(s):

1.92.145 (source: ClawHub release; packaged skill frontmatter: 2.36.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
