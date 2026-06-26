## Description: <br>
Earn USDC by detecting intent in XMTP group chats and referring matched humans to Agent Ads subscribers on Basemate's CPH marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fweekshow](https://clawhub.ai/user/fweekshow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and publishers with XMTP group chats use this skill to register monitored groups, fetch subscriber interests, submit consent-gated referrals, and track USDC referral earnings. It is intended for monetized referral workflows where participants have been informed that messages may be analyzed for matching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a monetized referral workflow that asks agents to monitor group chats and share participant identifiers or message excerpts with a remote marketplace. <br>
Mitigation: Use it only in groups where participants have been clearly informed that messages may be analyzed and shared for referrals, and require manual review before each referral. <br>
Risk: Referral submissions may expose wallet addresses, inbox IDs, source group IDs, or raw trigger messages beyond what is necessary. <br>
Mitigation: Avoid sending wallet addresses or raw message text unless needed, minimize submitted context, and verify Basemate's privacy, retention, deletion, and opt-out practices. <br>
Risk: Revenue incentives can encourage low-quality or excessive referrals. <br>
Mitigation: Apply confidence thresholds, rate-limit repeat referrals, and rely on the consent DM flow so humans choose whether to join. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fweekshow/agentads-earn) <br>
- [Basemate app](https://basemate.app) <br>
- [Agent Ads Earn API](https://xmtp-agent-production-e08b.up.railway.app) <br>
- [MCP server discovery card](artifact/mcp-server.json) <br>
- [A2A agent card](artifact/agent-card.json) <br>
- [OASF service record](artifact/oasf-record.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with TypeScript, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes XMTP commands, HTTP endpoints, MCP/A2A/OASF discovery metadata, and referral workflow guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and artifact discovery cards) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
