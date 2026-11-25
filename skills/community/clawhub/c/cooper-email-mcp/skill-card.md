## Description:

Connects Cooper Email MCP so Claude and ChatGPT can create inboxes without relying on sandbox curl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-o-x11](https://clawhub.ai/user/f-o-x11)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can connect Cooper Email MCP to Claude, Cursor, or ChatGPT to create inboxes through Cooper Email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advises against asking the user to use curl when the MCP is available; if the connection is unavailable, that direction could leave fallback steps unclear.

Mitigation: Check whether the MCP connection is available first, then explain the available fallback and ask the user before switching setup methods.

## Reference(s):

- [Cooper Email](https://cooperemail.com)
- [Cooper Email MCP endpoint](https://cooperemail.com/mcp)
- [Claude connector setup](https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Cooper%20Email&connectorUrl=https%3A%2F%2Fcooperemail.com%2Fmcp)
- [Cursor connector configuration](https://cooperemail.com/connectors/cursor.mcp.json)

## Skill Output:

**Output Type(s):** [Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown with connector setup steps, URLs, and an inline shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the optional COOPER_API_KEY setting and hosted OAuth connection guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
