## Description:

Connect your AI to 30+ business tools, including Gmail, Calendar, Sheets, Mindbody, Meta Ads, Linear, Airtable, Notion, Stripe, and more through one URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barflotek](https://clawhub.ai/user/barflotek)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure an MCP connection between an AI assistant and Bellink-supported business applications for calendar, email, booking, analytics, issue tracking, spreadsheet, and other operational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bellink URL carries one-URL authority to connected business apps and should be treated as a secret.

Mitigation: Store BELLINK_URL securely, avoid pasting it into prompts or shell history, and rotate or revoke it if exposed.

Risk: Broad app connections can allow an agent to read or act across many business systems.

Mitigation: Connect only required apps and scopes, and require human approval for sends, bookings, writes, payments, and other state-changing actions.

Risk: The npm setup example uses npx without a pinned package version.

Mitigation: Prefer a pinned, reviewed bellink-mcp package version when using the npm-based setup.

## Reference(s):

- [Bellink homepage](https://www.bellink.io)
- [Bellink dashboard](https://app.bellink.io)
- [bellink-mcp npm package](https://www.npmjs.com/package/bellink-mcp)
- [Bellink ClawHub skill page](https://clawhub.ai/barflotek/skills/bellink)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON configuration and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BELLINK_URL endpoint credential from the Bellink dashboard.]

## Skill Version(s):

1.0.2 (source: server evidence release.version and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
