## Description: <br>
Browse and search the AgentAPI directory - a curated database of APIs designed for AI agents. Find MCP-compatible APIs for search, AI, communication, databases, payments, and more. Includes x402 pay-per-use billing with USDC on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gizmo-dev](https://clawhub.ai/user/gizmo-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to find API services by category, capability, MCP compatibility, pricing, and examples. It also documents x402 pay-per-use access patterns for selected paid API endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes paid x402 API calls that can trigger USDC payments. <br>
Mitigation: Require explicit per-payment approval, verify the price and recipient before payment, and use a low-balance or spending-limited wallet. <br>
Risk: Agents may treat the payment examples as sufficient authorization to spend funds. <br>
Mitigation: Configure agent policy so the skill is informational unless a human or separate payment-control layer approves each paid request. <br>


## Reference(s): <br>
- [AgentAPI Hub ClawHub Listing](https://clawhub.ai/gizmo-dev/agentapi-hub) <br>
- [AgentAPI Website](https://agentapihub.com) <br>
- [AgentAPI Billing API](https://api.agentapihub.com) <br>
- [AgentAPI Docs](https://api.agentapihub.com/api/docs) <br>
- [AgentAPI Directory JSON Endpoint](https://agentapihub.com/api/v1/apis) <br>
- [Publisher Profile](https://clawhub.ai/user/gizmo-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with API endpoint examples, JSON response examples, and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents toward paid x402 API calls that require USDC payments on Base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
