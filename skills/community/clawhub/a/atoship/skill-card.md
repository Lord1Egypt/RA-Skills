## Description:

Ship packages with AI: compare rates across USPS, FedEx, and UPS, buy discounted labels, track shipments, and manage orders with required user confirmation before any purchase or wallet-affecting action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atoship-dev](https://clawhub.ai/user/atoship-dev)

### License/Terms of Use:

MIT

## Use Case:

External users, small businesses, e-commerce sellers, logistics teams, and developers use this skill to compare shipping rates, create and purchase labels, track packages, validate addresses, and manage shipping orders through the atoship API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The atoship API key can authorize label purchases and wallet-affecting actions.

Mitigation: Start with a sandbox key or small wallet balance, keep spending alerts enabled, and require explicit confirmation before purchases, voids, and preferably order creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atoship-dev/skills/atoship)
- [Atoship homepage](https://atoship.com)
- [Atoship documentation](https://atoship.com/docs)
- [Atoship API reference](https://atoship.com/docs/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with inline shell commands and REST API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ATOSHIP_API_KEY. Purchase and void actions should be confirmed explicitly before execution.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
