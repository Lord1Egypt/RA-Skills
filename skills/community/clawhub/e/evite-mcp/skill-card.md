## Description:

Evite MCP helps an agent read and manage Evite events, invitations, guest lists, RSVPs, messages, and event creation or edits through an Evite MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to an Evite account, inspect events and guest activity, and perform confirm-gated actions such as RSVPing, messaging guests, and creating or editing events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can give the MCP server access to an Evite account through a password or browser session cookie.

Mitigation: Install only after reviewing the package, use a unique Evite password, and avoid storing passwords or raw cookies in project files.

Risk: The documented npx setup can run an unpinned package version.

Mitigation: Use a pinned, reviewed package version before deployment.

Risk: Fetchproxy can lift session cookies from a signed-in browser tab.

Mitigation: Disable Fetchproxy unless it is explicitly needed.

Risk: The MCP tools can modify events, guests, messages, invitations, and event status.

Mitigation: Require careful confirmation for write actions such as messaging guests, editing events, sending invitations, or canceling events.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chrischall/skills/evite-mcp)
- [Evite](https://www.evite.com)
- [evite-mcp npm Package](https://www.npmjs.com/package/evite-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP setup guidance, environment variable names, tool recommendations, dry-run previews, and confirmation guidance for write actions.]

## Skill Version(s):

0.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
