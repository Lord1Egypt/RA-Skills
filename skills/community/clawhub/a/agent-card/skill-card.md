## Description: <br>
Manage prepaid virtual Visa cards for AI agents with AgentCard, including card creation, balance checks, credentials, payments, closure, and support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pipeabellos](https://clawhub.ai/user/pipeabellos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to let an agent manage AgentCard prepaid virtual cards, including setup, card issuance, balance checks, checkout support, transaction review, and support chat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create virtual cards and support real payment workflows. <br>
Mitigation: Use sandbox mode first, keep spending limits low, and have the user review and authorize card creation or checkout steps before real funds are used. <br>
Risk: Full card numbers and CVVs are sensitive payment credentials. <br>
Mitigation: Only retrieve or display card details when the user explicitly needs them, and prefer balance or transaction tools for routine checks. <br>
Risk: Closing a card is permanent and irreversible. <br>
Mitigation: Require explicit user confirmation before calling the card closure workflow. <br>
Risk: Setup and authentication require OAuth, MCP configuration, and some interactive CLI steps. <br>
Mitigation: Guide the user through documented setup, avoid raw API calls, and have the user run interactive signup steps in their own terminal. <br>


## Reference(s): <br>
- [AgentCard](https://agentcard.sh) <br>
- [AgentCard MCP Server](https://mcp.agentcard.sh/mcp) <br>
- [AgentCard Pay Extension](https://agentcard.sh/extension) <br>
- [AgentCard MCP Server Setup](references/setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/pipeabellos/agent-card) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with command snippets, configuration examples, and MCP tool-call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve OAuth sign-in, AgentCard MCP tools, Stripe payment-method setup, spending limits, approval flows, and sensitive payment-card details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
