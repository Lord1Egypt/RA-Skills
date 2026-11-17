## Description:

Helps freight brokers identify double-brokering, payment, and downstream liability risks when shipment or carrier details do not match.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

External freight brokers and brokerage teams use this checklist to investigate suspected double-brokering, carrier identity mismatches, unpaid-carrier claims, and related exposure before deciding how to handle a load.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A mismatch between the booked carrier and the hauling carrier can lead to payment disputes, cargo claims, or downstream liability.

Mitigation: Verify the hauling carrier against the booked carrier, require active tracking, and assess relevant bond or insurance exposure.

Risk: Withholding payment or reporting fraud based only on checklist signals could lead to an incorrect decision.

Mitigation: Review the evidence and applicable obligations before withholding payment or reporting fraud.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/deciqai/skills/freight-double-brokering-exposure)
- [Publisher skill page](https://www.deciqai.com/c/freight-double-brokering-exposure)
- [Machine-readable skill metadata](https://www.deciqai.com/s/freight-double-brokering-exposure.json)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Risk analysis]

**Output Format:** [Markdown checklist with explanatory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory only; it does not execute actions or change payment status.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
