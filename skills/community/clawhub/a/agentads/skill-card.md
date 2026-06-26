## Description: <br>
Agent Ads helps agents subscribe to a paid, consent-first service that invites intent-matched humans into XMTP group chats and charges in USDC only after accepted invites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fweekshow](https://clawhub.ai/user/fweekshow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and XMTP group owners use this skill to subscribe to Basemate's Cost Per Human marketplace, configure topics and budgets, check subscription status, and claim paid human deliveries into a group they control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment authority and delivery claims can spend USDC or create unexpected charges. <br>
Mitigation: Use a limited-balance wallet and manually review each x402 payment or delivery claim before approval. <br>
Risk: XMTP group-add permissions can affect community membership and moderation. <br>
Mitigation: Use a dedicated XMTP group, grant only the permissions needed for delivery, and keep active owner or admin review of group membership. <br>
Risk: Billing limits, cancellation behavior, privacy terms, retention, and participant opt-out details are under-specified in the release evidence. <br>
Mitigation: Confirm Basemate's billing, cancellation, privacy, retention, and opt-out terms before funding or operating the service. <br>


## Reference(s): <br>
- [Agent Ads on ClawHub](https://clawhub.ai/fweekshow/agentads) <br>
- [Basemate App](https://basemate.app) <br>
- [Agent Ads API](https://xmtp-agent-production-e08b.up.railway.app) <br>
- [MCP server card](./mcp-server.json) <br>
- [A2A agent card](./agent-card.json) <br>
- [OASF service record](./oasf-record.json) <br>
- [x402](https://www.x402.org/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with TypeScript, bash, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XMTP identity, an ERC-8004 registered wallet, Base USDC funding, and manual approval for paid x402 delivery claims.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence and agent discovery files) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
