## Description:

Guides agents in connecting to and using API Tool Calls' remote MCP tools for utilities, public-page research, and structured checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cowerxdev](https://clawhub.ai/user/cowerxdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure a remote MCP connection, discover tool schemas, and call tools for QR codes, public content, recalls, SEO, calculations, and other tasks.

### Deployment Geography for Use:

Global; some tools focus on U.S. data or Columbus, Ohio job postings.

## Known Risks and Mitigations:

Risk: Tool inputs may be sent to a third-party remote MCP service, including personal or business information.

Mitigation: Use only data appropriate to share with the service and review tool schemas before sending sensitive inputs.

Risk: An optional external CLI installer and API credentials add installation and credential-handling exposure.

Mitigation: Review the installer before use and keep keys in client credentials or environment settings, not tool arguments.

## Reference(s):

- [API Tool Calls skill release](https://clawhub.ai/cowerxdev/skills/apitoolcalls)
- [API Tool Calls agent tool information](https://apitoolcalls.com/api/)
- [API Tool Calls MCP tool listing](https://apitoolcalls.com/mcp?tools=all)

## Skill Output:

**Output Type(s):** [Text, Markdown, SVG, JSON, Guidance]

**Output Format:** [Tool-specific MCP responses, including text and structured results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by tool; check each tool schema before use.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
