## Description:

Tax compliance for AI agent transactions, including sales tax, capital gains, nexus monitoring, and 1099 tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenttax](https://clawhub.ai/user/agenttax)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI agent operators use this skill to call AgentTax APIs for sales and use tax calculation, trade logging for capital gains, nexus setup, tax-rate lookup, and 1099-DA export workflows.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Real financial, tax, transaction, nexus, and counterparty data may be sent to agenttax.io.

Mitigation: Confirm data-sharing approval before using the skill with real financial, tax, customer, or counterparty data.

Risk: API credentials and signup passwords can be exposed when copied directly into shell commands.

Mitigation: Use a dedicated AgentTax API key, avoid reusing passwords, and avoid putting real passwords directly in shell commands.

Risk: Placeholder replacement inside curl JSON strings can produce malformed requests or accidental disclosure in production workflows.

Mitigation: Prefer a safer client or JSON serializer for production use instead of manually replacing placeholders in shell snippets.

## Reference(s):

- [AgentTax homepage](https://agenttax.io)
- [AgentTax agent API docs](https://agenttax.io/api/v1/agents)
- [ClawHub skill page](https://clawhub.ai/agenttax/skills/agenttax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON request and response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and AGENTTAX_API_KEY for authenticated API calls.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
