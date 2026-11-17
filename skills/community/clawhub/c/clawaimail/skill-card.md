## Description:

Give your AI agent a real email address. Send, receive, and manage emails via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joansongjr](https://clawhub.ai/user/joansongjr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use ClawAIMail to give AI tools an API-backed email inbox, send messages, read and search mail, and manage inboxes from MCP clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server needs an API key that can access and mutate ClawAIMail email data.

Mitigation: Use a dedicated, revocable, least-privilege key and avoid connecting sensitive mailboxes.

Risk: The skill can send email and permanently delete inboxes.

Mitigation: Require human confirmation before sending messages or deleting inboxes.

Risk: The install command may resolve the latest npm package instead of a reviewed exact package version.

Mitigation: Pin the npm package to a reviewed exact version before deployment.

## Reference(s):

- [ClawAIMail Website](https://clawaimail.com)
- [ClawAIMail API Docs](https://clawaimail.com/docs/)
- [clawaimail-mcp npm Package](https://www.npmjs.com/package/clawaimail-mcp)
- [ClawHub Skill Page](https://clawhub.ai/joansongjr/skills/clawaimail)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration, Shell commands]

**Output Format:** [MCP text responses containing formatted JSON, plus Markdown setup guidance with command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CLAWAIMAIL_API_KEY secret for API-backed email operations.]

## Skill Version(s):

0.2.8 (source: evidence.release.version; artifact versions differ: SKILL.md 0.2.7, package.json/server.json 0.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
