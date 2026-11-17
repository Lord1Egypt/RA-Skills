## Description:

Protect online shopping by AI agents. Before buying clothes, shoes or ecommerce products, compare authorized cart against final checkout seller, SKU, size, quantity, taxes, shipping address, return policy, payment payee and price. Offline pre-payment allow/review/block, no funds moved.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy229651](https://clawhub.ai/user/andy229651)

### License/Terms of Use:

MIT-0

## Use Case:

External shopping agents and their developers use this skill to compare an independently authorized purchase with the final checkout terms before payment. It returns an allow, review, or block consistency decision; it does not authenticate buyer consent or initiate payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The GitHub dependency's executable code was unavailable for independent inspection.

Mitigation: Review and pin the dependency before installing it.

Risk: An allow verdict confirms only that declared checkout data match; it does not prove buyer consent or merchant identity.

Mitigation: Require independent buyer authentication, budget checks, and final order binding in the payment host.

Risk: The optional paid vendor service can incur charges.

Mitigation: Use it only with separate, explicit wallet authorization.

## Reference(s):

- [AgentKYB Commerce Guard data contract](https://github.com/Andy229651/agentkyb-agent-tools/blob/main/docs/COMMERCE_GUARD_V0.1.md)
- [AgentKYB Agent Tools project](https://github.com/Andy229651/agentkyb-agent-tools)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Allow, review, or block checkout consistency verdict with an explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pre-payment consistency check only; no payment is initiated.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
