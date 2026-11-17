## Description:

Stock Market Intelligence provides market data for AI agents across equities, fixed income, crypto, and macro, with Bitcoin Lightning micropayment support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[traderhc123](https://clawhub.ai/user/traderhc123)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI agents use this skill to register for TraderHC market-data access, query market overview and asset data, request agent-optimized or compact responses, run batch queries, and configure alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow registers with api.traderhc.com and sends an agent name and subsequent API requests to that third-party service.

Mitigation: Use a dedicated agent identity and install only when the data-sharing posture is acceptable for the deployment.

Risk: AGENTHC_API_KEY may be exposed through shared logs, shell history, or copied environment output.

Mitigation: Store the key in an appropriate secret store or local environment, avoid echoing it in shared contexts, and rotate it if exposure is suspected.

Risk: Alert subscriptions can send market-event callbacks to a configured webhook URL.

Mitigation: Use a dedicated webhook endpoint with normal access controls and validation before enabling alerts.

Risk: Market data and analysis could be mistaken for investment advice.

Mitigation: Treat responses as educational and informational material and require appropriate review before financial decisions.

## Reference(s):

- [TraderHC API Documentation](https://api.traderhc.com/docs)
- [TraderHC Live Site](https://api.traderhc.com/site)
- [ClawHub Skill Listing](https://clawhub.ai/traderhc123/skills/agenthc-market-intelligence)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTHC_API_KEY; API responses can use agent-optimized or compact formats.]

## Skill Version(s):

2.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
