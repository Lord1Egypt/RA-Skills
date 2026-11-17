## Description:

Deploy and operate apps on Render from OpenClaw using Blueprint plus Dashboard deeplinks, native MCP, or REST.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ojusave](https://clawhub.ai/user/ojusave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy, host, publish, and operate applications on Render, including creating render.yaml Blueprints, connecting Render MCP, validating deployments, and configuring services, environment variables, health checks, scaling, and previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live Render actions that create, change, redeploy, or destroy billable and persistent resources.

Mitigation: Require explicit user confirmation for the specific workspace, service or Blueprint, environment, plan or cost posture, and requested action before any mutating operation.

Risk: Render API keys, deploy-hook URLs, authorization headers, or secret environment values could be exposed in chat, logs, or configuration.

Mitigation: Check only whether credentials are present, keep secret values out of render.yaml and chat, use sync:false for secrets, and do not print deploy-hook URLs or authorization headers.

Risk: Render field names, CLI behavior, and service support can change, leading to invalid Blueprints or incorrect deployment guidance.

Mitigation: Confirm current Render Blueprint and MCP documentation before emitting YAML or API bodies, then validate render.yaml before asking the user to push or apply it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ojusave/skills/deploy-on-render)
- [Render documentation](https://render.com/docs)
- [Render Blueprint spec](https://render.com/docs/blueprint-spec.md)
- [Render MCP server documentation](https://render.com/docs/mcp-server.md)
- [Render OSS skills](https://github.com/render-oss/skills)
- [Render CLI](https://github.com/render-oss/cli)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline YAML, JSON, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Render Blueprint configuration, deployment commands, validation steps, MCP or REST action plans, and post-deploy checks.]

## Skill Version(s):

3.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
