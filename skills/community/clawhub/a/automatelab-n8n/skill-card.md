## Description:

Use when the user wants to build, debug, or extend an n8n workflow - generating workflow JSON from a description, scaffolding a custom TypeScript node, building an AI agent, iterating over items, writing Code-node JavaScript, linting an existing workflow, diagnosing a failed execution, or driving a live n8n instance via REST.

This skill is ready for commercial/non-commercial use.

## Publisher:

[automatelab](https://clawhub.ai/user/automatelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to generate, lint, debug, and deploy n8n workflows, including custom TypeScript nodes, Code-node JavaScript, AI-agent workflow clusters, and live-instance workflow operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The paired MCP server can create and activate workflows on a live n8n instance when API credentials are configured.

Mitigation: Use a dedicated least-privilege and revocable n8n API key, review generated workflow JSON before creation, and require explicit approval before activation on live or production instances.

Risk: The recommended MCP setup runs a third-party npm package and may be installed without pinning a package version.

Mitigation: Prefer a pinned and reviewed package version before connecting it to sensitive n8n environments.

Risk: Generated or modified workflows can contain incorrect logic, unsafe credentials usage, or unintended automation effects.

Mitigation: Run workflow linting, inspect credentials and node parameters, and test workflows in a non-production n8n environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/automatelab/skills/automatelab-n8n)
- [Project homepage](https://github.com/ratamaha-git/n8n-mcp)
- [AutomateLab publisher profile](https://clawhub.ai/user/automatelab)
- [npm package @automatelab/n8n-mcp](https://www.npmjs.com/package/@automatelab/n8n-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with workflow JSON, JavaScript or TypeScript code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated workflow JSON, lint findings, execution diagnostics, MCP setup configuration, and live n8n workflow management guidance.]

## Skill Version(s):

0.4.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
