## Description:

Deterministic legal compliance verification for cosmetic formulations against EU CosIng regulations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boriskuncer](https://clawhub.ai/user/boriskuncer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to screen cosmetic ingredient lists for EU CosIng restrictions, concentration limits, and product category constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each compliance check is a paid external API call.

Mitigation: Confirm payment intent and expected cost before submitting requests.

Risk: Submitted ingredient lists may reveal proprietary formulation information.

Mitigation: Avoid submitting confidential formulations unless external disclosure is approved.

Risk: Screening results may be incomplete for legal or market-access decisions.

Mitigation: Use the skill for initial screening and independently verify regulatory conclusions before launch or sale.

## Reference(s):

- [Cosmetic Compliance Check on ClawHub](https://clawhub.ai/boriskuncer/skills/complicheck-skill)
- [Publisher Profile](https://clawhub.ai/user/boriskuncer)
- [CompliCheck API endpoint](https://engine.lumensentry.com/webhook/check-cosmetic)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON, Guidance]

**Output Format:** [JSON API responses with agent-facing compliance guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid x402 API call; results may include ingredient resolution, CAS number, confidence, market status, restrictions, concentration limits, and payment error details.]

## Skill Version(s):

0.1.8 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
