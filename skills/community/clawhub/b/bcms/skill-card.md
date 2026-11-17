## Description:

BCMS helps coding agents build with the @thebcms/client SDK and operate BCMS content through MCP tools for content modeling, framework integrations, and agent-driven content operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bcms](https://clawhub.ai/user/bcms)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate BCMS with web frameworks, model content structures, work with entries, templates, groups, widgets, media, functions, and webhooks, and operate content through BCMS MCP when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BCMS API keys or MCP keys could be exposed in browser variables, repositories, logs, or shared configuration.

Mitigation: Use separate least-privilege keys, keep write/admin and MCP keys out of browser bundles and repositories, and rotate keys regularly.

Risk: MCP-enabled keys expose content and schema operations, including create, update, and delete actions.

Mitigation: Review destructive MCP actions before running them, inspect usage before deleting schema or media, and use scoped keys for the intended environment.

Risk: Unpinned npm or npx commands in production or CI can introduce unexpected dependency changes.

Mitigation: Pin package versions for production and CI workflows and review generated dependency changes before deployment.

## Reference(s):

- [BCMS Skill on ClawHub](https://clawhub.ai/bcms/skills/bcms)
- [BCMS agent setup guide](https://thebcms.com/agents)
- [BCMS documentation](https://thebcms.com/docs)
- [BCMS MCP documentation](https://thebcms.com/docs/mcp)
- [BCMS integration guides](https://thebcms.com/docs/integrations)
- [BCMS API Basics](references/bcms-api-basics.md)
- [BCMS Model Context Protocol](references/mcp.md)
- [Framework & Environment Integrations](references/frameworks.md)
- [BCMS Permissions](references/permissions.md)
- [BCMS Functions and Webhooks](references/functions-webhooks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SDK examples, MCP tool guidance, framework integration steps, and security recommendations; does not produce standalone artifacts by itself.]

## Skill Version(s):

1.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
