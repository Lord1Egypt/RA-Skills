## Description:

Agent Ads helps agents subscribe to Basemate's pay-per-human lead-generation service for consent-based XMTP group invitations paid in USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fweekshow](https://clawhub.ai/user/fweekshow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover XMTP groups, subscribe a target group to intent-matched lead delivery, check subscription status, and claim paid deliveries. It is intended for commercial lead generation where group owners authorize Basemate access and invite recipients explicitly choose whether to join.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports a high-impact paid commercial integration that can authorize USDC setup fees and per-delivery payments.

Mitigation: Confirm the target XMTP group, per-human price, setup fee, cancellation process, and delivery claims before authorizing payments.

Risk: Basemate participates in XMTP groups, processes matched group-message activity, and sends invite DMs to potential leads.

Mitigation: Confirm group-owner consent, Basemate group permissions, invite-recipient consent behavior, and applicable privacy or compliance terms before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fweekshow/skills/agentads)
- [Basemate app](https://basemate.app)
- [MCP server card](artifact/mcp-server.json)
- [A2A agent card](artifact/agent-card.json)
- [OASF service record](artifact/oasf-record.json)
- [x402 protocol](https://www.x402.org/)
- [XMTP CLI](https://github.com/xmtp/xmtp-cli)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with TypeScript, shell, HTTP, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes XMTP group setup, x402 payment flow, MCP tool definitions, A2A discovery, and OASF service metadata.]

## Skill Version(s):

1.1.0 (source: server release evidence and artifact cards)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
