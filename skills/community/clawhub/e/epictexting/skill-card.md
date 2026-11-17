## Description:

Send SMS text messages from the user's own Twilio number with EpicTexting. Use when the user asks to text someone, send an SMS, send a text message reminder or follow-up, send the same message to a list of people (bulk / mass text, personalised with {name}), check whether a text was delivered, or see recent texts and replies. Works with any country number in international (+countrycode) format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theindianappguy](https://clawhub.ai/user/theindianappguy)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use the agent to draft and send single or personalized bulk SMS messages from their own Twilio number, check delivery status, and review recent messages or replies. The agent should show the recipient list and final text and obtain explicit approval before each send.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMS may reach unintended recipients or incur charges.

Mitigation: Review the complete recipient list and final text, consider SMS charges, and obtain explicit approval before each send.

Risk: Connecting the hosted provider grants access to Twilio credentials.

Mitigation: Review the provider's credential storage and account access before connecting.

Risk: The hosted service implementation is outside the bundled artifact review.

Mitigation: Assess the hosted service provider before linking a Twilio account.

## Reference(s):

- [EpicTexting homepage](https://www.epictexting.app)
- [EpicTexting hosted MCP server](https://www.epictexting.app/api/mcp/mcp)
- [ClawHub skill release](https://clawhub.ai/theindianappguy/skills/epictexting)
- [Declared project repository](https://github.com/IndianAppGuy/epictexting-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Natural-language SMS drafts, recipient lists, setup instructions, and delivery or reply summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sending has external effects and requires explicit user confirmation; bulk sends are limited to 50 recipients.]

## Skill Version(s):

1.0.0 (source: release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
