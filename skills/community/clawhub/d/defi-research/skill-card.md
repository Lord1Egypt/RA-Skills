## Description:

Research tokens, check DEX liquidity, and get live gas prices for flash loan traders and DeFi agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kennywayn3](https://clawhub.ai/user/kennywayn3)

### License/Terms of Use:

MIT-0

## Use Case:

External DeFi traders and agent developers use this skill to guide token price checks, token research, DEX liquidity checks, and Ethereum gas price lookups through the documented DeFi API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API and crypto payment instructions are under-specified.

Mitigation: Independently verify the service domain, recipient wallet address, Base network, USDC token contract, amount, and fulfillment or refund terms before use.

Risk: An agent could send API keys or USDC without enough user oversight.

Mitigation: Require explicit user confirmation for every payment and do not allow automatic transfer of API keys or USDC.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kennywayn3/skills/defi-research)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown with API endpoint examples and JSON request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment flow guidance for Stripe credits or USDC pay-per-call requests.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
