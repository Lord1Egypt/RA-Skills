## Description: <br>
Discovers x402 paid services, MCP servers, and A2A agents in the agent-tools.cloud directory and returns matching call templates for an agent to inspect and use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joursbleu](https://clawhub.ai/user/joursbleu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to discover third-party x402 services, MCP servers, or A2A agents that match an intent, then review endpoint details, schemas, pricing, and protocol-specific call information before using them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid x402 results can involve wallet signing and real charges if a user or agent proceeds without review. <br>
Mitigation: Confirm the endpoint, provider, price, wallet details, and payment flow with the user before signing or settling any x402 challenge; use max_price_usd when a budget is known. <br>
Risk: Directory results may point to third-party MCP servers or A2A agents with their own trust, authentication, pricing, and behavior. <br>
Mitigation: Review provider details and protocol-specific metadata before connecting, delegating work, or sharing credentials. <br>


## Reference(s): <br>
- [Agent Tools Cloud](https://agent-tools.cloud) <br>
- [agent-tools-mcp on PyPI](https://pypi.org/project/agent-tools-mcp/) <br>
- [x402 Specification](https://x402.org) <br>
- [Model Context Protocol Documentation](https://modelcontextprotocol.io) <br>
- [A2A Protocol Documentation](https://a2a.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style call templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include endpoint URLs, transport details, pricing, schemas, examples, authentication notes, and protocol-specific call guidance.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
