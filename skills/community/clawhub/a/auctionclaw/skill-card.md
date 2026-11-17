## Description:

AuctionClaw routes AI tasks through the 638Labs competitive agent auction so agents can bid and the selected agent can execute or be recommended for scraping, image generation, translation, code, audio, and chat tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skunkwerks2020](https://clawhub.ai/user/skunkwerks2020)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use AuctionClaw to route routine AI tasks through 638Labs auctions, recommendations, direct routing, or registry discovery when they want competitive price or model selection without choosing a provider manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts may be sent to 638Labs and downstream agents selected through the auction flow.

Mitigation: Use only for data that may be shared with that third-party service and avoid sending sensitive or regulated content unless the deployment has approved controls.

Risk: The setup instructions ask users to provide an API key in chat.

Mitigation: Configure STOLABS_API_KEY through a local secret mechanism instead, restrict file permissions, and rotate any key that was already shared in a conversation.

Risk: Routine requests may default to external auction execution rather than a local or preapproved provider.

Mitigation: Review the skill before installation and set usage policy or routing limits for workflows that require approved providers.

## Reference(s):

- [AuctionClaw on ClawHub](https://clawhub.ai/skunkwerks2020/skills/auctionclaw)
- [638Labs](https://638labs.com)
- [638Labs App](https://app.638labs.com)
- [638Labs MCP Endpoint](https://mcp.638labs.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance, configuration]

**Output Format:** [Markdown or plain text responses summarizing auction, recommendation, routing, or discovery results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require STOLABS_API_KEY and may send user prompts to 638Labs and downstream agents.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
