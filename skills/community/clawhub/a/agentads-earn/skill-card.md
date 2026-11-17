## Description:

Agent Ads Earn helps agents register as Basemate publishers, detect intent in XMTP group chats, refer matched humans to Agent Ads subscribers, and track USDC referral earnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fweekshow](https://clawhub.ai/user/fweekshow)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to integrate with Basemate's supply-side referral flow: register monitored XMTP groups, fetch active subscriber interests, submit consent-based referrals, and check earnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill monetizes monitoring XMTP group chats, which can create privacy and consent concerns for group participants.

Mitigation: Use only explicitly approved group IDs and ensure group owners and participants receive clear notice and consent before monitoring.

Risk: Referral submissions may send message-derived identifiers and trigger-message content to external services before the referred person opts in.

Mitigation: Minimize or redact trigger messages and stable identifiers before submission, and send only data required for the referral workflow.

Risk: Referral and earnings endpoints may expose sensitive commercial activity if publisherId alone is accepted for access.

Mitigation: Confirm that Basemate enforces real authentication beyond publisherId before relying on referral submission or earnings dashboard access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fweekshow/skills/agentads-earn)
- [Publisher Profile](https://clawhub.ai/user/fweekshow)
- [Basemate App](https://basemate.app)
- [Basemate API](https://xmtp-agent-production-e08b.up.railway.app)
- [MCP Server Card](artifact/mcp-server.json)
- [A2A Agent Card](artifact/agent-card.json)
- [OASF Service Record](artifact/oasf-record.json)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with JSON, TypeScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes XMTP DM flows, HTTP API examples, MCP tool definitions, and discovery card references.]

## Skill Version(s):

1.1.0 (source: server release evidence and artifact protocol cards)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
