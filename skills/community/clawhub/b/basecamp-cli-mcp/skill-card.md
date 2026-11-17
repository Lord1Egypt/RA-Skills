## Description:

CLI and MCP server for Basecamp 4. Use when you need to interact with Basecamp projects, todos, messages, schedules, kanban cards, documents, or campfires. Provides 76 MCP tools for AI-driven project management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drkraft](https://clawhub.ai/user/drkraft)

### License/Terms of Use:

MIT

## Use Case:

Developers and external teams use this skill to let agents operate Basecamp 4 projects, todos, messages, schedules, documents, card tables, webhooks, and related project-management workflows through CLI or MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an AI assistant broad authority to change, delete, and route live Basecamp data.

Mitigation: Use a dedicated OAuth app or account with the minimum practical permissions, and confirm project and object IDs before mutating actions.

Risk: Webhook creation or testing can route Basecamp data to destinations the operator did not intend.

Mitigation: Allow assistant-created or assistant-tested webhooks only when the destination is trusted and reviewed.

Risk: Production or shared-team use may be exposed to dependency and pagination URL validation concerns.

Mitigation: Update dependencies and harden pagination URL validation before production or shared-team deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/drkraft/skills/basecamp-cli-mcp)
- [ClawHub Publisher Profile](https://clawhub.ai/user/drkraft)
- [Project Homepage](https://github.com/drkraft/basecamp-cli)
- [npm Package](https://www.npmjs.com/package/@drkraft/basecamp-cli)
- [Basecamp API Reference](https://github.com/basecamp/bc3-api)
- [Basecamp Integrations](https://launchpad.37signals.com/integrations)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; CLI commands may return table or JSON output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 20 and Basecamp OAuth credentials.]

## Skill Version(s):

2.0.0 (source: package.json, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
