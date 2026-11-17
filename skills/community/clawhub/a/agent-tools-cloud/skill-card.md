## Description:

Find x402 paid APIs, MCP servers and A2A agents by intent via agent-tools.cloud, and optionally pay-test an x402 service once from your own wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joursbleu](https://clawhub.ai/user/joursbleu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find x402 services, MCP servers, and A2A agents for a stated need, inspect service details, and optionally request a one-off paid verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries derived from user requests may be sent to agent-tools.cloud.

Mitigation: Avoid including secrets or unnecessary personal, confidential, or sensitive details in search queries.

Risk: Paid verification sends a one-off payment from the user's wallet to the selected service.

Mitigation: Review and show the quoted price to the user before they choose to sign; the skill documentation states that tools do not pay or sign for the user.

## Reference(s):

- [Agent Tools](https://agent-tools.cloud)
- [MCP Discovery Directory](https://agent-tools.cloud/mcp-discovery/)
- [agent-tools-mcp on PyPI](https://pypi.org/project/agent-tools-mcp/)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured service records, search results, and plain-language recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the search intent and optional filters; payment verification returns a quote or result and requires a user-provided signature.]

## Skill Version(s):

0.2.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
