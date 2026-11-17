## Description:

Bank Health & FDIC Data lets agents check a US bank's financial health, assets, deposits, and active status from FDIC institution data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinhughes2121](https://clawhub.ai/user/colinhughes2121)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, fintech teams, treasury agents, and due-diligence workflows use this skill to assess bank or counterparty risk, verify FDIC-active institutions, and screen banking partners before transacting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each lookup sends the requested bank name to GoCreative's external API.

Mitigation: Submit only the bank name needed for the lookup and avoid including sensitive internal notes, customer information, or unrelated confidential context.

Risk: Requests may trigger a small USDC x402 payment through an OpenClaw wallet.

Mitigation: Confirm wallet funding, payment policy, and expected per-call cost before enabling automated or repeated lookups.

## Reference(s):

- [Bank Health & FDIC Data on ClawHub](https://clawhub.ai/colinhughes2121/skills/bank-health-fdic-data)
- [Publisher profile](https://clawhub.ai/user/colinhughes2121)
- [GoCreative Bank Risk API](https://api.gocreativeai.com/v1/risk/bank/{name})

## Skill Output:

**Output Type(s):** [guidance, text, JSON]

**Output Format:** [Markdown guidance with HTTPS GET endpoint details and JSON API response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup requests submit the requested bank name to an external paid API and may trigger an x402 USDC payment through an OpenClaw wallet.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
