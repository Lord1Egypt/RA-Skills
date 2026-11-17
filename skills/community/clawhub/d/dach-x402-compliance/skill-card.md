## Description:

DACH compliance layer for x402 agents covering Impressum, DSGVO, BFSG, cookie banner, and Preisangaben checks via x402 on Base USDC for German, Austrian, and Swiss URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marketingkioldenburg](https://clawhub.ai/user/marketingkioldenburg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request deterministic DACH website compliance signals for Impressum, DSGVO, BFSG, cookie banner, pricing, cancellation-policy, preflight, and site-change checks. It is intended to support review workflows and does not replace qualified legal counsel.

### Deployment Geography for Use:

Germany, Austria, and Switzerland

## Known Risks and Mitigations:

Risk: An agent could initiate blockchain payments without adequate user review.

Mitigation: Require explicit approval and a spending limit before payment, and verify the Base network, USDC amount, pay-to address, and quote details.

Risk: Compliance signals are heuristic and may be mistaken for legal advice.

Mitigation: Use results as review signals only and escalate compliance decisions to qualified legal counsel.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marketingkioldenburg/skills/dach-x402-compliance)
- [Service Homepage](https://agent.kihustle.tech)
- [Service Catalog](https://agent.kihustle.tech/promo/catalog.json)
- [Payment Documentation](https://agent.kihustle.tech/docs/how-to-pay)
- [Agent Discovery Index](https://agent.kihustle.tech/llms.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and explicit x402 payment flow on Base USDC for paid endpoint results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
