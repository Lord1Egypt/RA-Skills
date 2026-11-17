## Description:

Issue virtual Visa/MC cards funded by USDT, check balance, get card credentials, and fetch OTP codes via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elvismusli](https://clawhub.ai/user/elvismusli)

### License/Terms of Use:


## Use Case:

External agents and operators use this skill to interact with AgentFin virtual payment cards for online purchases, including checking prepaid balance, retrieving card details, fetching 3DS OTP codes, topping up cards, and reviewing transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent access to PAN, CVV, billing details, and OTPs can expose payment credentials.

Mitigation: Require explicit approval before retrieving or using card credentials or OTPs, and avoid logging or storing returned secrets.

Risk: Top-up and purchase flows can move funds or enable spending.

Mitigation: Require explicit approval before any top-up, purchase, or OTP submission, including confirmation of amount, merchant, and card identifier.

Risk: The AGENTFIN_API_KEY bearer token grants access to payment-card operations.

Mitigation: Store the token only in the environment, restrict agent access to trusted sessions, and rotate it if exposure is suspected.

## Reference(s):

- [AgentFin ClawHub skill page](https://clawhub.ai/elvismusli/skills/agentfin)
- [AgentFin homepage](https://agentfin.tech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with REST API examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTFIN_API_KEY; API responses may include payment credentials, OTPs, transaction data, and balances.]

## Skill Version(s):

1.0.0 (source: evidence release, target metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
