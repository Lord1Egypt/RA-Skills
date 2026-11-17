## Description:

Financial Loan Amortization Calculator helps agents calculate loan payments, principal, payoff terms, interest, amortization schedules, loan comparisons, affordability, refinance break-even points, payoff acceleration, and rate conversions through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to run AgentPMT loan and mortgage calculations, including amortization schedules, affordability checks, refinance analysis, payoff acceleration, and rate conversion. It is suited for financial planning workflows that need structured calculation results rather than financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loan, income, debt, refinance, and affordability details are sent to AgentPMT-hosted services.

Mitigation: Send only the minimum financial details needed for the calculation and avoid identifiers such as names, addresses, account numbers, and government IDs.

Risk: Amortization schedule export can upload CSV files to cloud storage and return signed URLs.

Mitigation: Use schedule upload only when a downloadable file is needed, treat signed URLs as sensitive, and choose the shortest supported expiration.

Risk: The security verdict is suspicious because consent and retention details for sensitive financial inputs and uploaded schedules are not fully described.

Mitigation: Install only after accepting AgentPMT data handling for these inputs and prefer pinned or ClawHub-managed install paths over unpinned npx commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/financial-loan-amortization-calculator)
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/financial-loan-calculator)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)
- [Local action schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON request examples and structured JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some actions can return large amortization schedules, optional CSV file metadata, signed URLs, and expiration dates.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
