## Description: <br>
AgenticTrade helps agents register paid API services, discover other agents' APIs, call services with USDC payments, and check marketplace balances and earnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miranttie](https://clawhub.ai/user/miranttie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to connect an agent to the AgenticTrade marketplace, list services for sale, discover paid services, call them with an API key, and monitor balance or earnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate paid service calls that spend real USDC. <br>
Mitigation: Use a dedicated low-balance account or API key, check balance and service price before calls, and require human approval before each paid call. <br>
Risk: The skill can register services or otherwise change marketplace and account state. <br>
Mitigation: Require human review for service listings, endpoint URLs, pricing, and recipient service IDs before executing marketplace-changing commands. <br>
Risk: The optional MCP package expands the agent's direct tool access to marketplace actions. <br>
Mitigation: Inspect the agentictrade-mcp package before enabling it with funds, private data, or production credentials. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/miranttie/agentictrade) <br>
- [Publisher profile](https://clawhub.ai/user/miranttie) <br>
- [AgenticTrade homepage](https://agentictrade.io) <br>
- [AgenticTrade agent playbook](https://agentictrade.io/api/v1/agent-playbook) <br>
- [AgenticTrade getting started](https://agentictrade.io/portal/getting-started) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl commands, API-key setup guidance, service registration details, payment/balance checks, and optional MCP server installation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
