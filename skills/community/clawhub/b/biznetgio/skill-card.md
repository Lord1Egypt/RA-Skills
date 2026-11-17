## Description:

Manage Biznet Gio cloud infrastructure, including servers, virtual machines, storage, and IP resources, through the Biznet Gio CLI and MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biznetgio](https://clawhub.ai/user/biznetgio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect and manage Biznet Gio cloud resources through generated CLI commands, MCP tool guidance, and configuration snippets. It supports both read-only inventory tasks and controlled resource lifecycle operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs npm packages while using Biznet Gio cloud credentials.

Mitigation: Prefer a pinned or preinstalled verified CLI or MCP package, use least-privilege credentials, and review the package source or release before deployment.

Risk: The skill can guide create, update, delete, rebuild, and state-change operations on cloud resources.

Mitigation: Review every proposed mutable command before it runs, and require an explicit second confirmation for destructive or downtime-causing actions.

Risk: API keys can be exposed if they are placed in shell commands, environment snippets, or plaintext configuration.

Mitigation: Use the browser-based login workflow and local credential file when available, and avoid asking users to paste raw API keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biznetgio/skills/biznetgio)
- [Biznet Gio CLI homepage](https://github.com/BiznetGIO/biznetgio-cli)
- [Biznet Gio CLI releases](https://github.com/BiznetGIO/biznetgio-cli/releases)
- [npm package @biznetgio/cli](https://www.npmjs.com/package/@biznetgio/cli)
- [npm package @biznetgio/mcp](https://www.npmjs.com/package/@biznetgio/mcp)
- [Biznet Gio API OpenAPI document](https://api.portal.biznetgio.com/v1/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guidance for reviewing mutable cloud-resource operations before execution.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
