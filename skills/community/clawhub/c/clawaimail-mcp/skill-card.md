## Description:

ClawAIMail MCP Server lets AI agents create inboxes, send and receive email, search messages, read threads, delete inboxes, and inspect account usage through ClawAIMail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joansongjr](https://clawhub.ai/user/joansongjr)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this MCP server to give agents a managed email inbox for sending, receiving, reading, searching, and organizing real email during agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server can access mailbox data and perform email actions with the configured ClawAIMail API key.

Mitigation: Use a dedicated, revocable API key with the least practical access and prefer test inboxes during evaluation.

Risk: Agent-triggered actions can send email or delete an inbox.

Mitigation: Require explicit human approval before sending email or deleting an inbox.

Risk: Runtime execution through npx may resolve a package version that has not been reviewed.

Mitigation: Pin the npm package to a reviewed version before deployment.

Risk: Changing the API base URL could route mailbox data or credentials to an unintended endpoint.

Mitigation: Keep the base URL at the verified ClawAIMail HTTPS API endpoint unless a reviewed deployment requires otherwise.

## Reference(s):

- [ClawAIMail website](https://clawaimail.com)
- [ClawAIMail API documentation](https://clawaimail.com/docs/)
- [ClawHub skill page](https://clawhub.ai/joansongjr/skills/clawaimail-mcp)
- [MCP server schema](https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, configuration]

**Output Format:** [MCP tool responses containing JSON-formatted text from ClawAIMail API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ClawAIMail API key and communicates over stdio with the ClawAIMail HTTPS API.]

## Skill Version(s):

0.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
